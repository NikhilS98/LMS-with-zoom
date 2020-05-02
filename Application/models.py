from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum


# TODO: Add Backrefs

class UserRole(Enum):
    User = 1
    Admin = 2
class EnrollmentRole(Enum):
    Teacher = 1
    Student = 2


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "starburst"}

    userId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        nullabe=False
    )
    userRole = db.Column(Enum(UserRole))
    orgId = db.Column(db.Integer, db.ForeignKey('starburst.organizations.orgId'))
    organization = relationship("Organization")

class Organization(db.Model):
    __tablename__ = "organizations"
    __table_args__ = {"schema": "starburst"}

    orgId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    orgName = db.String(120)

class Course(db.Model):
    __tablename__ = "courses"
    __table_args__ = {"schema": "starburst"}

    courseId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseName = db.Column(
        db.String(250),
        index=True,
        nullable=False
    )

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = {"schema": "starburst"}

    enrollmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseId = db.Column(db.Integer, db.ForeignKey('starburst.courses.courseId'))
    course = relationship("Course")
    userId = db.Column(db.Integer, db.ForeignKey('starburst.user.userId'))
    user = relationship("User")

    enrollmentRole = db.Column(Enum(EnrollmentRole))

class Class(db.Model):
    __tablename__ = "classes"
    __table_args__ = {"schema": "starburst"}

    classId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    className = db.Column(
        db.String(250),
        nullable=False
    )
    recordingLink = db.Column(
        db.String(400)
    )
    classLink = db.Column(
        db.String(400)
    )
    courseId = db.Column(db.Integer, db.ForeignKey('starburst.courses.courseId'))
    course = relationship("Course")

class Resource(db.Model):
    __tablename__ = "resources"
    __table_args__ = {"schema": "starburst"}

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
    courseId = db.Column(db.Integer, db.ForeignKey('starburst.courses.courseId'))
    course = relationship("Course")


class Assignment(db.Model):
    __tablename__ = "assignments"
    __table_args__ = {"schema": "starburst"}

    assignmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    assignmentName = db.Column(
        db.String(250),
        nullable=False
    )
    deadline = db.Column(
        db.DateTime
    )
    courseId = db.Column(db.Integer, db.ForeignKey('starburst.courses.courseId'))
    course = relationship("Course")

class AssignmentFile(db.Model):
    __tablename__ = "assignment_files"
    __table_args__ = {"schema": "starburst"}

    assignmentFileId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    filePath = db.Column(
        db.String(250),
        nullable=False
    )
    assignmentId = db.Column(db.Integer, db.ForeignKey('starburst.assignments.assignmentId'))
    assignment = relationship("Assignment")

class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"
    __table_args__ = {"schema": "starburst"}

    assignmentSubmissionId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    assignmentId = db.Column(db.Integer, db.ForeignKey('starburst.assignments.assignmentId'))
    assignment = relationship("Assignment")
    userId = db.Column(db.Integer, db.ForeignKey('starburst.user.userId'))
    user = relationship("User")

    gradeReceived = db.Column(
        db.String(10)
    )

