# Requirements for server + database
from flask_restplus import Api, Resource, fields
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for

import datetime
import numpy as np
from werkzeug.datastructures import FileStorage
from PIL import Image

# Requirements for style transfer
from vgg_styletrans import TransferStyle

# Requirements to email output image to user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from imgur_upload import *

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

        make=TransferStyle('vgg_conv.npy')
        make.describe_style(style_image)
        make.infer_loss(subject_image)
        make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)

        # imgur upload section
        client = authenticate()
        image = upload_image(client, 'output.jpg')
        return image

# Python threading class
# whenever called, starts new thread

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)