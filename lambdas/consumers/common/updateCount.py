import os
import boto3

STATS_TABLE = os.environ.get('STATS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def updateCount(action, color):
  id = f"api_key_{action}_{color}"

  query = dynamodb_client.get_item(
    TableName=STATS_TABLE,
    Key={'Id': { 'S': id }}
  )

  item = query.get('Item')

  if item is None:
    count = 0
  else:
    count = int(item['Count']['N'])

  dynamodb_client.put_item(
    TableName=STATS_TABLE,
    Item={
      'Id': { 'S': id },
      'Action': { 'S': action },
      'Color': { 'S': color },
      'Count': { 'N': str(count + 1) }
    }
  )
