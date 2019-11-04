from PIL import Image
import pytesseract


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    pytesseract.pytesseract.tesseract_cmd = './OCR/tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename),lang='eng',config ='--psm 6')  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


