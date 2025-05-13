import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def setup_dynamodb_table():
    """Creates a DynamoDB table to store sensor data."""
    region = os.getenv('AWS_DEFAULT_REGION', 'eu-north-1')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table_name = 'weatherSensor'

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'deviceId', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'deviceId', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table '{table_name}' is being created...")
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully!")

    except Exception as error:
        print(f"Failed to create table: {error}")

if __name__ == "__main__":
    setup_dynamodb_table()
