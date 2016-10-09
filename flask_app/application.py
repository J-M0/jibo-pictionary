from flask import Flask
from flask import request
app = Flask(__name__)

import os
import uuid
import cv2
import sys
import tensorflow as tf
import json
import preprocess

@app.route('/', methods=['GET'])
def hello_world():
    return "hello world\n"

@app.route('/', methods=['POST'])
def post_img():
    result = {}
    try:
        f = open('img.jpg', 'wb')
        f.write(request.get_data())
        f.close()

        roi = preprocess.process('img.jpg')
        cv2.imwrite('cropped.jpg', roi)

        image_data = tf.gfile.FastGFile('cropped.jpg', 'rb').read()

        label_lines = [line.rstrip() for line in tf.gfile.GFile("/tf_files/retrained_labels.txt")]

        with tf.gfile.FastGFile("/tf_files/retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            best_guess = top_k[0]

            guesses = []
            result['error'] = False
            result['guesses'] = []
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                result['guesses'].append({
                    'name': human_string,
                    'confidence': "%0.5f" % score
                })

    except Exception as e:
        result = {
            "error" : True,
            "guesses" : []
        }
        app.logger.warning(e)

    return json.dumps(result) + "\n"

@app.route('/store', methods=['POST'])
def store_img():
    if not os.path.exists('saved'):
        os.mkdir('saved')

    filename = 'saved/' + str(uuid.uuid4()) + ".jpg"
    f = open(filename, 'wb')
    f.write(request.get_data())
    f.close()

    result = {
        'error': False,
        'name': filename,
        'confidence': ""
    }
    return json.dumps(result) + "\n"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
