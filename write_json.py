import json
from os import path


def write_json(filename, data):
    try:
        # Check if file exists, else create file with empty list
        if not path.isfile(filename):
            with open(filename, 'w') as json_file:
                json.dump([], json_file)

        # Read JSON file
        with open(filename) as fp:
            listObj = json.load(fp)

        # Append data to list
        listObj.append(data)

        # Write updated list back to file
        with open(filename, 'w') as json_file:
            json.dump(listObj, json_file, indent=4, separators=(',', ': '))

        return True
    except Exception as error:
        print(error)
        return False
