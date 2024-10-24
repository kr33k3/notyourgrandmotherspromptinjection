import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, DATETIME, Uuid, Boolean
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import SQLAlchemyError
import urllib
from datetime import datetime
from typing import Optional, List


from logging_wrapper import logging_wrapper
import pyodbc

pyodbc.pooling = False
load_dotenv()

__username = os.getenv('DATABASE_USER')
__password = os.getenv('DATABASE_PASSWORD')
__database_name = os.getenv('DATABASE_NAME')
__server_name = os.getenv('DATABASE_SERVER')

__obdc_driver = 'ODBC Driver 17 for SQL Server' ## Depending on the build agent or windows machine your on. Put 'ODBC Driver 17 for SQL Server' if you don't know.

__params = urllib.parse.quote_plus(r'Driver={' + __obdc_driver +
                                 '};Server=tcp:' + __server_name +
                                 ',1433;Database=' + __database_name +
                                 ';Uid=' + __username +
                                 ';Pwd=' + __password +
                                 ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryServicePrincipal;')

__connection_string = 'mssql+pyodbc:///?odbc_connect={}'.format(__params)
engine = create_engine(__connection_string, pool_recycle=1500)

## Check DB engine connectivity
try:
    engine.connect()
    logging_wrapper.logger.info("DATABASE ENGINE CREATED AND CONNECTED")
except SQLAlchemyError as err:
    logging_wrapper.logger.error("DATABASE ENGINE FAILED TO CONNECT" + str(err.__cause__))

class Base(DeclarativeBase):
    ## TODO - Can we move all the shared columns to this class? Id, CreatedDate, CreatedById, etc
    ## Rename as to_dict
    def as_dict(self):
       return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    pass

class User(Base):
    __tablename__ = 'Users'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Username: Mapped[str] = mapped_column(String(50))
    Password: Mapped[str] = mapped_column(String(64))
    Salt: Mapped[str] = mapped_column(String(64))
    ProfileId: Mapped[int] = mapped_column(ForeignKey("Profiles.Id"), unique=True, nullable=False)
    Profile: Mapped["Profile"] = relationship(back_populates="User", single_parent=True)
    UserRoleId: Mapped[int] = mapped_column(ForeignKey("UserRoles.Id", use_alter=True), nullable=False)
    UserRole: Mapped["UserRole"] = relationship(back_populates="Users", foreign_keys=[UserRoleId])
    Candidate: Mapped["Candidate"] = relationship(back_populates="User")
    UserCourseStatuses: Mapped[List["UserCourseStatus"]] = relationship(back_populates="User")
    #UserAssignmentStatuses: Mapped[List["UserAssignmentStatus"]] = relationship(back_populates="User")
    CreatedDate: Mapped[Optional[datetime]] = mapped_column("CreatedDate", default=func.now()) ## as_dict python field name and table name
    UpdatedDate: Mapped[Optional[datetime]] = mapped_column(default=func.now()) ## Same thing as the above field
    #ResetPassword: Mapped[bool] = mapped_column(Boolean())

class Profile(Base):
    __tablename__ = 'Profiles'
    Id: Mapped[int] = mapped_column(primary_key=True)
    GraphId: Mapped[Uuid] = mapped_column(Uuid, unique=True, nullable=False)
    User: Mapped["User"] = relationship(back_populates="Profile")
    Name: Mapped[str] = mapped_column(String(200))
    Description: Mapped[str] = mapped_column(String(2000), nullable=True)
    GroupProfile: Mapped["GroupProfile"] = relationship(back_populates="Profile")
    CreatedDate: Mapped[datetime] = mapped_column("CreatedDate", default=func.now())
    UpdatedDate: Mapped[datetime] = mapped_column(default=func.now())

class GroupProfile(Base):
    __tablename__ = 'GroupProfiles'
    Id: Mapped[int] = mapped_column(primary_key=True)
    ProfileId: Mapped[int] = mapped_column(ForeignKey("Profiles.Id"), unique=True, nullable=False)
    Profile: Mapped["Profile"] = relationship(back_populates="GroupProfile", single_parent=True)
    CreatedDate: Mapped[datetime] = mapped_column("CreatedDate", default=func.now())
    UpdatedDate: Mapped[datetime] = mapped_column(default=func.now())

class Candidate(Base):
    __tablename__ = 'Candidates'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(50))
    UserId: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    User: Mapped["User"] = relationship(back_populates="Candidate", single_parent=True)
    Enabled: Mapped[bool] = mapped_column(default=True)

    CandidateCertifications: Mapped[List["CandidateCertification"]] = relationship(back_populates="Candidate")
    CandidateSkills: Mapped[List["CandidateSkill"]] = relationship(back_populates="Candidate")
    JobCandidates: Mapped[List["JobCandidate"]] = relationship(back_populates="Candidate")
    JobInvites: Mapped[List["JobInvite"]] = relationship(back_populates="Candidate")

class Certification(Base):
    __tablename__ = 'Certifications'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Description: Mapped[str] = mapped_column(String(256))

    CandidateCertifications: Mapped[List["CandidateCertification"]] = relationship(back_populates="Certification")

class CandidateCertification(Base):
    __tablename__ = 'CandidateCertifications'
    Id: Mapped[int] = mapped_column(primary_key=True)
    CandidateId: Mapped[int] = mapped_column(ForeignKey("Candidates.Id"))
    Candidate: Mapped["Candidate"] = relationship(back_populates="CandidateCertifications")
    CertificationId: Mapped[int] = mapped_column(ForeignKey("Certifications.Id"))
    Certification: Mapped["Certification"] = relationship(back_populates="CandidateCertifications")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class Skill(Base):
    __tablename__ = 'Skills'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Description: Mapped[str] = mapped_column(String(256))

    CandidateSkills: Mapped[List["CandidateSkill"]] = relationship(back_populates="Skill")

class CandidateSkill(Base):
    __tablename__ = 'CandidateSkills'
    Id: Mapped[int] = mapped_column(primary_key=True)
    CandidateId: Mapped[int] = mapped_column(ForeignKey("Candidates.Id"))
    Candidate: Mapped["Candidate"] = relationship(back_populates="CandidateSkills")
    SkillId: Mapped[int] = mapped_column(ForeignKey("Skills.Id"))
    Skill: Mapped["Skill"] = relationship(back_populates="CandidateSkills")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class Job(Base):
    __tablename__ = 'Jobs'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String(256))
    Description: Mapped[str] = mapped_column(String(256))
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

    JobCandidates: Mapped[List["JobCandidate"]] = relationship(back_populates="Job")
    JobInvites: Mapped[List["JobInvite"]] = relationship(back_populates="Job")

class JobCandidate(Base):
    __tablename__ = 'JobCandidates'
    Id: Mapped[int] = mapped_column(primary_key=True)
    JobId: Mapped[int] = mapped_column(ForeignKey("Jobs.Id"))
    Job: Mapped["Job"] = relationship(back_populates="JobCandidates")
    CandidateId: Mapped[int] = mapped_column(ForeignKey("Candidates.Id"))
    Candidate: Mapped["Candidate"] = relationship(back_populates="JobCandidates")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class JobInvite(Base):
    __tablename__ = 'JobInvites'
    Id: Mapped[int] = mapped_column(primary_key=True)
    JobId: Mapped[int] = mapped_column(ForeignKey("Jobs.Id"))
    Job: Mapped["Job"] = relationship(back_populates="JobInvites")
    CandidateId: Mapped[int] = mapped_column(ForeignKey("Candidates.Id"))
    Candidate: Mapped["Candidate"] = relationship(back_populates="JobInvites")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class Course(Base):
    __tablename__ = 'Courses'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String(256))
    Description: Mapped[str] = mapped_column(String(256))
    Slides: Mapped[List["Slide"]] = relationship(back_populates="Course")
    UserCourseStatuses: Mapped[List["UserCourseStatus"]] = relationship(back_populates="Course")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class Slide(Base):
    __tablename__ = 'Slides'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String(256))
    CourseId: Mapped[int] = mapped_column(ForeignKey("Courses.Id"))
    Course: Mapped["Course"] = relationship(back_populates="Slides")
    Order: Mapped[int]
    SlideContent: Mapped[List["SlideContent"]] = relationship(back_populates="Slide")
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class SlideContent(Base):
    __tablename__ = 'SlideContent'
    Id: Mapped[int] = mapped_column(primary_key=True)
    SlideId: Mapped[int] = mapped_column(ForeignKey("Slides.Id"))
    Slide: Mapped["Slide"] = relationship(back_populates="SlideContent")
    Order: Mapped[int]
    ContentUuid: Mapped[str] = mapped_column(String(36))
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class UserCourseStatus(Base):
    __tablename__ = 'UserCourseStatus'
    Id: Mapped[int] = mapped_column(primary_key=True)
    CourseId: Mapped[int] = mapped_column(ForeignKey("Courses.Id"))
    Course: Mapped["Course"] = relationship(back_populates="UserCourseStatuses")
    UserId: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    User: Mapped["User"] = relationship(back_populates="UserCourseStatuses")
    CompletedSlideOrder: Mapped[Optional[int]]
    AssignedDate: Mapped[datetime]
    StartedDate: Mapped[Optional[datetime]]
    CompletedDate: Mapped[Optional[datetime]]
    CreatedDate: Mapped[datetime]
    UpdatedDate: Mapped[Optional[datetime]]

class VideoComment(Base):
    __tablename__ = 'VideoComments'
    Id: Mapped[int] = mapped_column(primary_key=True)
    VideoGraphId = mapped_column(Uuid, nullable=False)
    ParentId: Mapped[int] = mapped_column(ForeignKey("VideoComments.Id"), nullable=True)
    Content: Mapped[str]
    VideoCommentReaction: Mapped['VideoCommentReaction'] = relationship(back_populates="VideoComment")
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy: Mapped["User"] = relationship()
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]

class VideoReaction(Base):
    __tablename__ = 'VideoReactions'
    Id: Mapped[int] = mapped_column(primary_key=True)
    VideoGraphId = mapped_column(Uuid, nullable=False)
    Likes: Mapped[int] = mapped_column(default=0)
    Dislikes: Mapped[int] = mapped_column(default=0)
    Views: Mapped[Optional[int]] = mapped_column(default=0, nullable=False)
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]
    UserReactions: Mapped[Optional[List["VideoUserReaction"]]] = relationship(back_populates="VideoReaction")

class VideoUserReaction(Base):
    __tablename__ = 'VideoUserReactions'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Like: Mapped[bool]
    Dislike: Mapped[bool]
    VideoReactionId: Mapped[int] = mapped_column(ForeignKey("VideoReactions.Id"))
    VideoReaction: Mapped["VideoReaction"] = relationship(back_populates="UserReactions")
    ReactedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    ReactedBy = relationship("User", foreign_keys=[ReactedById])
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy = relationship("User", foreign_keys=[CreatedById])
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]

class VideoCommentReaction(Base):
    __tablename__ = 'VideoCommentReactions'
    Id: Mapped[int] = mapped_column(primary_key=True)
    VideoCommentId: Mapped[int] = mapped_column(ForeignKey("VideoComments.Id"))
    VideoComment: Mapped["VideoComment"] = relationship(back_populates="VideoCommentReaction")
    Likes: Mapped[int]
    Dislikes: Mapped[int]
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]
    UserReactions: Mapped[Optional[List["VideoCommentUserReaction"]]] = relationship(back_populates="VideoCommentReaction")

class VideoCommentUserReaction(Base):
    __tablename__ = 'VideoCommentReactionUsers'
    Id: Mapped[int] = mapped_column(primary_key=True)
    VideoCommentReactionId: Mapped[int] = mapped_column(ForeignKey("VideoCommentReactions.Id"))
    VideoCommentReaction: Mapped["VideoCommentReaction"] = relationship()
    Like: Mapped[bool]
    Dislike: Mapped[bool]
    ReactedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    ReactedBy = relationship("User", foreign_keys=[ReactedById])
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy = relationship("User", foreign_keys=[CreatedById])
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]

class UserFavorite(Base):
    __tablename__ = 'UserFavorites'
    Id: Mapped[int] = mapped_column(primary_key=True)
    GraphId: Mapped[str]= mapped_column(Uuid, nullable=False)
    FavoritedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    FavoritedBy = relationship("User", foreign_keys=[FavoritedById])
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy = relationship("User", foreign_keys=[CreatedById])
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())

class UserRole(Base):
    __tablename__ = 'UserRoles'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(100))
    Users: Mapped[List["User"]] = relationship(back_populates="UserRole", foreign_keys=[User.UserRoleId])
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"), nullable=False)
    CreatedBy = relationship("User", foreign_keys=[CreatedById])
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    UpdatedById: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.Id"))
    UpdatedBy = relationship("User", foreign_keys=[UpdatedById])
    UpdatedDate: Mapped[Optional[datetime]]

class Prompt(Base):
    __tablename__ = 'Prompts'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String(256))
    Content: Mapped[str] = mapped_column()
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy: Mapped["User"] = relationship(foreign_keys=[CreatedById])
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedById: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.Id"))
    UpdatedBy: Mapped[Optional["User"]] = relationship(foreign_keys=[UpdatedById])
    UpdatedDate: Mapped[Optional[datetime]]

class QuizLab(Base):
    __tablename__ = 'QuizLabs'
    Id: Mapped[int] = mapped_column(primary_key=True)
    QuizName: Mapped[str] = mapped_column(String(100))
    PromptId: Mapped[int] = mapped_column(ForeignKey("Prompts.Id"))
    Prompt: Mapped["Prompt"] = relationship()
    Content: Mapped[str] = mapped_column(String)
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy: Mapped["User"] = relationship(foreign_keys=[CreatedById])
    UpdatedDate: Mapped[Optional[datetime]]
    UpdatedById: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.Id"))
    UpdatedBy: Mapped[Optional["User"]] = relationship(foreign_keys=[UpdatedById])

class QuizLabResult(Base):
    __tablename__ = 'QuizLabResults'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(100))  # User provided name
    QuizLabId: Mapped[int] = mapped_column(ForeignKey("QuizLabs.Id"))
    QuizLab: Mapped["QuizLab"] = relationship()
    Transcript: Mapped[str] = mapped_column(String)  # varchar(max)
    QuizScore: Mapped[str] = mapped_column(String(50), nullable=True)  # Adjust the length as needed
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    UpdatedDate: Mapped[Optional[datetime]]

class Assignment(Base):
    __tablename__ = 'Assignments'
    Id: Mapped[int] = mapped_column(primary_key=True)
    GraphId: Mapped[Uuid] = mapped_column(Uuid, nullable=False)
    DueDate: Mapped[datetime]
    UserAssignmentStatuses: Mapped[List["UserAssignmentStatus"]] = relationship(back_populates="Assignment")
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    CreatedBy: Mapped["User"] = relationship(foreign_keys=[CreatedById])
    UpdatedDate: Mapped[Optional[datetime]]
    UpdatedById: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.Id"))
    UpdatedBy: Mapped["User"] = relationship(foreign_keys=[UpdatedById])

class UserAssignmentStatus(Base):
    __tablename__ = 'UserAssignmentStatuses'
    Id: Mapped[int] = mapped_column(primary_key=True)
    AssignmentId: Mapped[int] = mapped_column(ForeignKey("Assignments.Id"))
    Assignment: Mapped["Assignment"] = relationship(back_populates="UserAssignmentStatuses", foreign_keys=[AssignmentId])
    UserId: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    User: Mapped["User"] = relationship(foreign_keys=[UserId])
    CompletedDate: Mapped[Optional[datetime]]
    CreatedDate: Mapped[datetime] = mapped_column(default=func.now())
    CreatedById: Mapped[int] = mapped_column(ForeignKey("Users.Id"), nullable=False)
    CreatedBy: Mapped["User"] = relationship(foreign_keys=[CreatedById])
    UpdatedDate: Mapped[Optional[datetime]]
    UpdatedById: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.Id"))
    UpdatedBy: Mapped["User"] = relationship(foreign_keys=[UpdatedById])
