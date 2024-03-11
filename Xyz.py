import csv
import json

def csv_to_dynamodb_json(input_csv_file, output_json_file):
    # Open the CSV file and read data
    with open(input_csv_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        items = []

        for row in reader:
            item = {}
            for key, value in row.items():
                # Determine data type for DynamoDB (S for String, N for Number)
                # You might need to extend this logic for other data types like B (Binary), BOOL (Boolean), etc.
                if value.isdigit():  # Simple check to decide between 'S' and 'N'
                    dynamo_type = 'N'
                else:
                    dynamo_type = 'S'
                
                # Adjust the following line if your data requires more complex processing
                item[key] = {dynamo_type: value}
            
            items.append(item)

    # Write the JSON output
    with open(output_json_file, 'w') as json_file:
        json.dump(items, json_file, indent=2)

    print(f"Data has been converted and saved to {output_json_file}")

# Example usage:
csv_to_dynamodb_json("path/to/your/input.csv", "path/to/your/output.json")
