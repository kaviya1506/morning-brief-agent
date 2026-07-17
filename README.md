
# ☀️ Morning Productivity Brief Agent

An AI-powered agent that automatically runs every morning at 6 AM and sends you a personalized productivity brief via email.

## What It Does
- 🌤️ Fetches current weather for your city
- 💬 Generates a motivational quote
- 📋 Provides 3 productivity tips for the day
- 📧 Sends everything to your email automatically

## Architecture

## AWS Services Used
| Service | Purpose |
|---------|---------|
| AWS Lambda | Runs the agent code |
| Amazon Bedrock (Nova Micro) | AI-generated morning brief |
| Amazon EventBridge Scheduler | Triggers agent daily at 6 AM |
| Amazon SNS | Sends email notification |

## Setup Instructions

1. Create an AWS Free Tier account
2. Enable Amazon Nova Micro model in Bedrock
3. Create an SNS Topic and subscribe your email
4. Create a Lambda function with the code in `lambda_function.py`
5. Add permissions: `AmazonBedrockFullAccess` and `AmazonSNSFullAccess`
6. Set up EventBridge Scheduler with cron: `30 0 * * ? *` (6 AM IST)

## Environment Variables
- `CITY` - Your city name (default: Chennai)
- `WEATHER_API_KEY` - OpenWeatherMap API key (get free at openweathermap.org)
- `SNS_TOPIC_ARN` - Your SNS Topic ARN

## Built For
AWS Builder Center - Weekend Agent Challenge (July 2026)

## Author
Kaviya
