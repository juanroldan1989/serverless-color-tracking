import base64
import json
import os
import boto3

STATS_TABLE = os.environ.get('STATS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  try:
    for record in event['Records']:
      payload = record['kinesis']

      if payload is None:
        continue

      if payload.get('data') is None:
        continue

      message = base64.b64decode(payload['data']).decode('utf-8')

      print(f"HOVERS consumer - Kinesis Message:\n"
        f"  partition key: {payload['partitionKey']}\n"
        f"  sequence number: {payload['sequenceNumber']}\n"
        f"  kinesis schema version: {payload['kinesisSchemaVersion']}\n"
        f"  data: {message}\n")

      message = json.loads(message)
      color = message['action_color']['color_name']
      id = f"api_key_hover_{color}"

      query = dynamodb_client.get_item(
        TableName=STATS_TABLE,
        Key={'Id': { 'S': id }}
      )

      item = query.get('Item')

      if item is None:
        count = 0
      else:
        count = int(item['Count']['N'])

      dynamodb_client.put_item(
        TableName=STATS_TABLE,
        Item={
          'Id': { 'S': id },
          'Action': { 'S': 'hover' },
          'Color': { 'S': message['action_color']['color_name'] },
          'Count': { 'N': str(count + 1) }
        }
      )

  except Exception as error:
    print(error)
