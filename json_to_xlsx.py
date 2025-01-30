import pandas as pd
import json
import os

# Path to the JSON file (update the file name accordingly)
file_path = "./data.json"

# Load the JSON file
with open(file_path, 'r', encoding='utf-8') as file:
    repos = json.load(file)

# Convert the JSON data into a pandas DataFrame
df = pd.DataFrame(repos)

# Extract the file name (without extension) and add "_json_to_xls"
file_name, file_extension = os.path.splitext(file_path)
excel_file_name = f"{file_name}_json_to_xls.xlsx"

# Save the DataFrame to an Excel file
df.to_excel(excel_file_name, index=False)

# Print a confirmation message
print(f"Data has been written to {excel_file_name}")

# ex-json data sample.
'''
[
  {
    "number": 1,
    "title": "ProjectA",
    "address": "https://github.com/user/ProjectA",
    "description": "Sample project for training and practice.",
    "created_at": "2020-09-03",
    "updated_at": "2023-12-31",
    "language": "Java",
    "languages_url": "https://api.github.com/repos/user/ProjectA/languages",
    "visibility": "public"
  },
  {
    "number": 2,
    "title": "ProjectB",
    "address": "https://github.com/user/ProjectB",
    "description": "Class project, now moved to a new repository.",
    "created_at": "2020-10-12",
    "updated_at": "2023-12-31",
    "language": "Python",
    "languages_url": "https://api.github.com/repos/user/ProjectB/languages",
    "visibility": "private"
  },
  {
    "number": 3,
    "title": "ProjectC",
    "address": "https://github.com/user/ProjectC",
    "description": "Team project for library management system.",
    "created_at": "2020-10-14",
    "updated_at": "2021-04-13",
    "language": "JavaScript",
    "languages_url": "https://api.github.com/repos/user/ProjectC/languages",
    "visibility": "public"
  }
]
'''
