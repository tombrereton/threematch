# Three Match

A bejeweled/candy crush clone. The aim is to free the medals under the ice by match 3 or more gems of the 
same type on top of the ice. Matching on top of ice removes it. Once all medals are freed you win the game.

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
in `global_variables.py` under the GUI variables section. Recommended values are between and including 1 and 3.

## Game Rules

* 6 gem types (colours).
* 3 bonus types (star, cross, diamond)
* Star bonus removes all gems of the star gem's type
* The cross bonus removes all gems in the row/column. If the match is horizontal, the row is removed. Vertical 
removes the column.
* The diamond bonus removes the 9 surrounding gems of the diamond gem.
* If a match generates multiple bonuses only one is generated following the hierarchy: star, cross, bonus.
* If a bonus gem removes another bonus gem, it also performs its bonus action. This is done recursively.

1. 3 or more gems in a succession of the same type is a match.
2. 4 gems in a succession earns you a cross bonus.
3. 5 gems in a succession earns you a star bonus.
4. An intersection of a vertical and horizontal match earns you a diamond bonus.

## Running tests

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

