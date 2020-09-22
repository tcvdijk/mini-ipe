from miniipe import *

doc = Document()

doc.add_layout( page=(400,400) )
doc.add_gridsize( 'quarter', 25 )
doc.add_gridsize( 'hundreds', 100 )

gradient = doc.add_gradient('my gradient', type_='axial', coords='0 0 400 400')
add_gradient_stop( gradient, 0, '1 0.5 0.5')
add_gradient_stop( gradient, 1, '0.5 0.5 1')
doc.path( rectangle((0,0),(400,400)), gradient='my gradient', fill='1' )

doc.add_color_rgb( 'my color', 1, 0.8, 0 )
doc.add_color_rgb( 'my other color', 0, 0.1, 1 )

doc.add_pen('my pen', 5)
doc.add_dashstyle( 'dashing', '[6 1 5 1 4 1 3 2 1 2 1 3 1 4 1 5 1] 0')
doc.add_tiling('my tiling',45,5,2)

ps = [(100,100), (200,300), (300,100)]

doc.path( polygon(ps)
        , pen='my pen'
        , stroke='my color'
        , dash='dashing'
        , fill='my other color'
        , tiling='my tiling'
        )

doc.write('style.ipe')