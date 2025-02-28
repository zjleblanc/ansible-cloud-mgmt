AUTH_BASE = {
  "type": "bearer",
  "bearer": [
    {
        "key": "token",
        "value": "{{admin_token}}",
        "type": "string"
    }
  ]
}

VAR_BASE = 	[
  {
    "key": "instance_fqdn",
    "value": "",
    "type": "string"
  },
  {
    "key": "admin_token",
    "value": "",
    "type": "string"
  }
]