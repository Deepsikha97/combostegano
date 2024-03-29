from PIL import Image, ImageFont, ImageDraw
import os
import textwrap
from werkzeug.utils import secure_filename
from datetime import datetime
import stepic

def decode_image(file_location="./images/encoded_image.png", dest_location="./images/encoded_image.png"):
    """Decodes the hidden message in an image
    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    print(file_location)
    print(dest_location)
    encoded_image = Image.open(file_location)
    # red_channel = encoded_image.split()[0]

    # x_size = encoded_image.size[0]
    # y_size = encoded_image.size[1]

    decoded_msg = stepic.decode(encoded_image)
    return decoded_msg

    # pixels = decoded_image.load()

    # for i in range(x_size):
    #     for j in range(y_size):
    #         if bin(red_channel.getpixel((i, j)))[-1] == '0':
    #             pixels[i, j] = (255, 255, 255)
    #         else:
    #             pixels[i, j] = (0,0,0)
    #decoded_image.save(dest_location)

# def write_text(text_to_write, image_size):
#     """Writes text to an RGB image. Automatically line wraps
#     text_to_write: the text to write to the image
#     """
#     image_text = Image.new("RGB", image_size)
#     #font = ImageFont.load_default().font
#     font = ImageFont.truetype("arial.ttf", 53)
#     drawer = ImageDraw.Draw(image_text)

#     #Text wrapping. Change parameters for different text formatting
#     margin = offset = 0
#     for line in textwrap.wrap(text_to_write, width=14):
#         drawer.text((margin,offset), line, font=font)
#         offset += 72
#     return image_text

def encode_image(user_name,text_to_encode,APP_ROOT,template_image="./images/source.png"):
    """Encodes a text message into an image
    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    print(user_name+","+str(text_to_encode)+","+APP_ROOT+","+template_image)
    name=user_name
    temp_image = Image.open(template_image)
    # red_template = template_image.split()[0]
    # green_template = template_image.split()[1]
    # blue_template = template_image.split()[2]

    # x_size = template_image.size[0]
    # y_size = template_image.size[1]

    #text draw
    # image_text = write_text(text_to_encode, template_image.size)
    # bw_encode = image_text.convert('1')

    #encode text into image
    #encoded_image = Image.new("RGB", (x_size, y_size))
    # pixels = encoded_image.load()
    # for i in range(x_size):
    #     for j in range(y_size):
    #         red_template_pix = bin(red_template.getpixel((i,j)))
    #         old_pix = red_template.getpixel((i,j))
    #         tencode_pix = bin(bw_encode.getpixel((i,j)))

    #         if tencode_pix[-1] == '1':
    #             red_template_pix = red_template_pix[:-1] + '1'
    #         else:
    #             red_template_pix = red_template_pix[:-1] + '0'
    #         pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel((i,j)), blue_template.getpixel((i,j)))

    # encoded_image.save("images/encoded_image.png")

    encoded_image = stepic.encode(temp_image,text_to_encode)


    filename=user_name.split()[0]+"_"+datetime.now().strftime("%d_%m_%y-%H:%M:%S")+".png"
    UPLOAD_FOLDER = os.path.join(APP_ROOT,"images\\")
    print(filename)
    path = os.path.join(UPLOAD_FOLDER,secure_filename(filename))
    encoded_image.save(path)
    return (path)

if __name__ == '__main__':
    encode_image("Hidden Message")
    decode_image()
