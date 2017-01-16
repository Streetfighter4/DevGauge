#!/bin/bash

ELASTICSEARCH='devmeter'

[ ! -f ./shakespeare.json ] &&  wget https://download.elastic.co/demos/kibana/gettingstarted/shakespeare.json
[ ! -f ./accounts.json ] &&  wget https://download.elastic.co/demos/kibana/gettingstarted/accounts.zip && unzip accounts.zip
[ ! -f ./logs.jsonl ] &&  wget https://download.elastic.co/demos/kibana/gettingstarted/logs.jsonl.gz && gunzip logs.jsonl.gz


curl -XPUT "http://$ELASTICSEARCH:9200/shakespeare" -d '
{
 "mappings" : {
  "_default_" : {
   "properties" : {
    "speaker" : {"type": "string", "index" : "not_analyzed" },
    "play_name" : {"type": "string", "index" : "not_analyzed" },
    "line_id" : { "type" : "integer" },
    "speech_number" : { "type" : "integer" }
   }
  }
 }
}
';

curl -XPUT "http://$ELASTICSEARCH:9200/logstash-2015.05.18" -d '
{
  "mappings": {
    "log": {
      "properties": {
        "geo": {
          "properties": {
            "coordinates": {
              "type": "geo_point"
            }
          }
        }
      }
    }
  }
}
';

curl -XPUT "http://$ELASTICSEARCH:9200/logstash-2015.05.19" -d '
{
  "mappings": {
    "log": {
      "properties": {
        "geo": {
          "properties": {
            "coordinates": {
              "type": "geo_point"
            }
          }
        }
      }
    }
  }
}
';

curl -XPUT "http://$ELASTICSEARCH:9200/logstash-2015.05.20" -d '
{
  "mappings": {
    "log": {
      "properties": {
        "geo": {
          "properties": {
            "coordinates": {
              "type": "geo_point"
            }
          }
        }
      }
    }
  }
}
';

curl -XPOST "http://$ELASTICSEARCH:9200/bank/account/_bulk?pretty" --data-binary @accounts.json
curl -XPOST "http://$ELASTICSEARCH:9200/shakespeare/_bulk?pretty" --data-binary @shakespeare.json
curl -XPOST "http://$ELASTICSEARCH:9200/_bulk?pretty" --data-binary @logs.jsonl

curl "http://$ELASTICSEARCH:9200/_cat/indices?v"

echo 'Now go to https://www.elastic.co/guide/en/kibana/current/getting-started.html'
