#!/bin/bash

# Check if a lambda function name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <LAMBDA-FUNCTION-NAME>"
  exit 1
fi

# Lambda name passed as parameter
FUNCTION_NAME=$1

# AWS CLI checks

# 1. Check if the Lambda function exists
echo "Checking if function '$FUNCTION_NAME' exists..."
aws lambda get-function --function-name "$FUNCTION_NAME" &>/dev/null
if [ $? -eq 0 ]; then
  echo "Function '$FUNCTION_NAME' exists."
else
  echo "Function '$FUNCTION_NAME' does not exist or is inaccessible."
fi

# 2. Get the function configuration
echo "Retrieving configuration of function '$FUNCTION_NAME'..."
aws lambda get-function-configuration --function-name "$FUNCTION_NAME"

# 3. List function event invoke configurations
echo "Listing event invoke configurations of function '$FUNCTION_NAME'..."
aws lambda list-function-event-invoke-configs --function-name "$FUNCTION_NAME"

# 4. List function URL configurations
echo "Listing URL configurations of function '$FUNCTION_NAME'..."
aws lambda list-function-url-configs --function-name "$FUNCTION_NAME"

# 5. Get function URL configuration
echo "Retrieving function URL configuration of '$FUNCTION_NAME'..."
aws lambda get-function-url-config --function-name "$FUNCTION_NAME"

# 6. List versions by function
echo "Listing versions of function '$FUNCTION_NAME'..."
aws lambda list-versions-by-function --function-name "$FUNCTION_NAME"

# 7. List function aliases
echo "Listing aliases of function '$FUNCTION_NAME'..."
aws lambda list-aliases --function-name "$FUNCTION_NAME"

echo "AWS Lambda checks completed for function '$FUNCTION_NAME'."
