import PyD2XX
import time

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

PRINT_STREAM = True # If true, HS_StreamOutput will print each byte written.

def HS_StreamOutput(Device: PyD2XX.FT_Device, OutputStream: bytearray, StreamLength: int, IntervalMS: int):
    Status = PyD2XX.FT_OTHER_ERROR
    if((len(OutputStream) <  1) or (StreamLength < 1)):
        return PyD2XX.FT_INVALID_PARAMETER
    for i in range(StreamLength):
        Buffer = PyD2XX.FT_Buffer.from_int(OutputStream[i])
        Status, BytesWritten = PyD2XX.FT_Write(Device, Buffer, 1)
        if(PRINT_STREAM):
            print("Wrote(" + str(BytesWritten) + "): '" + hex(OutputStream[i]) + "'")
        if(Status != PyD2XX.FT_OK):
            return Status
        if(BytesWritten != 1):
            return PyD2XX.FT_IO_ERROR
        time.sleep(IntervalMS / 1000.0)
    return Status

# ---| Main Code Starts Here |---
OutputStream = bytearray.fromhex("90 80 F8 82 92 99 B0 A4 F9 C0 40 7F FF 7F") #Bytes are from left to right.
StreamLength = len(OutputStream)

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
if(DeviceCount > 1):
    print("Aborting: Too many FTDI devices connected!")
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

Status = PyD2XX.FT_SetBitMode(Device, int("0x00FF", 16), PyD2XX.FT_BITMODE_ASYNC_BITBANG)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BIT MODE: ABORTING")
    exit()
print("Entered Async Bit-Bang mode with all DATA pins as outputs.")
print("Outputing data...")
Status = HS_StreamOutput(Device, OutputStream, StreamLength, 1000)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO STREAM OUTPUT: ABORTING")
    exit()
print("Finished outputing data.")
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