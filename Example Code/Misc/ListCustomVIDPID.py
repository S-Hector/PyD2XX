import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# This grants user access to a device if they don't already have it on Linux.
# Without access to the device, the library will fail to get device information and not actually be able to use the device, despite detecting it.

CUSTOM_VID = int("0x1234",16)
CUSTOM_PID = int("0xABCD",16)
REGISTER_TO_FTDI_SIO = True # Set to false if you don't want the VID:PID combo to be registered & binded to FTDI_SIO.
#^ Registration to ftdi_sio lasts until the module is removed or the system is rebooted.
# Device automatically gets binded when registered. So no extra bind call is needed.

# ---| Main Code Starts Here |---

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
    print("Added VID:PID Combo | " + format(CVID, 'X') + ":" + format(CPID, 'X'))
else:
    print("This example is not for Windows!")
    exit()
Rebind = True
if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.linux_grant_user_access(VID = CUSTOM_VID, PID = CUSTOM_PID)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GRANT USER ACCESS: ABORTING")
        exit()
    print("Successfully granted user access to (VID:PID = " + format(CVID, 'X') + ":" + format(CPID, 'X') + ") devices!")
    Status = PyD2XX.unbind_ftdi_sio(VID = CUSTOM_VID, PID = CUSTOM_PID)
    if((Status != PyD2XX.FT_OK) and (Status != PyD2XX.FT_DEVICE_NOT_FOUND)):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO UNBIND FTDI DEVICES FROM ftdi_sio: ABORTING")
        exit()
    print("Unbinded all FTDI devices (VID:PID = " + format(CVID, 'X') + ":" + format(CPID, 'X') + ") from ftdi_sio!")
    Rebind = (Status != PyD2XX.FT_DEVICE_NOT_FOUND)
if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.unbind_ftdi_sio(VID = int("0x0403", 16))
    if((Status != PyD2XX.FT_OK) and (Status != PyD2XX.FT_DEVICE_NOT_FOUND)):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO UNBIND FTDI DEVICES FROM ftdi_sio: ABORTING")
        exit()
    print("Unbinded all FTDI devices (VID == 0x0403) from ftdi_sio!")
    Rebind = (Status != PyD2XX.FT_DEVICE_NOT_FOUND)

Status, DeviceCount = PyD2XX.FT_CreateDeviceInfoList()
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CREATE DEVICE INFO LIST: ABORTING")
    exit()
if(DeviceCount < 1):
    print("Aborting: No FTDI devices connected!")
    exit()
print("Detected " + str(DeviceCount) + " FTDI devices!")

Status, DeviceList = PyD2XX.FT_GetDeviceInfoList(DeviceCount)
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
    " | " + PyD2XX.FT_DEVICE_STR[Device.Type])
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
    Status = PyD2XX.bind_ftdi_sio(VID = int("0x0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")

if((PyD2XX.Platform == "linux") and Rebind and REGISTER_TO_FTDI_SIO):
    Status = PyD2XX.register_ftdi_sio(VID = CUSTOM_VID, PID = CUSTOM_PID)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO REGISTER: ABORTING")
        exit()
    print("Successfully registered (VID:PID = " + format(CVID, 'X') + ":" + format(CPID, 'X') + ") to ftdi_sio!")