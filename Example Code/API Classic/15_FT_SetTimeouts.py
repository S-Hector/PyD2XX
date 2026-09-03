import PyD2XX
import time

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

READ_TIMEOUT = 3000 # 3 Seconds until FT_Read times out.
READ_SIZE = 32768 # Put a byte length request you expect to fail/time out.
WRITE_TIMEOUT = 4000 # 4 Seconds until FT_Write times out.
WRITE_SIZE = 32768 # Put a byte length request you expect to fail/time out.
WRITE_TRY = 1 # How many writes to try to get a timeout response. It is not possible to get a timeout response.
# ^ Writes do not timeout. If too many write requests are issued without the chip responding
# to them (leaving the requests unfulfilled), you'll get an FT_IO_ERROR.
# E.g. FT_Write() has no timeout behavior and FT_SetTimeouts() does not affect FT_Write().

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
    print("  Device is free! Will attempt to set timeouts!")
    Status = PyD2XX.FT_Open(0, Device)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO OPEN DEVICE: ABORTING")
        exit()
    print("  Successfully opened!")
    Status = PyD2XX.FT_SetTimeouts(Device, READ_TIMEOUT, WRITE_TIMEOUT)
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO SET TIME OUTS: ABORTING")
        exit()
    print("  Successfully set read timeout to " + str(READ_TIMEOUT / 1000) + " seconds.")
    print("  Successfully set write timeout to " + str(WRITE_TIMEOUT / 1000) + " seconds.")
    StartTime = time.perf_counter() # Get start time of second.
    Status, DummyBuffer, BytesTransferred = PyD2XX.FT_Read(Device, READ_SIZE)
    if(BytesTransferred == READ_SIZE):
        print(PyD2XX.FT_STATUS_STR[Status] + " | READ FAILED TO TIME OUT: ABORTING")
        exit()
    ElapsedTime = time.perf_counter() - StartTime
    print("  FT_Read() read " + str(BytesTransferred) + " bytes before failing after " + "{:.2f}".format(ElapsedTime) + " seconds!")
    WriteTimeout = False
    for i in range(WRITE_TRY):
        StartTime = time.perf_counter() # Get start time of second.
        Status, BytesTransferred = PyD2XX.FT_Write(Device, PyD2XX.FT_Buffer(WRITE_SIZE) , WRITE_SIZE)
        if(BytesTransferred == WRITE_SIZE):
            print("  " + PyD2XX.FT_STATUS_STR[Status] + " | WRITE SUCCEEDED.")
        else:
            WriteTimeout = True
            break
    if(WriteTimeout):
        ElapsedTime = time.perf_counter() - StartTime
        print("  " + PyD2XX.FT_STATUS_STR[Status]  + " | FT_Write() wrote " + str(BytesTransferred) + " bytes before timing out after " + "{:.2f}".format(ElapsedTime) + " seconds!")
    else:
        print("  " + PyD2XX.FT_STATUS_STR[Status] + " | NO WRITES FAILED TO TIME OUT.")
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