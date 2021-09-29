# https://re-thought.com/how-to-suppress-scientific-notation-in-pandas/
# https://stackoverflow.com/questions/28218698/how-to-iterate-over-columns-of-pandas-dataframe-to-run-regression
# https://knowledge.autodesk.com/support/motionbuilder/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/MotionBuilder/files/GUID-46E090C5-34AD-4E26-872F-F7D21DC57C74-htm.html
# https://help.autodesk.com/view/MOBPRO/2018/ENU/?guid=__py_ref__tasks_2_time_code_keying_8py_example_html
# https://developer.apple.com/documentation/arkit/arfaceanchor/blendshapelocation

from pyfbsdk import *
from pyfbsdk_additions import *
import os
import re
import pandas as pd
import time

# debug functions
def prinlist(lst):
    print('\n'.join(lst))
def prinlen(lst):
    print(len(lst))
def printype(obj):
    print(type(obj))


class BlendShape:

    def __init__(self, name, target_map):
        self.name = name  # arkit bs name / string
        self.target_map = target_map  # mh bs mapping / dict {mh_bs_name: value}
        self.keys_dic = None  # animation values / dict {timecode: value}

    def __repr__(self):
        to_print = "BS Name:\n{}\n\n".format(self.name)
        to_print += "Mapping:\n"
        for key, value in self.target_map.items():
            to_print += "{} = {}\n".format(key, value)
        if self.keys_dic:
            to_print += "\nAnim Keys:\n"
            to_print += "{} >> {}\n".format(format_timecode(list(self.keys_dic.keys())[0]), list(self.keys_dic.values())[0])
            to_print += ".........\n"
            to_print += "{} >> {}\n".format(format_timecode(list(self.keys_dic.keys())[-1]), list(self.keys_dic.values())[-1])
        to_print += 50*'-'+'\n'  # separator

        return to_print

    def is_bs_target(self, target):
        ''' check if a target is triggered by this blendshape '''

        return target in self.target_map.keys()

        
def format_timecode(tc):
    ''' returns timecode in form HH:MM:SS:FF from a tuple of 4 elements '''
    timecode = [str(v).zfill(2) for v in map(int,tc)]
    return ':'.join(timecode)
    

def create_blendshapes(ue_map_file):
    """ opend the mapping file and create blendshape objects """

    # read and store full file contents
    with open(ue_map_file, 'r') as f:
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

    # create Blendshape
    bs_data = list()

    for i in range(len(arkit_bs)):
        name = arkit_bs[i]
        new_map = [float(f)for f in curve_data[i].split(',')]
        target_map = dict((k, v) for k, v in zip(mh_bs, new_map) if float(v))

        bs_data.append(BlendShape(name, target_map))

    return bs_data, mh_bs


def get_anim_data(llf_file, bs_data):
    
    # store csv file in a dataframe
    data = pd.read_csv(llf_file)

    # round up data to get rid of scientific notation like 1.e-5 that may confuse maya/mobu
    data = data.round(4)

    # replace NaN values by 0
    data = data.fillna(0.0)

    # extract timecode as a tuple of 4 elements
    timecode = list()
    for value in data['Timecode'].tolist():
        h, m, s, f = tuple(map(int, value[:-4].split(':')))
        f = float(f)
        timecode.append((h, m, s, f))

    # create list of blendshapes
    for col_name, col_values in data.transpose().iterrows():

        for bs in bs_data:
            if bs.name == col_name:
                bs.keys_dic = dict(zip(timecode, col_values.tolist()))

    # delete bs without keys (not part of the csv file)
    bs_data = [bs for bs in bs_data if bs.keys_dic]
            
    return bs_data, timecode


### MAIN ###
start = time.time()
pj_folder = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder"

# create blendshapes
ue_map_file = os.path.join(pj_folder, 't3d', 'mh_arkit_mapping_pose.T3D')
bs_data, mh_bs = create_blendshapes(ue_map_file)

# retrieve BS information from csv file
llf_file = os.path.join(pj_folder, 'csv', 'rom.csv')
bs_data, tc_range = get_anim_data(llf_file, bs_data)
tc_in, tc_out = tc_range[0], tc_range[-1]

# select root joint to access properties
lModelList = FBModelList()
FBGetSelectedModels(lModelList)
if not lModelList:
    raise ValueError("ERROR: Select Root Joint")
root = lModelList[0]

# create TimeCode object
tc = FBTimeCode(FBTimeCode.FRAMES_5994)

# browse through target shapes
for target in mh_bs:
    # find target property   
    mh_target = root.PropertyList.Find(target)
    # if found
    if mh_target:
        # set property as animated
        mh_target.SetAnimated(True)
        target_value = 0.0
        # browse through timecode
        for tc_frame in tc_range:        
            # find bs influencing this target
            for bs in bs_data:
                if bs.is_bs_target(target):
                    # add bs value depending on the influence
                    print(bs.name)
                    print(target)
                    print(tc_frame)
                    print(bs.keys_dic[tc_frame])
                    print(bs.target_map[target])
                    target_value += bs.keys_dic[tc_frame] * bs.target_map[target]
            # set target value at this timecode
            tc.SetTimeCode(*tc_frame)
            time = tc.GetTime() 
            mh_target.Data = target_value
            mh_target.KeyAt(time)
                    
# set timeframe
tc.SetTimeCode(*tc_in)
time_in = tc.GetTime()
tc.SetTimeCode(*tc_out)
time_out = tc.GetTime()
FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(time_in, time_out)

end = time.time()
duration = end - start
print("Mocap data copied in {} seconds / {} minutes".format(duration, duration/60))
