import os, zipfile
from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = './static/'
ALLOWED_EXTENSIONS = {'mp4', 'mpeg', 'mov', 'ogg'}

#Index
@app.route('/')
def uploader_file():
   return render_template('index.html')

#Arquivo com formato valido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Upload e processamento do arquivo
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if (not allowed_file(f.filename)):
         return('Formato inválido!')
      dt = datetime.now()
      timestamp = dt.strftime("%d-%b-%YT%H:%M:%S")
      name = f.filename.rsplit('.', 1)[0].lower()
      filename = secure_filename(name + "-" + timestamp)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      os.system('python3 processa.py ' + filename)
      return render_template('sucesso.html', filename=filename)

#Arquivo com todos os frames
@app.route('/todos_frames')
def todos_frames():
   FILE_NAME = request.args.get('filename')
   with zipfile.ZipFile('Frames/Zips/' + FILE_NAME + '-TodosFrames.zip','w') as zipf:
      for root,dirs,files in os.walk('Frames/Todos/'):
         for file in files:
            if(FILE_NAME.lower() in file.lower()):
               zipf.write('Frames/Todos/' + file)
   return send_file('Frames/Zips/' + FILE_NAME + '-TodosFrames.zip',
            mimetype = 'zip',
            attachment_filename= 'TodosFrames.zip',
            as_attachment = True)

#Arquivo com todos os keyframes
@app.route('/key_frames')
def key_frames():
   FILE_NAME = request.args.get('filename')
   with zipfile.ZipFile('Frames/Zips/' + FILE_NAME + '-KeyFrames.zip','w') as zipf:
      for root,dirs,files in os.walk('Frames/Keyframes/'):
         for file in files:
            if(FILE_NAME.lower() in file.lower()):
               zipf.write('Frames/Keyframes/' + file)
   return send_file('Frames/Zips/' + FILE_NAME + '-KeyFrames.zip',
            mimetype = 'zip',
            attachment_filename= 'KeyFrames.zip',
            as_attachment = True)

if __name__ == '__main__':
   app.run(debug = True)