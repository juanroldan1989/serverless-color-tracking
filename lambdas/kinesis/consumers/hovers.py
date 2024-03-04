import base64

def handler(event, context):
  try:
    for record in event['Records']:
      payload = record['kinesis']
      message = base64.b64decode(payload['data']).decode('utf-8')

      print(f"HOVERS consumer - Kinesis Message:\n"
          f"  partition key: {payload['partitionKey']}\n"
          f"  sequence number: {payload['sequenceNumber']}\n"
          f"  kinesis schema version: {payload['kinesisSchemaVersion']}\n"
          f"  data: {message}\n")

      # Do something
  except Exception as error:
    print(error)
