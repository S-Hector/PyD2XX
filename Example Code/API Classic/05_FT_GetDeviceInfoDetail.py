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

DeviceList = {}
for i in range(DeviceCount):
    Status, DeviceList[i] = PyD2XX.FT_GetDeviceInfoDetail(i)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET DEVICE INFO LIST: ABORTING")
        exit()

for i in range(DeviceCount):
    Device = DeviceList[i]
    print("---| Device " + str(i) + " (\"" +  Device.Description  + "\", \"" \
            + Device.SerialNumber \
            + "\") |---")
    print("  Flags = 0x" + format(Device.Flags, "08X") + \
        " | Device is " + ("High Speed" if(Device.Flags & PyD2XX.FT_FLAGS_HISPEED) else "Full Speed") + \
        " and " + ("in use by another process." if (Device.Flags & PyD2XX.FT_FLAGS_OPENED) else "free to use."))
    print("  Type = 0x" + format(Device.Type, "08X") + \
    " | Device Type = " + PyD2XX.FT_DEVICE_STR[Device.Type])
    VID = (Device.ID >> 16) & int("0x0FFFF", 16);
    PID = Device.ID & int("0x0FFFF", 16);
    print("  ID = 0x" + format(Device.ID, "08X") + \
    " | VID:PID = " + format(VID, "x").zfill(4) + ":" + format(PID, "x").zfill(4))
    print("  LocID = 0x" + format(Device.LocID, "08X"))
    print("  Serial Number = \"" + Device.SerialNumber + "\"")
    print("  Description = \"" + Device.Description + "\"")
    print("  Handle = ", end="")
    if(isinstance(Device.Handle, str)):
        print("\"" + Device.Handle + "\"")
    else:
        print("0x" + format(Device.ID, "016X"))

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")