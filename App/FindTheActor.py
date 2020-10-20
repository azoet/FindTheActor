from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'gi2tn2k6plnr9th5nad52jgofmp6'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename))


@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('edit.html', filename=filename)
    return


@app.route('/upload', methods=['POST'])
def upload():
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, port=5000)
