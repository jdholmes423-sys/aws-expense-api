import json
import os
import uuid

import boto3

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "POST":
        return create_expense(event)

    if http_method == "GET":
        return get_expenses(event)

    if http_method == "DELETE":
        return delete_expense(event)

    return {
        "statusCode": 405,
        "body": json.dumps({
            "message": "Method not allowed."
        })
    }


def create_expense(event):
    body = json.loads(event["body"])

    expense_id = str(uuid.uuid4())

    item = {
        "expense_id": expense_id, 
        "description": body["description"],
        "amount": body["amount"],
        "category": body["category"]
    }

    table.put_item(Item=item)


    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Expense created successfully.",
            "expense": item
        })
    }