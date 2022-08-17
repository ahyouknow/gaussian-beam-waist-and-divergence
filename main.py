#!/bin/python
import gaussianbeam
import numpy as np


def main():
    pixelSize   = 7.4     # microns/pixel
    wvl         = 532e-3  # microns
    f           = 10e4    # microns
    inch2Micron = 2.54e4  # microns/inch

    difference  = (620/1000 - 52.2/1000) * inch2Micron #microns
    #difference = ( 62/100 * inch2Micron - f ) 
    print(difference)
    print( (620./1000-52.2/1000)*inch2Micron)

    beams = gaussianbeam.analyze('focuspoint.jpg', 2)
    beam0waists= beams[0].waists * pixelSize
    beam1waists= beams[1].waists * pixelSize
    print(beam0waists)
    print("waist of beam 1 - x: {} microns y: {} microns".format(*beam0waists))
    print("waist of beam 2 - x: {} microns y: {} microns".format(*beam1waists))
    print("\n")
    div0 = 2 * wvl/(np.pi*beam0waists)
    div1 = 2 * wvl/(np.pi*beam1waists)
    print("divergence of beam 1 - x: {} milliradians y: {} milliradians".format(*div0*1000))
    print("divergence of beam 2 - x: {} milliradians y: {} milliradians".format(*div1*1000))
    print("\n")
    div0L = (difference / f) * div0
    div1L = (difference / f) * div1
    print("divergence before lens of beam 1 - x: {} milliradians y: {} milliradians".format(*div0L*1000))
    print("divergence before lens of beam 2 - x: {} milliradians y: {} milliradians".format(*div1L*1000))
    print("\n")
    beam0waists0 = 2 * wvl/(np.pi*div0L)
    beam1waists0 = 2 * wvl/(np.pi*div1L)
    print("waist before lens of beam 1 - x: {} microns y: {} microns".format(*beam0waists0))
    print("waist before lens of beam 2 - x: {} microns y: {} microns".format(*beam1waists0))

    #beams[0].showImage()
    #beams[1].showImage()

    import code
    import readline
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()

if __name__ == '__main__':
    main()
