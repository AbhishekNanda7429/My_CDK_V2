"""Baseline CDK resources for the onetrust-club-integrations AWS account(s)"""

from aws_cdk.aws_iam import (
    ManagedPolicy,
    PolicyDocument,
    PolicyStatement,
    Role,
    ServicePrincipal,
)
from aws_cdk.aws_ec2 import (
    Vpc,
    Subnet,
    SubnetSelection,
)

from aws_cdk import aws_events, aws_events_targets
from aws_cdk import Duration, Stack
from aws_cdk.aws_lambda import Code, Function, Runtime, LayerVersion, Tracing
# from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_scheduler_alpha as Schedule
from aws_cdk import aws_scheduler_targets_alpha as Target
from cdk_nag import NagPackSuppression, NagSuppressions
from constructs import Construct
from variables import *
import json
class OnetrustClubIntegrationsStack(Stack):

    def __init__(self, scope: Construct, id: str, env_vars, **kwargs) -> None:
        """
        OnetrustClubIntegrationsStack

        Args:
            scope: Scope
            id: Unique ID
            env_vars: Dictionary of variables passed in through cdk.json context
            **kwargs: Extra keyword argument list
        """
        super().__init__(scope, id, **kwargs)

        # Define your new CDK resources below

        vpc = Vpc.from_lookup(self, "OneTrustVPC", vpc_id=env_vars["vpc_id"])
        vpc_subnets = SubnetSelection(
            subnets=[
                Subnet.from_subnet_id(self, "subnet1", env_vars["private_subnet_1_id"]),
                Subnet.from_subnet_id(self, "subnet2", env_vars["private_subnet_2_id"]),
                Subnet.from_subnet_id(self, "subnet3", env_vars["private_subnet_3_id"]),
            ]
        )

        # # Lambda Layer
        # """ Create a layer for dependencies required for the lambda function to run."""
        # dependencies_layer = LayerVersion(
        #     self,
        #     "DependenciesLayer",
        #     code=Code.from_asset(
        #         "onetrust_club_integrations/src/lambda_layer/python.zip"
        #     ),
        #     compatible_runtimes=[Runtime.PYTHON_3_9],
        #     description="A layer for dependecies required for the lambda function to run.",
        #     layer_version_name="onetrust-dependency-layer",  # JAS_Added
        # )

        ''' Create a layer for dependencies required for the lambda function to run.'''
        dependencies_layer = LayerVersion(self, "DependenciesLayer",
            code=Code.from_asset("onetrust_club_integrations/src/dependencies/python.zip"),
            compatible_runtimes=[Runtime.PYTHON_3_9],
            description="A layer for dependecies required for the lambda function to run.",
            layer_version_name="requirements-dependency-layer"
        )
        
        ''' Create a layer for OT.'''
        OT_layer = LayerVersion(self, "OTLayer",
            code= Code.from_asset("onetrust_club_integrations/src/ot/python.zip"),
            compatible_runtimes=[Runtime.PYTHON_3_9],
            description="A layer for ot.",
            layer_version_name="ot-dependency-layer"
        )

        # ''' Create a layer for Global Authentication'''
        # GlobalAuth_layer = LayerVersion(self, "GlobalAuthLayer",
        #     code= Code.from_asset("onetrust_club_integrations/src/oauth/python.zip"),
        #     compatible_runtimes=[Runtime.PYTHON_3_9],
        #     description="A layer for oauth.",
        #     layer_version_name="global-auth-dependency-layer"
        # )
        
        ''' Create a layer for Marketo'''
        Marketo_layer = LayerVersion(self, "MarketoLayer",
            code=Code.from_asset("onetrust_club_integrations/src/marketo-lambda/python.zip"),
            compatible_runtimes=[Runtime.PYTHON_3_9],
            description="A layer for marketo.",
            layer_version_name="marketo-dependency-layer"
        )


        ''' Create a layer for Eloqua'''
        Eloqua_layer = LayerVersion(self, "EloquaLayer",
            code=Code.from_asset("onetrust_club_integrations/src/eloqua_lambda/python.zip"),
            compatible_runtimes=[Runtime.PYTHON_3_9],
            description="A layer for eloqua.",
            layer_version_name="eloqua-dependency-layer"
        )

        # Audit_Trace_layer = LayerVersion(self, "AuditTraceLayer",
        #     code=Code.from_asset("onetrust_club_integrations/src/audit_trace/python.zip"),
        #     compatible_runtimes=[Runtime.PYTHON_3_9],
        #     description="A layer for audit_trace.",
        #     layer_version_name="audit-trace-dependency-layer"
        # )


        # Sample Function
        # TODO: finalize IAM Permissions (Secrets Manager)
        lambda_execution_role = Role(
            self,
            "LambdaSampleFunctionRole",
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
            role_name="nfl-dna-onetrust-lambda-kcc-role",
            description="Lambda Execution Role, Access to secrets manager",
            inline_policies={
                "secret-policy": PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                "secretsmanager:GetSecretValue",
                                "secretsmanager:PutSecretValue"
                                ],
                            # resources=[env_vars["MARKETO_SECRET_BASE_ARN"] + "-??????"],
                            resources=["*"],  # TODO: restrict this....
                        ),
                        PolicyStatement(
                            actions=[
                                        "kms:Decrypt",               
                                    ],
                            resources=[
                                f"arn:aws:kms:{env_vars['region']}:{env_vars['account-id']}:key/*"
                            ],
                            conditions={
                                "ForAnyValue:StringLike": {
                                    "kms:ResourceAliases": f"alias/nfl-dna-onetrust-{env_vars['env']}-sm-key"
                                }
                            },
                        ),
                    ]
                ),
                "baseline-vpc-policy": PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                "ec2:CreateNetworkInterface",
                                "ec2:DescribeNetworkInterfaces",
                                "ec2:DeleteNetworkInterface",
                            ],
                            resources=["*"],
                        ),
                    ]
                ),
                # TODO: confirm that Lambda should read/write to Audit Bucket?  Can restrict if not
                "audit-bucket-policy": PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                # Get / Download
                                "s3:Get*",
                                # Create / Update
                                "s3:PutObject*",  # Object, tags, version acl, version tags, acl, retention, legalhold
                                "s3:DeleteObject",
                                # List
                                "s3:ListBucket",
                                "s3:ListBucketMultipartUploads",
                                "s3:ListBucketVersions",
                                "s3:ListMultipartUploadParts",
                            ],
                            resources=[
                                f"arn:aws:s3:::{env_vars['audit-bucket-name']}",
                                f"arn:aws:s3:::{env_vars['audit-bucket-name']}/*",
                            ],
                        ),
                        PolicyStatement(
                            actions=[
                                "kms:Decrypt",
                                "kms:Encrypt",
                                "kms:ReEncrypt",
                                "kms:GenerateDataKey",
                            ],
                            resources=[
                                f"arn:aws:kms:{env_vars['region']}:{env_vars['account-id']}:key/*"
                            ],
                            conditions={
                                "ForAnyValue:StringLike": {
                                    "kms:ResourceAliases": f"alias/nfl-dna-onetrust-audit-{env_vars['env']}-key",
	                                "kms:ResourceAliases": f"alias/nfl-dna-onetrust*",

                                    # f"arn:aws:kms:{env_vars['region']}:{env_vars['account-id']}:key/bf375252-eda3-492b-81b9-2c4ec9a4869c"
                                }
                            },
                        ),
                    ]
                ),
            },
        )

        lambda_execution_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AwsLambdaBasicExecutionRole"
            )
        )

        nos_lambda_handler_path = Code.from_asset(
            "onetrust_club_integrations/src/nos"
        )

        lambda_handler_path_kcc = Code.from_asset(
            "onetrust_club_integrations/src/kcc"
            )

        lambda_handler_path_cle = Code.from_asset(
            "onetrust_club_integrations/src/cle"
            )

        """ Create a lambda function to be triggered by the event bridge rule.
            It has secrets as environment variable."""
        nos_lambda_function = Function(
            self,
            "New-Orleans-Saints-Fn",
            runtime=Runtime.PYTHON_3_9,
            handler="app.handler",
            code=nos_lambda_handler_path,
            function_name="New-Orleans-Saints-Fn",
            role=lambda_execution_role,
            environment={
                "MARKETO_SECRET": MARKETO_SECRET,
                "MARKETO_ENDPOINT": MARKETO_ENDPOINT,
                "OT_SECRET": OT_SECRET,
                #"OT_ENDPOINT": OT_ENDPOINT,
                "OAUTH_TYPE": "credentials",
                "OT_AUTH_URL": OT_AUTH_URL,
                "OT_CONSENT_URL": OT_CONSENT_URL,
                "CLUB": "nos",
                "FIELDS_LIST": NOS_FIELDS_LIST,
                "BASE_URL_UNSUBSCRIBE_LINK":KCC_BASE_URL_UNSUBSCRIBE_LINK,
                "MARKETO_BATCH_SIZE": MARKETO_BATCH_SIZE,
                "OT_PURPOSES": json.dumps(NOS_OT_PURPOSES),
                
                #"START_DATETIME": START_DATETIME,
                #"END_DATETIME": END_DATETIME
                
            },
            layers=[dependencies_layer, OT_layer, Marketo_layer],
            timeout=Duration.minutes(15),
            vpc=vpc,  # JAS_Added
            vpc_subnets=vpc_subnets,  # JAS_Added
        )

        kcc_eloqua_lambda_function = Function(  
            self, "KCC-Fn",
            runtime=Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code= lambda_handler_path_kcc,
            function_name="KCC-Fn",
            role=lambda_execution_role,
            environment={
                "ELOQUA_SECRET": ELOQUA_SECRET,
                "ELOQUA_ENDPOINT": ELOQUA_ENDPOINT,
                "OT_SECRET": OT_SECRET,
                "OAUTH_TYPE": "refresh_token",
                "OT_AUTH_URL": OT_AUTH_URL,
                "OT_CONSENT_URL": OT_CONSENT_URL,
                "CLUB": "kcc",
                "BASE_URL_UNSUBSCRIBE_LINK": KCC_BASE_URL_UNSUBSCRIBE_LINK,
                "OT_PURPOSES": json.dumps(KCC_OT_PURPOSES),
                "BUCKET_NAME": BUCKET_NAME,
                "POWERTOOLS_LOG_LEVEL": "DEBUG",
                "CONTACT_VIEW_ID": KCC_CONTACT_VIEW_ID,
                "ELOQUA_EXPORT_URL": KCC_ELOQUA_EXPORT_URL,
                "ELOQUA_IMPORT_URL": KCC_ELOQUA_IMPORT_URL,
                "IMPORT_BATCH_SIZE": KCC_IMPORT_BATCH_SIZE,
                "EXPORT_BATCH_SIZE": KCC_EXPORT_BATCH_SIZE
            },
            layers=[dependencies_layer,OT_layer,Eloqua_layer],
            timeout=Duration.minutes(15),
            tracing=Tracing.ACTIVE,
            vpc=vpc,  # JAS_Added
            vpc_subnets=vpc_subnets, 
        )

        cle_eloqua_lambda_function = Function(
            self, "CLE-Fn",
            runtime=Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code= lambda_handler_path_cle,
            function_name="CLE-Fn",
            role=lambda_execution_role,
            environment={
                "ELOQUA_SECRET": ELOQUA_SECRET,
                "ELOQUA_ENDPOINT": ELOQUA_ENDPOINT,
                "OT_SECRET": OT_SECRET,
                "OAUTH_TYPE": "refresh_token",
                "OT_AUTH_URL": OT_AUTH_URL,
                "OT_CONSENT_URL": OT_CONSENT_URL,
                "CLUB": "cle",
                "BASE_URL_UNSUBSCRIBE_LINK": CLE_BASE_URL_UNSUBSCRIBE_LINK,
                "OT_PURPOSES": json.dumps(CLE_OT_PURPOSES),
                "BUCKET_NAME": BUCKET_NAME,
                "POWERTOOLS_LOG_LEVEL": "DEBUG",
                "CONTACT_VIEW_ID": CLE_CONTACT_VIEW_ID,
                "ELOQUA_EXPORT_URL": CLE_ELOQUA_EXPORT_URL,
                "ELOQUA_IMPORT_URL": CLE_ELOQUA_IMPORT_URL,
                "IMPORT_BATCH_SIZE": CLE_IMPORT_BATCH_SIZE,
                "EXPORT_BATCH_SIZE": CLE_EXPORT_BATCH_SIZE
            },
            layers=[dependencies_layer,OT_layer,Eloqua_layer],
            timeout=Duration.minutes(15),
            tracing=Tracing.ACTIVE,
            vpc=vpc,  # JAS_Added
            vpc_subnets=vpc_subnets, 
        )

        # dlq = sqs.Queue(self, "KCC-DLQ",
        #                        queue_name="KCC-DLQ")
        target = Target.LambdaInvoke(  kcc_eloqua_lambda_function,
                                      input=Schedule.ScheduleTargetInput.from_object({
                                             
                                            "Payload": "{\"endtime\":\"<aws.scheduler.scheduled-time>\",\"interval\":\"50\"}", 
                                      }),
                                      retry_attempts=4,
                                    #   dead_letter_queue=dlq
                                            
                                            # "InvocationType": "Event"
                                        )
        cron_based_schedule = Schedule.Schedule(self, "Schedule",
                                       schedule=Schedule.ScheduleExpression.cron(
                                            minute="*/30",
                                            hour="*",
                                            day="*",
                                            month="*",
                                            # week_day="?",
                                            year="*",
            
        ),
        target=target,
        description="This is a test cron-based schedule that will run every 30 minutes"
        )



        ################## NAG SUPPRESSIONS ###################
        NagSuppressions.add_stack_suppressions(
            self,
            [
                {
                    "id": "AwsSolutions-IAM5",
                    "reason": "temp permit wildcards in IAM entities",
                },
            ],
        )

        NagSuppressions.add_stack_suppressions(
            self,
            [
                NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="Lambda can use AWS Lambda managed policy",
                ),
                NagPackSuppression(
                    id="AwsSolutions-L1",
                    reason="Lambda can use AWS Lambda managed policy",
                ),
            ],
            True,
        )
