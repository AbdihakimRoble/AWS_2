# Internet Of Things Temperature Monitoring System

This project demonstrates a robust **Temperature Monitoring System** that leverages **AWS IoT Core**, **DynamoDB**, and a **Flask web application** to simulate, collect, and visualize temperature data in real-time. The system integrates **temperature sensor simulation**, **cloud storage**, and **web-based data visualization** for an efficient and scalable monitoring solution.

---

## Key Features

- **Temperature Sensor Simulation**: Simulates real-time temperature readings and publishes the data to **AWS IoT Core**.
- **Fallback Data Handling**: In case of sensor failure, temperature data is fetched from the **SMHI API** to ensure continuous data collection.
- **AWS Cloud Integration**: The system uses **AWS IoT Core** for communication and **DynamoDB** to store sensor data.
- **Web-Based Dashboard**: A **Flask-based dashboard** uses **Plotly** to present temperature data from the last 24 hours.
- **Automatic Data Publishing**: Data is automatically published to **AWS IoT** and stored in **DynamoDB**.
- **Robust Error Handling**: Includes retry mechanisms for both MQTT communication and data storage to ensure data reliability.

---

## Getting Started

### Prerequisites

- **AWS Account**: Ensure you have an AWS account with necessary permissions for **IoT Core** and **DynamoDB**.
- **Python**: Version 3.10.12 or higher is recommended.
- **Required Libraries**: Install dependencies via `requirements.txt`.
- **Certificates**: Properly configure your AWS IoT Core certificates for MQTT communication.
- **SMHI API Access**: The system uses **SMHI API** as a fallback data source for temperature readings.

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
## Install Dependencies

2. **To install the required Python libraries, use the following command**:

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file with the following details:

```env
AWS_REGION=eu-north-1
IOT_ENDPOINT=<Your_IoT_Endpoint>
ROOT_CA_PATH=<Path_to_Root_CA>
PRIVATE_KEY_PATH=<Path_to_Private_Key>
CERTIFICATE_PATH=<Path_to_Certificate>
AWS_ACCESS_KEY_ID=<Your_AWS_Access_Key_ID>
AWS_SECRET_ACCESS_KEY=<Your_AWS_Secret_Access_Key>
```


##Make sure to replace the placeholders with your specific values:

- <Your_IoT_Endpoint>: The endpoint for your AWS IoT Core instance.
- <Path_to_Root_CA>: The path to the root certificate for AWS IoT.
- <Path_to_Private_Key>: The path to the private key for your IoT certificate.
- <Path_to_Certificate>: The path to the certificate for your IoT device.
- <Your_AWS_Access_Key_ID>: Your AWS access key ID.
- <Your_AWS_Secret_Access_Key>: Your AWS secret access key.

## System Design Overview

[[![Skärmbild 2025-05-13 112336](https://github.com/user-attachments/assets/7cece6ab-0ba0-4c6f-ae1b-ff6bee07f672)](https://imgur.com/a/3G5IeIv)




## Dashboard Screenshot

Here is a screenshot of the data visualization dashboard:


## ![0MZqCkk](https://github.com/user-attachments/assets/b9573ca6-e730-4788-9f83-0d721f51807f)


### Temperature Sensor Simulator
**File:** `sensor.py`

The `sensor.py` file simulates temperature readings and publishes the data to AWS IoT Core and DynamoDB.

**Key Features:**

- Simulates temperature data and publishes it to AWS IoT Core using MQTT.
- Saves sensor data to DynamoDB for persistent storage.
- In case of failure, fetches fallback temperature data from the SMHI API.
- Includes retry logic to ensure reliable data transmission.

**Usage:**

```bash
python sensor.py

```

### 2. Data Visualization Dashboard (`dashboard.py`)

The dashboard serves as the frontend interface for users to visualize temperature data collected in the last 24 hours. It:

- Queries DynamoDB for temperature data from the past 24 hours.
- Uses Plotly to create a graph of temperature vs. time.
- Displays the graph in a clean, responsive web interface using Flask.

**Usage:**

To start the Flask application and view the dashboard:

```bash
python dashboarda.py

```
### AWS Resource Setup (`amazonDB.py`)

The `amazonDB.py` file automates the creation of a DynamoDB table to store the sensor data.

**Key Features:**

- Creates a table with `deviceId` as the partition key and `timestamp` as the sort key.
- Configures ProvisionedThroughput for reads and writes.

**Usage:**

To set up your DynamoDB table:

```bash
python amazonDB.py
```

### Example Workflow

**1. Create AWS Resources:**

Run `amazonDB.py` to set up the necessary AWS infrastructure:

```bash
python amazonDB.py
```

### 2. Run the Temperature Sensor Simulator:

Execute `sensor.py` to simulate the temperature sensor and publish data to AWS IoT:

```bash
python sensor.py
```
### File Overview:

**amazonDB.py**
- Purpose: Sets up DynamoDB resources to store temperature sensor data.
- Key Functions:
 - Creates a DynamoDB table with deviceId as the partition key and timestamp as the sort key.
 - Configures provisioned throughput for efficient read and write operations.

**dashboard.py**
- Purpose: A Flask web application to visualize the temperature data.
- Key Features:
  - Queries temperature data from DynamoDB for the last 24 hours.
  - Displays the data using Plotly for easy-to-read visualizations.

**sensor.py**
- Purpose: Simulates temperature sensor data and sends it to AWS IoT Core and DynamoDB.
- Key Functions:
   - Simulates temperature readings.
   - Publishes data to AWS IoT Core using MQTT.
   - Fetches fallback data from the SMHI API when necessary.



## Technologies Used
Backend: Python, Flask
IoT: AWS IoT Core (MQTT)
Cloud Storage: Amazon DynamoDB
Data Visualization: Plotly, Bootstrap
External API: SMHI Open Weather API



## Contributing
We welcome contributions to improve the project. If you would like to contribute, please fork the repository, create a feature branch, and submit a pull request.




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

