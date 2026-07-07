#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

RANDOM_NUMBER=$RANDOM
NAME="test user $RANDOM_NUMBER"
EMAIL="test-$RANDOM_NUMBER@example.com"
CONTENT="test post from curl $RANDOM_NUMBER"

echo "creating a timeline post..."
echo "name: $NAME"
echo "email: $EMAIL"
echo "content: $CONTENT"

POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/timeline_post" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "POST response:"
echo "$POST_RESPONSE"

POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo "checking that the post appears in GET /api/timeline_post..."
GET_RESPONSE=$(curl -s "$BASE_URL/api/timeline_post")

echo "GET response:"
echo "$GET_RESPONSE"

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "success: timeline post was found!"
else
  echo "error: timeline post was not found."
  exit 1
fi

echo "deleting test timeline post..."
curl -s -X DELETE "$BASE_URL/api/timeline_post/$POST_ID"
echo ""

echo "done."
