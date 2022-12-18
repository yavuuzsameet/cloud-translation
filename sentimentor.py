import json
import boto3

sentiment = boto3.client('comprehend')

def lambda_handler(event, context):
    
    source = event['source']
    
    text = event['text']
    lang = event['language']
    
    response = sentiment.detect_sentiment(Text=text, LanguageCode=lang)
    sentiment_analysis = response['Sentiment']
    
    put2table(source, text, sentiment_analysis)
    
    return {
        'statusCode': 200,
        'body': response
    }

def put2table(source, translation, analysis):
    table = boto3.resource('dynamodb').Table('sentiment')
    
    resp = table.scan()
    count = resp['Count']
    
    table.put_item(
        Item={
            "id": count,
            "source": source,
            "translation": translation,
            "sentiment": analysis
        }
    )
    