import boto3
import plotly.graph_objects as go
from flask import Flask, render_template_string
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# AWS-konfiguration
REGION = os.getenv('AWS_REGION', 'eu-north-1')
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table('IoTWeatherData')

app = Flask(__name__)

def retrieve_sensor_data():
    """Hämtar temperaturdata från de senaste 24 timmarna."""
    current_time = int(time.time())
    try:
        response = table.query(
            KeyConditionExpression="deviceId = :deviceId AND #ts > :recent",
            ExpressionAttributeNames={"#ts": "timestamp"},
            ExpressionAttributeValues={
                ':deviceId': 'sensor-01',
                ':recent': current_time - (24 * 60 * 60)
            }
        )
        return sorted(response.get('Items', []), key=lambda item: item['timestamp'])
    except Exception as error:
        print(f"Fel vid hämtning av data: {error}")
        return []

@app.route('/')
def dashboard():
    """Visar temperaturgraf i webbläsaren."""
    data = retrieve_sensor_data()
    if not data:
        return "<h1 style='text-align:center; margin-top:50px;'>❌ Ingen data tillgänglig för senaste 24 timmarna.</h1>"

    temperatures = [float(item['temperature']) for item in data]
    timestamps = [datetime.fromtimestamp(int(item['timestamp'])) for item in data]

    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines+markers'))
    fig.update_layout(
        title='Temperaturdata (senaste 24 timmarna)',
        xaxis_title='Tidpunkt',
        yaxis_title='Temperatur (°C)',
        template='plotly_dark'
    )

    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <title>Temperaturdashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #1e11e2f;
                color: #ffffff;
                padding-top: 40px;
            }
            .container {
                max-width: 1000px;
                margin: auto;
                background-color: #6a8a50;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.4);
            }
            h1 {
                text-align: center;
                margin-bottom: 40px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌡️ IoTWeatherData</h1>
            {{ graph | safe }}
        </div>
    </body>
    </html>
    ''', graph=graph_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
