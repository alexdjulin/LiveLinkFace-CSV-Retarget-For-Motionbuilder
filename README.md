# Live Link Face to Unreal MataHuman
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

