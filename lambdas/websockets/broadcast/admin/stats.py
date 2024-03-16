# When user A (with api_key "api_key_A") hovers on red cell
# Then we should ONLY broadcast this update back to Admin Stats Dashboard:

# {
#   "api_key": "api_key_A",
#   "action": "hover",
#   "color": "red",
#   "count": "15"
# }

# Within Admin Stats dashboard, we should update cell: <td id="api_key_A_hover_red">15</td>

# This is a more "granular" approach when updating stats

import json
from lambdas.common.extractUtils import extract_payload
from lambdas.common.statsUtils import get_single_stat
from lambdas.websockets.broadcast.common.connectionUtils import get_connections, send_to_connection

def handler(event, context):
  print("event: ", event)

  try:
    for record in event['Records']:
      payload = extract_payload(record)

      print("payload: ", payload)

      if payload['api_key'] is None:
        continue

      connections = get_connections(payload['api_key'])
      stat = get_single_stat(payload['api_key'], payload['action_color']['action_name'], payload['action_color']['color_name'])

      print("stat: ", stat)

      for connection in connections["Items"]:
        print("connection in loop: ", connection)

        data = {
          "api_key": payload['api_key'],                    # read from kinesis stream
          "action": payload['action_color']['action_name'], # read from kinesis stream
          "color": payload['action_color']['color_name'],   # read from kinesis stream
          "count": stat['Count']['N']                       # read from dynamodb
        }

        send_to_connection(connection, data)

  except Exception as error:
    print('error: ', error)
    return {
      'statusCode': 500,
      'body': json.dumps({
          'message': str(error)
      })
    }
