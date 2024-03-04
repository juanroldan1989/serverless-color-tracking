import os
import boto3
import json
import uuid

def handler(event, context):
  kinesis = boto3.client('kinesis', region_name='us-east-1')
  streamName = os.environ.get('KINESIS_STREAM')

  if 'body' not in event:
    return {
      'statusCode': 400,
      'body': json.dumps({
        'message': 'No body was found'
      })
    }

  if streamName is None:
    return {
        'statusCode': 400,
        'body': json.dumps({
          'message': 'streamName is not set in the environment variables.'
        })
      }

  try:
    kinesis.put_record(
      StreamName=streamName,
      PartitionKey=str(uuid.uuid4()),
      Data=event['body']
    )
    message = 'Message placed in the Event Stream!'
    status_code = 200
  except Exception as e:
    print(e)
    message = str(e)
    status_code = 500

  return {
    'statusCode': status_code,
    'body': json.dumps({
      'message': message
    })
  }
