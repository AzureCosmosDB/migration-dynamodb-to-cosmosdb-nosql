import random
from faker import Faker
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize Faker
fake = Faker()

# AWS credentials and region
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION = "us-east-1"

# Initialize DynamoDB client with credentials
try:
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    # Specify the table name
    table_name = 'customers'
    table = dynamodb.Table(table_name)
except NoCredentialsError:
    print("AWS credentials not found. Please configure them.")
    exit()
except PartialCredentialsError:
    print("Incomplete AWS credentials provided.")
    exit()
except Exception as e:
    print(f"Error initializing DynamoDB: {e}")
    exit()

# Function to generate a random 20-digit customer_id number
def generate_customer():
    id = ''.join(random.choices('0123456789', k=20))
    if not id:
        raise ValueError("Generated ID is empty.")
    return id

# Function to generate sample data
def generate_sample_data(num_records):
    data = []
    for _ in range(num_records):
        name = fake.name()
        customer_id = generate_customer()
        email = fake.email()
        address = fake.address().replace('\n', ', ')
        phone = fake.phone_number()
        data.append({
            'customer_id': customer_id,  # Correct key name to match table schema
            'Name': name,
            'Email': email,
            'Address': address,
            'Phone': phone
        })
    return data

# Function to insert data into DynamoDB
def insert_data_to_dynamodb(data):
    for record in data:
        try:
            # Insert the record into DynamoDB
            table.put_item(Item=record)
            print(f"Inserted: {record['customer_id']}")  # Correct key name for output
        except Exception as e:
            print(f"Error inserting record {record['customer_id']}: {e}")

# Main function
def main():
    num_records = 500  # Number of records to generate
    sample_data = generate_sample_data(num_records)
    insert_data_to_dynamodb(sample_data)

if __name__ == '__main__':
    main()
