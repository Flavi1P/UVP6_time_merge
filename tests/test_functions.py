import sys
sys.path.append('/remote/complex/home/fpetit/UVP6_time_merge')
from time_merge.functions import read_acq
from time_merge.functions import check_acq
import pathlib


path_tree = pathlib.Path("Data_test/Data")
data_txt_list = path_tree.rglob("*.txt")
data_txt_string = [str(file_path) for file_path in data_txt_list]

test = read_acq(data_txt_string)

result = check_acq(test)
if result:
    print("Non-constant columns:")
    for column, values in result.items():
        print(f"{column}: {values}")
else:
    print("All columns have constant values.")