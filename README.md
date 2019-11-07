# miptools
This is a medical image processing toolbox for quick preprocessing of CTs and MRIs

Download the latest release ```pip install --upgrade miptools```

Sample usage:
~~~~{.python}
# import library
import miptools as mt

# preprocessing usage
mt.preprocess('./data/test', org='brain', windowing='bsb', resample=True, visualize=True)
~~~~

## CT Preprocessing
Currently supporting CT windowing preprocessing only. Available windows include:
- Simple windowing (```window='simple'```)
- Brain, Subdural, Bone windowing (```window='bs'```)
- Sigmoid windowing (```window='sigmoid'```)

Also supporting resampling of pixel spacing to ```[1, 1]```

## Versions
Python == 3.7.2

## Todo
- [ ] MRI processing
- [ ] gradient windowing for CT
- [X] add saving function
- [ ] add tests
- [ ] add normalization functions

## Author
Chi Nok Enoch Kan/ [@chinokenochkan](https://github.com/chinokenochkan)
