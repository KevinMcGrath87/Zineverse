import os
from flask_app.__init__ import app
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.getcwd()),'cd_final_project','flask_app','static','zinelib')
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg','svg'}