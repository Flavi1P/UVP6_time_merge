import pathlib
from datetime import datetime
from os import path
import os
from usr_input import PathInput
from functions import extract_date
from functions import append_files
from usr_input import StartInput
from usr_input import StepInput
from functions import split_data
from usr_input import PathOutput
from functions import write_splitted_data

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

#Create one file
my_data = append_files(data_txt_string)

#with open("Data_test/output_test.txt", 'w') as output_file:
#    # Write the content of the variable to the file
#    output_file.write(my_data)

#Ask when the user wants to start 
start_input = StartInput()
#Ask for the time step
step_input = StepInput()

#Split the long data
splitted_data = split_data(my_data, step_input, start_input)

num_time_steps = len(splitted_data)

print(f"Total Number of Time Steps: {num_time_steps}")

#Decide the output folder 
output_folder = PathOutput()

#Save all data txt in the folder
write_splitted_data(splitted_data, output_folder, step_input, start_input)