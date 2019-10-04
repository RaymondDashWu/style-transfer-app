# Requirements for Flask server
from flask_restplus import Api, Resource, fields, reqparse
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for
from werkzeug.datastructures import FileStorage
from PIL import Image

# Requirements for style transfer
from vgg_styletrans import TransferStyle

# Requirements to email output image to user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Requirements to upload to Imgur
import requests
import imgur_upload
from imgur_upload import authenticate, upload_image
import os

application = app = Flask(__name__)
api = Api(app, version='1.0', title='Style Transfer TEST',
          description='Style Transfer')
ns = api.namespace('Make_School', description='Methods')

parser = reqparse.RequestParser()
# parser.add_argument('weights', location='files', type=FileStorage, required=False, default='vgg_conv.npy')
# parser.add_argument('email', type="string", required=True)
parser.add_argument('subject', location='files',
                    type=FileStorage, required=True)
parser.add_argument('style', location='files', type=FileStorage, required=True)
# parser.add_argument('output', location='files', type=FileStorage, required=False, default='output.jpg')​

@ns.route('/prediction')
@ns.expect(parser)
class CNNPrediction(Resource):
    """Uploads your data to the CNN"""
    # @api.doc(parser=parser, description='Upload an mnist image')

    def post(self):
        # TODO Make code DRYer by combining upload section for args and output
        args = parser.parse_args()
        style_image = args['style']
        subject_image = args['subject']

        client = imgur_upload.authenticate()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


        # set options for the imgur request
        url = 'https://api.imgur.com/3/upload'
        style_img_payload = {'image': style_image}
        subject_img_payload = {'image': subject_image}
        headers = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}

        # upload files to imgur using requests
        style_img_req = requests.post(
            url, files=style_img_payload, headers=headers)
        subject_img_req = requests.post(
            url, files=subject_img_payload, headers=headers)

        # parse json responses from imgur
        style_img_resp = style_img_req.json()
        subject_img_resp = subject_img_req.json()

        # status check
        print(style_img_resp, "\n", subject_img_resp)

        # format a response
        resp = {
            'style_image_url': style_img_resp['data']['link'],
            'subject_image_url': subject_img_resp['data']['link']
        }

        # Style transfer section. Calls on vgg_styletrans functions
        make=TransferStyle('vgg_conv.npy')
        make.describe_style(Image.open(style_image))
        make.infer_loss(Image.open(subject_image))
        make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)

        # imgur upload section
        client = authenticate()
        image = upload_image(client, 'output.jpg')

        # return formatted response and 200 OK
        return resp, 200

# Python threading class
# whenever called, starts new thread


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)