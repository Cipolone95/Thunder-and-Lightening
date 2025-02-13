#!/bin/bash

# Check if a bucket name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <S3_BUCKET_NAME>"
  exit 1
fi

# S3 bucket name passed as parameter
BUCKET_NAME=$1

# AWS CLI checks

# 1. Check if the bucket exists
echo "Checking if bucket '$BUCKET_NAME' exists..."
aws s3api head-bucket --bucket "$BUCKET_NAME" &>/dev/null
if [ $? -eq 0 ]; then
  echo "Bucket '$BUCKET_NAME' exists."
else
  echo "Bucket '$BUCKET_NAME' does not exist or is inaccessible."
fi

# 2. List the contents of the bucket (first 5 items)
echo "Listing contents of bucket '$BUCKET_NAME'..."
aws s3 ls "s3://$BUCKET_NAME" --recursive | head -n 5

# 3. Check if versioning is enabled
echo "Checking versioning status of '$BUCKET_NAME'..."
aws s3api get-bucket-versioning --bucket "$BUCKET_NAME" | jq '.Status'

# 4. Check the bucket's region
echo "Checking the region of '$BUCKET_NAME'..."
aws s3api get-bucket-location --bucket "$BUCKET_NAME" | jq '.LocationConstraint'

# 5. Check bucket policy
echo "Checking the bucket policy of '$BUCKET_NAME'..."
aws s3api get-bucket-policy --bucket "$BUCKET_NAME" &>/dev/null
if [ $? -eq 0 ]; then
  echo "Bucket '$BUCKET_NAME' has a policy."
else
  echo "Bucket '$BUCKET_NAME' does not have a policy."
fi

# 6. Check if public access block is enabled
echo "Checking public access block status of '$BUCKET_NAME'..."
aws s3api get-bucket-policy-status --bucket "$BUCKET_NAME" &>/dev/null
if [ $? -eq 0 ]; then
  echo "Public access block is enabled for '$BUCKET_NAME'."
else
  echo "Public access block is not enabled for '$BUCKET_NAME'."
fi

echo "AWS S3 checks completed for bucket '$BUCKET_NAME'."
