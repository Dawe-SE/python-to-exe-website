import os, request, json, ast, shutil, time
from flask import Flask, flash, request, redirect, url_for, session, render_template, send_file
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1000 * 1000
app.config['SECRET_KEY'] = 'sutminpiksutminpiksutminpik'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertToExe(file):
    os.system('cd ' + os.getcwd())
    os.system('nuitka uploads/' + file.filename)
    name_of_file_without_extension = file.filename.split('.')[0]
    #os.replace(name_of_file_without_extension + '.exe', name_of_file_without_extension + '.exe')
    payload = json.dumps({'filename':name_of_file_without_extension})
    session['messages'] = payload
    return redirect(url_for('download', messages=payload))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    payload = request.args['messages']
    filename = ast.literal_eval(payload)['filename']
    try:
        return send_file(filename + '.exe')
    finally:
        shutil.rmtree(filename + '.build')
        os.remove(filename + '.cmd')

@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return convertToExe(file)
    else:
        return redirect((url_for('error')))





app.run()