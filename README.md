# IFT3335-TP2

Script that formats input annotated text into arff file format and extract features for disambiguation of the targeted word sense.

Authors: Jean-Pierre T., Sofiene F. *- University of Montreal*

## Setup
#### Dependencies:
* Python 3.5+

## Usage
### Basic Usage

1. Run the command with specific arguments:
```
python senses.py <arguments>
```
*Example*:
```
python senses.py --stopwords
```

#### Arguments
* `--ws`: Window size (Number of preceding and following words to consider). *Default*: `3`
* `--stopwords`: Boolean flag indicating if stopwords are ignored during feature extraction