import PyD2XX

CUSTOM_VID = int("0x1234",16)
CUSTOM_PID = int("0xABCD",16)

# VID:PID combo is registered until the module is unloaded or the system reboots.
Status = PyD2XX.register_ftdi_sio(VID = CUSTOM_VID, PID = CUSTOM_PID)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO REGISTER: ABORTING")
    exit()
print("Successfully registered to ftdi_sio!")