
# AWS Contact Us Form API

## Project Overview

This project demonstrates how to build a serverless Contact Us Form API using AWS services.

Users can create, retrieve, update, and delete contact messages through API endpoints.

The project uses Amazon API Gateway, AWS Lambda, Amazon DynamoDB, IAM, and CloudWatch.

## Architecture

```text
              User / Postman
                    |
                    v
              API Gateway
                HTTP API
                    |
                    v
               AWS Lambda
               Python 3.12
                    |
                    v
                DynamoDB
             ContactMessages

                    |
                    v
               CloudWatch
             Logs & Metrics
```

## AWS Services Used

| AWS Service | Purpose |
|---|---|
| API Gateway | Receives HTTP API requests |
| AWS Lambda | Executes Python backend code |
| DynamoDB | Stores contact messages |
| IAM | Manages permissions |
| CloudWatch | Monitoring and logging |

## AWS Resource Configuration

| Resource | Name |
|---|---|
| DynamoDB Table | ContactMessages |
| Partition Key | contactId (String) |
| IAM Role | LambdaContactUsRole |
| IAM Policy | ContactMessagesDynamoDBAccess |
| Lambda Function | ContactUsFunction |
| API Gateway | ContactUsAPI |
| API Stage | dev |
| Environment Variable | TABLE_NAME=ContactMessages |
| Runtime | Python 3.12 |
| AWS Region | ap-south-1 (Mumbai) |

## API Base URL

Replace YOUR_API_ID with your actual API Gateway ID.

```text
https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/dev
```

## API Endpoints

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | /contact | Create a new contact |
| GET | /contacts | Retrieve all contacts |
| GET | /contact/{id} | Retrieve a contact by ID |
| PUT | /contact/{id} | Update an existing contact |
| DELETE | /contact/{id} | Delete a contact |

### 1. Create Contact - POST

Endpoint:

```text
POST /contact
```

Request Body:

```json
{
  "name": "John",
  "email": "john@example.com",
  "subject": "AWS Project",
  "message": "I am interested in your services."
}
```

Expected Status: `201 Created`

### 2. Get All Contacts - GET

Endpoint:

```text
GET /contacts
```

Retrieves all contact messages stored in DynamoDB.

Expected Status: `200 OK`

### 3. Get Contact by ID - GET

Endpoint:

```text
GET /contact/{id}
```

Retrieves a specific contact using its unique contact ID.

Expected Status: `200 OK`

### 4. Update Contact - PUT

Endpoint:

```text
PUT /contact/{id}
```

Request Body:

```json
{
  "name": "John Updated",
  "email": "john@example.com",
  "subject": "Updated Subject",
  "message": "This is an updated message."
}
```

Expected Status: `200 OK`

### 5. Delete Contact - DELETE

Endpoint:

```text
DELETE /contact/{id}
```

Deletes a contact record from DynamoDB using its unique contact ID.

Expected Status: `200 OK`

## DynamoDB Configuration

Table Name: `ContactMessages`

Partition Key: `contactId`

Data Type: String

Example DynamoDB Item:

```json
{
  "contactId": "unique-contact-id",
  "name": "John",
  "email": "john@example.com",
  "subject": "AWS Project",
  "message": "Interested in your services.",
  "createdAt": "2026-11-17T10:00:00+00:00"
}
```

Updated records also contain an `updatedAt` attribute.

## IAM Permissions

Lambda Execution Role:

`LambdaContactUsRole`

Custom Inline Policy:

`ContactMessagesDynamoDBAccess`

DynamoDB permissions:

- dynamodb:PutItem
- dynamodb:GetItem
- dynamodb:Scan
- dynamodb:DeleteItem
- dynamodb:UpdateItem

The policy is scoped to the ContactMessages DynamoDB table.

The role also uses the AWS managed policy:

`AWSLambdaBasicExecutionRole`

This allows Lambda to write execution logs to CloudWatch.

## CloudWatch Monitoring

CloudWatch is used to monitor the Lambda function.

Log Group:

```text
/aws/lambda/ContactUsFunction
```

Metrics:

- Invocations
- Errors
- Duration
- Throttles

Log retention: 7 days.

## API Testing

The API was tested using Postman.

Test scenarios:

| Test Scenario | Expected Status |
|---|---|
| Create contact | 201 |
| Get all contacts | 200 |
| Get contact by ID | 200 |
| Update contact | 200 |
| Delete contact | 200 |
| Invalid API route | 404 |
| Contact not found | 404 |
| Invalid email | 400 |
| Missing required field | 400 |

## Key Features

- Serverless application architecture
- API Gateway HTTP API integration
- Python backend using AWS Lambda
- DynamoDB CRUD operations
- Unique contact ID generation
- IAM role and policy configuration
- Environment variable configuration
- Error handling
- CloudWatch logging and monitoring
- API testing using Postman

## What I Learned

Through this hands-on project, I learned:

1. Creating and configuring DynamoDB tables.
2. Creating IAM roles and policies.
3. Developing AWS Lambda functions using Python.
4. Connecting Lambda with DynamoDB using Boto3.
5. Creating HTTP APIs using API Gateway.
6. Configuring API routes and integrations.
7. Performing CRUD operations through API endpoints.
8. Testing APIs using Postman.
9. Monitoring Lambda executions using CloudWatch.
10. Applying the principle of least privilege in IAM.

## Future Improvements

- Build a frontend Contact Us form.
- Add authentication and authorization.
- Configure AWS WAF.
- Implement pagination.
- Add automated testing.
- Configure CI/CD using GitHub Actions.
- Add email notifications using Amazon SES.

## Project Structure

```text
aws-contact-us-api/
│
├── lambda_function.py
│
└── README.md
```

## Technologies Used

- AWS
- Python 3.12
- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch
- Postman
- GitHub

## Disclaimer

This project was created for AWS learning and hands-on practice.

Additional security, authentication, and operational controls are required before using this application in production.
