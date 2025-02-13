import json
import argparse
import sys

def search_keywords(data, keywords):
    try:
        # Convert JSON to string for easier keyword searching
        json_string = json.dumps(data)
        
        for keyword in keywords:
            if keyword in json_string:
                print(f"{keyword} found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for keywords in a JSON file.")
    parser.add_argument("--file", help="Path to the JSON file")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, 'r') as file:
            data = json.load(file)
    else:
        data = json.load(sys.stdin)
    
    keywords = ["example", "test", "keyword"]  # Replace with your keywords
    search_keywords(data, keywords)
