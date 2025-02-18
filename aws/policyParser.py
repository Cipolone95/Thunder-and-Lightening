import json
import sys

def parse_iam_policy(policy_path):
    try:
        with open(policy_path, "r") as file:
            policy = json.load(file)

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
                    print(f"Permission {action} exists over resource {resource}.")
    except Exception as e:
        print(f"Error reading policy file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <policy.json>")
        sys.exit(1)
    
    policy_file = sys.argv[1]
    parse_iam_policy(policy_file)
