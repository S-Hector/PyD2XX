import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# ---| Main Code Starts Here |---
if(PyD2XX.Platform != "windows"):
    print("Only Windows has COM port number!")
    exit()

Status, DeviceCount = PyD2XX.FT_CreateDeviceInfoList()
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CREATE DEVICE INFO LIST: ABORTING")
    exit()
if(DeviceCount < 1):
    print("Aborting: No FTDI devices connected!")
    exit()
print("Detected " + str(DeviceCount) + " FTDI devices!")

Status, Device = PyD2XX.FT_GetDeviceInfoDetail(0)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET DEVICE INFO LIST: ABORTING")
    exit()
print("---| Device 0 (\"" +  Device.Description  + "\", \"" \
        + Device.SerialNumber \
        + "\") |---")
if(Device.Flags & PyD2XX.FT_FLAGS_OPENED):
    print("  Device is in use by another process! Will not attempt to open!")
else:
    print("  Device is free! Will attempt to get COM port number!")
    Status = PyD2XX.FT_Open(0, Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
        exit()
    print("  Successfully opened!")
    Status, COM = PyD2XX.FT_GetComPortNumber(Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET COM NUMBER: ABORTING")
        exit()
    print("  Device is COM" + str(COM))
    
    Status = PyD2XX.FT_Close(Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
        exit()
    print("  Successfully closed!")
