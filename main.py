#!/bin/python
import gaussianbeam
import numpy as np


def main():
    pixelSize = 7.4 #microns
    wvl = 532e-3    #microns
    inch2Micron = 2.54e4 #microns/inch
    difference = (62/100 - 22/1000) * inch2Micron #microns
    print(difference)
    print( (620./1000-52.2/1000)*inch2Micron)
    f = 10e4 # microns

    beams = gaussianbeam.analyze('focuspointOld.jpg', 2)
    beam0waists= beams[0].waists * pixelSize
    beam1waists= beams[1].waists * pixelSize
    print("waist of beam 1 - x: {} microns y: {} microns".format(*beam0waists))
    print("waist of beam 2 - x: {} microns y: {} microns".format(*beam1waists))
    print("\n")
    div0 = 2*wvl/(np.pi*beam0waists)
    div1 = 2*wvl/(np.pi*beam1waists)
    print("divergence of beam 1 - x: {} radians y: {} radians".format(*div0))
    print("divergence of beam 2 - x: {} radians y: {} radians".format(*div1))
    print("\n")
    div0L = difference / f * div0
    div1L = difference / f * div1
    print("divergence before lens of beam 1 - x: {} radians y: {} radians".format(*div0L))
    print("divergence before lens of beam 2 - x: {} radians y: {} radians".format(*div1L))
    print("\n")
    beam0waists0 = difference / f * div0
    beam1waists0 = difference / f * div1
    print("waist before lens of beam 1 - x: {} microns y: {} microns".format(beam0waist0))
    print("waist before lens of beam 2 - x: {} microns y: {} microns".format(beam1waist0))

    beams[0].showImage()
    beams[1].showImage()

    import code
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()

if __name__ == '__main__':
    main()
