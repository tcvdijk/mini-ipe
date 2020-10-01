# Demonstrates making and using symbols

from miniipe import Document, symbol_name, segment, circle, arc
from math import pi

doc = Document()
doc.add_layout( page=(48,48) )


### A diagonal cross symbol

# Symbols have a name. If you want them to show up in the marks
# list in the Ipe interface, they must start with 'mark/'
x = symbol_name('mark/x')
# Add a symbol with this name to the style
x_symbol = doc.add_symbol( x )
# A symbol can only contain a single object.
# We want two lines, so we nest it in a group
x_group = doc.group(parent=x_symbol)
doc.path( segment((-1,-1),(1,1)), parent=x_group )
doc.path( segment((1,-1),(-1,1)), parent=x_group )

# Now put it on the page a couple of times
doc.use( x, pos=(16,16) )
doc.use( x, pos=(16,32) )
doc.use( x, pos=(32,16) )
doc.use( x, pos=(32,32) )


### A scalable circle symbol

# Whether a symbol reacts to scale depends on its name.
o = symbol_name('mark/o', size=True)
o_symbol = doc.add_symbol(o)
doc.path( circle((0,0),1), parent=o_symbol)

# Make some symbol sizes, since we haven't included the basic Ipe style file
doc.add_symbolsize( 'large', 2 )
doc.add_symbolsize( 'ginormous', 16 )

# Now use the symbol
doc.use( o, pos=(24,24) )
doc.use( o, pos=(24,24), size='large' )
doc.use( o, pos=(24,24), size='ginormous' )

# Size doesn't work on the x symbol, since we did not say so in its name
doc.use( x, pos=(24,24), size='ginormous' )


### A smiley face with flexible color

# Whether a symbol's fill in configurable depends on its name.
# Anything with fill='sym-fill' will get the symbol's fill.
smiley = symbol_name( 'mark/smiley', fill=True )
smiley_symbol = doc.add_symbol(smiley)
smiley_group = doc.group(parent=smiley_symbol)
doc.path( circle((0,0),4), fill='sym-fill', parent=smiley_group )
doc.path( circle((-2,1),0.5), fill='black', parent=smiley_group )
doc.path( circle(( 2,1),0.5), fill='black', parent=smiley_group )
doc.path( arc((0,0), 2.5, 9*pi/8, 15*pi/8), parent=smiley_group )

doc.use( smiley, pos=( 8, 8), )
doc.use( smiley, pos=(40, 8), fill='1 1 0' )
doc.use( smiley, pos=(40,40), fill='0 1 1' )
doc.use( smiley, pos=( 8,40), fill='1 0 1' )

### Write document

doc.write('symbol.ipe')