from pymongo import MongoClient
import pandas as pd
import os

def export_label_data(mongo_uri, db_name, collection_name, path="data/"):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    labels = collection.distinct("label")

    for label in labels:
        pipeline = [
            {"$match": {"label": label}},
            {"$unwind": "$data"},
            {"$replaceRoot": {"newRoot": "$data"}},
            {"$sort": {"timestamp": 1}}  
        ]
        cursor = collection.aggregate(pipeline)

        df = pd.DataFrame(list(cursor))

        column_order = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'timestamp']

        if not df.empty and all(col in df.columns for col in column_order):
            df = df[column_order] 
            os.makedirs(path, exist_ok=True)
            output_file = f"{path}{label.replace(' ', '_')}.csv"  
            df.to_csv(output_file, index=False)
            print(f"Data for label '{label}' exported successfully to {output_file}")
        else:
            print(f"No data or missing columns for label '{label}'.")

mongo_uri = "mongodb://localhost:27017/"
db_name = "sensor_data_db"
collection_name = "sensor_data"

export_label_data(mongo_uri, db_name, collection_name)
