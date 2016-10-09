from flask import Flask
from flask import request
app = Flask(__name__)

import cv2
import sys
import tensorflow as tf
import json

@app.route('/', methods=['GET'])
def hello_world():
    return "hello world\n"

@app.route('/', methods=['POST'])
def post_img():
    # data = request.files['media']
    # data.save('img.jpg')

    f = open('img.jpg', 'wb')
    f.write(request.get_data())
    f.close()

    img = cv2.imread('img.jpg')
    app.logger.warning(img.shape)
    res = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(im_bw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    t = res.copy()
    cnt = contours[2]
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    result = {}

    try:
        x1 = approx[0][0][0]
        y1 = approx[0][0][1]
        x2 = approx[2][0][0]
        y2 = approx[2][0][1]

        roi = t[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]

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

            human_string = label_lines[best_guess]
            score = predictions[0][best_guess]
            result['error'] = False
            result['name'] = human_string
            result['confidence'] = "%0.5f" % score

    except Exception:
        result = {"error" : True}

    return json.dumps(result) + "\n"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
