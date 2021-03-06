from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from markupsafe import escape
import os

from Application.decorators.authenticate import authenticate

RESOURCE_UPLOAD_FOLDER = 'resources'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))


@app.route('/downloadResource/<id>', methods=['GET'])
@authenticate
def downloadResource(id):
    fileId = escape(id)
    if not fileId:
        flash('send file id')
        return 'send file id'
    q = models.Resource.query.filter_by(resourceId=fileId).first()
    if not q:
        flash('No file found')
        return 'no file found'
    else:
        resource = q
        return send_file(resource.filePath, as_attachment=True)


# Get list of resources By Course
@app.route('/resources/<id>', methods=['GET'])
@authenticate
def getResourcesByCourse(id):
    resources = models.Resource.query.filter_by(courseId=id).all()
    return render_template('resources.html', resources=resources, course_id=id,
                           isTeacher=session['isTeacher'])


@app.route('/createResource/<courseId>', methods=['POST'])
@authenticate
def createResource(courseId):
    formData = request.form
    resourceName = formData['resourceName']


    cid = escape(courseId)
    resources = models.Resource.query.filter_by(courseId=cid).all()

    if resourceName == '':
        return render_template('resources.html', resources=resources, err_msg='Resource name cannot be left empty',
                               course_id=cid, show_modal=True, isTeacher=session['isTeacher'])

    newResource = models.Resource()
    newResource.resourceName = resourceName
    newResource.uploadedDate = datetime.utcnow() + timedelta(hours=5)
    newResource.courseId = cid

    file = request.files['file']
    # this is needed to create dir if it doesn't exist, otherwise file.save fails.
    resourceDir = os.path.join(PROJECT_DIR, RESOURCE_UPLOAD_FOLDER)
    if not os.path.exists(resourceDir):
        os.makedirs(resourceDir)

    if file:
        path = os.path.join(resourceDir, secure_filename(file.filename))
        file.save(path)
        newResource.filePath = path

        models.db.session.add(newResource)
        models.db.session.commit()
        flash("Resource uploaded")
        return redirect('/resources/' + cid)
    else:
        return render_template('resources.html', resources=resources, err_msg='Please upload a file',
                               course_id=cid, show_modal=True, resource_name=resourceName,
                               isTeacher=session['isTeacher'])


@app.route('/deleteResource/<courseId>/<id>', methods=["GET"])
@authenticate
def deleteResource(courseId, id):
    cid = escape(courseId)
    resourceId = escape(id)

    if not cid:
        return jsonify(success=True, msg='Course id is missing')
    elif not resourceId:
        return jsonify(success=True, msg='Please select a resource')
    else:
        resource = models.Resource.query.filter_by(resourceId=resourceId).first()
        if not resource:
            return jsonify(success=True, msg='Please select a resource')
        os.remove(resource.filePath)
        models.db.session.delete(resource)
        models.db.session.commit()
        flash("Successfully Deleted")

    return jsonify(success=True)
