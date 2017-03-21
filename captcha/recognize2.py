import sys
import pytesseract
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter


def main(fname):
    img = Image.open(fname)
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255)
    bw.show()
    text = pytesseract.image_to_string(bw, config='-psm 8') # -c tessedit_char_whitelist=0123456789
    print 'Text: [%s]\n' % text

def parse_args():
    args = sys.argv
    if len(args) != 2:
        print 'Usage: %s <FILE>' % args[0]
        sys.exit(-1)

    return args[1]

if __name__ == '__main__':
    main(parse_args())

