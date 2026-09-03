import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

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

for i in range(DeviceCount): # Open only the first device not in use by a process.
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
        print("Device selected for reading!")
        break

if isinstance(Device, int):
    print(PyD2XX.FT_STATUS_STR[Device] + " | FAILED TO OPEN ANY DEVICE: ABORTING")
    exit()

CommandString = ""

# Below loop reads 1 byte at a time forever until we receive "exit()".
print("---| Basic Input Terminal (Baud Rate = " + str(BAUD_RATE) + ") |---")
print("Send \"exit()\" from your external device to end the program.")
Status = PyD2XX.FT_SetBaudRate(Device, BAUD_RATE)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BAUD RATE: ABORTING")
    exit()
Status = PyD2XX.FT_Purge(Device, PyD2XX.FT_PURGE_RX | PyD2XX.FT_PURGE_TX)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO PURGE RX & TX BUFFERS: ABORTING")
    exit()
while(True):
    Status, Byte, BytesRead = PyD2XX.FT_Read(Device, 1)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO READ: ABORTING")
        exit()
    if(BytesRead != 1):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO READ BYTE: ABORTING")
        exit()
    Byte = Byte.Value().decode("ascii")
    match Byte:
        case '\n': # Newline
            if(CommandString.strip() == "exit()"): # Exit loop.
                break
            CommandString = ""
            print("")
        case '\r': # Newline
            if(CommandString.strip() == "exit()"): # Exit loop.
                break
            CommandString = ""
            print("")
        case '\b': # Backspace
            print(Byte + " " + Byte, end="", flush=True)
            CommandString = CommandString[:-1] # Remove last byte from command string.
        case _: # Default, print other characters.
            CommandString += Byte
            print(Byte, end="", flush=True) # Force Python to print (flush output) immediately.
print("") # Newline.
Status = PyD2XX.FT_Close(Device)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
    exit()
print("Successfully closed the device!")

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")