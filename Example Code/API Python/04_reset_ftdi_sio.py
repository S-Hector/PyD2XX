import PyD2XX

Status = PyD2XX.reset_ftdi_sio()
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO RESET: ABORTING")
    exit()
print("Successfully reset ftdi_sio!")