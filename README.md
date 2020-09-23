# Mini-Ipe

This is a source-only, no-dependencies Python package to write [Ipe](http://ipe.otfried.org/) files.
The proper way to work with Ipe files from Python would probably be to use `ipepython` from [ipe-tools](https://github.com/otfried/ipe-tools), but this requires building a number of things from source, which may be difficult (or just time-consuming) depending on your computing environment.
Mini-Ipe is a quick way to easily write Ipe files with minimum effort, from a plain Python environment.

Mini-Ipe is now on PyPI. Get it anywhere using (python3 -m) `pip install miniipe`.

## What are Ipe files

Ipe is an "extensible drawing editor" that is excellent for making diagrams for scientific papers and presentations.
This makes its file format ideal as output from computational experiments.

**Important!** An Ipe file needs a valid style file. See the remarks section below.

## Getting started


First, get `miniipe` visible to your interpeter, for example using pip. (No need to clone the github repository.)

```
pip install miniipe
```

Then try the following small program and go from there.

```python
from miniipe import Document, polygon

doc = Document()

ps = [(100,100), (200,200), (300,100)]
doc.path( polygon(ps) )

doc.write('simple.ipe')
```

## Remarks

This is not a complete documentation, but looking at the [examples](example) will get you a long way.
The best way to find out about all the methods and arguments is probably to `import miniipe` and use an IDE to look around (or skim the source source); here are some general remarks.

### Points

Mini-Ipe accesses the X and Y coordinates 2D points you give it using index `[0]` and `[1]`.
This means a 2-tuple of numbers is probably the easiest way to go in many cases (see the example above).
We do not provide a class for working with 2D points/vectors: if you need to do nontrivial geometric computations, you probably already have some way to do that and we do not want to create additional API boundaries.

*Note.* We do provide a `Matrix` class for affine transformations, since this is an important concept in Ipe.

### Document.path(...)

In Ipe, **what** is drawn is mostly orthogonal to **how** it it drawn.
Polygons, circles, splines: almost everything is a *path*.
Even filled shapes are paths with a `fill` property.
This is reflected in the Mini-Ipe API: it is `document.path( polygon(...), ...)` rather than `document.polygon( ..., ...)`.

* A path is described by a series of "path construction operators" ([Ipe documentation](http://ipe.otfried.org/manual/manual_59.html)).
The `Document.path` method takes a string of such drawing instructions.
You can write these on your own, but should probably use the convenience functions like `rectangle`, `circle`, `polygon`, and so forth.
Under most circumstances, you can have multiple shapes be part of one "path" by concatenating these strings.

### Layers

All objects (`path`, `text`, `use`) belong to a layer.
As a consequence of the Ipe file format, if you don't specify the `layer` argument, the object goes in the same layer as the previous object.

### Matrix

Matrices occur in multiple places in Ipe, most prominently as a property of objects: when drawing something that has a `matrix` property, Ipe transforms it using the given matrix.
Use the `Matrix` class for this: it supports matrix multiplication using the `@` operator, and helper functions for common transformations such as `Translate`, `Scale` and `Rotate` are provided.
See the [matrix fun](example/matrix_fun.py) example.

*Note.* Transformation by the matrix property is not done by `miniipe`: it merely writes the `matrix` property in the Ipe file. To actually transform a single point in a way that is consistent with Ipe, use the `Matrix.transform(p)` method.
See the [transform](example/transform.py) example to confirm that the results match.

### Ellipse

The `ellipse` function takes a `Matrix` argument: it draws the ellipse resulting from transforming the unit circle by this matrix.

### The 'parent' argument

The methods `path`, `text` and `use` take an optional argument called `parent`.
If omitted, the object is added to the default page that a `miniipe.Document` starts with.
If you make more pages, pass the page you want to add the object to instead.
To put the object in a group (`miniipe.Document.group(...)`), pass the group instead.

### Style files

It is not clear to me that I have the rights to distribute the standard Ipe style file, so you will have to provide your own. There are several ways to go about this.

1. Call `import_stylefile()` without arguments. This tries to import `~/.ipe/styles/basic.isy`, which may or may not exist on your system. You get an error if this file does not exist.
2. Call `import_stylefile(filename)` with the filename of a valid style file. You can get one from Ipe as follows: make a new document, select `Edit > Style sheets`, select `basic` and click `Save`.
3. Do not import a style file when you make the document with `miniipe` and save it anyway. Ipe may complain when you open the file - colours, symbols et cetera will be missing. You can then add the `basic` style file after the fact. (See option 2 for how to get the basic style file.) 

You can also make styles using Mini-Ipe. See the [style](example/style.py) example code.