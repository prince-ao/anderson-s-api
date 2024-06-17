import boto3
import json
import random
import time

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    path = event['rawPath']
    request_method = event['requestContext']['http']['method']
    bucket_name = 'anderson-api'
    path_parameters = event.get('pathParameters', {})
    response = 'unable to process your request'
    jokes_key = 'jokes.json'
    body = event.get('body')

    if request_method == 'GET':
        if path.startswith('/api/jokes'):

            if path_parameters.get('id'):
                jokes = s3_client.get_object(Bucket=bucket_name, Key=jokes_key)
                joke_id = path_parameters['id']

                parsed_jokes = json.load(jokes['Body'])
                joke = next((j for j in parsed_jokes if j['id'] == int(joke_id)), None)

                if joke:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(joke)
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'Joke not found'})
                    }

            elif path == '/api/jokes/random':
                jokes = s3_client.get_object(Bucket=bucket_name, Key=jokes_key)

                parsed_jokes = json.load(jokes['Body'])

                current_time = int(time.time())
                random.seed(current_time)

                random_index = random.randint(0, len(parsed_jokes) - 1)

                return {
                    'statusCode': 200,
                    'body': json.dumps(parsed_jokes[random_index])
                }

        elif path == '/api/meaning-of-life':
            return {
                'statusCode': 200,
                'body': json.dumps('42')
            }
            
        elif path == '/api/helloworld':
            return {
                'statusCode': 200,
                'body': json.dumps('Hello World')
            }

    elif request_method == 'POST':
        if path == '/api/jokes':
            if body:
                new_joke_data = json.loads(body)
                new_joke_text = new_joke_data.get('joke')

                if not new_joke_text:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': 'Joke text is required. Example: { joke: "joke text}'})
                    }
                
                jokes = s3_client.get_object(Bucket=bucket_name, Key=jokes_key)
                parsed_jokes = json.load(jokes['Body'])

                if parsed_jokes:
                    max_id = max(int(joke['id']) for joke in parsed_jokes)
                    new_id = max_id + 1
                else:
                    new_id = 1


                new_joke = {
                    'id': new_id,
                    'joke': new_joke_text
                }

                parsed_jokes.append(new_joke)

                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=jokes_key,
                    Body=json.dumps(parsed_jokes)
                )

                return {
                    'statusCode': 201,
                    'body': json.dumps(new_joke)
                }

            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Request body is required. Example: { joke: "joke text}'})
                }


    return {
        'statusCode': 404,
        'body': json.dumps(f'404: request {request_method} {path} not found')
    }
