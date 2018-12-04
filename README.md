# Palika Profile Report Generation

## Setup

Cairo: https://pycairo.readthedocs.io/en/latest/getting_started.html
PyG: https://pygobject.readthedocs.io/en/latest/getting_started.html
libffi: https://sourceware.org/libffi/
pip install -e requirements.txt

[Cairo](https://cairographics.org/pycairo/)
and
[PyGObject bindings](https://pygobject.readthedocs.io/en/latest/getting_started.html)
are required to run the pdf generation library (drafter).

To run the test file:

```bash
# Clone the drafter repo at this location
git clone https://github.com/bibekdahal/drafter

# Run with python (Python version 3 is required)
python test.py
```

A pdf file `test.pdf` is then generated in the project path.
