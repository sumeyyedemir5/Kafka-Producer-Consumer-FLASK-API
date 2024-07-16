from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('scraped-data',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

with open('scraped_data.json', 'w') as file:
    for message in consumer:
        file.write(json.dumps(message.value) + "\n")
