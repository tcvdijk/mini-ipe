![MINI-IPE logo](logo.png)

# Mini-Ipe

This is a source-only, no-dependencies Python package to write [Ipe](http://ipe.otfried.org/) files.
The proper way to write Ipe files from Python would probably be to use `ipepython` from [ipe-tools](https://github.com/otfried/ipe-tools), but this requires building a number of things from source, which may be difficult (or just time-consuming) depending on your computing environment.
Mini-Ipe is a quick way to easily write Ipe files with minimum effort, from a plain Python environment.

Mini-Ipe is now on PyPI. Get it anywhere using (python3 -m) `pip install miniipe`.

## What are Ipe files

Ipe is an "extensible drawing editor" that is excellent for making diagrams for scientific papers and presentations.
This makes its file format ideal as output from computational experiments.

**Important!** An Ipe file needs a valid style file. It is not clear to me that I have the rights to distribute the standard style file, so you will have to provide your own. There are several ways to go about this.

1. Call `import_stylefile()` without arguments. This tries to import `~/.ipe/styles/basic.isy`, which may or may not exist on your system. You get an error if this file does not exist.
2. Call `import_stylefile(filename)` with the filename of a valid style file. You can get one from Ipe as follows: make a new document, select `Edit > Style sheets`, select `basic` and click `Save`.
3. Do not import a style file when you make the document with `miniipe` and save it anyway. This will lead to errors when you open the file in Ipe (most prominently, colours and symbols will be missing), but you can then add the `basic` style file after the fact. (See option 2 for how to get the basic style file.) 

## Example

See the [example](example) directory to get an idea for more options; here is a small example.

```python
from miniipe import Document, polygon

doc = Document()
doc.import_stylefile()

doc.add_layer('alpha')

ps = [(100,100), (200,200), (300,100)]
doc.path( polygon(ps), stroke='black', layer='alpha')

doc.write('simple.ipe')
```