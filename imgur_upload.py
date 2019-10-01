from imgurpython import ImgurClient
from dotenv import load_dotenv
import os

def authenticate():
    """
    Authenticates with Imgur API. Used in this app to upload images and create a gallery
    containing subject, style, output
    """
    load_dotenv(dotenv_path='imgur.env')
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    client = ImgurClient(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
    return client

def upload_image(client, image):
    """
    Uploads images to Imgur
    """
    # TODO account for PIL image or filestorage upload to make code DRYer
    album = None #TODO figure out how to do dynamic albums
    image_path = image #TODO change later. Currently tells image_path for upload_from_path

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

    # print("Image was posted! You can find it here: {0}".format(image['link']))