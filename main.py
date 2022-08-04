#!/bin/python
from scipy import optimize
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def main():
    pixelSize = 7.4 #micometers
    files = ['focus1.png', 'focus2.png']
    for file in files:
        picArray = getPicArray(file)
        waist = getAvgWaist(picArray)
        waist = waist * pixelSize

        print(waist)

# convert L is since the image is greyscale
def getPicArray(filename):
    return np.asarray(Image.open(filename).convert('L'))


def getAvgWaist(picArray):
    plt.rcParams["figure.autolayout"] = True
    waist0 = 0
    fig, ax = plt.subplots(2)
    for axis in (0, 1):
        flatten = np.sum(picArray, axis=axis)
        x = np.linspace(0, flatten.shape[0], flatten.shape[0])

        popt, _ = optimize.curve_fit(gaussianBeam, x, flatten)
        ax[axis].plot(x, flatten, 'o')
        ax[axis].plot(x, gaussianBeam(x, *popt))
        waist0+=abs(popt[1])
    plt.show()
    return waist0/2


# Formula for intensity of a gaussian beam
# https://en.wikipedia.org/wiki/Gaussian_beam#Mathematical_form
# w(z) becomes w0 at the focus
def gaussianBeam(x, I0, waist0, b, c):
    return I0 * np.exp(-2 * (((x+b)) / waist0)**2 ) + c


if __name__ == '__main__':
    main()
