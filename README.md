# Three Match

The aim of Gem Island is to match three or more gems of the same type over the ice to free the medals underneath. 
Each game begins by generating gems in a 9x9 grid each of which is randomly one of 6 different types. 
Additionally, opaque ice covers the bottom five row of the game to hide the medals, which are randomly placed 
underneath. The Figure below illustrates a beginning state of the game. A legal move is made by swapping two adjacent 
gems which results in at least one match.

To account for the hidden information of the medals, we used a simulator to predict state **s** given observations **o**
. To handle the stochastic elements of the gem generation we used a flat UCT MCTS, which stores the actions only from the root state rather than building a tree. 

<p align="center">
  <img src="https://i.imgur.com/2j0mG6i.png">
</p>

## Getting Started

### Prerequisites

- Python 3.6 (may work with 3.x)
- Pip
- virtualenv (should come with Python 3, if not pip install it)
- h5py==2.7.1
- Keras==2.0.8
- numpy==1.13.1
- pygame==1.9.3
- PyYAML==3.12
- scipy==0.19.1
- six==1.10.0
- Theano==0.9.0

Install Python 3.6 via the URL below or your package manager (e.g. apt-get or brew).

[https://www.python.org/downloads/release/python-362/](https://www.python.org/downloads/release/python-362/)

To install prerequisites change into the directory and first create a python virtual environment to avoid any 
dependency conflicts. Then install the dependencies via the requirements file. The commands for this are outlined below.

```
cd ~/
git clone https://github.com/tombrereton/threematch.git
cd ~/threematch
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

or on some machines
```
pip3 install -r requirements.txt
```

### Running the Game and AI

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

4. Run Gem Island with Monte Carlo Tree Search and Heuristic Based Evaluation Function
```
cd ~/threematch
python main_mcts.py
```

For help with inputs to change the MCTS parameters type:
```
cd ~/threematch
python main_mcts.pt -h
```

5. Run Gem Island with Monte Carlo Tree Search and Value Network
```
cd ~/threematch
python main_mcts_DL.py
```

6. Depending on if you have a HiDPi screen or not, you can change the `HD_SCALE` variable
in `global_variables.py` under the GUI variables section. Recommended values are between and including 1 and 3.

## Game Rules

#### Gem Types
* 6 gem types (colours).
* 3 bonus types (star, cross, diamond)

#### Bonus Actions
* Star bonus removes all gems of the star gem's type
* The cross bonus removes all gems in the row/column. If the match is horizontal, the row is removed. Vertical 
removes the column.
* The diamond bonus removes the 9 surrounding gems of the diamond gem.

#### Earning Bonuses
* If a bonus gem removes another bonus gem, it also performs its bonus action. This is done recursively.
* 3 or more gems in a succession of the same type is a match.
* 4 gems in a succession earns you a cross bonus.
* 5 gems in a succession earns you a star bonus.
* An intersection of a vertical and horizontal match earns you a diamond bonus.
* If a match generates multiple bonuses only one is generated following the hierarchy: star, cross, diamond.

## Running tests

Pytest is required to run the tests and it is included in the requirements file.

2. Run pytest 

To run the test change into the threematch directory and run pytest.
You need to run pytest as a python command so that it adds the current directory to PYTHONPATH.
```
cd ~/threematch
pytest
```

## Style guide

Refer to the pep-8 website for a consistent style.

[https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

## Authors

* **Thomas Brereton** 
* **Elliott Davies**

## Acknowledgements

* Project Supervisor: **Claudio Zito** 
<a href="http://www.freepik.com">Designed by 0melapics / Freepik</a>
<a href="1001.com">Gem design by 1001.com</a>
<a href="www.kenney.nl">Explosion design by kenney</a>


## License

The MIT License (MIT)

Copyright (c) 2017 Thomas Brereton Elliott Davies

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

