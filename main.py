from pyfbsdk import *
from pyfbsdk_additions import *

lModelList = FBModelList()
FBGetSelectedModels(lModelList)
root = lModelList[0]
print(root.Name)

for x in lModelList:
    
    lBS = x.PropertyList.Find('CTRL_expressions_jawOpen')
    lBS.Data = 0.2
    lBS.SetAnimated(True)
    time = FBTimeCode()
    time.SetTimeCode(0,0,0,4)
    lBS.KeyAt(time)
    print("done")


