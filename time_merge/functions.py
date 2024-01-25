import re
import os 
import pandas as pd
from io import StringIO
import shutil

def extract_date(text):
    """Extract a date from the data string of the UVP6 data.txt.

    Args:
        text (string): A line of data from data.txt

    Returns:
        string: Return a string in the format YYYYmmdd
    """    
    matches = re.findall("[0-9]{8}-[0-9]{6}", text)
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

def read_acq(uvp6_files):
    """Read the acquisition parameters in a list of uvp6 data files and returns a dataframe with all the parameters as different columns and the date of each configurations.

    Args:
        uvp6_files (string): The path of one or several UVP data files
    Returns:
        A pandas dataframe.
    """    
    acq_header = ["rame", "configuration_name", "pt_mode", "acquisition_frequency", "frames_per_bloc", "blocs_per_pt", "pressure_for_auto_start", "pressure_difference_for_auto_stop",
               "result_sending", "save_synthetic_data_for_delayed_request", "limit_lpm_detection_size", "save_images", "vignetting_lower_limit_size", "appendices_ratio",
               "interval_for_measuring_background_noise", "image_nb_for_smoothing", "analog_output_activation", "gain_for_analog_out", "minimum_object_number",
               "maximal_internal_temperature", "operator_email", "0", "sd_card_mem", "datetime"]
    
    acq_df = pd.DataFrame(columns = acq_header)
    acq_list = []
    for input_file_path in uvp6_files:
        # Open the input file for reading
        with open(input_file_path, 'r') as input_file:
        # Read all lines from the input file, skipping the first two rows
            acq = input_file.readlines()[2]
        date = extract_date(input_file_path)
        # Convert the string to a DataFrame
        temp_df = pd.read_csv(StringIO(acq), header=None, names=acq_header)
        temp_df["datetime"] = date
        acq_list.append(temp_df)
    acq_df = pd.concat(acq_list, ignore_index = True)
    return(acq_df)

def check_acq(acq_data):
    non_constant_columns = {}
    for column in acq_data.columns:
        if column not in ["sd_card_mem"]:
            if acq_data[column].nunique() > 1:
                non_constant_columns[column] = acq_data[column].tolist()
    return non_constant_columns

def init_folders(acq_data, path_input):

    #Remove date and memory, because they are not supposed to be constant obviously
    acq_data_unique = acq_data.drop(["datetime", "sd_card_mem"], axis=1)
    # Create a new column 'unique_identifier' by concatenating values from each row
    acq_data_unique['unique_identifier'] = acq_data_unique.apply(lambda row: '_'.join(map(str, row)), axis=1)

    # Get the number of unique rows
    unique_rows = acq_data_unique['unique_identifier'].nunique()

    identifiers = acq_data_unique['unique_identifier'].unique()

    # Create folders
    folder_prefix = path_input + "_"

    # Create a new column 'folder' to store the folder information
    acq_data['folder'] = ''

    for i in range(unique_rows):

        i_identifier = identifiers[i]
        # Filter rows based on the current unique identifier
        subset = acq_data_unique[acq_data_unique['unique_identifier'] == i_identifier]
        
        folder_name = f"{folder_prefix}{chr(ord('a') + i)}"

        # Update the 'folder' column for rows that match the current folder
        acq_data.loc[acq_data.index.isin(subset.index), 'folder'] = folder_name

        # Check if folder already exists, if not, create it
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    # Drop the 'unique_identifier' column as it is no longer needed
    #acq_data = acq_data.drop('unique_identifier', axis=1)

    return acq_data


def closest_project_index(dt):
    return min(range(1, unique_rows + 1), key=lambda i: abs((i-1) * 3600 - dt.timestamp()))

def acq_sort(acq_data_with_folder, path_input):
     for index, row in acq_data_with_folder.iterrows():
        datetime_str = row['datetime']
        closest_folder = row['folder']

        # Files should be in the current working directory and named "YYYYmmdd-HHMMSS_data.txt"
        file_name = f"{datetime_str}_data.txt"
        source_path = os.path.join(path_input, datetime_str, file_name)
        destination_folder = os.path.join(closest_folder, datetime_str)
        destination_path = os.path.join(destination_folder, file_name)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copy(source_path, destination_path)
