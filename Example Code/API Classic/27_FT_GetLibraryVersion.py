import PyD2XX

PyD2XX.SetPrintLevel(PyD2XX.PRINT_NONE)

# ---| Main Code Starts Here |---
Status, LibraryVersion = PyD2XX.FT_GetLibraryVersion()
if(Status != PyD2XX.FT_OK):
    print(PyD2XX.FT_STATUS_STR[Status] + " | FAILED TO GET LIBRARY VERSION: ABORTING")
    exit()
print("Library Version: " + format((LibraryVersion & int("0xFF000000", 16)) >> 24, 'x') + '.' \
    + format((LibraryVersion & int("0x00FF0000", 16)) >> 16, 'x') + '.' \
    + format((LibraryVersion & int("0x0000FF00", 16)) >> 8, 'x') + '.' \
    + format(LibraryVersion & int("0x000000FF", 16), 'x')
    )