from scipy import optimize
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class GaussianBeam:
    def __init__(self, array):
        self.array = array
        x, y = array.shape
        self.img = Image.fromarray(self.array)
        self.flatX = np.floor(1/y * np.sum(self.array, axis=0))
        self.flatY = np.floor(1/x * np.sum(self.array, axis=1))
        self.linspace = np.linspace(-x/2, x/2, len(self.flatX))
        self.fitlinspace = np.linspace(-x/2, x/2, 100)
        popt = [ 24.44155195, 3.65223563, 0 ] 
        self.xOpt, _ = optimize.curve_fit(gaussianBeamEquation, self.linspace, self.flatX, p0=popt)
        self.yOpt, _ = optimize.curve_fit(gaussianBeamEquation, self.linspace, self.flatY, p0=popt)
        self.waistX = self.xOpt[1] ##inverseGBeamEqn(*self.xOpt)
        self.waistY = self.yOpt[1] ##inverseGBeamEqn(*self.yOpt)
        self.waists = np.array(self.waistX, self.waistY)

    def showImage(self):
        self.img.show()

    def showGraphs(self):
        fig, ax = plt.subplots(2)
        ax[0].plot(self.linspace, self.flatX, 'o')
        ax[0].plot(self.fitlinspace, gaussianBeamEquation(self.fitlinspace, *self.xOpt))
        ax[1].plot(self.linspace, self.flatY, 'o')
        ax[1].plot(self.fitlinspace, gaussianBeamEquation(self.fitlinspace, *self.yOpt))
        plt.show()

    def calcDivergence(self, wvl):
        self.divergence = 2*wvl / (np.pi*self.waist)
        return self.divergence


def analyze(filename, numOfBeams):
    picarray = np.array(Image.open(filename).convert('L'))
    backgroundNoise = picarray[0][0]
    picarray = picarray - backgroundNoise * np.ones(picarray.shape)
    sortedArray = (-picarray).flatten().argsort()
    indices = np.unravel_index(sortedArray, picarray.shape)
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
    return beams

# Formula for intensity of a gaussian beam
# https://en.wikipedia.org/wiki/Gaussian_beam#Mathematical_form
# w(z) becomes w0 at the focus
def gaussianBeamEquation(x, I0, waist0, b):
    return I0 * np.exp(-2 * (((x+b)) / waist0)**2 )
