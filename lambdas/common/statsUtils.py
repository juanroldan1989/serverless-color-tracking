import os
import boto3

STATS_TABLE = os.environ.get('STATS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def get_stats(api_key, action):
  data = dynamodb_client.scan(
    TableName=STATS_TABLE,
    FilterExpression='begins_with(Id, :api_key) and #action = :action',
    ExpressionAttributeNames={ "#action": "Action" },
    ExpressionAttributeValues={
      ':api_key': { 'S': api_key },
      ':action': { 'S': action }
    }
  )

  return data

def format_stats(data, action):
  stats = []

  for item in data["Items"]:
    stats.append({
      'action': action,
      'color': item['Color']['S'],
      'count': int(item['Count']['N'])
    })

  return stats
