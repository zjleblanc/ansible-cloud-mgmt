import json
from common.postman import AUTH_BASE, VAR_BASE

EDA_BASE_PATH = ['api','eda','v1']

def process_items(items: list):
  for item in items:
    if item.get('request', None):
      item['request'].pop('auth', None)
      item['request']['url'].pop('raw', None)
      path = EDA_BASE_PATH + item['request']['url']['path']
      item['request']['url']['path'] = path
    if item.get('response', None):
      idx = 1
      for resp in item['response']:
        resp['name'] = f'Example Response {idx}'
        idx += 1
    if item.get('item', None):
      process_items(item['item'])

eda_raw = {}
with open("data/eda_raw_postman_collection.json", 'r') as _in:
  eda_raw = json.load(_in)

base_item = eda_raw['item']
process_items(base_item)

collection = {
  "info": {
		"name": "AAP 2.5 - EDA API",
		"description": "AAP 2.5 - EDA API",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
  "item": base_item,
  "auth": AUTH_BASE,
  "variable": VAR_BASE
}
with open('data/eda_postman_collection.json', 'w+') as postman_collection:
  json.dump(collection, postman_collection)