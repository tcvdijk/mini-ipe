# Demonstrates the use of add_bitmap and image

from miniipe import Document, Matrix, Scale, Stretch, Rotate, Translate
from base64 import b64encode

doc = Document()
doc.import_stylefile()
doc.add_layout(page=(90,160))

# First define a bitmap in the Ipe style. Images are identified by an integer id.
# We don't really provide any convenience features for bitmap images. There
# are other options, but here we show the basic usage: a base64-encoded jpeg.
# Note that the actual image data is included in the Ipe file, not just a reference.
image_id = 1
filename = 'logo.jpg'
width = 635
height = 433
with open(filename,'rb') as f:
    png = f.read()
    blob = b64encode(png).decode('utf-8')
    doc.add_bitmap( image_id, width, height, blob=blob, Filter='DCTDecode', encoding='base64', length=len(blob) )

# Then put the image on the page. This supports transformation matrices.
doc.image( image_id, (0,0)+(width,height), matrix=Translate((1,116))@Scale(0.1) )
doc.image( image_id, (0,0)+(width,height), matrix=Translate((50,100))@Rotate(4.5)@Stretch(0.1,0.05) )
doc.image( image_id, (0,0)+(width,height), matrix=Matrix(0.1,0.05,0.025,0.05,0,0) )


doc.write('bitmap.ipe')