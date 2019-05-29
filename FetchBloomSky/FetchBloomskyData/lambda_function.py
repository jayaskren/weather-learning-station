
import boto3
import json
import os
from botocore.vendored import requests
from datetime import datetime
print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    weatherData = getWeatherData()
    date = changeDateFormat(weatherData['TS'])
    copyS3File(date, weatherData)
    

def getWeatherData():
    headers = {'Content-Type': 'application/json',
           'Authorization': os.environ['BLOOMSKY_API_KEY']}
    resp = requests.get('https://api.bloomsky.com/api/skydata/', headers=headers)
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /tasks/ {}'.format(resp.status_code))
    print(resp.text)
    print(resp.json()[0])
    print(resp.json()[0]['UTC'])
    print(resp.json()[0]['Data'])
    return resp.json()[0]['Data']
    # for todo_item in resp.json():
    #     print('{} {}'.format(todo_item['id'], todo_item['summary']))

def copyS3File(date, imageData):
    s3KeyName = getS3KeyName(imageData['ImageURL'])
    s3 = boto3.resource('s3')
    copy_source = {
          'Bucket': 'bskyimgs',
          'Key': s3KeyName
        }
    bucket = s3.Bucket('igniteutah-uploads')
    
    bucket.copy(copy_source, 'bloomsky/' + date + ".jpg")
    print("Finished")

def changeDateFormat(timestamp):
    SECONDS_TO_HOURS = 60*60
    mstTimestamp = timestamp - 6 * (SECONDS_TO_HOURS)
    timeAsDate = datetime.fromtimestamp(mstTimestamp)
    return timeAsDate.strftime("%Y-%m-%d_%H:%M")
    
def getS3KeyName(url):
    return url[url.rfind('/')+1:]
    
def writeToDyanmo():
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
        
        