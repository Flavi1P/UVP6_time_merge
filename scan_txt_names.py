import pathlib
from os import path
from user_input import PathInput

path_to_look_at = PathInput()
#print "\nChecking the dates from your data in: "%(path_to_look_at)  
if not path.isdir(path_to_look_at) :
    print("This path does not exists :", path_to_look_at)


path_tree = pathlib.Path(path_to_look_at)
data_txt_list = list(path_tree.rglob("*.txt"))

print(data_txt_list)