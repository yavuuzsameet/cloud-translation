import json
import boto3

FUNCTION_NAME = 'arn:aws:lambda:us-east-1:907047290331:function:sentimentor'

translate = boto3.client('translate')
child = boto3.client('lambda')

def lambda_handler(event, context):
    
    #raw json data
    event = eval(event['body'])
    
    text = event['text']
    source = event['source'] if event['source'] else 'auto'
    target = event['target'] if event['target'] else 'en'
    
    api_response = translate.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    translated_text = api_response['TranslatedText']
    print(translated_text)

    child_response = child.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=json.dumps({
            'source':text,
            'text':translated_text,
            'language':target
        })
    )
    
    json_response = json.load(child_response['Payload'])
    sentiment_analysis = json_response['body']['Sentiment']
    
    return_response = {
        'source_text': text,
        'translated_text': translated_text,
        'sentiment_analysis':sentiment_analysis
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(return_response),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': '*'
        }
    }
