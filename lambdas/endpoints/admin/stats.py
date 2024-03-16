import json
import os
import boto3
from lambdas.common.statsUtils import format_stats, get_stats

ADMIN_API_KEY = os.environ.get('ADMIN_API_KEY')
CONNECTIONS_TABLE = os.environ.get('CONNECTIONS_TABLE')
STATS_TABLE = os.environ.get('STATS_TABLE')

dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
  api_key = event.get('headers', {}).get('Authorization')

  if api_key is None or api_key != ADMIN_API_KEY:
    return {
      'statusCode': 401,
      'body': json.dumps({
        'message': 'Unauthorized'
      })
    }

  all_stats = []

  try:
    for record in _get_api_keys():
      for action in ['hover', 'click']:
        api_key = record['ApiKey']['S']
        data = get_stats(api_key, action)
        stats = format_stats(data, action)

        all_stats.append({
          'api_key': api_key,
          'action': action,
          'counts': stats
        })

    return {
      'statusCode': 200,
      'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True
      },
      'body': json.dumps({
        'stats': all_stats
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

def _get_api_keys():
  response = dynamodb_client.scan(
    TableName=CONNECTIONS_TABLE,
    ProjectionExpression='ApiKey'
  )
  return response['Items']
