import re
import os 

def TimeStepInput():
    """Prompt the user to choose a time step, in hours, to split the data. 

    Returns:
        integer : returns the Time step from chosen by the user.
    """    """"""      
    time_step = input("Enter the value of your time step (in hours): ")     
    return time_step
  
def PathInput():
    """Prompt the user to give the path of the UVP6 project where all the data.txt to merge/split can be found.

    Returns:
        string : A string of the absolute path given by the user
    """    
    path_input = input("Enter the path of the folder where the data.txt to merged are stored: ")
    return path_input

def StartInput():
    """Prompt the user to give the date time of when the split/merge should start.

    Returns:
        string : A string in the format %Y%m%d-%H%M%S
    """    
    start_input = input("At which day time do you want to start the split ? ('%Y%m%d-%H%M%S' format) ")
    return start_input

def StepInput():
    """Prompt the user to choose a time step, in hours, to split the data. 

    Returns:
        integer : returns the Time step from chosen by the user.
    """    
    step_input = input("What's the time step of the split ? (in hours) ")
    return step_input

def PathOutput():
    """Prompt the user to choose a path to save the results.

    Returns:
        strings : An absolute path where all the files will be saved in a UVP6 project structure.
    """    
    output_folder = input("Where do you want to store the output data ? ")
    return output_folder

def extract_date(text):
    """Extract a date from the data string of the UVP6 data.txt.

    Args:
        text (string): A line of data from data.txt

    Returns:
        string: Return a string in the format YYYYmmdd
    """    
    matches = re.findall("[0-9]{8}", text)
    if matches:
        return matches[-1]
    else:
        return None

def append_files(data_paths):
    """Create one txt data from all the data.txt files of the UVP6 project.

    Args:
        data_paths (list): A list of data paths that point data.txt files.
    
    Returns: A dictionnary with a list of strings per time step.
    """    
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
    """Split the large data txt (output from append_files function) from the start date time and using the time step provided. 

    Args:
        data (dictionnary): A large text file with all the data lines of  the UVP6 project (output from append_files())
        time_step (int): The time step from the user (output from StepInput())
        start_datetime (string): The start date time from the user (output from SartInput())
    Returns: 
        Dictionnary : A dictionnary with a list of string per time step (output from append_files())
    """    
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
    """Write the data.txt files in the output folder

    Args:
        splitted_data (dictionnary): A dictionnary with all the different data (output from split_data())
        output_folder (string): The output folder
        time_step (integer): The time step
        start_datetime (string): The datetime of the beginning of the split
    """    
        # Write each time step's data to a separate text file
    step_float = float(time_step)
    start_datetime = datetime.strptime(start_datetime, '%Y%m%d-%H%M%S')
    for time_step_index, data_list in splitted_data.items():
        # Get the datetime of the first data in the time step
        time_step_datetime = start_datetime + timedelta(hours=time_step_index * step_float)
        
        # Format the datetime as a string for the file name
        file_name = os.path.join(output_folder, time_step_datetime.strftime('%Y%m%d-%H%M%S') + "merged_data.txt")
        with open(file_name, 'w') as file:
            for value in data_list:
                file.write(f'{value}\n')