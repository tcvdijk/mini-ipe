from mini_ipe import Document

doc = Document()
doc.import_stylefile()

doc.add_layer("hello world")

p = [(0,0), (100,100), (200,0)]
doc.add_path( p, color='black', layer='hello world')

doc.write('test.xml')