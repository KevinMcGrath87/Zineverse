from flask_app.models import user, zine
from flask_app.__init__ import app
from flask import render_template, redirect, session, flash, request, send_from_directory
import os
from werkzeug.utils import secure_filename
# app.config['UPLOAD_FOLDER']
# rootDirectory = os.path.dirname(os.getcwd())
# library = os.path.join(rootDirectory,'solo_project','flask_app','assets')
# allowed_extensions = {'png','jpg','jpeg','svg'}
from flask_app.config.utils import UPLOAD_FOLDER, ALLOWED_EXTENSIONS


@app.route('/create_zine', methods =['POST'])
def create_zine():
    data = request.form.to_dict()
    data['users.id']=(session['user'])
    # data should com in as a dictionary containing the title and author.
    if zine.Zine.validate_zine(data,session['user']):
        os.mkdir(os.path.join(UPLOAD_FOLDER, data['title']))
        data['path']= os.path.join(UPLOAD_FOLDER, data['title'])
        zine.Zine.save(data)
        return(redirect('/profile'))
    return(redirect('/profile'))

@app.route('/upload', methods = ['POST'])
def upload():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
    if 'file' not in request.files:
        flash('no file')
        return(redirect('/profile'))
    file = request.files['file']
    zineId = request.form['zine']
    zineDict = (zine.Zine.get_by_id(zineId))[0]
    selectedZine = zine.Zine(zineDict)
    zinePath = selectedZine.path
    # need a length of number of pages in the zine..
    length = len(os.listdir(zinePath))
    if file.filename == '':
        flash('no file selected')
        return(redirect('/profile'))
    if file and allowed_file(file.filename):
        namesplit = file.filename.rsplit('.',1)
        namesplit[0]=str(length)
        file.filename = namesplit[0] + '.' + namesplit[1]
        securedFilename = secure_filename(file.filename)
    # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(os.path.join(UPLOAD_FOLDER, selectedZine.title, securedFilename))
        return(redirect('/profile'))
    else:
        flash('issues with file upload. likely an incorrect filetype.')
        return(redirect('/profile'))
    
@app.route('/insert/page/<int:id>/<int:index>', methods = ['GET', 'POST'])
def insert(id, index):
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
    if 'file' not in request.files:
        flash('no file')
        return(redirect(f'/edit/{id}'))
    file = request.files['file']
    zineId = id
    zineDict = (zine.Zine.get_by_id(zineId))[0]
    selectedZine = zine.Zine(zineDict)
    zinePath = selectedZine.path
    zinePages = os.listdir(zinePath)
    # #need index of postiton to insert page
    # index = len(os.listdir(zinePath))
    if file.filename == '':
        flash('no file selected')
        return(redirect(f'/edit/{id}'))
    if file and allowed_file(file.filename):
        namesplit = file.filename.rsplit('.',1)
        namesplit[0]=str(index)
        file.filename = namesplit[0] + '.' + namesplit[1]
        for page in range(len(zinePages)-1, index-1, -1):
            pageIncremented = zinePages[page].rsplit('.', 1);
            pageIncremented[0] = int(pageIncremented[0])+1
            print("the page number is now " + str(pageIncremented[0]))
            pageIncremented =str(pageIncremented[0])+'.'+pageIncremented[1]
            print("here we go " + pageIncremented)
            os.rename(os.path.join(zinePath,zinePages[page]),os.path.join(zinePath,pageIncremented))
        securedFilename = secure_filename(file.filename)
        print(securedFilename)
    # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(os.path.join(UPLOAD_FOLDER, selectedZine.title, securedFilename))
        return(redirect(f'/edit/{id}'))
    else:
        flash('issues with file upload. likely an incorrect filetype.')
        return(redirect(f'/edit/{id}'))




@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    zineData = (zine.Zine.get_by_id(id)[0])
    zineToEdit = zine.Zine(zineData)
    if request.method == 'GET':
        zinePath = zineToEdit.path
        pages = os.listdir(zinePath)
        print(zineToEdit)
        return(render_template('edit.html',zineToEdit = zineToEdit, pages = pages))
    if request.method == 'POST':
        # query function here.
        data = request.form.to_dict()
        newTitle = data['title']
        oldTitle = zineToEdit.title
        os.rename(os.path.join(UPLOAD_FOLDER, oldTitle),os.path.join(UPLOAD_FOLDER, newTitle))
        data['path']=os.path.join(UPLOAD_FOLDER, newTitle)
        zine.Zine.update_zine(data)
        return(redirect(f'/edit/{id}'))

@app.route('/delete/<int:id>',methods = ['POST'])
def delete(id):
    zineToDelete = zine.Zine(zine.Zine.get_by_id(id)[0])
    if zineToDelete.path == UPLOAD_FOLDER:
        flash('no can do. that this the root directory')
        return(redirect('/profile'))
    pages = os.listdir(zineToDelete.path)
    if pages:
        flash('directory is not empy')
        return(redirect(f'/edit/{id}'))
    zine.Zine.delete_zine(id)
    os.removedirs(zineToDelete.path)
    return(redirect('/profile'))

@app.route('/delete/page/<int:id>/<int:index>', methods =['POST'])
def delete_page(id,index):
    zineToDeleteFrom = zine.Zine(zine.Zine.get_by_id(id)[0])
    fileToDelete = os.listdir(zineToDeleteFrom.path)[index]
    deletePath = os.path.join(zineToDeleteFrom.path, fileToDelete)
    os.remove(deletePath)
    return(redirect(f'/edit/{id}'))




@app.route('/test')
def cwd():
    print(os.getcwd())
    print(UPLOAD_FOLDER)
    title ="a title!"
    print(f'{UPLOAD_FOLDER}\\{title}')
    return(redirect('/profile'))
    