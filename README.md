# Live Link Face to Unreal MetaHuman
*Retarget facial animations recorded with the Live Link Face app onto an Unreal MetaHuman character, using MotionBuilder and Python.*

## Description
This motionbuilder script will open the CSV files created by the Live Link Face app and extract the facial animation in the form of blendshape/timecode values. Using the T3D mapping file from Unreal, it will create connections between the ARKit blendshapes used by the app and the custom properties used by Unreal to drive your MetaHuman’s face. It will then load your MH rig and retarget the facial motion onto it before exporting it as an fbx file, ready to be used in Unreal. The script can also operate in batch mode over multiple CSV files.

## Requirements and installation
Hardware:
+ An iPhone 10 or superior (supported by Live Link Face) and connected to the same network or to the PC via USB.

Software:
+ [Motionbuilder](https://www.autodesk.com/products/motionbuilder/) version 2022 / python3 (to be tested on earlier versions with python2)
+ [Unreal Engine](https://www.unrealengine.com/en-US/) version 4.XX
+ [Live Link Face](https://apps.apple.com/us/app/live-link-face/id1495370836) available for free on the app store
+ [Quixel Bridge](https://quixel.com/bridge) if you want to export your MH to Unreal after creation

Libraries:
+ Pandas for CSV extraction

See [Autodesk documentation](https://knowledge.autodesk.com/support/motionbuilder/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/MotionBuilder/files/GUID-46E090C5-34AD-4E26-872F-F7D21DC57C74-htm.html) on adding libraries to motionbuilder using mobupy.

## Script contents
The script relies on the following files:
+ **run.py**: Entry point, displays the UI when calling main()
+ **ui.py**: UI file, creates and displays the UI, collects information and start the retargeting process
+ **ctrl.py**: Defines the BlendShape class and methods to parse the T3D map file and CSV animation and timecode files. Batch retargets the animations onto the MH rig file and exports FBXs.
+ **data.json**: Optional file, saves the current user input or loads the latest one
The anim, export, map, rig and timecode directories are just for testing and can be moved anywhere, as long as their content is specified correctly in the UI fields.

## How to run the script
Drag-and-drop and execute **run.py** in MotionBuilder, or open it in the Python Editor and run it. It will call the **main()** function and display the UI. Fill up the required fields and click **OK** to start the retargeting batch.
Alternatively you can call **main()** from a menu element or a shortcut.

## UI description
The script offers a basic UI to enter the required and optional paths.
![UI](readme/ui.png?raw=true)

### Required fields
+ **MH Rig File [FBX]**: path to your Unreal MetaHuman skeleton. You can use the one from Ada in the rig folder, which I exported from the [MetaHuman project](https://www.unrealengine.com/marketplace/en-US/product/metahumans).
+ **Map File [t3D]**: path to your map file exported from unreal. You can use teh one from the map folder, which I exported from that same project.
+ **Animation(s) [CSV]**: path to an animation file created by Live Link Face. You can specify a directory with multiple files to run the batch on all of them
### Optional fields:
+ **Export Folder**: path to the folder where fbx animations should be exported. If not specified, takes will be saved in the Animation folder, in an Export subfolder.
+ **TC Sync File [CSV]**: path to a CSV file specifying for each take the starting timecode for synchronisation. If not specified, the animation file timecode will be used.
### Buttons:
+ **Help**: Opens this page
+ **Reset**: Delete all the entries
+ **OK**: Start the batch process

