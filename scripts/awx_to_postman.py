import json

SKIP = [
  "/api/v2/analy",
  "/api/v2/bulk/",
  "/api/v2/confi",
  "/api/v2/servi",
  "/api/v2/ad_ho",
]

FOLDER = "unk"
FOLDER_IDX = -1
SUBFOLDER = "unk"
SUBFOLDER_IDX = -1

def get_req_object(name, path_parts, method) -> dict:
  path_parts = [parts[1]]
  path_parts.extend(['controller'])
  path_parts.extend(parts[2:])
  return {
    "name": name,
    "request": {
      "method": method,
      "url": {
        "protocol": "https",
        "host": ["{{instance_fqdn}}"],
        "path": path_parts
      }
    }
  }

collection_base = {}
with open('data/aap_postman_base.json', 'r') as base:
  collection_base = json.load(base)

awx_schema = {}
with open('data/awx_project_schema.json') as schema:
  awx_schema = json.load(schema)

paths = filter(lambda p: p.startswith('/api/v2'), awx_schema['paths'])
for path in paths:
  parts = path.split('/')
  if len(parts) <= 4:
    continue
  if path[:13] in SKIP:
    continue

  # Top-level Folder
  if len(parts) == 5:
    SUBFOLDER_IDX = -1
    FOLDER = parts[3]
    collection_base['item'].append({
      "name": FOLDER, 
      "item": []
    })
    FOLDER_IDX += 1

    # Create Top-level Requests
    path_meta = awx_schema['paths'][path]
    path_name = " ".join(parts[3:-1])
    for k in path_meta.keys():
      if k != 'parameters':
        _request = get_req_object(path_name, parts, k)
        collection_base['item'][FOLDER_IDX]['item'].append(_request)

  # Child by Id
  if len(parts) == 6:
    path_meta = awx_schema['paths'][path]
    path_name = " ".join(parts[3:-1])
    for k in path_meta.keys():
      if k != 'parameters':
        _request = get_req_object(path_name, parts, k)
        collection_base['item'][FOLDER_IDX]['item'].append(_request)

  # Sub folder
  if len(parts) == 7:
    SUBFOLDER = parts[5]
    collection_base['item'][FOLDER_IDX].setdefault('item', [])
    collection_base['item'][FOLDER_IDX]['item'].append({
      "name": SUBFOLDER, 
      "item": []
    })
    SUBFOLDER_IDX = len(collection_base['item'][FOLDER_IDX]['item']) - 1

    path_meta = awx_schema['paths'][path]
    path_name = " ".join(parts[5:-1])
    for k in path_meta.keys():
      if k != 'parameters':
        _request = get_req_object(path_name, parts, k)
        collection_base['item'][FOLDER_IDX]['item'][SUBFOLDER_IDX]['item'].append(_request)

  # Sub folder child by id
  if len(parts) == 8:
    print("Subfolder child")

with open('data/awx_postman_collection.json', 'w+') as postman_collection:
  json.dump(collection_base, postman_collection)