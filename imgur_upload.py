from imgurpython import ImgurClient
from dotenv import load_dotenv
import os

def authenticate():
    load_dotenv(dotenv_path='imgur.env')
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    client = ImgurClient(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
    print("Authentication success", client)
    return client

def upload_image(client, image):
    album = None #TODO figure out 
    image_path = image #TODO change later

    config = {
        'album': album,
        'name': 'output', #TODO dynamic name based on either style,image,output or names of them
        'title': 'style transfer',
        'description': 'This is the output image. Go to link to try TODO' 
    }
    image = client.upload_from_path(image_path, config = config, anon = False)
    return image

if __name__ == "__main__":
    client = authenticate()
    image = upload_image(client, 'output.jpg')

    print("Image was posted! Go check your images you sexy beast!")
    print("You can find it here: {0}".format(image['link']))
    # items = client.gallery()
    # for item in items:
    #     print(item.title, item.link, item.views)