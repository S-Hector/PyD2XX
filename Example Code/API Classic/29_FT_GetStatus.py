import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# ---| Main Code Starts Here |---
if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.unbind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO UNBIND FTDI DEVICES FROM ftdi_sio: ABORTING")
        exit()
    print("Unbinded all FTDI devices (VID == 0x0403) from ftdi_sio!")

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
    print("  Device is free! Will attempt to get status!")
    Status = PyD2XX.FT_Open(0, Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
        exit()
    print("  Successfully opened!")
    Status, QueueRX, QueueTX, Event = PyD2XX.FT_GetStatus(Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET STATUS: ABORTING")
        exit()
    print("  RX Queue has " + str(QueueRX) + " bytes!")
    print("  TX Queue has " + str(QueueTX) + " bytes!")
    print("  Event Status = ", end="")
    match Event:
        case PyD2XX.FT_EVENT_RXCHAR:
            print("FT_EVENT_RXCHAR")
        case PyD2XX.FT_EVENT_MODEM_STATUS:
            print("FT_EVENT_MODEM_STATUS")
        case PyD2XX.FT_EVENT_LINE_STATUS:
            print("FT_EVENT_LINE_STATUS")
        case _: # Default.
            print("NO EVENT")
    
    Status = PyD2XX.FT_Close(Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
        exit()
    print("  Successfully closed!")

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")