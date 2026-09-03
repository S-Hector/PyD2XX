import PyD2XX
import time
import threading

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# Note for Windows, make sure no COM port is assigned or the FT_SetFlowControl silently
# fails (returns FT_OK) and you will get garbage data. This is an issue with the underlying
# C library. (e.g. if you wrote code in C, you will get the same behavior)

CHAR_XON = ord('[')
CHAR_XOFF = ord(']')

RECEIVE_PROCESS_TIME = 150 # How much time in ms the receiver takes to "process" a byte.
RECEIVE_MAX_BYTES = 10 # How many bytes the receiver will request & accept at a time.
SENDER_MESSAGE = "This is my message!" # Message Sender sends once.
EOM = ord('\0') # If the receiver gets this char, that's the end of the message.
#^ Strings end in '\0' by default. You can change EOM to say '$',
#^ but then you need to add '$' to the end of SENDER_MESSAGE.

def ReceiverRead(Device: PyD2XX.FT_Device): # Keeps read pipe calls queued up.
    Full = True
    Message = bytearray(0)
    BytesToProcess = 0
    MessageIndex = 0
    while(True):
        if(BytesToProcess == 0):
                print("Receiver Requesting: " + str(RECEIVE_MAX_BYTES) + " byte FT_Read().")
                Status, Buffer, BytesToProcess = PyD2XX.FT_Read(Device, RECEIVE_MAX_BYTES)
                if((Status != PyD2XX.FT_OK) or (BytesToProcess < 1)):
                    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO RECEIVE")
                    break
                Message += Buffer.Value() # Add read bytes to message.
        else:
            time.sleep(RECEIVE_PROCESS_TIME / 1000)
            BytesToProcess -= 1
            Character = chr(Message[MessageIndex])
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
            print("Receiver Processed: '" + Character + "' / 0x" + "{:02X}".format(Message[MessageIndex]))
            if(Message[MessageIndex] == EOM):
                Message = Message[0:(MessageIndex - BytesToProcess + 1)] # Shorten message to remove "unprocessed" bytes.
                print("Received full message below between brackets:\n[\"\n" + Message.decode("ascii") + "\n\"]")
                break
            MessageIndex += 1

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

Receiver = False
Sender = False

for i in range(DeviceCount):
    Device = DeviceList[i]
    print("---| Device " + str(i) + " (\"" +  Device.Description  + "\", \"" \
            + Device.SerialNumber + "\", " \
            + "0x" + format(Device.LocID, "08X") + ") |---")
    if(Device.Flags & PyD2XX.FT_FLAGS_OPENED):
        print("  Device is in use by another process! Will not attempt to open!")
    else:
        print("  Device is free! Will attempt to open!")
        Status = PyD2XX.FT_Open(i, Device)
        if(Status != PyD2XX.FT_OK):
            print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
            exit()
        if isinstance(Receiver, bool):
            Receiver = Device
            print("  Selected device as Receiver.")
        else:
            Sender = Device
            print("  Selected device as Sender.")
            break
if isinstance(Sender, bool):
    print("Failed to open both a Receiver and a Sender: ABORTING")
    exit()

Status = PyD2XX.FT_SetTimeouts(Receiver, 0, 0) # Disable time outs.
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO DISABLE TIME OUTS: ABORTING")
    exit()
Status = PyD2XX.FT_SetTimeouts(Sender, 0, 0) # Disable time outs.
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO DISABLE TIME OUTS: ABORTING")
    exit()

Status = PyD2XX.FT_SetBaudRate(Receiver, 9600)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BAUD RATE: ABORTING")
    exit()
Status = PyD2XX.FT_SetBaudRate(Sender, 9600)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET BAUD RATE: ABORTING")
    exit()

Status = PyD2XX.FT_SetFlowControl(Receiver, PyD2XX.FT_FLOW_XON_XOFF, CHAR_XON, CHAR_XOFF)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET FLOW CONTROL: ABORTING")
    exit()
Status = PyD2XX.FT_SetFlowControl(Sender, PyD2XX.FT_FLOW_XON_XOFF, CHAR_XON, CHAR_XOFF)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET FLOW CONTROL: ABORTING")
    exit()

Status = PyD2XX.FT_Purge(Receiver, PyD2XX.FT_PURGE_RX | PyD2XX.FT_PURGE_TX)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO PURGE RX & TX BUFFERS: ABORTING")
    exit()
Status = PyD2XX.FT_Purge(Sender, PyD2XX.FT_PURGE_RX | PyD2XX.FT_PURGE_TX)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO PURGE RX & TX BUFFERS: ABORTING")
    exit()

ReceiverThread = threading.Thread(target=ReceiverRead, args=(Receiver,))
ReceiverThread.start() # Start Receiver thread.

# Send message
Status, BytesTransferred = PyD2XX.FT_Write(Device, PyD2XX.FT_Buffer.from_str(SENDER_MESSAGE), len(SENDER_MESSAGE))
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO WRITE: ABORTING")
    exit()
while(ReceiverThread.is_alive()): # Send EOM char until ReceiverThread stops.
    Status, BytesTransferred = PyD2XX.FT_Write(Device, PyD2XX.FT_Buffer.from_int(EOM), 1)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO WRITE: ABORTING")
        exit()
ReceiverThread.join()

Status = PyD2XX.FT_Close(Receiver)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
    exit()
print("Successfully closed Receiver!")
Status = PyD2XX.FT_Close(Sender)
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO CLOSE DEVICE: ABORTING")
    exit()
print("Successfully closed Sender!")

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES TO ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")