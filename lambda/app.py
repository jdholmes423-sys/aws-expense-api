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

def get_expenses(event):
   # Get the path parameters from the API Gateway event. 
   # For /expenses/abc123, this should contain {"id": "abc123"}.
   path_parameters = event.get("pathParameters")

   # Check whether the request included an expense ID.
   if path_parameters and path_parameters.get("id"):

       # Retrieve the requested expense ID. 
       expense_id = path_parameters["id"]

       #Ask DynamoDB for the item with this partition key.
       response = table.get_item(
           Key={
               "expense_id": expense_id
           }
       )

       # Try to get the returned item from DynamoDB. 
       item = response.get("Item")

       # If DynamoDB didn't return an item, the expense doesn't exist. 
       if not item:

           # Return an HTTP 404 "Not Found" response.
           return {
               "statusCode": 404,

               # Convert the Python dictionary to JSON text. 
               "body": json.dumps({
                   "message": "Expense not found."
               })
           } 

       # If the expense exists, return it to the client.
       return {
           "statusCode": 200,

           # Convert the DynamoDB item into JSON text. 
           "body": json.dumps(item)
       }

   # If no ID is supplied, retrieve the collection of expenses.
   response = table.scan()

   # Return all the items found by the scan.
   return {
       "statusCode": 200,

       # Get the Items list from DynamoDB.
       # If Items doesn't exist, use an empty list. 
       "body": json.dumps(response.get("Items, []"))
   }

def delete_expense(event):
    # Get the path parameters from the API Gateway event.
    path_parameters = event.get("pathParameters")

    # Make sure the request actually contains an expense ID. 
    if not path_parameters or not path_parameters.get("id"):

        # Return HTTP 400 because the request is missing required information. 
        return {
            "statusCode": 400,

            # Explain what the client needs to provide.
            "body": json.dumps({
                "message": "Expense ID is required."
            })
        }

    # Retrieve the expense ID from the URL.
    expense_id = path_parameters["id"]

    # Delete the item and ask DynamoDB to return the item that was deleted.  
    response = table.delete_item(
        Key={
            "expense_id": expense_id
        },
        ReturnValues = "ALL_OLD"
    )

    # Check whether DynamoDB returned an item.
    deleted_item = response.get("Attributes")

    # If no item was returned, that expense didn't exist. 
    if not deleted_item:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Expense not found.",
                "expense_id": expense_id
            })
        }

    # The item existed and was successfully deleted.
    return {
       "statusCode": 200,

       # Return a JSON response containing the deleted ID.
       "body": json.dumps({
           "message": "Expense deleted successfully.",
           "expense_id": expense_id
       })
   }