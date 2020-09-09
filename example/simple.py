from miniipe import Document

doc = Document()
doc.import_stylefile()

doc.add_layer('alpha')

ps = [(0,0), (100,100), (200,0)]
doc.add_path( ps, color='black', layer='alpha')

doc.write('simple.ipe')