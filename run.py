## LiveLinkFace To MetaHuman Retargeting in MotionBuidler ###########################################################################################
### Author: Alexandre Donciu-Julin, a.djulin@mimicproductions.com
#### Description: Retarget facial animation files exported from Apple's LiveLinkFace app as CSV files to a MetaHuman skeleton in MotionBuilder
##### Requirements: A MetaHuman skeleton (ideally the facial one exported from Unreal), a CSV file from LLF app and a T3D mapping file from Unreal
#####################################################################################################################################################

# add project folder to the PATH varialbes
import sys
sys.path.append(r'M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder')

from . import ui
import importlib    # python3. use reload() for python2
importlib.reload(ui)

def main():
    """ call this function below or from a menu/keyboard shortcut to run the script """
    ui.CreateTool()

main()