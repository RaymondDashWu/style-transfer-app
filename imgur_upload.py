from imgurpython import ImgurClient
from dotenv import load_dotenv
import os
import requests
from werkzeug.datastructures import FileStorage


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

def upload_image(client, image, filename):
    """
    Uploads images to Imgur
    """
    # TODO account for PIL image or filestorage upload to make code DRYer
    album = None #TODO figure out how to do dynamic albums
    # image_path = image #TODO change later. Currently tells image_path for upload_from_path
    print("image", image)
    # This is for the style + subject images that are taken in as args and stored in FileStorage
    if type(image) == FileStorage:
        # set options for the imgur request
        url = 'https://api.imgur.com/3/upload'
        style_img_payload = {'image': image}
        # subject_img_payload = {'image': image}
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        headers = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}

        print("style_img_payload", style_img_payload)
        # upload files to imgur using requests
        style_img_req = requests.post(
            url, files=style_img_payload, headers=headers)
        # subject_img_req = requests.post(
        #     url, files=subject_img_payload, headers=headers)
        print("style_img_req", style_img_req)

        # parse json responses from imgur
        style_img_resp = style_img_req.json()
        # subject_img_resp = subject_img_req.json()
        print("style_img_resp", style_img_resp)
        # status check
        # print(style_img_resp, "\n", subject_img_resp)

        # format a response
        resp = {
            'style_image_url': style_img_resp['data']['link'],
            # 'subject_image_url': subject_img_resp['data']['link']
        }

        # return formatted response and 200 OK
        return resp, 200

    else:
        config = {
            'album': album,
            'name': filename, 
            'title': 'style transfer',
            'description': 'This was created with DEPLOYED SITE. This is the {} image. Go to link to try TODO'.format(filename) 
        }
        client.upload_from_path(image, config = config, anon = False)

if __name__ == "__main__":
    client = authenticate()
    image = upload_image(client, 'output.jpg', "output")

    # print("Image was posted! You can find it here: {0}".format(image['link']))