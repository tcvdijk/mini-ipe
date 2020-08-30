# Mini-Ipe

This is a source-only, no-dependencies Python package to write [Ipe](http://ipe.otfried.org/) files.
The proper way to write Ipe files from Python would be to use `ipepython` from [ipe-tools](https://github.com/otfried/ipe-tools), but this requires building a number of things from source, which may be difficult (or just time-consuming) depending on your computing environment.
Mini-Ipe is a "quick and dirty" way to easily write Ipe files with minimum effort, from a plain Python environment.

## What are Ipe files

Ipe is an "extensible drawing editor" that is excellent for making diagrams for scientific papers and presentations.
This makes its file format ideal as output from computational experiments.

## Example
```python
from mini_ipe import Document

doc = Document()
doc.import_stylefile()

doc.add_layer("hello world")

p = [(0,0), (100,100), (200,0)]
doc.path( p, color='black', layer='hello world')

doc.write('test.xml')
```