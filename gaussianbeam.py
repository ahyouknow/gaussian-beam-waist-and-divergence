from scipy import optimize
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class GaussianBeam:
    def __init__(self, array):
        self.array = array
        self.img = Image.fromarray(self.array)
        self.flatX = np.sum(self.array, axis=0)
        self.flatY = np.sum(self.array, axis=1)
        self.linspace = np.linspace(0, self.flatX.shape[0], self.flatX.shape[0])
        self.xOpt, _ = optimize.curve_fit(gaussianBeamEquation, self.linspace, self.flatX)
        self.yOpt, _ = optimize.curve_fit(gaussianBeamEquation, self.linspace, self.flatY)
        self.waistX  = self.xOpt[1]
        self.waistY  = self.yOpt[1]
        self.waist  = (self.waistY + self.waistX) / 2

    def showImage(self):
        self.img.show()

    def showGraphs(self):
        fig, ax = plt.subplots(2)
        ax[0].plot(self.linspace, self.flatX, 'o')
        ax[0].plot(self.linspace, gaussianBeamEquation(self.linspace, *self.xOpt))
        ax[1].plot(self.linspace, self.flatY, 'o')
        ax[1].plot(self.linspace, gaussianBeamEquation(self.linspace, *self.yOpt))
        plt.show()


def analyze(filename, numOfBeams):
    picarray = np.array(Image.open(filename).convert('L'))
    test = (-picarray).flatten().argsort()
    indices = np.unravel_index(test, picarray.shape)
    maxIndex = np.array((indices[0][0],indices[1][0]))
    centerindices = np.array([maxIndex])
    n = 1
    while (len(centerindices) != numOfBeams):
        index = np.array((indices[0][n], indices[1][n]))
        if all([x or y for x, y in abs(np.tile(index, (len(centerindices), 1)) - centerindices) > 50]):
            centerindices = np.vstack([centerindices, index])
        n+=1
    beams = []
    for x, y in centerindices:
        beamArray = picarray[x - 10:x + 10, y - 10:y + 10]
        beam = GaussianBeam(beamArray)
        beams.append(beam)
    print(beams[0].waist)
    print(beams[0].waistX)
    print(beams[0].waistY)
    print('\n')
    beams[0].showGraphs()
    print(beams[1].waist)
    beams[1].showGraphs()

# Formula for intensity of a gaussian beam
# https://en.wikipedia.org/wiki/Gaussian_beam#Mathematical_form
# w(z) becomes w0 at the focus
def gaussianBeamEquation(x, I0, waist0, b, c):
    return I0 * np.exp(-2 * (((x+b)) / waist0)**2 ) + c
