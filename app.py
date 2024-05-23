from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Use ENV variables get MongoDB connection
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client.sensor_data_db
collection = db.sensor_data  # 使用一个统一的collection存储所有传感器数据

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    
    # 将数据保存到MongoDB
    collection.insert_one(data)
    
    return jsonify({"status": "success"})

@app.route('/stats', methods=['GET'])
def stats():
    pipeline = [
        {"$unwind": "$data"},  # 展开data数组
        {"$group": {"_id": "$label", "count": {"$sum": 1}}}
    ]
    results = collection.aggregate(pipeline)
    stats = {doc['_id']: doc['count'] for doc in results}
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
