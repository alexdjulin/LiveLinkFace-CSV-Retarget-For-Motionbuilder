# https://re-thought.com/how-to-suppress-scientific-notation-in-pandas/
# https://stackoverflow.com/questions/28218698/how-to-iterate-over-columns-of-pandas-dataframe-to-run-regression
# https://knowledge.autodesk.com/support/motionbuilder/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/MotionBuilder/files/GUID-46E090C5-34AD-4E26-872F-F7D21DC57C74-htm.html
# https://help.autodesk.com/view/MOBPRO/2018/ENU/?guid=__py_ref__tasks_2_time_code_keying_8py_example_html

from pyfbsdk import *
from pyfbsdk_additions import *
import pandas as pd


class BlendShape:

    def __init__(self, name, keys_dic):
        self.name = name
        self.keys_dic = keys_dic

    def __repr__(self):
        to_print = "{}\n".format(self.name)
        for key, value in self.keys_dic.items():
            to_print += "{}: {}\n".format(key, value)
        return to_print
        

def get_bs_data(csv_file):

    # store csv file in a dataframe
    data = pd.read_csv(csv_file)

    # round up data to get rid of scientific notation like 1.e-5 that may confuse maya/mobu
    data = data.round(4)

    # extract timecode as a tuple of 4 elements
    timecode = list()
    for value in data['Timecode'].tolist():
        h, m, s, f = tuple(map(int, value[:-4].split(':')))
        f = float(f)
        timecode.append((h, m, s, f))

    # create list of blendshapes
    bs_data = list()
    for col_name, col_values in data.transpose().iterrows():
        bs_data.append(BlendShape(col_name, dict(zip(timecode, col_values.tolist()))))

    # get rid of the first two columns (Timecode/BlendShapeCount)
    bs_data = bs_data[2:]

    return bs_data

# retrieve BS information from csv file
csv_file = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\facial.csv"
bs_data = get_bs_data(csv_file)

# select root joint to access properties
lModelList = FBModelList()
FBGetSelectedModels(lModelList)
root = lModelList[0]
print(root.Name)

arkit_bs_name = "JawOpen"
mh_bs_name = "CTRL_expressions_jawOpen"
tc = FBTimeCode(FBTimeCode.FRAMES_30)

for bs in bs_data:
    if bs.name == arkit_bs_name:
        print(arkit_bs_name)
        print(mh_bs_name)
        
        mh_bs = root.PropertyList.Find(mh_bs_name) 
        mh_bs.SetAnimated(True)
        
        for frame, value in bs.keys_dic.items():
            tc.SetTimeCode(frame)
            time = tc.GetTime()
            mh_bs.Data = value
            mh_bs.KeyAt(time)

print("done")
'''
time = FBTimeCode()
time.SetTimeCode(0,0,0,4)
lBS.KeyAt(time)
print("done")
''' 

'''
for bs in bs_data:
    bs_name = 'CTRL_expressions_' + bs.name[0].lower() + bs.name[1:]
    lBS = root.PropertyList.Find(bs_name)
'''  