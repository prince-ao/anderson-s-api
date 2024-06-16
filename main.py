import boto3
import json
import random
import time

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    path = event['rawPath']
    request_method = event['requestContext']['http']['method']
    bucket_name = 'anderson-api'
    response = 'unable to process your request'

    if request_method == 'GET':
        if path == '/api/jokes/random':
            file_key = 'jokes.json'
            jokes = s3_client.get_object(Bucket=bucket_name, Key=file_key)

            parsed_jokes = json.load(jokes['Body'])

            current_time = int(time.time())
            random.seed(current_time)

            random_index = random.randint(0, len(parsed_jokes) - 1)

            return {
                'statusCode': 200,
                'body': json.dumps(parsed_jokes[random_index])
            }
        
        if (path == '/api/meaningoflife'):
            return {
                'statusCode': 200,
                'body': json.dumps('42')
            }

    return {
        'statusCode': 404,
        'body': json.dumps(f'404: request {request_method} {path} not found')
    }

