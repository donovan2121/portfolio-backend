import boto3
import json
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'portfolio-visitor'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
healthPath = '/health'
visitorsPath = '/visitors'
indexPath = '/'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == visitorsPath:
        response = getVisitors(event['queryStringParameters']['id'])
    elif httpMethod == postMethod and path == visitorsPath:
        response = saveVisitors(json.loads(event['body']))
    elif httpMethod == patchMethod and path == visitorsPath:
        requestBody = json.loads(event['body'])
        response = modifyVisitors(requestBody['id'], requestBody['updateKey'], requestBody['updateValue'])
    else:
        response = buildResponse(404, 'Not Found')
    
    return response

def buildResponse(statusCode, body=None):
    response = {
        "isBase64Encoded": False,
        'statusCode': statusCode,
        'headers': {
            'content-type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response


def getVisitors(Id):
    try:
        response = table.get_item(
            Key={
                'id': Id
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {"Message": "Id: ${Id} not Found"})
    except:
        logger.exception('Unable to query Id from ${table}')

def saveVisitors(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Unable to save PUT operation')

def modifyVisitors(Id, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'id': Id
            },
            UpdateExpression = 'set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdateAttributes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Unable to update value of ${Id}')
    



