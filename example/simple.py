from miniipe import Document, polygon

doc = Document()
doc.import_stylefile()

doc.add_layer('alpha')

ps = [(100,100), (200,200), (300,100)]
doc.path( polygon(ps), stroke='black', layer='alpha')

doc.write('simple.ipe')