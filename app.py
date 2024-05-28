import aws_cdk as cdk
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk import aws_sqs as sqs
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk import aws_events as events
from variable import *
import json
from constructs import Construct
from aws_cdk.aws_events import Schedule
from aws_cdk import Duration
from aws_cdk import aws_logs as logs
from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
)

# Define a function to create the environment dynamically for each club
def create_environment(club):
    environment = {
        "CLUB": club,
        "SECRET": globals().get(f"{club.upper()}_ESP_SECRET", ""),
        "ENDPOINT": globals().get(f"{club.upper()}_ESP_ENDPOINT", ""),
        "OT_SECRET": globals().get("OT_SECRET", ""),
        "OAUTH_TYPE": globals().get(f"{club.upper()}_OAUTH_TYPE", ""),
        "OT_AUTH_URL": globals().get("OT_AUTH_URL", ""),
        "OT_CONSENT_URL": globals().get("OT_CONSENT_URL", ""),
        "FIELDS_LIST": globals().get(f"{club.upper()}_FIELDS_LIST", ""),
        "BASE_URL_UNSUBSCRIBE_LINK": globals().get(f"{club.upper()}_BASE_URL_UNSUBSCRIBE_LINK", ""),
        "BATCH_SIZE": globals().get("BATCH_SIZE", ""),
        "OT_PURPOSES": json.dumps(globals().get(f"{club.upper()}_OT_PURPOSES", "")),
        "BUCKET_NAME": globals().get("BUCKET_NAME", ""),
        "POWERTOOLS_LOG_LEVEL": globals().get("POWERTOOLS_LOG_LEVEL", ""),
        "CONTACT_VIEW_ID": globals().get(f"{club.upper()}_CONTACT_VIEW_ID", ""),
        "EXPORT_URL": globals().get(f"{club.upper()}_ELOQUA_EXPORT_URL", ""),
        "IMPORT_URL": globals().get(f"{club.upper()}_ELOQUA_IMPORT_URL", ""),
        "IMPORT_BATCH_SIZE": globals().get(f"{club.upper()}_IMPORT_BATCH_SIZE", ""),
        "EXPORT_BATCH_SIZE": globals().get(f"{club.upper()}_EXPORT_BATCH_SIZE", "")
    }
    return environment

# Define your list of club
clubs = ["nos", "kcc", "cle"]

class EventbridgeSqsLambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        for club in clubs:
            print(f"Processing element: {club}")

            #create the dynamic environment variable here
            env = create_environment(club)

        
            #Define a DLQ for the sqs
            dlq = sqs.Queue(
                self,
                id=f"{club}_SQS_DLQ",
                queue_name=f"{club}_SQS_DLQ",
                visibility_timeout=None
            )

            #mention that the queue is a DLQ
            dead_letter_queue = sqs.DeadLetterQueue(
                max_receive_count=4,
                queue=dlq
                )

            # Create an SQS queue with dynamic name according to list
            # dynamic_sqs_name = f"{club}_Queue"
            dynamic_sqs_name = sqs.Queue(
                self,
                id=f"{club}_Queue", 
                queue_name=f"{club}_Queue",
                visibility_timeout=None,
                dead_letter_queue= dead_letter_queue
            )

            #configure the DQL to the SQS
            # dynamic_sqs_name.dead_letter_queue = dlq


            # Define the DLQ for the first Lambda function
            # Dynamic_DLQ_1= f"{club}_Dlq_1"
            # Dynamic_DLQ_1 = sqs.Queue(
            #     self, 
            #     id=f"{club}_Dlq_1", 
            #     visibility_timeout=None
            # ) 

            log_group = logs.LogGroup(self,
                                      id=f"{club}_LogGroup",
                                      log_group_name=f"nfl-dna-onetrust-{club}-logs",
                                      retention = logs.RetentionDays.SIX_MONTHS
                                      )

            # Lambda function that sends data to SQS
            lambda1 = f"{club}_lambda_1"
            lambda1 = Function(
                self,
                id=f"{club}_lambda_1",
                runtime=Runtime.PYTHON_3_9,
                code=Code.from_asset("lambda_code/send_to_sqs"),
                handler="send_to_sqs.handler",
                log_group=log_group,
                function_name= f"PC-{club.upper()}-Retrival-Function",
                environment={
                    "QUEUE_URL": dynamic_sqs_name.queue_url,
                    **env
                    },
                # dead_letter_queue=Dynamic_DLQ_1
            )

            # Define the DLQ for the second Lambda function
            # Dynamic_DLQ_2= f"{club}_Dlq_2"
            # Dynamic_DLQ_2 = sqs.Queue(
            #     self, 
            #     id=f"{club}_Dlq_2", 
            #     visibility_timeout=None
            # )

            # Lambda function triggered by SQS
            lambda2 = f"{club}_lambda_2"
            lambda2 = Function(
                self,
                id= f"{club}_lambda_2",
                runtime=Runtime.PYTHON_3_9,
                code=Code.from_asset("lambda_code/process_sqs_message"),
                handler="process_sqs_message.handler",
                log_group=log_group, 
                function_name= f"PC-{club.upper()}-Processing-Function",
                environment=env,
                # dead_letter_queue=Dynamic_DLQ_2,
                # reserved_concurrent_executions=5
            )

            # lambda1.log_group = log_group
            # lambda2.log_group = log_group

            # Define the DLQ for even bridge function
            event_bridge_dlq = sqs.Queue(
                self, 
                id= f"{club}_EventBridgeDLQ", 
                visibility_timeout=None
            )

            dead_letter_queue = sqs.DeadLetterQueue(
                max_receive_count=4,
                queue=event_bridge_dlq
                )

            #define a cron Schedule expression
            cron_schedule = Schedule.cron(
                minute="0",  # Run every hour at the beginning of the hour            
                hour="*",            
                month="*",            
                week_day="MON-FRI",  # Monday to Friday            
                year="*"
                )

            # EventBridge rule to trigger lambda1 on a schedule
            event_rule = events.Rule(
                self,
                id=f"{club}_ScheduleRule",
                # event_pattern=EventPattern.schedule(expression="rate(30 minute)"),
                schedule = cron_schedule
            )
            
            #add target for the event bridge
            event_rule.add_target(LambdaFunction(lambda1,
                                                 retry_attempts=4,
                                                 dead_letter_queue=event_bridge_dlq))

            # Grant lambda2 permission to consume messages from the queue
            dynamic_sqs_name.grant_consume_messages(lambda2)

            # Grant lambda1 permission to send messages to the queue
            dynamic_sqs_name.grant_send_messages(lambda1)

            event_source=SqsEventSource(dynamic_sqs_name,
                                        batch_size=10,
                                        max_batching_window= Duration.minutes(1))

            lambda2.add_event_source(event_source)

app = cdk.App()
EventbridgeSqsLambdaStack(app, "EventbridgeSqsLambdaStack")
app.synth()