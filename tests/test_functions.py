import sys
sys.path.append('/remote/complex/home/fpetit/UVP6_time_merge')
from time_merge.functions import read_acq
import pathlib


path_tree = pathlib.Path("Data_test/Data")
data_txt_list = path_tree.rglob("*.txt")
data_txt_string = [str(file_path) for file_path in data_txt_list]

test = read_acq(data_txt_string)
print(test.head())
