import re
import os 

def TimeStepInput():      
    time_step = input("Enter the value of your time step (in days): ")     
    return time_step
  
def PathInput():
    path_input = input("Enter the path of the folder where the data.txt to merged are stored: ")
    return path_input

def StartInput():
    start_input = input("At which day time do you want to start the split ? ('%Y%m%d-%H%M%S' format) ")
    return start_input

def StepInput():
    step_input = input("What's the time step of the split ? (in hours) ")
    return step_input

def PathOutput():
    output_folder = input("Where do you want to store the output data ? ")
    return output_folder

def extract_date(text):
    matches = re.findall("[0-9]{8}", text)
    if matches:
        return matches[-1]
    else:
        return None

def append_files(data_paths):
    my_long_data = ""
    for input_file_path in data_paths:
        # Open the input file for reading
        with open(input_file_path, 'r') as input_file:
        # Read all lines from the input file, skipping the first two rows
            lines = input_file.readlines()[4:]
    
        # Concatenate the lines to the existing data
        my_long_data += ''.join(lines)
    return(my_long_data)

from datetime import datetime, timedelta

def split_data(data, time_step, start_datetime):
    # Initialize a dictionary to store data for each time step
    time_steps_data = {}
    start_datetime = datetime.strptime(start_datetime, '%Y%m%d-%H%M%S')
    lines = data.split('\n')
    for line in lines:
        if line:
            # Extract the date and time from the line
            date_time_str, data_str = line.split(',', 1)
            date_time = datetime.strptime(date_time_str, '%Y%m%d-%H%M%S')

            # Calculate the difference in hours from the start_datetime
            time_difference = (date_time - start_datetime).total_seconds() / 3600

            step_float = float(time_step)

            # Determine the time step index
            time_step_index = int(time_difference / step_float)

            # Append the data to the corresponding time step in the dictionary
            if time_step_index not in time_steps_data:
                time_steps_data[time_step_index] = []
            time_steps_data[time_step_index].append(line)
    return(time_steps_data)
        
def write_splitted_data(splitted_data, output_folder, time_step, start_datetime):
        # Write each time step's data to a separate text file
    step_float = float(time_step)
    start_datetime = datetime.strptime(start_datetime, '%Y%m%d-%H%M%S')
    for time_step_index, data_list in splitted_data.items():
        # Get the datetime of the first data in the time step
        time_step_datetime = start_datetime + timedelta(hours=time_step_index * step_float)
        
        # Format the datetime as a string for the file name
        file_name = os.path.join(output_folder, time_step_datetime.strftime('%Y%m%d-%H%M%S') + "_data.txt")
        with open(file_name, 'w') as file:
            for value in data_list:
                file.write(f'{value}\n')