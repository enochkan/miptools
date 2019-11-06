# miptools
This is a medical image processing toolbox for quick preprocessing of CTs and MRIs

Download the latest release ```pip install --upgrade miptools```

Sample usage:
~~~~{.python}
# import library
import miptools as mt

mt.preprocess('./data/test', org='brain', windowing='bsb', resample=True, visualize=True):

~~~~

## Versions
Python == 3.7.2

## Todo
- [ ] MRI processing
- [ ] gradient windowing for CT
- [ ] add saving function
- [ ] add tests

## Author
Chi Nok Enoch Kan/ [@chinokenochkan](https://github.com/chinokenochkan)
