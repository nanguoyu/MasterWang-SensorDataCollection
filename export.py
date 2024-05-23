from pymongo import MongoClient
import pandas as pd
import os

def export_label_data(mongo_uri, db_name, collection_name, path="data/"):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # 找到所有唯一的label
    labels = collection.distinct("label")

    for label in labels:
        # 对于每个label，聚合查询以获取按时间排序的数据
        pipeline = [
            {"$match": {"label": label}},
            {"$unwind": "$data"},
            {"$replaceRoot": {"newRoot": "$data"}},
            {"$sort": {"timestamp": 1}}  # 确保数据按时间顺序排序
        ]
        cursor = collection.aggregate(pipeline)

        # 将查询结果转换成DataFrame
        df = pd.DataFrame(list(cursor))

        # 指定列的顺序
        column_order = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'timestamp']

        # 如果DataFrame不为空，且包含所需的列，重新排序列并写入CSV文件
        if not df.empty and all(col in df.columns for col in column_order):
            df = df[column_order]  # 重新排序列
            os.makedirs(path, exist_ok=True)
            output_file = f"{path}{label.replace(' ', '_')}.csv"  # 将空格替换为下划线以避免文件名问题
            df.to_csv(output_file, index=False)
            print(f"Data for label '{label}' exported successfully to {output_file}")
        else:
            print(f"No data or missing columns for label '{label}'.")

mongo_uri = "mongodb://localhost:27017/"
db_name = "sensor_data_db"
collection_name = "sensor_data"

export_label_data(mongo_uri, db_name, collection_name)
