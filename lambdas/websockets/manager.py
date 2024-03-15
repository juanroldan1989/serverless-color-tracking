import json
import boto3
import os

CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
STATS_TABLE = os.environ.get('STATS_TABLE')

dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  print("event: ", event)
  # TODO: use api_key from client
  # api_key = event.get('headers', {}).get('Sec-WebSocket-Protocol')
  connectionId = event.get("requestContext", {}).get("connectionId")

  print("connectionId: ", connectionId)

  try:
    if event["requestContext"]["eventType"] == "CONNECT":
      dynamodb_client.put_item(
        TableName=CONNECTIONS_TABLE,
        Item={
          'ConnectionId': { 'S': connectionId },
          'DomainName': { 'S': event["requestContext"]["domainName"] },
          'Stage': { 'S': event["requestContext"]["stage"] },
          'ApiKey': { 'S': 'api_key' }
        }
      )

      return {
        "statusCode": 200,
        "body": "Connected."
      }

    if event["requestContext"]["eventType"] == "DISCONNECT":
      dynamodb_client.delete_item(
        TableName=CONNECTIONS_TABLE,
        Key={'ConnectionId': { 'S': connectionId } }
      )

      return {
        "statusCode": 200,
        "body": "Disconnected."
      }

    else:
      return {
        "statusCode": 500,
        "body": "Unrecognized event type."
      }

  except Exception as error:
    print(error)
    return {
      'statusCode': 500,
      'body': json.dumps({
        'message': str(error)
      })
    }
