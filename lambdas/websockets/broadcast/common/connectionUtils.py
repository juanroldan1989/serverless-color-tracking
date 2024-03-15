import boto3
import json
import os

CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def get_connections(api_key):
  connections = dynamodb_client.scan(
    TableName=CONNECTIONS_TABLE,
    FilterExpression='#api_key = :api_key',
    ExpressionAttributeNames={ "#api_key": "ApiKey" },
    ExpressionAttributeValues={ ':api_key': { 'S': api_key } }
  )

  return connections

def send_to_connection(connection, data):
  endpoint_url = "https://" + connection["DomainName"]["S"] + "/" + connection["Stage"]["S"]
  print("endpoint_url: ", endpoint_url)

  gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

  gatewayapi.post_to_connection(
    ConnectionId=connection["ConnectionId"]["S"],
    Data=json.dumps(data).encode('utf-8')
  )
