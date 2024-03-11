import base64
import json
import os
import boto3
from lambdas.consumers.common.updateCount import updateCount

def handler(event, context):
  try:
    for record in event['Records']:
      payload = record['kinesis']

      if payload is None:
        continue

      if payload.get('data') is None:
        continue

      message = base64.b64decode(payload['data']).decode('utf-8')

      print(f"CLICKS consumer - Kinesis Message:\n"
        f"  partition key: {payload['partitionKey']}\n"
        f"  sequence number: {payload['sequenceNumber']}\n"
        f"  kinesis schema version: {payload['kinesisSchemaVersion']}\n"
        f"  data: {message}\n")

      message = json.loads(message)
      color = message['action_color']['color_name']
      updateCount('click', color)

  except Exception as error:
    print(error)
