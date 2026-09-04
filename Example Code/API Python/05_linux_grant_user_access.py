import PyD2XX

CUSTOM_VID = int("0x1234",16)
CUSTOM_PID = int("0xABCD",16)

# User access lasts until device is unplugged/reset/power cycled.
Status = PyD2XX.linux_grant_user_access(VID = CUSTOM_VID, PID = CUSTOM_PID)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GRANT USER ACCESS: ABORTING")
    exit()
print("Successfully granted user access!")