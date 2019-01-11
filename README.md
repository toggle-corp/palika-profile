# Palika Profile Report Generation

## Requirements

- Cairo: https://pycairo.readthedocs.io/en/latest/getting_started.html 

- PyG: https://pygobject.readthedocs.io/en/latest/getting_started.html
  
- libffi: https://sourceware.org/libffi/
  
- drafter: https://github.com/bibekdahal/drafter

- maps: https://github.com/eoglethorpe/hrrp-maps


# Docker

```
# TODO: Add volume for input folder
# cd to folder where you need output
docker run --rm -it -v "$(pwd):/code/output/" devtc/palika-profile:dev bash -c 'python3 main.py'
```
