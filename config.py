
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# URL encode the username and password
username = quote_plus("jazxii")
password = quote_plus("Jazxii@mongo")

uri = f"mongodb+srv://{username}:{password}@a11ytest.8gkexxj.mongodb.net/?retryWrites=true&w=majority&appName=a11ytest"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db

collection = db["todo_data"]