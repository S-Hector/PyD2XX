# Created by Hector Soto
# A Python conversion of the FTD2XX library.
# While the MAJOR version is 0, this is considered incomplete
# and not a full translation of the D2XX library to Python.
# The API and behavior can change at any time until the MAJOR version is 1.

print("PyD2XX: PyD2XX is still in EXTREMELY early development!")
print("PyD2XX: You should use PyFTDI instead: https://github.com/eblot/pyftdi")

import ctypes
import ctypes.wintypes
import typing
import platform as _Platform
import subprocess
import shutil
import os

from importlib.resources import files as _files
from sys import platform as Platform

# ---| Python Library Specific Definitions |---

VERSION = "0.0.3"
VERSION_TEST = "0.0.5_legătură_sufletească"

PRINT_NONE =            int("00000", 2) # Print no messages.
PRINT_ERROR_CRITICAL =  int("00001", 2) # Print critical error messages.
PRINT_ERROR_MAJOR =     int("00010", 2) # Print major error messages.
PRINT_ERROR_MINOR =     int("00100", 2) # Print minor error messages.
PRINT_ERROR_ALL =       int("00111", 2) # Print all error messages.

PRINT_INFO_START =      int("01000", 2) # Print informational startup messages.
PRINT_INFO_DEVICE =     int("10000", 2) # Print device information.
PRINT_INFO_ALL =        int("11000", 2) # Print all informational messages.
PRINT_ALL =             int("11111", 2) # Print all messages.

_PrintLevel = PRINT_NONE # What levels of printing are allowed.
_PrintQueue = []

def SetPrintLevel(PrintLevel: int) -> int:
    global _PrintLevel
    global _PrintQueue
    _PrintLevel = PrintLevel
    if _PrintQueue:
        for Message in _PrintQueue:
            _Print(Message[0], Message[1], False)
        _PrintQueue = []
    return FT_OK

def _Print(Message: str, Level: int, Queue: bool):
    if Queue:
        _PrintQueue.append([Message, Level])
    elif(Level & PRINT_ERROR_CRITICAL & _PrintLevel):
        print("PyD2XX - CRITICAL ERROR: " + Message)
    elif(Level & PRINT_ERROR_MAJOR & _PrintLevel):
        print("PyD2XX - MAJOR ERROR: " + Message)
    elif(Level & PRINT_ERROR_MINOR & _PrintLevel):
        print("PyD2XX - MINOR ERROR: " + Message)
    elif(Level & PRINT_INFO_START & _PrintLevel):
        print("PyD2XX - Startup INFO: " + Message)

# Determine OS and type sizes.
if (Platform.startswith("linux")):
    Platform = "linux"
elif (Platform.startswith("win")):
    Platform = "windows"
elif (Platform.startswith("darwin")):
    Platform = "darwin"
elif (Platform.startswith("cygwin")):
    Platform = "windows"
else: # Default to linux if we didn't catch the platform.
    _Print("OS UNKNOWN: Assuming OS is linux.", PRINT_INFO_START, True)
    Platform = "linux"

if Platform == "linux":
    import gc

_IsARM = _Platform.machine().startswith('arm') or _Platform.machine().startswith('aarch64')

if ((Platform == "linux") or (Platform == "darwin")): #Fix type sizes for Linux and macOS
    ctypes.c_ulong = ctypes.c_int32
    ctypes.wintypes.DWORD = ctypes.c_int32

SIZE_UINT = ctypes.sizeof(ctypes.c_uint)
SIZE_ULONG = ctypes.sizeof(ctypes.c_ulong)
SIZE_SHORT = ctypes.sizeof(ctypes.c_short)
SIZE_CHAR = ctypes.sizeof(ctypes.c_char)
SIZE_WCHAR = ctypes.sizeof(ctypes.c_wchar)
SIZE_PTR = ctypes.sizeof(ctypes.c_void_p)
SIZE_DWORD = ctypes.sizeof(ctypes.wintypes.DWORD)

# ---| FTD2XX C/C++ HEADER EQUIVALENT STARTS HERE |---
# THIS IS NOT A FULL EQUIVALENT TO THE FTD2XX HEADER.
# I HAVE TAKEN MY OWN LIBERTIES ON HOW TO REPRESENT STRUCTS.

NULL = ctypes.c_void_p(0)

#FT_STATUS values.
FT_OK = 0
FT_INVALID_HANDLE = 1
FT_DEVICE_NOT_FOUND = 2
FT_DEVICE_NOT_OPENED = 3
FT_IO_ERROR = 4
FT_INSUFFICIENT_RESOURCES = 5
FT_INVALID_PARAMETER = 6
FT_INVALID_BAUD_RATE = 7
FT_DEVICE_NOT_OPENED_FOR_ERASE = 8
FT_DEVICE_NOT_OPENED_FOR_WRITE = 9
FT_FAILED_TO_WRITE_DEVICE = 10
FT_EEPROM_READ_FAILED = 11
FT_EEPROM_WRITE_FAILED = 12
FT_EEPROM_ERASE_FAILED = 13
FT_EEPROM_NOT_PRESENT = 14
FT_EEPROM_NOT_PROGRAMMED = 15
FT_INVALID_ARGS = 16
FT_NOT_SUPPORTED = 17
FT_OTHER_ERROR = 18
FT_DEVICE_LIST_NOT_READY = 19

# Describe dictionaries for easier error code conversion.
FT_STATUS_STR = {
    FT_OK: "FT_OK",
    FT_INVALID_HANDLE: "FT_INVALID_HANDLE",
    FT_DEVICE_NOT_FOUND: "FT_DEVICE_NOT_FOUND",
    FT_DEVICE_NOT_OPENED: "FT_DEVICE_NOT_OPENED",
    FT_IO_ERROR: "FT_IO_ERROR",
    FT_INSUFFICIENT_RESOURCES: "FT_INSUFFICIENT_RESOURCES",
    FT_INVALID_PARAMETER: "FT_INVALID_PARAMETER",
    FT_INVALID_BAUD_RATE: "FT_INVALID_BAUD_RATE",
    FT_DEVICE_NOT_OPENED_FOR_ERASE: "FT_DEVICE_NOT_OPENED_FOR_ERASE",
    FT_DEVICE_NOT_OPENED_FOR_WRITE: "FT_DEVICE_NOT_OPENED_FOR_WRITE",
    FT_FAILED_TO_WRITE_DEVICE: "FT_FAILED_TO_WRITE_DEVICE",
    FT_EEPROM_READ_FAILED: "FT_EEPROM_READ_FAILED",
    FT_EEPROM_WRITE_FAILED: "FT_EEPROM_WRITE_FAILED",
    FT_EEPROM_ERASE_FAILED: "FT_EEPROM_ERASE_FAILED",
    FT_EEPROM_NOT_PRESENT: "FT_EEPROM_NOT_PRESENT",
    FT_EEPROM_NOT_PROGRAMMED: "FT_EEPROM_NOT_PROGRAMMED",
    FT_INVALID_ARGS: "FT_INVALID_ARGS",
    FT_NOT_SUPPORTED: "FT_NOT_SUPPORTED",
    FT_OTHER_ERROR: "FT_OTHER_ERROR"
}
FT_STATUS = {v: k for k, v in FT_STATUS_STR.items()}

FT_DEVICE_BM = 0
FT_DEVICE_AM = 1
FT_DEVICE_100AX = 2
FT_DEVICE_UNKNOWN = 3
FT_DEVICE_2232C = 4
FT_DEVICE_232R = 5
FT_DEVICE_2232H = 6
FT_DEVICE_4232H = 7
FT_DEVICE_232H = 8
FT_DEVICE_X_SERIES = 9
FT_DEVICE_4222H_0 = 10
FT_DEVICE_4222H_1_2 = 11
FT_DEVICE_4222H_3 = 12
FT_DEVICE_4222_PROG = 13
FT_DEVICE_900 = 14
FT_DEVICE_930 = 15
FT_DEVICE_UMFTPD3A = 16
FT_DEVICE_2233HP = 17
FT_DEVICE_4233HP = 18
FT_DEVICE_2232HP = 19
FT_DEVICE_4232HP = 20
FT_DEVICE_233HP = 21
FT_DEVICE_232HP = 22
FT_DEVICE_2232HA = 23
FT_DEVICE_4232HA = 24
FT_DEVICE_232RN = 25
FT_DEVICE_2233HPN = 26
FT_DEVICE_4233HPN = 27
FT_DEVICE_2232HPN = 28
FT_DEVICE_4232HPN = 29
FT_DEVICE_233HPN = 30
FT_DEVICE_232HPN = 31
FT_DEVICE_BM_A = 32

FT_DEVICE_STR = {
    FT_DEVICE_BM: "FT_DEVICE_BM",
	FT_DEVICE_AM: "FT_DEVICE_AM",
	FT_DEVICE_100AX: "FT_DEVICE_100AX",
	FT_DEVICE_UNKNOWN: "FT_DEVICE_UNKNOWN",
	FT_DEVICE_2232C: "FT_DEVICE_2232C",
	FT_DEVICE_232R: "FT_DEVICE_232R",
	FT_DEVICE_2232H: "FT_DEVICE_2232H",
	FT_DEVICE_4232H: "FT_DEVICE_4232H",
	FT_DEVICE_232H: "FT_DEVICE_232H",
	FT_DEVICE_X_SERIES: "FT_DEVICE_X_SERIES",
	FT_DEVICE_4222H_0: "FT_DEVICE_4222H_0",
	FT_DEVICE_4222H_1_2: "FT_DEVICE_4222H_1_2",
	FT_DEVICE_4222H_3: "FT_DEVICE_4222H_3",
	FT_DEVICE_4222_PROG: "FT_DEVICE_4222_PROG",
	FT_DEVICE_900: "FT_DEVICE_900",
	FT_DEVICE_930: "FT_DEVICE_930",
	FT_DEVICE_UMFTPD3A: "FT_DEVICE_UMFTPD3A",
	FT_DEVICE_2233HP: "FT_DEVICE_2233HP",
	FT_DEVICE_4233HP: "FT_DEVICE_4233HP",
	FT_DEVICE_2232HP: "FT_DEVICE_2232HP",
	FT_DEVICE_4232HP: "FT_DEVICE_4232HP",
	FT_DEVICE_233HP: "FT_DEVICE_233HP",
	FT_DEVICE_232HP: "FT_DEVICE_232HP",
	FT_DEVICE_2232HA: "FT_DEVICE_2232HA",
	FT_DEVICE_4232HA: "FT_DEVICE_4232HA",
	FT_DEVICE_232RN: "FT_DEVICE_232RN",
	FT_DEVICE_2233HPN: "FT_DEVICE_2233HPN",
	FT_DEVICE_4233HPN: "FT_DEVICE_4233HPN",
	FT_DEVICE_2232HPN: "FT_DEVICE_2232HPN",
	FT_DEVICE_4232HPN: "FT_DEVICE_4232HPN",
	FT_DEVICE_233HPN: "FT_DEVICE_233HPN",
	FT_DEVICE_232HPN: "FT_DEVICE_232HPN",
	FT_DEVICE_BM_A: "FT_DEVICE_BM_A"
}
FT_DEVICE = {v: k for k, v in FT_DEVICE_STR.items()}

FT_BITMODE_RESET = int("0x00", 16)
FT_BITMODE_ASYNC_BITBANG = int("0x01", 16)
FT_BITMODE_MPSSE = int("0x02", 16)
FT_BITMODE_SYNC_BITBANG = int("0x04", 16)
FT_BITMODE_MCU_HOST = int("0x08", 16)
FT_BITMODE_FAST_SERIAL = int("0x10", 16)
FT_BITMODE_CBUS_BITBANG = int("0x20", 16)
FT_BITMODE_SYNC_FIFO = int("0x40", 16)

FT_FLAGS_OPENED = 1
FT_FLAGS_HISPEED = 2

FT_PURGE_RX	= 1
FT_PURGE_TX = 2

class FT_Buffer:
    def __init__(self, Size: int = None):
        if(isinstance(Size, int)):
            self._RawAddress = ctypes.c_buffer(init=0, size=Size)
            self._Length = Size
        else:
            self._RawAddress = "FT_OTHER_ERROR"
            self._Length = 0
    def from_int(Integer: int):
        NewBuffer = FT_Buffer()
        if(isinstance(Integer, int)):
            NewBuffer._RawAddress = ctypes.c_buffer(Integer.to_bytes(SIZE_UINT, "little"), SIZE_UINT)
            NewBuffer._Length = SIZE_UINT
        else:
            _Print("FT_Buffer(int), not given an int!", PRINT_ERROR_MINOR, False)
        return NewBuffer
    def from_str(String: str):
        NewBuffer = FT_Buffer()
        if(isinstance(String, str)):
            NewBuffer._Length = len(String) + 1
            NewBuffer._RawAddress = ctypes.create_string_buffer(init=String.encode("ascii"))
        else:
            _Print("FT_Buffer(str), not given a str!", PRINT_ERROR_MINOR, False)
        return NewBuffer
    def from_bytearray(ByteArray: bytearray):
        NewBuffer = FT_Buffer()
        if(isinstance(ByteArray, bytearray)):
            NewBuffer._Length = len(ByteArray)
            NewBuffer._RawAddress = ctypes.c_buffer(init=bytes(ByteArray), size=NewBuffer._Length)
        else:
            _Print("FT_Buffer(bytearray), not given a bytearray!", PRINT_ERROR_MINOR, False)
        return NewBuffer
    def from_bytes(Bytes: bytes):
        NewBuffer = FT_Buffer()
        if(isinstance(Bytes, bytes)):
            NewBuffer._Length = len(Bytes)
            NewBuffer._RawAddress = ctypes.c_buffer(init=Bytes, size=NewBuffer._Length)
        else:
            _Print("FT_Buffer(bytes), not given bytes!", PRINT_ERROR_MINOR, False)
        return NewBuffer
    def Value(self) -> bytearray:
        if isinstance(self._RawAddress, str):
            return self._RawAddress.encode("ascii")
        return bytearray(self._RawAddress)

class _FT_DEVICE_LIST_INFO_NODE(ctypes.Structure):
    _fields_ = [
        ("Flags", ctypes.c_int32), #ULONG for Windows is 4 bytes. Linux library follows same byte alignment against normal convention.
        ("Type", ctypes.c_int32),
        ("ID", ctypes.c_int32),
        ("LocID", ctypes.c_int32),
        ("SerialNumber", ctypes.c_char * 16),
        ("Description", ctypes.c_char * 64),
        ("Handle", ctypes.c_void_p)
    ]
class FT_Device:
    _Handle = "FT_OTHER_ERROR"
    Handle = "FT_OTHER_ERROR"
    Flags = 0
    Type = 0
    ID = 0
    LocID = 0
    SerialNumber = ""
    Description = ""

def _CreateDevice():
    NewDevice = FT_Device()
    NewDevice._Handle = ctypes.c_void_p(0)
    NewDevice.Flags = 0
    NewDevice.Type = 0
    NewDevice.ID = 0
    NewDevice.LocID = 0
    NewDevice.SerialNumber = ""
    NewDevice.Description = ""
    return NewDevice

# ---| END OF EQUIVALENT HEADER PORTION |---

# ---| LIBRARY INCLUSION PART |---
_Python64 = (ctypes.sizeof(ctypes.c_void_p) == 8) # True if 64-bit version of Python is running.

# ---| Try to Load Dynamic Library |---
_LibraryFile = ""
_LibraryFile += "FTD2XX" if (Platform=="windows") else "libftd2xx"
_LibraryFile += ("_ARM" if (_IsARM and (Platform!="darwin")) else "")
_LibraryFile += ("_32" if not(_Python64) else "")
_LibraryFile += ".dll" if (Platform=="windows") else (".dylib" if (Platform=="darwin") else ".so")
_DLL_Path = str(_files("PyD2XX").joinpath(_LibraryFile))
try:
    if(Platform == "windows"):
        _DLL = ctypes.windll.LoadLibrary(_DLL_Path) # Check if dll exists in same directory as executable.
    else:
        _DLL = ctypes.cdll.LoadLibrary(_DLL_Path) # Check if dll exists in same directory as executable.
except:
    print("PyD3XX ERROR: Did not find '" + _DLL_Path + "', EXITING.")
    exit()
_Print("Successfully loaded D2XX: '" + _LibraryFile + "'", PRINT_INFO_START, True)

# ---| FTD2XX Python Function Implementations |---

def FT_CreateDeviceInfoList() -> tuple[int, int]:
    DeviceCount = ctypes.c_ulong(0)
    Status = _DLL.FT_CreateDeviceInfoList(ctypes.byref(DeviceCount))
    return Status, DeviceCount.value # Device count is converted to a Python int.

def FT_GetDeviceInfoList(DeviceCount: int) -> tuple[int, list[FT_Device]] | tuple[int, str]:
    Status = FT_OK
    DeviceCount = ctypes.c_ulong(DeviceCount)
    if(DeviceCount.value < 1):
        _Print(FT_STATUS_STR[Status] + " | ERROR: DeviceCount IS LESS THAN 1.", PRINT_ERROR_MINOR, False)
        return Status, "FT_OTHER_ERROR"
    DeviceList = (_FT_DEVICE_LIST_INFO_NODE * DeviceCount.value)()
    Status = _DLL.FT_GetDeviceInfoList(ctypes.byref(DeviceList), ctypes.byref(DeviceCount))
    if(Status != FT_OK):
        _Print(FT_STATUS_STR[Status] + " | ERROR: FAILED TO GET DEVICE INFO LIST.", PRINT_ERROR_MAJOR, False)
        return Status, "FT_OTHER_ERROR"
    ReturnDeviceList = []
    for i in range(DeviceCount.value):
        ReturnDeviceList.append(_CreateDevice())
        ReturnDeviceList[i].Handle = "FT_OTHER_ERROR"
        ReturnDeviceList[i].Flags = DeviceList[i].Flags
        ReturnDeviceList[i].Type = DeviceList[i].Type
        ReturnDeviceList[i].ID = DeviceList[i].ID
        ReturnDeviceList[i].LocID = DeviceList[i].LocID
        ReturnDeviceList[i].SerialNumber = DeviceList[i].SerialNumber.decode("utf-8")
        ReturnDeviceList[i].Description = DeviceList[i].Description.decode("utf-8")
        ReturnDeviceList[i].Handle = DeviceList[i].Handle.value if (DeviceList[i].Handle is not None) else 0
    return Status, ReturnDeviceList

def FT_GetDeviceInfoDetail(Index: int) -> tuple[int, FT_Device] | tuple[int, str]:
    Status = FT_OK
    Index = ctypes.c_ulong(Index)
    Device = _FT_DEVICE_LIST_INFO_NODE()
    Status = _DLL.FT_GetDeviceInfoDetail(Index, 
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.Flags.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.Type.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.ID.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.LocID.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.SerialNumber.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.Description.offset,
                                         ctypes.addressof(Device) + _FT_DEVICE_LIST_INFO_NODE.Handle.offset)
    if(Status != FT_OK):
        _Print(FT_STATUS_STR[Status] + " | ERROR: FAILED TO GET DEVICE INFO DETAIL.", PRINT_ERROR_MAJOR, False)
        return Status, "FT_OTHER_ERROR"
    ReturnDevice = _CreateDevice()
    ReturnDevice.Handle = "FT_OTHER_ERROR"
    ReturnDevice.Flags = Device.Flags
    ReturnDevice.Type = Device.Type
    ReturnDevice.ID = Device.ID
    ReturnDevice.LocID = Device.LocID
    ReturnDevice.SerialNumber = Device.SerialNumber.decode("utf-8")
    ReturnDevice.Description = Device.Description.decode("utf-8")
    ReturnDevice.Handle = Device.Handle.value if (Device.Handle is not None) else 0
    return Status, ReturnDevice

def FT_Open(Index: int, Device: FT_Device) -> int:
    Status = FT_OTHER_ERROR
    if(not(isinstance(Device, FT_Device))):
        _Print("FT_Open(), did not get an FT_Device!", PRINT_ERROR_MAJOR, False)
    elif(not(isinstance(Device._Handle, ctypes.c_void_p))):
        _Print("FT_Open(), got an uninitialized or broken FT_Device object!", PRINT_ERROR_MAJOR, False)
    else:
        Status = _DLL.FT_Open(ctypes.c_int(Index), ctypes.byref(Device._Handle))
        Device.Handle = Device._Handle.value
    return Status

def FT_Close(Device: FT_Device) -> int:
    Status = FT_OTHER_ERROR
    if(not(isinstance(Device, FT_Device))):
        _Print("FT_Close(), did not get an FT_Device!", PRINT_ERROR_MAJOR, False)
    elif(not(isinstance(Device._Handle, ctypes.c_void_p))):
        _Print("FT_Close(), got an uninitialized or broken FT_Device object!", PRINT_ERROR_MAJOR, False)
    else:
        Status = _DLL.FT_Close(Device._Handle)
        Device.Handle = "FT_OTHER_ERROR"
    return Status

def FT_SetBitMode(Device: FT_Device, Mask: int, Mode: int) -> int:
    Status = FT_OTHER_ERROR
    Status = _DLL.FT_SetBitMode(Device._Handle, ctypes.c_char(Mask), ctypes.c_char(Mode))
    return Status

def FT_Write(Device: FT_Device, Buffer: FT_Buffer, BufferLength: int) -> tuple[int, int]:
    Status = FT_OTHER_ERROR
    if(isinstance(Buffer._RawAddress, FT_Buffer)):
        _Print("FT_Write(), was not given expected FT_Buffer.", PRINT_ERROR_MAJOR, False)
        return Status, 0
    BytesTransferred = ctypes.wintypes.DWORD(0)
    Status = _DLL.FT_Write(Device._Handle,
                            ctypes.byref(Buffer._RawAddress),
                            BufferLength,
                            ctypes.byref(BytesTransferred))
    return Status, BytesTransferred.value

def FT_Read(Device: FT_Device, BufferLength: int) -> tuple[int, FT_Buffer, int]:
    Status = FT_OTHER_ERROR
    Buffer = FT_Buffer()
    Buffer._RawAddress = ctypes.c_buffer(BufferLength)
    Buffer._Length = BufferLength
    BytesTransferred = ctypes.c_ulong(0)
    Status = _DLL.FT_Read(Device._Handle,
                            ctypes.byref(Buffer._RawAddress),
                            BufferLength,
                            ctypes.byref(BytesTransferred))
    return Status, Buffer, BytesTransferred.value

def FT_Purge(Device: FT_Device, Mask: int) -> int:
    Status = FT_OTHER_ERROR
    Status = _DLL.FT_Purge(Device._Handle, ctypes.c_char(Mask))
    return Status
    
# ---| Python Specific Functions |---

def _linux_find_usb_matches(Directory: str, VID: int | None=None, PID: int | None=None, Manufacturer: str | None=None, Description: str | None=None, SerialNumber: str | None=None, FindAll: bool=True) -> list[str]:
    Status = FT_OK
    DeviceListString = subprocess.Popen(["ls", Directory], stdout=subprocess.PIPE).stdout.read()
    DeviceListString = DeviceListString.decode("utf-8").split()
    DeviceList = []
    for Device in DeviceListString:
        if((Device != "bind") and (Device != "unbind") and (Device != "module") and (Device != "uevent") and ("usb" not in Device)):
            DeviceList.append(Device)
    DeviceListLength = len(DeviceList)
    Matches = []
    for i in range(DeviceListLength):
        VendorID = open(Directory + DeviceList[i] + "/../idVendor", "r").read().strip()
        if(isinstance(VID, int)):
            if(VID != int(VendorID, 16)):
                continue # Device does not match, skip.
        ProductID = open(Directory + DeviceList[i] + "/../idProduct", "r").read().strip()
        if(isinstance(PID, int)):
            if(PID != int(ProductID, 16)):
                continue # Device does not match, skip.
        Man = open(Directory + DeviceList[i] + "/../manufacturer", "r").read().strip()
        if(isinstance(Manufacturer, str)):
            if(Man != Manufacturer):
                continue # Device does not match, skip.
        Des = open(Directory + DeviceList[i] + "/../product", "r").read().strip()
        if(isinstance(Description, str)):
            if(Des != Description):
                continue # Device does not match, skip.
        Ser = open(Directory + DeviceList[i] + "/../serial", "r").read().strip()
        if(isinstance(SerialNumber, str)):
            if(Ser != SerialNumber):
                continue # Device does not match, skip.
        Matches.append(DeviceList[i])
        if not FindAll: # Only find first device match. Default is find all matching devices.
            break
    return Matches

def unbind_ftdi_sio(VID: int | None=None, PID: int | None=None, Manufacturer: str | None=None, Description: str | None=None, SerialNumber: str | None=None, UnbindAll: bool=True, RequestGUI: bool=True) -> int:
    if(Platform != "linux"):
        return FT_NOT_SUPPORTED
    ftdi_sio_dir = "/sys/bus/usb/drivers/ftdi_sio/"
    if not(os.path.isdir(ftdi_sio_dir)): # Kernel module is not installed or not active... so automatic success!
        return FT_OK
    Status = FT_OK
    Matches = _linux_find_usb_matches(ftdi_sio_dir, VID, PID, Manufacturer, Description, SerialNumber, UnbindAll)
    if(len(Matches) == 0):
        return FT_DEVICE_NOT_FOUND
    if (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and RequestGUI:
        if shutil.which("pkexec") is not None: # Launch GUI prompt for admin access to unbind device from driver.
            UnbindProcess = subprocess.Popen(["pkexec", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
            pass # Unbind graphically
        else:
            UnbindProcess = subprocess.Popen(["sudo", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
            pass #Unbind terminally
    else:
        UnbindProcess = subprocess.Popen(["sudo", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
        pass #Unbind terminally
    for Device in Matches:
        #print("Unbinded: " + Device)
        UnbindProcess.stdin.write("echo -n " + Device + " > " + ftdi_sio_dir + "unbind\n")
        UnbindProcess.stdin.flush()
    UnbindProcess.stdin.close()
    UnbindProcess.wait()
    return Status

def bind_ftdi_sio(VID: int | None=None, PID: int | None=None, Manufacturer: str | None=None, Description: str | None=None, SerialNumber: str | None=None, BindAll: bool=True, RequestGUI: bool=True) -> int:
    if(Platform != "linux"):
        return FT_NOT_SUPPORTED
    ftdi_sio_dir = "/sys/bus/usb/drivers/ftdi_sio/"
    if not(os.path.isdir(ftdi_sio_dir)): # Kernel module is not installed or not active... so automatic failure!
        return FT_NOT_SUPPORTED
    Status = FT_OK
    Matches = _linux_find_usb_matches("/sys/bus/usb/devices/", VID, PID, Manufacturer, Description, SerialNumber, BindAll)
    if(len(Matches) == 0):
        return FT_DEVICE_NOT_FOUND
    if (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and RequestGUI:
        if shutil.which("pkexec") is not None: # Launch GUI prompt for admin access to bind device to driver.
            BindProcess = subprocess.Popen(["pkexec", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
            pass # Unbind graphically
        else:
            BindProcess = subprocess.Popen(["sudo", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
            pass #Unbind terminally
    else:
        BindProcess = subprocess.Popen(["sudo", "sh"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=None, text=True)
        pass #Unbind terminally
    for Device in Matches:
        #print("Binded: " + Device)
        BindProcess.stdin.write("echo -n " + Device + " > " + ftdi_sio_dir + "bind\n")
        BindProcess.stdin.flush()
    BindProcess.stdin.close()
    BindProcess.wait()
    return Status