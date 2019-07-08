from setuptools import setup

##---

setup(
    name         = 'e4plot',
    version      = '0.0.9',
    author       = 'Andy Wharton',
    author_email = 'andy.wharton@lancaster.ac.uk',

    packages         = [ 'e4plot',
                         'e4plot.commands',
                         'e4plot.data',
                         'e4plot.fits',
                         'e4plot.plots'],
    install_requires = [ 'numpy',
                         'scipy',
                         'matplotlib'],

    entry_points = {
        'console_scripts' : ['e4plot_plotIV = e4plot.commands.plotIV:main']
    }
)
