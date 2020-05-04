from Application import app
from Application import models
from Application.decorators.authenticate import authenticate
from flask import request, render_template, redirect, flash, session
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
# making a files directory to keep things tidy. Also easy to add in gitignore
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

@app.route('/createAssignment', methods=['GET', 'POST'])
@authenticate
def createAssignment():
    if request.method == 'GET':
        return render_template('create_assignment_modal.html')
    else:
        formData = request.form
        assignmentName = formData['assignmentName']
        assignmentDesc = formData['assignmentDesc']

        # We need to include time here as well. When u change it to that,
        # I'll add time in html modal as well
        assignmentDeadline = datetime.strptime(formData['assignmentDeadline'], '%Y-%m-%d')

        print(assignmentName, assignmentDesc, assignmentDeadline)

        if assignmentDesc == '' or assignmentName == '':
            flash('assignment fields empty')
            return 'assignment fields empty'

        newAssignment = models.Assignment()
        newAssignment.assignmentDesc = assignmentDesc
        newAssignment.assignmentName = assignmentName
        newAssignment.assignmentDeadline = assignmentDeadline

        files = request.files.getlist("files")

        # this is needed to create dir if it doesn't exist, otherwise file.save fails.
        assignmentDir = os.path.join(PROJECT_DIR, ASSIGNMENT_UPLOAD_FOLDER)
        if not os.path.exists(assignmentDir):
            os.makedirs(assignmentDir)

        for file in files:
            # for some reason when not uploading any file it was still reaching this code
            # with an empty file so I included this check for now
            if file:
                path = os.path.join(assignmentDir, secure_filename(file.filename))
                file.save(path)
                newAssignmentFile = models.AssignmentFile()
                newAssignmentFile.filePath = path

                newAssignment.assignmentFiles.append(newAssignmentFile)

        models.db.session.add(newAssignment)
        models.db.session.commit()
        return 'uploaded!'
