import sys
sys.path.append('/remote/complex/home/fpetit/UVP6_time_merge')
from time_merge.functions import extract_data_dates
from time_merge.functions import vig_select
from time_merge.functions import vig_move
import pathlib


path_tree = pathlib.Path("Data_test/Data")
data_txt_list = path_tree.rglob("*.txt")
data_txt_string = [str(file_path) for file_path in data_txt_list]

mydates = extract_data_dates("Data_test/Data/20210711-120000/20210711-120000_data.txt")
test = vig_select(mydates, 'Data_test/Data')
testest = vig_move("/home/fpetit/complex/UVP6_time_merge/Data_test/Data_a/20210710-120000merged/20210710-120000merged_data.txt", "Data_test/Data")
print(testest)
