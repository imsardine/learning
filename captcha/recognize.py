import sys
import pytesseract
from PIL import Image

def main(fname):
    img = Image.open(fname)
    text = pytesseract.image_to_string(img)
    print 'Text: [%s]\n' % text

def parse_args():
    args = sys.argv
    if len(args) != 2:
        print 'Usage: %s <FILE>' % args[0]
        sys.exit(-1)

    return args[1]

if __name__ == '__main__':
    main(parse_args())

