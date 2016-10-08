from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "hello world\n"

@app.route('/', methods=['POST'])
def post_img():
    data = request.files['media']
    data.save('img.jpg')
    return 'image uploaded!\n'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
