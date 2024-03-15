import json
import os
import boto3

CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
STATS_TABLE = os.environ.get('STATS_TABLE')

dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  print("broadcast_stats event: ", event)

  # TODO: use api_key from kinesis event similar as in consumers logic.

  try:
    connections = dynamodb_client.scan(
      TableName=CONNECTIONS_TABLE,
      FilterExpression='#api_key = :api_key',
      ExpressionAttributeNames={ "#api_key": "ApiKey" },
      ExpressionAttributeValues={ ':api_key': { 'S': 'api_key' } }
    )
    data = dynamodb_client.scan(
      TableName=STATS_TABLE,
      FilterExpression='begins_with(Id, :api_key) and #action = :action',
      ExpressionAttributeNames={ "#action": "Action" },
      ExpressionAttributeValues={
        ':api_key': { 'S': 'api_key' },
        ':action': { 'S': 'click' }
      }
    )
    stats = []
    for item in data["Items"]:
      stats.append({
        'action': 'click',
        'color': item['Color']['S'],
        'count': int(item['Count']['N'])
      })

    print("stats: ", stats)
    print("connections['Items']: ", connections["Items"])

    for connection in connections["Items"]:
      print("connection in loop: ", connection)
      data = { 'stats': stats, 'event_type': 'click' }
      _send_to_connection(connection, data)

  except Exception as error:
    print('error: ', error)
    return {
      'statusCode': 500,
      'body': json.dumps({
          'message': str(error)
      })
    }

def _send_to_connection(connection, data):
  endpoint_url = "https://" + connection["DomainName"]["S"] + "/" + connection["Stage"]["S"]
  print("endpoint_url: ", endpoint_url)
  gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)
  gatewayapi.post_to_connection(
    ConnectionId=connection["ConnectionId"]["S"],
    Data=json.dumps(data).encode('utf-8')
  )
