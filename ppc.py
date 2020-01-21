#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests

response = requests.post(
    "http://127.0.0.1:5000/vulnerability"
)

print(response.json())