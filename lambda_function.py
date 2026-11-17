
import json
import boto3
import uuid
import os
import logging

from datetime import datetime, timezone
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")

# Get table name from environment variable
table_name = os.environ["TABLE_NAME"]

# Select DynamoDB table
table = dynamodb.Table(table_name)


# Common response function
def response(status_code, body):

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    logger.info("Contact Us API started")
    logger.info("Received event: %s", json.dumps(event))

    # Identify HTTP method and path
    method = event.get("requestContext", {}).get(
        "http", {}
    ).get("method", "")

    path = event.get("rawPath", "")

    try:

        # ---------------------------------
        # POST /contact
        # Create a new contact
        # ---------------------------------

        if method == "POST" and path.endswith("/contact"):

            body = event.get("body")

            if isinstance(body, str):
                body = json.loads(body)

            if not isinstance(body, dict):
                return response(400, {
                    "message": "Request body is required"
                })

            name = body.get("name")
            email = body.get("email")
            subject = body.get("subject")
            message = body.get("message")

            if not all([
                isinstance(value, str) and value.strip()
                for value in [name, email, subject, message]
            ]):
                return response(400, {
                    "message": "All fields are required"
                })

            name = name.strip()
            email = email.strip()
            subject = subject.strip()
            message = message.strip()

            if "@" not in email:
                return response(400, {
                    "message": "Invalid email address"
                })

            contact_id = str(uuid.uuid4())

            item = {
                "contactId": contact_id,
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
                "createdAt": datetime.now(
                    timezone.utc
                ).isoformat()
            }

            table.put_item(Item=item)

            logger.info("Contact saved: %s", contact_id)

            return response(201, {
                "message": "Contact submitted successfully",
                "contactId": contact_id
            })


        # ---------------------------------
        # GET /contacts
        # Retrieve all contacts
        # ---------------------------------

        elif method == "GET" and path.endswith("/contacts"):

            result = table.scan()

            contacts = result.get("Items", [])

            # Handle pagination
            while "LastEvaluatedKey" in result:

                result = table.scan(
                    ExclusiveStartKey=result["LastEvaluatedKey"]
                )

                contacts.extend(result.get("Items", []))

            return response(200, {
                "message": "Contacts retrieved successfully",
                "count": len(contacts),
                "contacts": contacts
            })


        # ---------------------------------
        # DELETE /contact/{id}
        # Delete one contact
        # ---------------------------------

        elif method == "DELETE":

            path_parameters = event.get("pathParameters") or {}

            contact_id = path_parameters.get("id")

            if not contact_id:
                return response(400, {
                    "message": "Contact ID is required"
                })

            result = table.delete_item(
                Key={
                    "contactId": contact_id
                },
                ReturnValues="ALL_OLD"
            )

            deleted_contact = result.get("Attributes")

            if not deleted_contact:
                return response(404, {
                    "message": "Contact not found"
                })

            logger.info("Contact deleted: %s", contact_id)

            return response(200, {
                "message": "Contact deleted successfully",
                "contactId": contact_id
            })


        # ---------------------------------
        # PUT /contact/{id}
        # Update an existing contact
        # ---------------------------------

        elif method == "PUT":

            path_parameters = event.get("pathParameters") or {}

            contact_id = path_parameters.get("id")

            if not contact_id:
                return response(400, {
                    "message": "Contact ID is required"
                })

            body = event.get("body")

            if isinstance(body, str):
                body = json.loads(body)

            if not isinstance(body, dict):
                return response(400, {
                    "message": "Request body is required"
                })

            name = body.get("name")
            email = body.get("email")
            subject = body.get("subject")
            message = body.get("message")

            if not all([
                isinstance(value, str) and value.strip()
                for value in [name, email, subject, message]
            ]):
                return response(400, {
                    "message": "All fields are required"
                })

            name = name.strip()
            email = email.strip()
            subject = subject.strip()
            message = message.strip()

            if "@" not in email:
                return response(400, {
                    "message": "Invalid email address"
                })

            result = table.update_item(
                Key={
                    "contactId": contact_id
                },
                UpdateExpression="""
                    SET #n = :name,
                        email = :email,
                        subject = :subject,
                        #m = :message,
                        updatedAt = :updatedAt
                """,
                ConditionExpression="attribute_exists(contactId)",
                ExpressionAttributeNames={
                    "#n": "name",
                    "#m": "message"
                },
                ExpressionAttributeValues={
                    ":name": name,
                    ":email": email,
                    ":subject": subject,
                    ":message": message,
                    ":updatedAt": datetime.now(
                        timezone.utc
                    ).isoformat()
                },
                ReturnValues="ALL_NEW"
            )

            updated_contact = result.get("Attributes")

            logger.info("Contact updated: %s", contact_id)

            return response(200, {
                "message": "Contact updated successfully",
                "contact": updated_contact
            })


        # ---------------------------------
        # GET /contact/{id}
        # Retrieve one contact
        # ---------------------------------

        elif method == "GET":

            path_parameters = event.get("pathParameters") or {}

            contact_id = path_parameters.get("id")

            if not contact_id:
                return response(400, {
                    "message": "Contact ID is required"
                })

            result = table.get_item(
                Key={
                    "contactId": contact_id
                }
            )

            contact = result.get("Item")

            if not contact:
                return response(404, {
                    "message": "Contact not found"
                })

            return response(200, {
                "message": "Contact retrieved successfully",
                "contact": contact
            })


        # ---------------------------------
        # Unsupported request
        # ---------------------------------

        else:

            return response(404, {
                "message": "Route not found"
            })


    except json.JSONDecodeError:

        return response(400, {
            "message": "Invalid JSON request"
        })


    except ClientError as error:

        error_code = error.response["Error"]["Code"]

        logger.exception("DynamoDB error")

        if error_code == "ConditionalCheckFailedException":
            return response(404, {
                "message": "Contact not found"
            })

        return response(500, {
            "message": "DynamoDB operation failed",
            "error": error.response["Error"]["Message"]
        })


    except Exception as error:

        logger.exception("Unexpected error")

        return response(500, {
            "message": "Internal server error",
            "error": str(error)
        })
