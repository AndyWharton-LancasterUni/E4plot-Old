import e4plot
import e4plot.Common

from e4plot.data     import Utils
from e4plot.fits     import IV    as e4pIV
from e4plot.plots.IV import DummyPlotFunction

##---

def main():
    print("Hello, world.")

    e4plot.Common.DummyCommonFunction()

    Utils.DummyUtilFunction()
    e4pIV.DummyFitFunction()
    DummyPlotFunction()
