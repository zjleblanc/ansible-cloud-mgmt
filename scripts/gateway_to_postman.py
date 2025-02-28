import json
from common.postman import AUTH_BASE, VAR_BASE

def process_items(items: list):
  for item in items:
    if item.get('request', None):
      item['request'].pop('auth', None)
    if item.get('response', None):
      idx = 1
      for resp in item['response']:
        resp['name'] = f'Example Response {idx}'
        idx += 1
    if item.get('item', None):
      process_items(item['item'])

gateway_raw = {}
with open("data/gateway_raw_postman_collection.json", 'r') as _in:
  gateway_raw = json.load(_in)

base_item = gateway_raw['item'][0]['item'][0]['item'][0]['item']
process_items(base_item)

collection = {
  "info": {
		"name": "AAP 2.5 - Gateway API",
		"description": "AAP 2.5 - Gateway API",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
  "item": base_item,
  "auth": AUTH_BASE,
  "variable": VAR_BASE
}
with open('data/gateway_postman_collection.json', 'w+') as postman_collection:
  json.dump(collection, postman_collection)