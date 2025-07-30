This repository contains files for thre diferent projects:

## Online calculations
The goal of the project is to perform calculations on the data coming from the baffle to asses its status.
FFt.py aggregates 2048 frames fo data, claulates the fft and stores the result. To run a directory named Output is needed to store the results, when pressing Ctrl + C the program will stop and save the data.

## Flicker noise
The goal of the project is to caracterize the fliker noise of the resistors on the baffle.

flicker-noise-tests.ipynb is a jupyter notebool containing various functions to plot the data from the pedestals.

## PD calibration
The goal of the project is to calculate the califration coefficien in therms of W/ADC, to do so we have two setups.

In setup 1 we have a reference photodiode and a calibrated power meter, calibration-coefficient-setup-1.ipynb contains functions to calculate and plot the coeficient in therms of W/V.
calibration-coeficient-setup-1-temperature.ipynb contains fucntion to plot the data as a function of temperature or relative humidity.

In setup 2 we have the same reference photodiode and the baffle photodiodes.
calibraton-coeficient-setup-2.ipynb contains functions to calulate and plot the coefficient in therms of V/ADC and a finction to calculate the coeficient in therms of W/ADC given the coeficients from  setups 1 and 2.
