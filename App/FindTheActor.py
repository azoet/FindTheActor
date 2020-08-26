from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'gi2tn2k6plnr9th5nad52jgofmp6'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if request.files['image'].filename == '':
            return redirect(url_for('index'))

        f = request.files['image']
        return redirect(url_for('result'))

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
