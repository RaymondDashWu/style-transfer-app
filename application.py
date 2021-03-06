# Requirements for Flask server
from flask_restplus import Api, Resource, fields, reqparse
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for
from werkzeug.datastructures import FileStorage
from PIL import Image
from flask_cors import CORS

# Requirements for style transfer
from vgg_styletrans import TransferStyle

# Requirements to email output image to user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid_email import send_styled_email # My function. Not part of Sendgrid API

# Requirements to upload to Imgur
import requests
import imgur_upload
from imgur_upload import authenticate, upload_image
import os
import copy
from io import BytesIO

import time
import resource
import platform

try:
  import unzip_requirements
except ImportError:
  pass

application = app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='Style Transfer',
          description='Style Transfer')
ns = api.namespace('style_transfer', description='Methods')

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('subject', location='files', type=FileStorage, required=True)
parser.add_argument('style', location='files', type=FileStorage, required=True)

@ns.route('/')
@ns.expect(parser)
class CNNPrediction(Resource):
    """Uploads your data to the CNN"""
    def post(self):

        args = parser.parse_args()
        style_image = args['style']
        subject_image = args['subject']
        email = args['email']

        # Style transfer section. Calls on vgg_styletrans functions
        make=TransferStyle('vgg_conv.npy')
        opened_style = Image.open(style_image)
        make.describe_style(opened_style)
        opened_style.save(style_image.filename)

        opened_subject = Image.open(subject_image)
        make.infer_loss(opened_subject)
        opened_subject.save(subject_image.filename)
        make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)

        # imgur upload section
        client = authenticate()
        upload_image(client, style_image.filename, "style")
        upload_image(client, subject_image.filename, "subject")
        upload_image(client, 'output.jpg', "output")

        # Sends the resulting stylized image to email via Sendgrid
        send_styled_email(email)

        # TODO NOTE Cleanup. Couldn't figure out how to upload Pillow object so
        # subject/style images are temporarily saved and then deleted here
        # os.remove(style_image.filename)
        # os.remove(subject_image.filename)

        # # Code from Edwin Cloud https://github.com/edwintcloud
        # # get memory usage
        # usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # # linux returns kb and macOS returns bytes, here we convert both to mb
        # if platform.system() == 'Linux':
        # # convert kb to mb and round to 2 digits
        #     usage = round(usage/float(1 << 10), 2)
        # else:
        # # convert bytes to mb and round to 2 digits
        #     usage = round(usage/float(1 << 20), 2)
        # # print memory usage
        # print("Memory Usage: {} mb.".format(usage))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)