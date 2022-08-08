#!/bin/python
import gaussianbeam


def main():
    beams = gaussianbeam.analyze('focuspoint.jpg', 2)
    pixelSize = 7.4 #micometers

if __name__ == '__main__':
    main()
