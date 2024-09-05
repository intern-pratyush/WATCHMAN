import yaml
from input_data import list_of_inputs  # Import the input data from input_data.py
import argparse

def update_nested_dict(d, keys, value):
    """
    Recursively updates the value of a nested dictionary key.
    """
    if isinstance(d, dict) and keys:
        key = keys[0]
        if len(keys) == 1 and key in d:
            print(f"Modifying {key}")
            d[key] = value
            return True
        elif key in d:
            return update_nested_dict(d[key], keys[1:], value)
    return False

def modify_yaml_document(yaml_content, key, new_value):
    """
    Modifies the specified key in the YAML document.
    """
    keys = tuple(key.split("."))  # Split the key path into individual keys
    for doc in yaml_content:
        if isinstance(doc, dict):
            if not update_nested_dict(doc, keys, new_value):
                print(f"Path {keys} not found in the document.")
    return yaml_content

def modify_yaml_file(file_path, key, new_value):
    """
    Modifies the YAML file at the given path by updating the specified key's value.
    """
    with open(file_path, 'r') as file:
        yaml_content = list(yaml.safe_load_all(file))  # Load all YAML documents
    yaml_content = modify_yaml_document(yaml_content, key, new_value)
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        yaml.dump_all(yaml_content, file, default_flow_style=False)

def main(scale_type):
    # Iterate through the list_of_inputs and apply the changes
    for input_item in list_of_inputs:
        file_path = input_item["filepath"]
        key = input_item["key"]

        # Select the appropriate replica count based on the scale_type
        new_value = input_item[f"{scale_type}_replicas_count"]

        print(f"Processing file: {file_path} with key: {key} and new value: {new_value}")
        modify_yaml_file(file_path, key, new_value)

    print("Modification complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify YAML files with scale-up or scale-down values.")
    parser.add_argument("--scale-type", choices=["scale_up", "scale_down"], required=True,
                        help="Specify whether to scale up or scale down replicas.")

    args = parser.parse_args()

    # Call the main function with the selected scale type (either 'scale_up' or 'scale_down')
    main(args.scale_type)
