#app.py
from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename
import subprocess
import demo as d
import predict
app = Flask(__name__)
 
app.secret_key = "caircocoders-ednalan"
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Homepage'

@app.route('/add/<int:a>',methods=['GET'])
def add(a):
    #b=fun.hello(a)
    resp = jsonify({'message' : a})
    success = True
    return resp

@app.route('/voilent_detector', methods=['POST'])
def voilent_detector():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file.filename)
            #   p = subprocess.Popen(['python3', 'age_detector.py','--image',file.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #out, err = p.communicate()
            is_voilent = predict.call_pred(file.filename)
            d.demo()
            success = True
            #age = 18
            #age = out.decode('UTF-8')  
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Success','result' : is_voilent})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run(debug=True)