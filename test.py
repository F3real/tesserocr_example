#!/usr/bin/python3

import tesserocr
from PIL import Image

print(tesserocr.tesseract_version())  # print tesseract-ocr version
print(tesserocr.get_languages())  # prints tessdata path and list of available languages


image = Image.open('holy.png')

# https://pypi.python.org/pypi/tesserocr

# Basic usage

print(tesserocr.image_to_text(image))
print(tesserocr.file_to_text('holy.png'))

# Advanced usage

img = 'holy.png'

with tesserocr.PyTessBaseAPI() as api:
    api.SetImageFile(img)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())

# Best results
    boxes = api.GetComponentImages(tesserocr.RIL.WORD, True)
    print('Found {} textline image components.'.format(len(boxes)))
    for i, (im, box, _, _) in enumerate(boxes):
        # im is a PIL image object
        # box is a dict with x, y, w and h keys
        api.SetRectangle(box['x'], box['y'], box['w'], box['h'])           #affects results greatly
        ocrResult = api.GetUTF8Text()
        conf = api.MeanTextConf()
        print((u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
               "confidence: {1}, text: {2}").format(i, conf, ocrResult, **box))


    it = api.AnalyseLayout()
    orientation, direction, order, deskew_angle = it.Orientation()
    print("Orientation: {:d}".format(orientation))
    print("WritingDirection: {:d}".format(direction))
    print("TextlineOrder: {:d}".format(order))
    print("Deskew angle: {:.4f}\n".format(deskew_angle))

    api.Recognize()
    ri = api.GetIterator()
    level = tesserocr.RIL.SYMBOL
    for r in tesserocr.iterate_level(ri, level):
        symbol = r.GetUTF8Text(level)  # r == ri
        conf = r.Confidence(level)
        box =  r.BoundingBox(level)
        if symbol:
            print(u'symbol {}, conf: {}'.format(symbol, conf))
            print(box)
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.











#NOTES about functions and constants

#cdef enum PageIteratorLevel:  
#RIL_BLOCK,                    # of text/image/separator line
#RIL_PARA,                     # within a block.
#RIL_TEXTLINE,                 # within a paragraph.
#RIL_WORD,                     # within a textline.
#RIL_SYMBOL                    # character within a word.

#GetComponentImages
#Get the given level kind of components (block, textline, word etc.) as a leptonica-style Boxa, Pixa pair, in reading order. Can be called before or after Recognize. 
#If blockids is not NULL, the block-id of each component is also returned as an array of one element per component. delete [] after use. 
#If text_only is true, then only text components are returned. 

#AllWordConfidences
#Returns all word confidences (between 0 and 100) in an array, terminated by -1. The calling function must delete [] after use.  
#The number of confidences should correspond to the number of space-delimited words in GetUTF8Text.
#Returns an array of all word confidences, terminated by -1. 

#MeanTextConf
#Returns the (average) confidence value between 0 and 100.
#Returns the average word confidence for Tesseract page result. 
#Basically average of result of AllWordConfidences.


#PyTessBaseAPI
#Constructor
#def __cinit__(self, path=_DEFAULT_PATH, lang=_DEFAULT_LANG, PageSegMode psm=PSM_AUTO, bool init=True):
#
#An enum that defines all available page segmentation modes.
#Attributes:
#        OSD_ONLY: Orientation and script detection only.
#        AUTO_OSD: Automatic page segmentation with orientation and script detection. (OSD)
#        AUTO_ONLY: Automatic page segmentation, but no OSD, or OCR.
#        AUTO: Fully automatic page segmentation, but no OSD. (:mod:`tesserocr` default)
#        SINGLE_COLUMN: Assume a single column of text of variable sizes.
#        SINGLE_BLOCK_VERT_TEXT: Assume a single uniform block of vertically aligned text.
#        SINGLE_BLOCK: Assume a single uniform block of text.
#        SINGLE_LINE: Treat the image as a single text line.
#        SINGLE_WORD: Treat the image as a single word.
#        CIRCLE_WORD: Treat the image as a single word in a circle.
#        SINGLE_CHAR: Treat the image as a single character.
#        SPARSE_TEXT: Find as much text as possible in no particular order.
#        SPARSE_TEXT_OSD: Sparse text with orientation and script det.
#        RAW_LINE: Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
#        COUNT: Number of enum entries.
#
# lang (str): An ISO 639-3 language string. Defaults to 'eng'.



#Recognize
#Recognize the image from :meth:`SetImage`, generating Tesseract
#internal structures. Returns ``True`` on success.



#Confidence(self, PageIteratorLevel level):
#Return the mean confidence of the current object at the given level.
#The number should be interpreted as a percent probability. (0.0-100.0)










