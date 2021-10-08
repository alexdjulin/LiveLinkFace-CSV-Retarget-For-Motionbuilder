import ctrl
importlib.reload(ctrl)


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

# EDITABLE FIELDS
eRigFile = FBEdit()
eMapFile = FBEdit()
eAnimSource = FBEdit()
eExportDir = FBEdit()
eSyncFile = FBEdit()

# BUTTONS
bResetBtn = FBButton()
bOKBtn = FBButton()

# CONTROL/EEVENT FUNCTIONS #########################################################
def startBatch(control, event):    
    """ call main batch retarget function """
    rig_file = eRigFile.Text
    map_file = eMapFile.Text
    anim_source = eAnimSource.Text
    export_dir = eExportDir.Text
    sync_file = eSyncFile.Text
    ctrl.batch_retarget_animations(rig_file, map_file, anim_source, export_dir, sync_file)

def resetFields(control, event):
    """ reset all fields """
    eRigFile.Text = ''
    eMapFile.Text = ''
    eAnimSource.Text = ''
    eExportDir.Text = ''
    eSyncFile.Text = ''

# POPULATE LAYOUT #################################################################
def PopulateLayout(mainLyt):
    
    lWidth = 80
    eWidth = 370
    btnWidth = 225

    # RIG FILE
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(15,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytRigFile","lytRigFile", x, y, w, h)
    mainLyt.SetControl("lytRigFile",lytRigFile)
    lRigFile.Caption = "MH Rig:"
    eRigFile.Text = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\rig\Unrealmetahuman_TPose.fbx"
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
    lMapFile.Caption = "Map File:"
    eMapFile.Text = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\map\mh_arkit_mapping_pose.T3D"
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
    lAnimSource.Caption = "Animation(s):"
    eAnimSource.Text = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\anim"
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
    lExportDir.Caption = "Export Folder:"
    eExportDir.Text = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\export"
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
    lSyncFile.Caption = "TC Sync File:"
    eSyncFile.Text = r"M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder\timecode\tc.csv"
    eSyncFile.Hint = "Path to CSV file containing timecode starts (not required)"
    lytSyncFile.Add(lSyncFile,lWidth)
    lytSyncFile.Add(eSyncFile,eWidth)
    
    # BUTTONS: RESET AND OK
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(200,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(30,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("lytButtons","lytButtons", x, y, w, h)
    mainLyt.SetControl("lytButtons",lytButtons)
    
    bResetBtn.Caption = "RESET"
    bResetBtn.Hint = "Reset all fields"
    bResetBtn.Justify = FBTextJustify.kFBTextJustifyCenter
    bResetBtn.Look = FBButtonLook.kFBLookColorChange
    bResetBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.8, 0.0, 0.2))
    lytButtons.Add(bResetBtn,btnWidth)
    bResetBtn.OnClick.Add(resetFields)
    
    bOKBtn.Caption = "OK"
    bOKBtn.Hint = "Start the batch retarget"
    bOKBtn.Justify = FBTextJustify.kFBTextJustifyCenter
    bOKBtn.Look = FBButtonLook.kFBLookColorChange
    bOKBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.0, 0.5, 0.2))
    lytButtons.Add(bOKBtn,btnWidth)
    bOKBtn.OnClick.Add(startBatch)
    
    
# CREATE UI ##############################################################################
def CreateTool():
    global globalTool
    globalTool = FBCreateUniqueTool("LiveLinkFace to MetaHuman Animation Retarget")
    globalTool.StartSizeX = 500
    globalTool.StartSizeY = 270
    PopulateLayout(globalTool)
    ShowTool(globalTool)
    return globalTool
