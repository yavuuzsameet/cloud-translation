import json
import boto3

def lambda_handler(event, context):
    
    table = boto3.resource('dynamodb').Table('sentiment')
    
    resp = table.scan()
    
    return {
        'statusCode': 200,
        'body': resp
    }
