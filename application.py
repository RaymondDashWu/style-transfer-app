# Requirements for Flask server
from flask_restplus import Api, Resource, fields
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for
from werkzeug.datastructures import FileStorage
from PIL import Image

# Requirements for style transfer
from vgg_styletrans import TransferStyle

# Requirements to email output image to user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Requirements to upload to Imgur
from imgur_upload import *
# from imgurpython import client as C
import requests
import base64


application = app = Flask(__name__)
api = Api(app, version='1.0', title='Style Transfer TEST', description='Style Transfer')
ns = api.namespace('Make_School', description='Methods')

parser = api.parser()
# parser.add_argument('weights', location='files', type=FileStorage, required=False, default='vgg_conv.npy')
# parser.add_argument('email', type="string", required=True)
parser.add_argument('subject', location='files', type=FileStorage, required=True)
parser.add_argument('style', location='files', type=FileStorage, required=True)
# parser.add_argument('output', location='files', type=FileStorage, required=False, default='output.jpg')

@ns.route('/prediction')
class CNNPrediction(Resource):
    """Uploads your data to the CNN"""
    @api.doc(parser=parser, description='Upload an mnist image')
    def post(self):
        # parser = make_parser()
        args = parser.parse_args()
        
        style_image = Image.open(args.style)
        subject_image = Image.open(args.subject)

        # print("args", args)
        # print("style_image", style_image)
        # print("args.style", args.style)
        # print("args.style.filename", args.style.filename)
        # print("style_image.filename", style_image.filename)
# request.files['upload'].filename

        client = authenticate()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")

        with open(args.style, 'rb') as f:
            data = f.read()
            f.close()

        url = 'https://api.imgur.com/3/image'
        payload = {'image': base64.b64encode(data)}
        # TRIED: args.style, style_image, base64.b64encode(args.style, style_image)
        # base64.b64encode(data).decode()
        files = {}
        headers = {
        'Authorization': 'Client-ID 1ed8da9ed686569'
        }
        response = requests.request('POST', url, headers = headers, data = payload, files = files, allow_redirects=False, timeout=60000)
        print("response.text", response.text)
        # C.upload(client, args.style)
        upload(client, args.subject)

        make=TransferStyle('vgg_conv.npy')
        make.describe_style(style_image)
        make.infer_loss(subject_image)
        make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)

        # imgur upload section
        # client = authenticate()
        # upload_image(client, subject_image.open())
        # upload_image(client, style_image.open())

        image = upload_image(client, 'output.jpg')
        return image

# Python threading class
# whenever called, starts new thread

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)