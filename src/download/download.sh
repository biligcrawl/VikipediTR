#!/bin/bash

BUCKET_NAME="biligcrawlopenturkishdata"

PREFIX="WikipediaTR"

LOCAL_DIR="data"

aws s3 sync s3://$BUCKET_NAME/$PREFIX $LOCAL_DIR --no-sign-request
