import json
from lambdas.websockets.broadcast.common.connectionUtils import get_connections, send_to_connection
from lambdas.common.statsUtils import format_stats, get_stats

def handler(event, context):
  print("broadcast_stats event: ", event)

  # TODO: use api_key from kinesis event similar as in consumers logic.

  try:
    connections = get_connections('api_key')
    data = get_stats('api_key', 'hover')
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
