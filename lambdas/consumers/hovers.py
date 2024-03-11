import base64
import json
import os
import boto3
from lambdas.consumers.common.updateCount import updateCount

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
      updateCount('hover', color)

  except Exception as error:
    print(error)
