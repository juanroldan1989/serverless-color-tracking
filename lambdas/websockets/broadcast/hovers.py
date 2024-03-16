import json
from lambdas.common.extractUtils import extract_payload
from lambdas.websockets.broadcast.common.connectionUtils import get_connections, send_to_connection
from lambdas.common.statsUtils import format_stats, get_stats

def handler(event, context):
  print("broadcast_stats event: ", event)

  try:
    for record in event['Records']:
      payload = extract_payload(record)

      print("payload: ", payload)

      if payload['api_key'] is None:
        continue

      connections = get_connections(payload['api_key'])
      data = get_stats(payload['api_key'], 'hover')
      stats = format_stats(data, 'hover')

      print("stats: ", stats)
      print("connections['Items']: ", connections["Items"])

      for connection in connections["Items"]:
        print("connection in loop: ", connection)
        data = { 'stats': stats, 'event_type': 'hover' }
        send_to_connection(connection, data)

  except Exception as error:
    print('error: ', error)
    return {
      'statusCode': 500,
      'body': json.dumps({
          'message': str(error)
      })
    }
