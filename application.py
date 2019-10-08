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
import copy
from io import BytesIO


application = app = Flask(__name__)
api = Api(app, version='1.0', title='Style Transfer TEST',
          description='Style Transfer')
ns = api.namespace('Make_School', description='Methods')

parser = reqparse.RequestParser()
# parser.add_argument('email', type="string", required=True)
parser.add_argument('subject', location='files', type=FileStorage, required=True)
parser.add_argument('style', location='files', type=FileStorage, required=True)

@ns.route('/prediction')
@ns.expect(parser)
class CNNPrediction(Resource):
    """Uploads your data to the CNN"""
    # @api.doc(parser=parser, description='Upload an mnist image')
# [1, 8, 12, ...]
# "1","8", "12", ..."
# bla = map(str, list)
# reduce(split(), set(bla))

    def post(self):
        args = parser.parse_args()
        style_image = args['style']
        subject_image = args['subject']
        # email = args['email']

        # TODO Issue where opening image somehow changes the filestorage object?
        # Tried putting the uploads above and commenting out style transfer section
        # tried deepcopy but recursion error?

        # Style transfer section. Calls on vgg_styletrans functions
        make=TransferStyle('vgg_conv.npy')
        opened_style = Image.open(style_image)
        make.describe_style(opened_style)
        print("style_image.filename", style_image.filename)
        opened_style.save(style_image.filename)
        print("style_image.filename after save", style_image.filename)

        opened_subject = Image.open(subject_image)
        make.infer_loss(opened_subject)
        opened_subject.save(subject_image.filename)
        make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)

        # imgur upload section
        client = authenticate()
        upload_image(client, style_image.filename, "style")
        upload_image(client, subject_image.filename, "subject")
        upload_image(client, 'output.jpg', "output")

        # TODO NOTE Cleanup. Couldn't figure out how to upload Pillow object so
        # subject/style images are temporarily saved and then deleted here
        os.remove(style_image.filename)
        os.remove(subject_image.filename)

# Python threading class
# whenever called, starts new thread


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)