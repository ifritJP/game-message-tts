from PIL import Image

import pyocr
import pyocr.builders

def getTxt( image ):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found!!!")
        return None
    
    tool = tools[0]
    
    return tool.image_to_string(
        image, lang='eng', builder=pyocr.builders.TextBuilder() )
    
if __name__ == '__main__':
    print("'%s'" % (getTxt( Image.open('box.png') )) )
