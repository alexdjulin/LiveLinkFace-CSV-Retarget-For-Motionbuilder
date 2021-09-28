import os
import re

ue_path = "t3d/mh_arkit_mapping_pose.T3D"

def prinlist(lst):
	print('\n'.join(lst))
def prinlen(lst):
	print(len(lst))
def printype(obj):
	print(type(obj))

# read and store full file contents
with open(ue_path, 'r') as f:
	ue_contents = f.read()

# retrieve arkit poses in an array >> 53 bs
pattern = r'DisplayName="([\w_]+)"'
arkit_bs = [data for data in re.findall(pattern, ue_contents) if not 'CTRL_' in data and not 'head_' in data]

# retrieve mh poses in an array >> 323 targets
pattern = r'DisplayName="[\w_]+"'
mh_bs = [bs.split('=')[-1][1:-1] for bs in re.findall(pattern, ue_contents) if 'CTRL_' in bs or 'head_' in bs]

# retrieve bs values as an aray of arrays (for each arkit bs => all mh bs mapping values)
pattern = r',CurveData=\((([-+]?[0-9]\.[0-9]+,?)*)\)'
curve_data = [data[0] for data in re.findall(pattern, ue_contents)]
last = curve_data[-1].split(',')
target_map = dict(zip(mh_bs, last))
prinlist(mh_bs)

		




# mh_mapping = list()
# for data in curve_data:
# 	mh_mapping.append(data.split(','))

# printlen(curve_data)
# printlist([v for v in mh_mapping[-2] if float(v)])






	
# # for val in mh_values:
# 	print(50*'#')
# 	print(val)