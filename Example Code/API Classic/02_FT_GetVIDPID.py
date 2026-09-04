import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# Check out: ../Misc/ListCustomVIDPID.py

CUSTOM_VID = int("0x1234",16)
CUSTOM_PID = int("0xABCD",16)

if(PyD2XX.Platform != "windows"):
    Status = PyD2XX.FT_SetVIDPID(CUSTOM_VID, CUSTOM_PID)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET CUSTOM VID:PID COMBO: ABORTING")
        exit()
    Status, CVID, CPID = PyD2XX.FT_GetVIDPID()
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET CUSTOM VID:PID COMBO: ABORTING")
        exit()
    if((CVID != CUSTOM_VID) or (CPID != CUSTOM_PID)):
        print("FAILED TO SET/GET CUSTOM VID:PID COMBO: ABORTING")
        exit()
    print("Added and got VID:PID Combo | " + format(CVID, 'X') + ":" + format(CPID, 'X'))
else:
    print("This example is not for Windows!")
    exit()