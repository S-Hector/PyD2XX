import PyD2XX
import time

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

CHECK_RX = 100 # Every ms, check RX queue.
BAUD_RATE = 9600

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

Status, DeviceList = PyD2XX.FT_GetDeviceInfoList(DeviceCount)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET DEVICE INFO LIST: ABORTING")
    exit()

for i in range(DeviceCount):
    Device = DeviceList[i]
    print("---| Device " + str(i) + " (\"" +  Device.Description  + "\", \"" \
            + Device.SerialNumber + "\", " \
            + "0x" + format(Device.LocID, "08X") + ") |---")
    if(Device.Flags & PyD2XX.FT_FLAGS_OPENED):
        print("  Device is in use by another process! Will not attempt to open!")
        Device = PyD2XX.FT_DEVICE_NOT_FOUND # Indicate we did not find an unopened device.
    else:
        print("  Device is free! Will attempt to open!")
        Status = PyD2XX.FT_Open(i, Device)
        if(Status != PyD2XX.FT_OK):
            print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
            exit()
        print("  Device selected for reading!")
        break
    Device = False

if isinstance(Device, bool):
    print("Failed to open any device: ABORTING")
    exit()

Status = PyD2XX.FT_SetBaudRate(Device, BAUD_RATE)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BAUD RATE: ABORTING")
    exit()
Status = PyD2XX.FT_Purge(Device, PyD2XX.FT_PURGE_RX | PyD2XX.FT_PURGE_TX)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO PURGE RX & TX BUFFERS: ABORTING")
    exit()
Stop = ord('A')
print("---| Queue Input Terminal (Baud Rate = " + str(BAUD_RATE) + ") |---")
#Stop receiving bytes if we obtain a newline or carriage return.
while((Stop != ord('\n')) and (Stop != ord('\r'))):
    time.sleep(CHECK_RX / 1000)
    Status, QueueStatus = PyD2XX.FT_GetQueueStatus(Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET QUEUE STATUS: ABORTING")
        exit()
    if(QueueStatus > 0):
        Status, Buffer, BytesTransferred = PyD2XX.FT_Read(Device, QueueStatus)
        if(Status != PyD2XX.FT_OK):
            print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO READ: ABORTING")
            exit()
        Data = Buffer.Value()
        for i in range(BytesTransferred):
            Character = chr(Data[i])
            match Character:
                case '\r':
                    Character = "\\r"
                case '\n':
                    Character = "\\n"
                case '\t':
                    Character = "\\t"
                case '\0':
                    Character = "\\0"
                case _: # Default case
                    pass
            print("Receiver Processed: '" + Character + "' / 0x" + "{:02X}".format(Data[i]))
            Stop = Data[i]

Status = PyD2XX.FT_Close(Device)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
    exit()
print("Successfully closed!")

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")