
import json
import boto3
import urllib.request
from datetime import datetime

def lambda_handler(event, context):
    
    # --- CONFIG ---
    CITY = "Chennai"  # உன் city மாத்திக்கோ
    WEATHER_API_KEY = "YOUR_API_KEY_HERE"  # OpenWeatherMap API key paste பண்ணு
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:626274382488:morning-brief-topic"
    
    # --- 1. Get Weather ---
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        with urllib.request.urlopen(weather_url) as response:
            weather_data = json.loads(response.read().decode())
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            weather_info = f"Weather in {CITY}: {temp}°C, {description}"
    except Exception as e:
        weather_info = f"Weather data unavailable: {str(e)}"
    
    # --- 2. Get Today's Date ---
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    # --- 3. Call Bedrock Nova for Morning Brief ---
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    prompt = f"""You are a helpful morning productivity assistant. 
    Today is {today}. {weather_info}.
    
    Create a short, energizing morning brief that includes:
    1. A greeting with today's date and weather
    2. A motivational quote to start the day
    3. 3 suggested productivity tips for today
    4. A reminder to stay hydrated and take breaks
    
    Keep it concise, friendly, and under 200 words."""
    
    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 500,
            "temperature": 0.7
        }
    })
    
    response = bedrock.invoke_model(
        modelId="amazon.nova-micro-v1:0",
        contentType="application/json",
        accept="application/json",
        body=body
    )
    
    result = json.loads(response['body'].read())
    morning_brief = result['output']['message']['content'][0]['text']
    
    # --- 4. Send Email via SNS ---
    sns = boto3.client('sns', region_name='us-east-1')
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"Your Morning Brief - {today}",
        Message=morning_brief
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Morning brief sent successfully!')
    }

