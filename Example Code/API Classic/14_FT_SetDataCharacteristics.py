import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

WORD_LENGTH = PyD2XX.FT_BITS_7
STOP_BITS = PyD2XX.FT_STOP_BITS_2
PARITY = PyD2XX.FT_PARITY_ODD

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
    print("  Device is free! Will attempt to set data characteristics!")
    Status = PyD2XX.FT_Open(0, Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
        exit()
    print("  Successfully opened!")
    Status = PyD2XX.FT_SetDataCharacteristics(Device, WORD_LENGTH, STOP_BITS, PARITY)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET DATA CHARACTERISTICS: ABORTING")
        exit()
    print("  Successfully set word bit length to " + str(WORD_LENGTH) + ".")
    print("  Successfully set stop bits to " \
            + ("1" if STOP_BITS == PyD2XX.FT_STOP_BITS_1 else str(STOP_BITS)) \
            + ".")
    print("  Successfully set parity to ", end="")
    match PARITY:
        case PyD2XX.FT_PARITY_NONE:
            print("FT_PARITY_NONE.")
        case PyD2XX.FT_PARITY_ODD:
                print("FT_PARITY_ODD.")
        case PyD2XX.FT_PARITY_EVEN:
                print("FT_PARITY_EVEN.")
        case PyD2XX.FT_PARITY_MARK:
                print("FT_PARITY_MARK.")
        case PyD2XX.FT_PARITY_SPACE:
                print("FT_PARITY_SPACE.")
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