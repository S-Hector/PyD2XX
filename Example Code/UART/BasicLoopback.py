import PyD2XX
import time

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

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

Status, DeviceList = PyD2XX.FT_GetDeviceInfoList(DeviceCount)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET DEVICE INFO LIST: ABORTING")
    exit()
Device = DeviceList[0]
print("---| Device 0 (" +  PyD2XX.FT_DEVICE_STR[Device.Type]  + ", " \
    + ("High Speed" if(Device.Flags == PyD2XX.FT_FLAGS_HISPEED) else "Full Speed") \
    + ") |---")

print("  Device is " + ("in use by another process." if (Device.Flags == PyD2XX.FT_FLAGS_OPENED) else "free to use."))
VID = (Device.ID >> 16) & int("0x0FFFF", 16);
PID = Device.ID & int("0x0FFFF", 16);
print("  VID:PID = " + format(VID, "x").zfill(4) + ":" + format(PID, "x").zfill(4))
print("  Description = \"" + Device.Description + "\"")
print("  Serial Number = \"" + Device.SerialNumber + "\"")

Status = PyD2XX.FT_Open(0, Device)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE 0: ABORTING")
    exit()
print("Opened device 0!")

Status = PyD2XX.FT_SetBitMode(Device, int("0x0000", 16), PyD2XX.FT_BITMODE_RESET)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BIT MODE: ABORTING")
    exit()

Status = PyD2XX.FT_Purge(Device, PyD2XX.FT_PURGE_RX | PyD2XX.FT_PURGE_TX)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO PURGE DEVICE BUFFERS: ABORTING")
    exit()

LoopbackString = "Hello World"
LS_Length = len(LoopbackString)
Buffer = PyD2XX.FT_Buffer.from_str(LoopbackString)
Status, BytesWritten = PyD2XX.FT_Write(Device, Buffer, LS_Length)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO WRITE STRING: ABORTING")
    exit()
if(BytesWritten != LS_Length):
    print("Only " + str(BytesWritten) + " bytes were written when " + str(LS_Length) + " bytes were expected!")
    exit()
print("Wrote(" + str(BytesWritten) + "): \"" + LoopbackString +"\"")
Status, Buffer, BytesRead = PyD2XX.FT_Read(Device, BytesWritten)
if(BytesRead != BytesWritten):
    print("Only " + str(BytesRead) + " bytes were read when " + str(BytesWritten) + " bytes were expected!")
    exit()

ReadString = Buffer.Value().decode("utf-8")
print("Read(" + str(BytesRead) + "): \"" + ReadString +"\"")
if(ReadString != LoopbackString):
    print("ERROR: Received string does not match sent string!")

Status = PyD2XX.FT_Close(Device)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE 0: ABORTING")
    exit()
print("Closed device!")

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")