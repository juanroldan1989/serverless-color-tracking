import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

def create(event):
    data = json.loads(event["body"])

    if data is None:
        print("Validation Failed")
        raise Exception("Couldn't create the event item.")

    if data['action_color']['color'] not in ['red', 'blue', 'green']:
        print("Validation Failed")
        raise Exception("Couldn't create the event item.")

    if data['action_color']['action'] not in ['click', 'hover']:
        print("Validation Failed")
        raise Exception("Couldn't create the event item.")

    timestamp = str(datetime.now())

    # table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    item = {
        "id": str(uuid.uuid1()),
        "action": data['action_color']['action'],
        "color": data['action_color']['color'],
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }

    # # write the event to the database
    # table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item),
    }

    return response
