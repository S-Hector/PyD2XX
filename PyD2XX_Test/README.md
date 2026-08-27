# PyD2XX
A Python wrapper for the FTDI D2XX library.
PyD2XX will eventually support Windows, Linux, and MacOS.  
Most D2XX dynamic library variants are included in this package, so you don't need to include them directly in your project!  
\^You don't need and should not have any D2XX .dll, .dylib, or .so file in your script's directory.  
This was designed so the user needs zero ctypes knowledge and not need to import anything besides PyD2XX to interact with D2XX devices. The user should never have to interact with a ctypes object or method.  

## Documentation
None yet! This is still in extremely early development mainly as a test.
While the MAJOR version is 0, this is considered incomplete and not a full translation of the D2XX library to Python.
The API and behavior can change at any time until the MAJOR version is 1.
You should use PyFTDI instead: https://github.com/eblot/pyftdi

## Licensing
The PyD2XX package is licensed under MIT.
The underlying D2XX libraries distributed with this package fall under FTDI's license.
FTDI's License: https://ftdichip.com/driver-licence-terms-details/