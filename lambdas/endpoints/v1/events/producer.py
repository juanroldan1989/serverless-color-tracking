import os
import boto3
import json
import uuid

def handler(event, context):
  api_key = event.get('headers', {}).get('Authorization')

  if api_key is None:
    return {
      'statusCode': 401,
      'body': json.dumps({
        'message': 'Unauthorized: Missing `Authorization` header'
      })
    }

  if 'body' not in event:
    return {
      'statusCode': 400,
      'body': json.dumps({
        'message': 'Missing request body.'
      })
    }

  body = json.loads(event['body'])
  body['api_key'] = api_key

  print(f"Event Body: {body}")

  if body['action_color']['action_name'] == 'hover':
    streamName = os.environ.get('HOVERS_STREAM')

  if body['action_color']['action_name'] == 'click':
    streamName = os.environ.get('CLICKS_STREAM')

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
      Data=json.dumps(body)
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
