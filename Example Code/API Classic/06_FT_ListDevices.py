import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE) # Make PyD2XX not print anything.

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.unbind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO UNBIND FTDI DEVICES FROM ftdi_sio: ABORTING")
        exit()
    print("Unbinded all FTDI devices (VID == 0x0403) from ftdi_sio!")

print("---| Testing FT_ListDevices() Calls |---")
Status, Count = PyD2XX.FT_ListDevices(PyD2XX.NULL, PyD2XX.FT_LIST_NUMBER_ONLY)
print("Device Count: " + str(Count))
Status, SerialNumber = PyD2XX.FT_ListDevices(0, PyD2XX.FT_LIST_BY_INDEX | PyD2XX.FT_OPEN_BY_SERIAL_NUMBER)
print("Device 0 Serial Number: " + str(SerialNumber))
Status, Description = PyD2XX.FT_ListDevices(0, PyD2XX.FT_LIST_BY_INDEX | PyD2XX.FT_OPEN_BY_DESCRIPTION)
print("Device 0 Description: " + str(Description))
Status, SerialNumbers = PyD2XX.FT_ListDevices(Count, PyD2XX.FT_LIST_ALL | PyD2XX.FT_OPEN_BY_SERIAL_NUMBER)
for i in range(Count):
    print("Device " + str(i) + " Serial Number: " + str(SerialNumbers[i]))
Status, Descriptions = PyD2XX.FT_ListDevices(Count, PyD2XX.FT_LIST_ALL | PyD2XX.FT_OPEN_BY_DESCRIPTION)
for i in range(Count):
    print("Device " + str(i) + " Description: " + str(Descriptions[i]))

if(PyD2XX.Platform == "linux"):
    Status = PyD2XX.bind_ftdi_sio(VID = int("0403", 16))
    if(Status != PyD2XX.FT_OK):
        print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO BIND FTDI DEVICES to ftdi_sio: ABORTING")
        exit()
    print("Rebinded all FTDI devices (VID == 0x0403) to ftdi_sio!")