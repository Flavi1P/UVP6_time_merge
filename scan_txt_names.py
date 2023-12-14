import pathlib
from os import path
from user_input import PathInput
from utils import extract_date

path_to_look_at = PathInput()
print("\nChecking the dates from your data in: ", path_to_look_at)
if not path.isdir(path_to_look_at) :
    print("This path does not exists :", path_to_look_at)


path_tree = pathlib.Path(path_to_look_at)
data_txt_list = path_tree.rglob("*.txt")
data_txt_string = [str(file_path) for file_path in data_txt_list]


for i in data_txt_string:
    date_t = extract_date(i)
    print(date_t)