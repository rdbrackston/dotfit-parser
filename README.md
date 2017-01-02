# dotfit-parser
Project to parse and analyse .fit activity files.

The project is written python 3 and makes use of the Ant+ fit-SDK to perform the translation from .fit to .csv file format. The main source code is currently all within the fit_parser file, including utilities and an "activity" class definition.

Planned future extensions include:

- Altitude correction. A tool to correct the altitude of the raw GPS data using the latitude and longitude and the NASA SRTM altitude data.

- Power estimation. A crude power estimation based upon speed, gradient etc. This will likely be inaccurate without measurement of dynamic head, however it may be possible to correct this using heart rate data and a calibration.

- Training analyser. A tool to assess the intensity of a ride or training session using the heart rate data.
