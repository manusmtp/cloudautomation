import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Specify the sender and recipient email addresses
    sender = "man1@gmail.com"  # Update with your verified sender email
    recipient = "man2@gmail.com"  # Update with your verified recipient email
    
    # Set the AWS region
    aws_region = "us-east-1"  # Update with your region
    
    # Create the subject and body of the email
    subject = f"New Object Created in S3 Bucket {bucket_name}"
    body_text = (f"An object has been created in the S3 bucket {bucket_name}.\n"
                 f"Object Key: {object_key}")
    
    # Create a new SES resource and specify a region
    ses_client = boto3.client('ses', region_name=aws_region)
    
    # Try to send the email
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=sender,
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully!')
    }
