from google.cloud import vision
import io

def detect_text(path="./images/decoded_image.png"):
    """Detects text in the file."""
    print(path)
    client = vision.ImageAnnotatorClient()
    print(client)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    print(content)
    image = vision.types.Image(content=content)
    print(image)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

detect_text()
