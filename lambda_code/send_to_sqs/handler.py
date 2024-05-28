import json
import boto3
import os

def handler(event, context):
    # Get the SQS queue URL from environment variable set by CDK
    queue_url = os.environ['QUEUE_URL']

    # Create an SQS client
    sqs = boto3.client('sqs')

    # Sample data to send to SQS
    message = {
        'message': 'Hello from the sender Lambda function!'
    }

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

    print("Message sent to SQS:", response)

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to SQS successfully!')
    }
