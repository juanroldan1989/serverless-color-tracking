import os
import boto3
import json
import uuid

def handler(event, context):
  if 'body' not in event:
    return {
      'statusCode': 400,
      'body': json.dumps({
        'message': 'No body was found'
      })
    }

  body = json.loads(event['body'])

  print(f"Event Body: {body}")

  if body['action_color']['action_name'] == 'hover':
    streamName = os.environ.get('KINESIS_HOVERS_STREAM')

  if body['action_color']['action_name'] == 'click':
    streamName = os.environ.get('KINESIS_CLICKS_STREAM')

  if streamName is None:
    return {
        'statusCode': 400,
        'body': json.dumps({
          'message': 'streamName is not set in the environment variables.'
        })
      }

  kinesis = boto3.client('kinesis', region_name='us-east-1')

  try:
    kinesis.put_record(
      StreamName=streamName,
      PartitionKey=str(uuid.uuid4()),
      Data=event['body']
    )
    message = f'Message placed in {streamName} successfully.'
    status_code = 200
  except Exception as e:
    print(e)
    message = str(e)
    status_code = 500

  return {
    'statusCode': status_code,
    'headers': {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': True
    },
    'body': json.dumps({
      'message': message
    })
  }
