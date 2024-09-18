import boto3
import json

def lambda_handler(event, context):
    bucket_name = 'krolok.pics'
    
    # Parse the body of the request
    if 'body' in event:
        body = json.loads(event['body'])
        folder_name = body.get('folder_name', 'krolok')
    else:
        folder_name = event.get('folder_name', 'krolok')
    
    # Construct the full prefix path
    prefix = f'images/{folder_name}'
    
    # Ensure the prefix ends with a slash
    if not prefix.endswith('/'):
        prefix += '/'
    
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # List all objects in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # Get the region of the bucket
    region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    
    # Construct URLs for each image
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    image_urls = []
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if any(key.lower().endswith(ext) for ext in image_extensions):
                # Construct the S3 URL for each object
                url = f'https://s3.{region}.amazonaws.com/{bucket_name}/{key}'
                image_urls.append(url)
    
    # Create a JSON response with the image URLs
    json_response = json.dumps({'image_urls': image_urls, 'pet': folder_name, 'event': event})
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json_response
    }