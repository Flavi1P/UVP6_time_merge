import re

def TimeStepInput():      
    time_step = input("Enter the value of your time step (in days): ")     
    return time_step
  
def PathInput():
    path_input = input("Enter the path of the folder where the data.txt to merged are stored: ")
    return path_input

def extract_date(text):
    matches = re.findall("[0-9]{8}", text)
    if matches:
        return matches[-1]
    else:
        return None
