import io
import json
import os
import re

import boto3
import numpy as np
import tensorflow as tf
from flask import Flask, request, Response
from keras.models import load_model
from sorensen import sorensen_dice_coef, sorensen_dice_coef_loss

PREFIX = '/opt/ml'
MODEL_PATH = os.path.join(PREFIX, 'model')
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
MANGROVE_CHIP_BUCKET = ''


class SegmentationService(object):
    model = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = load_model(os.path.join(MODEL_PATH, 'model.h5'),
                                   custom_objects={
                                       'sorensen_dice_coef': sorensen_dice_coef,
                                       'sorensen_dice_coef_loss': sorensen_dice_coef_loss
                                   })
            global graph
            graph = tf.get_default_graph()
        return cls.model

    @classmethod
    def predict(cls, chips):
        mdl = cls.get_model()
        with graph.as_default():
            predictions = mdl.predict(chips, batch_size=8, verbose=1)
        return np.argmax(predictions, axis=3)


app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    health = SegmentationService.get_model() is not None
    status = 200 if health else 404
    return Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    request_body = request.get_json()
    chip_paths = request_body['chip_paths']
    validated_chip_paths = validate_chip_paths(chip_paths)
    chips, chip_keys = get_chips_from_s3(validated_chip_paths)
    predictions = SegmentationService.predict(chips)
    response = json.dumps({"message": ''})
    return Response(response=response, status=200, mimetype='application/json')


def validate_chip_paths(chip_paths):
    valid_chip_path_regex = '.*(chip_[0-9]{1,2}_[0-9]{1,2}.npy)$'
    valid_chip_paths = []
    for chip_path in chip_paths:
        if re.fullmatch(valid_chip_path_regex, chip_path):
            valid_chip_paths.append(chip_path)
        else:
            print('Invalid chip path: {0}, not predicting'.format(chip_path))
    return valid_chip_paths


def get_chips_from_s3(chip_paths):
    s3_r = boto3.resource('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name='eu-west-2')
    chip_array = None
    chip_keys = []
    for chip_path in chip_paths:
        try:
            with io.BytesIO() as chipio:
                s3_obj = s3_r.Object(MANGROVE_CHIP_BUCKET, chip_path)
                s3_obj.download_fileobj(chipio)
                chipio.seek(0)
                if chip_array is None:
                    chip_array = np.expand_dims(np.load(chipio), axis=0)
                else:
                    chip_array = np.insert(chip_array, chip_array.shape[0], np.load(chipio), axis=0)
                chipio.close()
                chip_keys.append(chip_path)
        except Exception as ex:
            print('Error when retrieving chip: {0} \r\n{1}'.format(chip_path, ex))
    return chip_array, chip_keys
