import json

def handler(event, context):
    # Log the event received from SQS
    print("Received SQS event:", json.dumps(event))

    # Process the SQS message
    for record in event['Records']:
        # Extract message body
        message_body = json.loads(record['body'])

        # Process the message
        print("Received message:", message_body['message'])

    return {
        'statusCode': 200,
        'body': json.dumps('SQS message processed successfully!')
    }
