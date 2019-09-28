# Requirements for server + database
from flask_restplus import Api, Resource, fields
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for
# from firebase_admin import credentials, firestore, initialize_app

import datetime
import numpy as np
from werkzeug.datastructures import FileStorage
from PIL import Image

# Requirements for style transfer
from vgg_styletrans import TransferStyle

# Requirements to email output image to user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 


application = app = Flask(__name__)
api = Api(app, version='1.0', title='Style Transfer TEST', description='Style Transfer')
ns = api.namespace('Make_School', description='Methods')

# Initialize Firestore DB
# cred = credentials.Certificate('key.json')
# default_app = initialize_app(cred)
# db = firestore.client()
# todo_ref = db.collection('mnist_responses')

parser = api.parser()
# parser.add_argument('weights', location='files', type=FileStorage, required=False, default='vgg_conv.npy')
parser.add_argument('email', type="string", required=True)
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
        return make.synthesize_image('output.jpg', optimizer = 'bfgs', steps=80)
# Python threading class
# whenever called, starts new thread

# FUTURE TODO hook it up to imgur api so I don't have to store this


        # image_red = img.resize((28, 28))
        # image = img_to_array(image_red)
        # print(image.shape)
        # x = image.reshape(1, 1, 28, 28)
        # # x = image.reshape(1, 28, 28, 1)
        # x = x/255
        # # This is not good, because this code implies that the model will be
        # # loaded each and every time a new request comes in.
        # # model = load_model('my_model.h5')
        # with graph.as_default():
        #     out = model.predict(x)
        # print("out[0]", out[0])
        # # print("out[1]", out[1])
        # print(np.argmax(out[0]))

        # # What will be shown in flask_restplus
        # r = np.argmax(out[0])
        # softmax_interval = np.around(model.predict(x)[0], decimals = 2)

        # # id = request.json['id']
        # # todo_ref.document(id).update(request.json)

        # # Note: Sends response but only a random id
        # # todo_ref.add(request.json)

        # todo_ref.document().set({"Filename": str(image_file), "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Prediction": int(r), "Activation": [float(x) for x in softmax_interval]})

        # return jsonify({'prediction': "{} {}".format(r, softmax_interval)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)