from pyfbsdk import *
from pyfbsdk_additions import *
import os

# LIBRARIES #########################################################################################################################################
import pandas as pd # to be installed, see documentation
from datetime import datetime

# CLASSES ###########################################################################################################################################

class BlendShape:
    """ describes an ARKit blendshape """

    def __init__(self, name, target_map):
        # (string) bs name as used in the CSV column's header, e.g.: EyeBlinkLeft
        self.name = name
        # (dict mh_target:value) mapping of the metahuman target shapes influenced by this blendshape, e.g.: for EyeBlinkLeft CTRL_expressions_eyeBlinkL: 1.0
        self.target_map = target_map
        # (dict timecode: value) animation values for this blenshape (CSV column header) over the whole timecode (CSV 1st column)
        self.keys_dic = None

    def __repr__(self):
        to_print = "BS Name:\n{}\n\n".format(self.name)
        to_print += "Mapping:\n"
        for key, value in self.target_map.items():
            to_print += "{} = {}\n".format(key, value)
        if self.keys_dic:
            to_print += "\nAnim Keys:\n"
            to_print += "{} >> {}\n".format(convert_timecode_to_string(list(self.keys_dic.keys())[0]), list(self.keys_dic.values())[0])
            to_print += ".........\n"
            to_print += "{} >> {}\n".format(convert_timecode_to_string(list(self.keys_dic.keys())[-1]), list(self.keys_dic.values())[-1])
        to_print += 50*'-'+'\n'  # separator
        return to_print

    def is_bs_target(self, target):
        ''' check if a target is triggered by this blendshape '''
        return target in self.target_map.keys()


# SCRIPT METHODS ####################################################################################################################################     

def convert_timecode_to_string(tc):
    """ returns timecode in form HH:MM:SS:FF from a tuple of 4 elements (hh, mm, dd, ff) """
    timecode = [str(v).zfill(2) for v in map(int,tc)]
    return ':'.join(timecode)

def convert_timecode_to_tuple(tc):
    """ returns timecode in form of a tuple (hh, mm, dd, ff) from a string in form HH:MM:SS:FF """
    h, m, s, f = tuple(map(int, tc.split(':')))
    return h, m, s, f

def convert_fbtime_to_string(fbtime):
    """ returns timecode in form HH:MM:SS:FF from an FBTime object """
    mode = FBTimeMode.kFBTimeModeDefault
    format = FBTime().ETimeFormats.eSMPTE
    return fbtime.GetTimeString(mode, format)

def convert_fbtime_to_tuple(fbtime):
    """ returns timecode in form of a tuple (hh, mm, dd, ff) from an FBTime object """
    return convert_timecode_to_tuple(convert_fbtime_to_string(fbtime))

def log(Str, Date = False, Time = True):
    """ print a string with time log """
    now = datetime.now()
    Date = now.strftime("%m/%d/%Y, ") if Date else ""
    Time = now.strftime("%H:%M:%S") if Time else ""
    print("{}{} > {}".format(Date, Time, Str))

def create_blendshapes(ue_map_file):
    """ open the T3D mapping file from UE and create blendshape objects """

    # read and store full file contents
    with open(ue_map_file, 'r') as f:
        ue_contents = f.read()

    import re

    # retrieve ARKit poses in an array of 53 BlendShapes objects
    pattern = r'DisplayName="([\w_]+)"'
    arkit_bs = [data for data in re.findall(pattern, ue_contents) if not 'CTRL_' in data and not 'head_' in data]

    # retrieve MetaHuman poses in an array of 323 targets. Targets shapes starts with 'CTRL' and correctives with 'head'
    pattern = r'DisplayName="[\w_]+"'
    mh_bs = [bs.split('=')[-1][1:-1] for bs in re.findall(pattern, ue_contents) if 'CTRL_' in bs or 'head_' in bs]

    # retrieve bs values as an aray of arrays (for each ARKit BlendShape => all corresponding MetaHuman target mapping values)
    pattern = r',CurveData=\((([-+]?[0-9]\.[0-9]+,?)*)\)'
    curve_data = [data[0] for data in re.findall(pattern, ue_contents)]

    # create and fill up list of BlendShape objects
    bs_data = list()

    for i in range(len(arkit_bs)):
        name = arkit_bs[i]
        new_map = [float(f)for f in curve_data[i].split(',')]
        target_map = dict((k, v) for k, v in zip(mh_bs, new_map) if float(v))
        bs_data.append(BlendShape(name, target_map))

    # return the list of BlendShape objects and the list of targets
    return bs_data, mh_bs


def get_anim_data(llf_file, bs_data, start_tc):
    """ reads the CSV file and extracts for each BlendShape objects all timecode and animation values """

    # store csv file in a dataframe
    data = pd.read_csv(llf_file)

    # round up data to get rid of scientific notation like 1.e-5 that may confuse maya/mobu
    data = data.round(4)

    # replace NaN values by 0
    data = data.fillna(0.0)

    # extract timecode values from the dataframe (deleting the unwanted last 4 digits)
    tc_list = [v[:-4] for v in data['Timecode'].tolist()]
    tc_offset = FBTime(0, 0, 0, 0)

    # if starting timecode specified
    if start_tc:

        # calculate offset between (required) timecode start and anim start
        fbtime_tc_start = FBTime(*convert_timecode_to_tuple(start_tc))
        fbtime_anim_start = FBTime(*convert_timecode_to_tuple(tc_list[0]))
        tc_offset = fbtime_tc_start - fbtime_anim_start
        log("Timecode found. Animation starts at {}".format(start_tc))
    else:
        log("No Timecode found. Animation starts at {}".format(tc_list[0]))

    # store new timecode as a tuple with offset for each frame
    timecode = list()
    for value in tc_list:
        tc_frame = FBTime(*convert_timecode_to_tuple(value)) + tc_offset
        timecode.append(convert_fbtime_to_tuple(tc_frame))

    # browse through column header (BlendShape name) and column contents (values)
    for col_name, col_values in data.transpose().iterrows():
        # if valid BlendShape object found, fills up it's dict of {timecode:animation} values
        for bs in bs_data:
            if bs.name == col_name:
                bs.keys_dic = dict(zip(timecode, col_values.tolist()))

    # delete BlendShapes without keys (not part of the csv file)
    bs_data = [bs for bs in bs_data if bs.keys_dic]
    
    # return the list of BlendShape objects and the list of timecodes
    return bs_data, timecode


def get_starting_tc(tc_file):
    """ extract audio timecode information from a csv file (e.g.: created with Tentacle Timecode Tool) """

    # extract file name and starting TC from csv file
    df = pd.read_csv(tc_file)
    df_len = len(df['Filename'])

    # store info in dictionnary of {Filename: Timecode}
    start_tc = dict()
    for i in range(df_len):
        filename = df.iloc[i]['Filename'] # file name header
        timecode = df.iloc[i]['Timecode'] # starting TC header
        start_tc[filename] = timecode

    return start_tc
    

def batch_retarget_animations(rig_file, map_file, anim_source, export_dir=None, sync_file=None):
    """ main function called by the UI """

    # paths verification
    if not os.path.isfile(rig_file) or not rig_file.lower().endswith('.fbx'):
        raise ValueError("rig_file is not a valid path or does not point to an FBX file")

    # list animations to process (batch mode)
    anims_to_process = list()

    if os.path.isfile(anim_source) and anim_source.lower().endswith('.csv'):
        anims_to_process.append(anim_source)
    elif os.path.isdir(anim_source):
        anims_to_process = [os.path.join(anim_source, f) for f in os.listdir(anim_source) if f.lower().endswith('.csv')]
        if not anims_to_process:
            raise ValueError("No CSV files found in anim_source folder")
    else:
        raise ValueError("anim_source is not a valid path to a CSV file or a folder containing CSV files")

    # create list of BlendShapes objects and list of MetaHuman target names (done once, outside of the batch)
    bs_data, mh_bs = create_blendshapes(map_file)

    # get starting timecodes
    # start_tic = dict()
    # if os.path.isfile(sync_file) and sync_file.lower().endswith('.csv'):
    #     start_tc = get_starting_tc(sync_file)

    # mobu file load options
    lRigImportOptions = FBFbxOptions(False)
    lRigImportOptions.TakeSpan = FBTakeSpanOnLoad().kFBLeaveAsIs
    lRigImportOptions.ShowOptionsDialog = False

    # ensure export dir is valid
    if not export_dir:
        export_dir = os.path.join(anim_source, "Export")
    elif export_dir and not os.path.exists(export_dir):
        os.makedirs(export_dir)
        
    # create counters for end summary
    counter_success = 0
    counter_fail = 0

    # batch process csv files
    for anim_file in anims_to_process:

        if True:# try:
            # get animation name without path or extension
            anim_name = os.path.split(anim_file)[-1][:-4]
            log("Retargeting {} >> START".format(anim_name))

            # get starting timecode if available for this animation
            anim_start_tc = ''

            # open rig file
            FBApplication().FileOpen(rig_file, False, lRigImportOptions)

            # retrieve BlendShape information and timecode list from the CSV animation file
            bs_data, tc_range = get_anim_data(anim_file, bs_data, anim_start_tc)

            # store timecode in and out
            tc_in, tc_out = tc_range[0], tc_range[-1]

            # select root joint to access its properties and delete all keys from it and children
            root = FBFindModelByLabelName('root')
            for node in root.AnimationNode.Nodes:
                if node.FCurve:
                    node.FCurve.EditClear()

            # create TimeCode object at given framerate (LLF uses 59.94 fps)
            tc = FBTimeCode(FBTimeCode.FRAMES_5994)

            # browse through blendshapes
            for bs in bs_data:
                # look for bs property on root joint
                mh_target = root.PropertyList.Find(bs.name)
                # if target found (i.e. name valid)
                if mh_target:
                    print(mh_target.Name)
                    # set property as animated
                    mh_target.SetAnimated(True)
                    # browse through timecode
                    for tc_frame in tc_range:
                        # create a value that will be keyed onto that property target at given timecode  
                        target_value = bs.keys_dic[tc_frame]    
                        # set target value at this timecode
                        tc.SetTimeCode(*tc_frame)
                        lTime = tc.GetTime()
                        # round up to 0 the very small influences
                        if target_value < 0.01:
                            target_value = 0.0
                        # key value at given timecode frame
                        mh_target.Data = target_value
                        mh_target.KeyAt(lTime)
                        
            # set the animation timespan
            tc.SetTimeCode(*tc_in)
            time_in = tc.GetTime()
            tc.SetTimeCode(*tc_out)
            time_out = tc.GetTime()
            FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(time_in, time_out)

            # save animation
            export_path = os.path.join(export_dir, anim_name + '.fbx')
            FBApplication().FileSave(export_path)

        # except Exception as e:
        #     log("Retargeting {} >> ERROR {}".format(anim_name, e))
        #     counter_fail += 1
        # else:
        #     log("Retargeting {} >> DONE".format(anim_name))
        #     counter_success += 1
        # finally:
        #     print(60 * "-")

    # Summary and counters
    log("Batch script done\nFiles Processed: {} / Success: {} / Failed: {}".format(counter_success + counter_fail, counter_success, counter_fail))


rig_file = r'D:\mocap\llf_to_mh\rig\ada_face_skeleton.fbx'
map_file = r'D:\mocap\llf_to_mh\map\mh_arkit_mapping_pose.T3D'
anim_source = r'D:\mocap\llf_to_mh\anim\alex_face_rom_1_live.csv'
batch_retarget_animations(rig_file, map_file, anim_source, export_dir=None, sync_file=None)