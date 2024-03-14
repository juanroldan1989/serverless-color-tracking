import base64
import json
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
      message = json.loads(message)

      if message['api_key'] is None:
        continue

      updateCount(message['api_key'], 'click', message['action_color']['color_name'])

  except Exception as error:
    print(error)
