import json
import os
import boto3
from lambdas.common.statsUtils import format_stats, get_stats

STATS_TABLE = os.environ.get('STATS_TABLE')
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
    data = get_stats(api_key, action)
    stats = format_stats(data, action)

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
