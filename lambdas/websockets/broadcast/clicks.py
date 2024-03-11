import json
import os
import boto3

CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
STATS_TABLE = os.environ.get('STATS_TABLE')

dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  print("broadcast_stats event: ", event)

  try:
    connections = dynamodb_client.scan(TableName=CONNECTIONS_TABLE)
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
      _send_to_connection(connection["ConnectionId"]["S"], { 'stats': stats, 'event_type': 'click' }, event)

  except Exception as error:
    print('error: ', error)
    return {
      'statusCode': 500,
      'body': json.dumps({
          'message': str(error)
      })
    }

def _send_to_connection(connection_id, data, event):
  # TODO: build endpoint_url using requestContext from event
  #       requestContext values are present for lambdas that handle API Gateway events
  # endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
  endpoint_url = "https://s1h9o8dplb.execute-api.us-east-1.amazonaws.com/dev"
  print("endpoint_url: ", endpoint_url)
  gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)
  gatewayapi.post_to_connection(
    ConnectionId=connection_id,
    Data=json.dumps(data).encode('utf-8')
  )
