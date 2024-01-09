#!/bin/bash
app="ptc.ai.assistant"
docker build -t ${app} .
docker run -d -p 56733:56733 \
  --name=${app} \
  --env ASTRA_DB_APPLICATION_TOKEN \
  --env OPENAI_API_KEY \
  --env ASTRA_DB_KEYSPACE \
  --env ASTRA_DB_TABLE \
  --env ASTRA_DB_ID \
  -v $PWD:/app ${app}