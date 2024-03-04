import json
import os
import boto3

STATS_TABLE = os.environ.get('DYNAMODB_STATS_TABLE')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  api_key = event.get('headers', {}).get('Authorization')

  if api_key is None:
    return {
      'statusCode': 401,
      'body': json.dumps({
        'message': 'Unauthorized: Missing `Authorization` header'
      })
    }

  action = event.get('queryStringParameters', {}).get('action')

  if action is None:
    return {
      'statusCode': 400,
      'body': json.dumps({
        'message': 'Bad Request: Missing `action` query parameter'
      })
    }

  try:
    response = dynamodb_client.scan(
      TableName=STATS_TABLE,
      FilterExpression='begins_with(Id, :api_key) and #action = :action',
      ExpressionAttributeNames={ "#action": "Action" },
      ExpressionAttributeValues={
        ':api_key': { 'S': api_key },
        ':action': { 'S': action }
      }
    )
    items = response.get('Items')
    stats = []
    for item in items:
      stats.append({
        'action': action,
        'color': item['Color']['S'],
        'count': int(item['Count']['N'])
      })
    return {
      'statusCode': 200,
      'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True
      },
      'body': json.dumps({
        'stats': stats
      })
    }
  except Exception as error:
    print(error)
    return {
      'statusCode': 500,
      'body': json.dumps({
        'message': str(error)
      })
    }
