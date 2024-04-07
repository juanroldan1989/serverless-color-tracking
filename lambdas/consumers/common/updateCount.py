import os
import boto3

STATS_TABLE = os.environ.get('STATS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def updateCount(api_key, action, color):
  id = f"{api_key}_{action}_{color}"

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

# TODO: instead of using `get_item` and `put_item`, use `update_item` to increment the count
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.SET.ADD

dynamodb_client.update_item(
  TableName=STATS_TABLE,
  Key={
    'Id': { 'S': id }
  },
  UpdateExpression="ADD Count :val",
  ExpressionAttributeValues={
    ':val': { 'N': '1' }
  }
)

# or

dynamodb_client.update_item(
  TableName=STATS_TABLE,
  Key={
    'Id': { 'S': id }
  },
  UpdateExpression="SET Count = if_not_exists(Count, :default_count) + :val",
  ExpressionAttributeValues={
    ':default_count': 0,
    ':val': 1
  }
)
