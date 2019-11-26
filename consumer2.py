from kafka import KafkaConsumer
import json

kafka = '100.123.35.0:9092'
topic = "juniper" 

# auto_offset_reset can be set to 'latest' or 'earliest'
consumer2 = KafkaConsumer(topic, bootstrap_servers=kafka, security_protocol="PLAINTEXT", auto_offset_reset='latest')

# Return True if the client is connected to the kafka server 
# consumer2.bootstrap_connected()

# Get all topics the user is authorized to view. 
# consumer2.topics()

for message in consumer2:
  if (message.topic == "juniper"): 
    message_json = json.loads(message.value)
    if (message_json["name"] == "/network-instances/network-instance/protocols/protocol/bgp/"):
      device = message_json["tags"]["device"]
      device_timestamp = message_json["timestamp"]
      openconfig_data = message_json["fields"]
      print ("######## new message #########")
      print ("topic=%s offset=%d device=%s timestamp=%s" % (message.topic, message.offset, device, device_timestamp))
      print ("openconfig_data=%s" % (openconfig_data))

# consumer2.close()
