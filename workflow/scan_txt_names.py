import pathlib
from datetime import datetime
from os import path
from user_input import PathInput
from functions.utils import extract_date

path_to_look_at = PathInput()
print("\nChecking the dates from your data in: ", path_to_look_at)
if not path.isdir(path_to_look_at) :
    print("This path does not exists :", path_to_look_at)


path_tree = pathlib.Path(path_to_look_at)
data_txt_list = path_tree.rglob("*.txt")
data_txt_string = [str(file_path) for file_path in data_txt_list]

date_strings = list()
for i in data_txt_string:
    date_t = extract_date(i)
    date_strings.append(date_t)
# Convert strings to datetime objects
date_objects = [datetime.strptime(date_str, "%Y%m%d") for date_str in date_strings]

# Find the minimum and maximum dates
min_date = min(date_objects)
max_date = max(date_objects)

# Convert back to string format
min_date_str = min_date.strftime("%Y-%m-%d")
max_date_str = max_date.strftime("%Y-%m-%d")

# Print the range
print(f"\nYou have data that goes from: {min_date_str} to: {max_date_str}")
