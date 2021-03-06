import enum
from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import datetime


db.create_all()
db.session.commit()


# TODO: Add Backrefs

class UserRole(enum.Enum):
    User = 1
    Admin = 2
class EnrollmentRole(enum.Enum):
    Teacher = 1
    Student = 2


class User(db.Model):

    # TODO: Add Support for organizations later

    __tablename__ = "users"
    # __table_args__ = {"schema": "starburst"}

    userId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(100),
        index=True,
        nullable=False,
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255)
    )
    userRole = db.Column(Enum(UserRole))
    orgId = db.Column(db.Integer, db.ForeignKey('organizations.orgId'))
    organization = relationship("Organization")

class Organization(db.Model):
    __tablename__ = "organizations"
    # __table_args__ = {"schema": "starburst"}

    orgId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    orgName = db.String(120)

class Course(db.Model):
    __tablename__ = "courses"
    # __table_args__ = {"schema": "starburst"}

    courseId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseName = db.Column(
        db.String(120),
        index=True,
        nullable=False
    )
    courseDesc = db.Column(
        db.String(255),
        nullable=False
    )
    courseSemester = db.Column(
        db.String(50)
    )
    courseYear = db.Column(
        db.String(12),
    )

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    # __table_args__ = {"schema": "starburst"}

    enrollmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course", backref="enrollments")
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    user = relationship("User", backref="enrollments")

    enrollmentRole = db.Column(Enum(EnrollmentRole))

class Lecture(db.Model):
    __tablename__ = "lectures"
    # __table_args__ = {"schema": "starburst"}

    lectureId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    lectureName = db.Column(
        db.String(60),
        nullable=False
    )
    lectureAgenda = db.Column(
        db.String(255)
    )
    startDatetime = db.Column(
        db.DateTime,
        nullable=False
    )
    videoAccessKey = db.Column(
        db.String(50)
    )
    videoRoomId = db.Column(
        db.String(50)
    )
    hostLink = db.Column(
        db.String(400),
        nullable=False
    )
    guestLink = db.Column(
        db.String(400)
    )
    isRecordingActive = db.Column(
        db.Boolean
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course", backref="lectures")

class Recording(db.Model):
    __tablename__ = "lecture_recordings"

    recordingId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    identifier = db.Column(
        db.String(50),
        nullable=False
    )
    link = db.Column(
        db.String(400)
    )
    lectureId = db.Column(db.Integer, db.ForeignKey('lectures.lectureId'))
    lecture = relationship("Lecture", backref="recordings")

class Resource(db.Model):
    __tablename__ = "resources"
    # __table_args__ = {"schema": "starburst"}

    resourceId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    resourceName = db.Column(
        db.String(250),
        nullable=False
    )
    filePath = db.Column(
        db.String(250)
    )
    uploadedDate = db.Column(
        db.DateTime,
        nullable=False
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course")


class Assignment(db.Model):
    __tablename__ = "assignments"
    # __table_args__ = {"schema": "starburst"}

    assignmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    assignmentName = db.Column(
        db.String(120),
        nullable=False
    )
    assignmentDesc = db.Column(
        db.String(255),
        nullable=False
    )
    assignmentDeadline = db.Column(
        db.DateTime
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course", backref="assignments")
    totalMarks = db.Column(db.Float, nullable=False)
    uploadDateTime = db.Column(db.DateTime, nullable=False)

class AssignmentFile(db.Model):
    __tablename__ = "assignment_files"
    # __table_args__ = {"schema": "starburst"}

    assignmentFileId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    filePath = db.Column(
        db.String(250),
        nullable=False
    )
    fileName = db.Column(
        db.String(100)
    )
    assignmentId = db.Column(db.Integer, db.ForeignKey('assignments.assignmentId'))
    assignments = relationship("Assignment",backref='assignmentFiles')

class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"
    # __table_args__ = {"schema": "starburst"}

    assignmentSubmissionId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    submissionTime = db.Column(db.DateTime, nullable=False)
    assignmentId = db.Column(db.Integer, db.ForeignKey('assignments.assignmentId'))
    assignment = relationship("Assignment")
    assignmentGrade = db.Column(db.String(20))
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    user = relationship("User")
    comment = db.Column(db.String(500))

    gradeReceived = db.Column(
        db.String(10)
    )

class SubmissionFile(db.Model):
    __tablename__ = "submission_files"
    # __table_args__ = {"schema": "starburst"}

    submissionFileId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    filePath = db.Column(
        db.String(250),
        nullable=False
    )
    fileName = db.Column(
        db.String(255)
    )
    submissionId = db.Column(db.Integer, db.ForeignKey('assignment_submissions.assignmentSubmissionId'))
    submission = relationship("AssignmentSubmission", backref='submissionFiles')

