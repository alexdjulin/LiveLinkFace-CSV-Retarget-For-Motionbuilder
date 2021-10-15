from pyfbsdk import *
from pyfbsdk_additions import *
import ctrl
importlib.reload(ctrl)  # python3. Use reload() for python2
import os
import json

# Window elements ############################################################################

# LAYOUTS
lytRigFile = FBHBoxLayout()
lytMapFile = FBHBoxLayout()
lytAnimSource = FBHBoxLayout()
lytExportDir = FBHBoxLayout()
lytSyncFile = FBHBoxLayout()
lytButtons = FBHBoxLayout()

# LABELS
lRigFile = FBLabel()
lMapFile = FBLabel()
lAnimSource = FBLabel()
lExportDir = FBLabel()
lSyncFile = FBLabel()
lRequired = FBLabel()

# EDITABLE FIELDS
eRigFile = FBEdit()
eMapFile = FBEdit()
eAnimSource = FBEdit()
eExportDir = FBEdit()
eSyncFile = FBEdit()

# BUTTONS
bResetBtn = FBButton()
bOKBtn = FBButton()
bHelpBtn = FBButton()

# READ/WRITE JSON DATA
json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def load_data():
    if os.path.isfile(json_file):
        with open(json_file, 'r') as infile:    
            data_dict = json.load(infile)
            eRigFile.Text = data_dict['RigFile']
            eMapFile.Text = data_dict['MapFile']
            eAnimSource.Text = data_dict['AnimSource']
            eExportDir.Text = data_dict['ExportDir']
            eSyncFile.Text = data_dict['SyncFile']

def save_data():
    data_dict = dict()
    data_dict['RigFile'] = eRigFile.Text
    data_dict['MapFile'] = eMapFile.Text
    data_dict['AnimSource'] = eAnimSource.Text
    data_dict['ExportDir'] = eExportDir.Text
    data_dict['SyncFile'] = eSyncFile.Text
    with open(json_file, 'w') as outfile:    
        json.dump(data_dict, outfile, indent=2)


# CONTROL/EEVENT FUNCTIONS #########################################################
def startBatch(control, event):    
    """ call main batch retarget function """
    # get fields contents
    rig_file = eRigFile.Text
    map_file = eMapFile.Text
    anim_source = eAnimSource.Text
    export_dir = eExportDir.Text
    sync_file = eSyncFile.Text
    # save data to json file
    save_data()
    # start batch
    ctrl.batch_retarget_animations(rig_file, map_file, anim_source, export_dir, sync_file)

def resetFields(control, event):
    """ reset all fields """
    eRigFile.Text = ''
    eMapFile.Text = ''
    eAnimSource.Text = ''
    eExportDir.Text = ''
    eSyncFile.Text = ''
    
def openDocumentation(control, event):
    """ open the online documentation page """
    import webbrowser
    webbrowser.open('https://github.com/alexdjulin/LiveLinkFace-CSV-Retarget-For-Motionbuilder')

# POPULATE LAYOUT #################################################################
def PopulateLayout(mainLyt):
    
    # LOAD DATA FROM JSON FILE
    load_data()

    # UI ELEMENTS SIZE
    mainLyt.StartSizeX = 760
    mainLyt.StartSizeY = 270
    lWidth = 120
    eWidth = 600
    btnWidth = int(eWidth/6)
    
    # RIG FILE
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(15,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytRigFile","lytRigFile", x, y, w, h)
    mainLyt.SetControl("lytRigFile",lytRigFile)
    lRigFile.Caption = "MH Rig File [FBX] *"
    eRigFile.Hint = "Path to MetaHuman rig FBX file"
    lytRigFile.Add(lRigFile,lWidth)
    lytRigFile.Add(eRigFile,eWidth)
    
    # MAP FILE
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(50,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytMapFile","lytMapFile", x, y, w, h)
    mainLyt.SetControl("lytMapFile",lytMapFile)
    lMapFile.Caption = "Map File [T3D] *"
    eMapFile.Hint = "Path to the T3D map file used for retargeting in Unreal"
    lytMapFile.Add(lMapFile,lWidth)
    lytMapFile.Add(eMapFile,eWidth)
    
    # ANIM SOURCE
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(85,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytAnimSource","lytAnimSource", x, y, w, h)
    mainLyt.SetControl("lytAnimSource",lytAnimSource)
    lAnimSource.Caption = "Animation(s) [CSV] *"
    eAnimSource.Hint = "Path to a CSV file or folder containing CSV files to process from LiveLinkFace"
    lytAnimSource.Add(lAnimSource,lWidth)
    lytAnimSource.Add(eAnimSource,eWidth)
    
    # EXPORT DIR
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(120,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytExportDir","lytExportDir", x, y, w, h)
    mainLyt.SetControl("lytExportDir",lytExportDir)
    lExportDir.Caption = "Export Folder"
    eExportDir.Hint = "Path to folder where files will be exported (not required)"
    lytExportDir.Add(lExportDir,lWidth)
    lytExportDir.Add(eExportDir,eWidth)

    # SYNC FILE
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(155,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytSyncFile","lytSyncFile", x, y, w, h)
    mainLyt.SetControl("lytSyncFile",lytSyncFile)
    lSyncFile.Caption = "TC Sync File [CSV]"
    eSyncFile.Hint = "Path to CSV file containing timecode starts (not required)"
    lytSyncFile.Add(lSyncFile,lWidth)
    lytSyncFile.Add(eSyncFile,eWidth)
    
    # BUTTONS: HELP, RESET AND OK
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(200,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(30,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytButtons","lytButtons", x, y, w, h)
    mainLyt.SetControl("lytButtons",lytButtons)

    lRequired.Caption = "* Required Fields"
    lytButtons.Add(lRequired,120)
    
    bHelpBtn.Caption = "HELP"
    bHelpBtn.Hint = "Documentation"
    bHelpBtn.Justify = FBTextJustify.kFBTextJustifyCenter
    bHelpBtn.Look = FBButtonLook.kFBLookColorChange
    bHelpBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.4, 0.4, 0.4))
    lytButtons.Add(bHelpBtn,btnWidth)
    bHelpBtn.OnClick.Add(openDocumentation)
        
    bResetBtn.Caption = "RESET"
    bResetBtn.Hint = "Reset all fields"
    bResetBtn.Justify = FBTextJustify.kFBTextJustifyCenter
    bResetBtn.Look = FBButtonLook.kFBLookColorChange
    bResetBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.4, 0.4, 0.4))
    lytButtons.Add(bResetBtn,btnWidth)
    bResetBtn.OnClick.Add(resetFields)
    
    bOKBtn.Caption = "OK"
    bOKBtn.Hint = "Start the batch retarget"
    bOKBtn.Justify = FBTextJustify.kFBTextJustifyCenter
    bOKBtn.Look = FBButtonLook.kFBLookColorChange
    bOKBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0, 165/255, 255/255))
    lytButtons.Add(bOKBtn,btnWidth*4-8)
    bOKBtn.OnClick.Add(startBatch)
    
    
# CREATE UI ##############################################################################
def CreateTool():
    global globalTool
    globalTool = FBCreateUniqueTool("LiveLinkFace to MetaHuman Animation Retarget")
    PopulateLayout(globalTool)
    ShowTool(globalTool)
    return globalTool
