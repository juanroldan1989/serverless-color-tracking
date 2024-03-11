# TODO: share function across consumers
def updateCount(dynamodb_client, table, message):
  action = message['action_color']['action']
  color = message['action_color']['color_name']
  id = f"api_key_{action}_{color}"

  query = dynamodb_client.get_item(
    TableName=table,
    Key={'Id': { 'S': id }}
  )

  item = query.get('Item')

  if item is None:
    count = 0
  else:
    count = int(item['Count']['N'])

  dynamodb_client.put_item(
    TableName=table,
    Item={
      'Id': { 'S': id },
      'Action': { 'S': action },
      'Color': { 'S': color },
      'Count': { 'N': str(count + 1) }
    }
  )
