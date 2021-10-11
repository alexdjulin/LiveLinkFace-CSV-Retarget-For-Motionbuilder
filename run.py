import sys
sys.path.append(r'M:\Artist_Personal\Alexandre\Scripts\Git\LiveLinkFace-CSV-to-MotionBuilder')

import importlib
import ui
importlib.reload(ui)

def main():
    """ call this function below or from a menu/keyboard shortcut to run the script """
    ui.CreateTool()

main()