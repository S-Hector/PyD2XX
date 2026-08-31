# PyD2XX
A Python wrapper for the FTDI D2XX library.

PyD2XX supports Windows, Linux, and MacOS.  
Most D2XX dynamic library variants are included in this package, so you don't need to include them directly in your project!  
\^You don't need and should not have any D2XX .dll, .dylib, or .so file in your script's directory.  
This was designed so the user needs zero ctypes knowledge and not need to import anything besides PyD2XX to interact with D2XX devices. The user should never have to interact with a ctypes object or method.  

## Install
If you have Python installed simply run a pip install command to install PyD2XX like one of the below examples.
* "pip install PyD2XX"
* "py -m pip install PyD2XX"
* "python -m pip install PyD2XX"
* "python3 -m pip install PyD2XX"
### DO NOT manually copy files from the GitHub repository to your Python install/s.

## Issues, Requests, or Questions
If you encounter issues, have a request, and/or have any questions, email them directly to hector.soto@ftdichip.com. The Issues page will remain closed until PyD2XX release major version is 1.

## PyPi Links
Official Package: https://pypi.org/project/PyD2XX/  
^ This is the official package.  

Test Package: https://test.pypi.org/project/PyD2XX/  
^ This is the test package which will contain early, experimental, and unstable changes.
