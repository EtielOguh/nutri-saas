#!/bin/bash

# Test client creation with Bearer token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1MjM1MzEwfQ.LGbqQK_xxa_YFj13e0aWqOpbu12PMa04axhKzJF8N74"

curl -X POST "http://localhost:8000/nutricionistas/1/clientes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Client",
    "age": 30,
    "height": 1.75,
    "objective": "Weight loss",
    "nutricionista_id": 1
  }'
