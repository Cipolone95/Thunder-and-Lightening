#!/usr/bin/python3

import json
import argparse
import sys

def search_keywords(data, keywords):
    try:
        policy = data

        statements = policy.get("Statement", [])
        for statement in statements:
            actions = statement.get("Action", [])
            resources = statement.get("Resource", [])
            
            # Ensure actions and resources are lists
            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resources, str):
                resources = [resources]
            
            for action in actions:
                for resource in resources:
                    if action in keywords:
                        print(f"Permission {action} exists over resource {resource}.")

        print("\n")
    except Exception as e:
        print(f"Error reading policy file: {e}")


def load_keywords(file_path):
    try:
        with open(file_path, "r") as file:
            keywords = [line.strip() for line in file if line.strip()]  # Read and strip whitespace
        return keywords # Store in a list
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for keywords in a JSON file.")
    parser.add_argument("--file", help="Path to the JSON file")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, 'r') as file:
            data = json.load(file)
        print(f"Enumerating file {args.file} for interesting permissions...\n")
    else:
        data = json.load(sys.stdin)
    
    keywords = load_keywords("../resources/privescKeywords.txt")# Replace with your keywords
    search_keywords(data, keywords)
