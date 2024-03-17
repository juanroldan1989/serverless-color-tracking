from lambdas.common.extractUtils import extract_payload
from lambdas.consumers.common.updateCount import updateCount

def handler(event, context):
  try:
    for record in event['Records']:
      payload = extract_payload(record)

      if payload['api_key'] is None:
        continue

      updateCount(payload['api_key'], 'hover', payload['color'])

  except Exception as error:
    print(error)
