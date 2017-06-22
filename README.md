# Three Match

A bejeweled/candy crush clone.

This game is in development and is being built for a masters project at the University of Birmingham.

Once the game is completed, we will build an AI to play and (hopefully) solve it.

Game rules are detailed below.

[https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Pygame - install via pip

Python 3.x - install via website or your computer's package manager

Once Python 3 is installed, install pygame
```
pip install pygame
```

or on some machines
```
pip3 install pygame
```

### Installing

To install Gem Island clone the repository to your home directory or wherever you prefer, then run main.py with python.

1. Clone repo: 
```
git clone ~/https://github.com/tombrereton/threematch.git
```

2. Run Gem Island
```
cd ~/threematch
python main.py
```
or
```
cd ~/threematch
python3 main.py
```

3. Depending on if you have a HiDPi screen or not, you can change the `HD_SCALE` variable
in `global_variables.py` under the GLOBAL CONSTANSTS section. Recommended values are between and including 1 and 3.

## Running the tests

Pytest is required to run the tests.
 
To install pytest use pip:

1. Install pytest
```
pip install pytest
```

2. Run pytest 

To run the test change into the threematch directory and run pytest.
You need to run pytest as a python command so that it adds the current directory to PYTHONPATH.
```
cd ~/threematch
python -m pytest
```

### Style guide

Refer to the pep-8 website for a consistent style.

[https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

## Deployment

Add additional notes about how to deploy this on a live system

## Authors

* **Thomas Brereton** 
* **Elliott Davies**

## License

The MIT License (MIT)

Copyright (c) 2017 Thomas Brereton Elliott Davies

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

