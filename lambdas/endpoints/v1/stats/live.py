import json
import boto3
import os

CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
STATS_TABLE = os.environ.get('STATS_TABLE')

dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  print("event: ", event)

  connectionId = event.get("requestContext", {}).get("connectionId")

  print("connectionId: ", connectionId)

  try:
    if event["requestContext"]["eventType"] == "CONNECT":
      dynamodb_client.put_item(
        TableName=CONNECTIONS_TABLE,
        Item={'ConnectionId': { 'S': connectionId } }
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

def broadcast_stats(event, context):
  print("broadcast_stats event: ", event)
  print("requestContext: ", event['requestContext'])
  print("body: ", event['body'])
  body = json.loads(event['body'])
  api_key = body['api_key']

  if api_key is None:
    return {
      'statusCode': 401,
      'body': json.dumps({
        'message': 'Unauthorized: Missing `api_key`'
      })
    }

  event_type = body['event_type']

  if event_type is None:
    return {
      'statusCode': 400,
      'body': json.dumps({
        'message': 'Bad Request: Missing `event_type`'
      })
    }
  try:
    connections = dynamodb_client.scan(TableName=CONNECTIONS_TABLE)
    data = dynamodb_client.scan(
      TableName=STATS_TABLE,
      FilterExpression='begins_with(Id, :api_key) and #action = :action',
      ExpressionAttributeNames={ "#action": "Action" },
      ExpressionAttributeValues={
        ':api_key': { 'S': api_key },
        ':action': { 'S': event_type } # click or hover
      }
    )
    stats = []
    for item in data["Items"]:
      stats.append({
        'action': item['Action']['S'],
        'color': item['Color']['S'],
        'count': int(item['Count']['N'])
      })

    print("stats: ", stats)
    print("connections['Items']: ", connections["Items"])

    for connection in connections["Items"]:
      _send_to_connection(connection["ConnectionId"]["S"], stats, event)

    return {
      'statusCode': 200,
      'headers': {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Credentials': True
      },
      'body': 'Data sent.'
    }

  except Exception as error:
    print(error)
    return {
      'statusCode': 500,
      'body': json.dumps({
          'message': str(error)
      })
    }

def _send_to_connection(connection_id, data, event):
  endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
  print("endpoint_url: ", endpoint_url)
  gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

  try:
    gatewayapi.post_to_connection(
      ConnectionId=connection_id,
      Data=json.dumps(data).encode('utf-8')
    )
  except Exception as e:
    print("post_to_connection error: ", e)
    dynamodb_client.delete_item(
      TableName=CONNECTIONS_TABLE,
      Key={'ConnectionId': { 'S': connection_id } }
    )
