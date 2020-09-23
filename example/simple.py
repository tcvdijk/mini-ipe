# A very small example. It draws a triangle.

from miniipe import Document, polygon

# Make a miniipe.Document.
doc = Document()

# Ipe files usually need a style file.
# If this line gives an error, check the README.
doc.import_stylefile()

# Add a layer.
doc.add_layer('my layer')

# Draw a triangle.
ps = [(100,100), (200,200), (300,100)]
doc.path( polygon(ps), stroke='black', layer='my layer')

# Write it to a file.
doc.write('simple.ipe')