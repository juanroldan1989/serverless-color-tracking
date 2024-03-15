import base64
import json

def extract_payload(record):
  payload = record['kinesis']

  if payload is None:
    return None

  if payload.get('data') is None:
    return None

  message = base64.b64decode(payload['data']).decode('utf-8')
  message = json.loads(message)

  return message
