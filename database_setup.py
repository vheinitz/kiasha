import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_name = Column( String(50), nullable=False )
    user_password = Column( String(50), nullable=False )
    user_real_name= Column( String(50), nullable=False )
    user_email = Column( String(50) )
    user_group = Column( String(30), nullable=False )
    user_id = Column(Integer, primary_key = True)

class Question(Base):
    __tablename__ = 'question'
    question_short_text = Column( String, nullable=False )
    question_text = Column( String )
    question_instructions = Column( String )
    question_help = Column( String )
    question_answer_type = Column( String(50) )
    question_attachment_applicable = Column( Integer )
    question_comments_applicable = Column( Integer )
    question_user = Column(Integer, ForeignKey("user.user_id"))
    question_id = Column(Integer, primary_key = True)
    
class Survey(Base):
    __tablename__ = 'survey'
    survey_name = Column( String(200), nullable=False )
    survey_info = Column( String, nullable=False )
    survey_instructions = Column( String, nullable=False )
    survey_help = Column( String )
    survey_owner = Column(Integer, ForeignKey("user.user_id"))
    survey_id = Column(Integer, primary_key = True)
    
class SurveyQuestion(Base):
    __tablename__ = 'survey_question'
    survey_question_order = Column(Integer)
    survey_question_survey_id = Column(Integer, ForeignKey("survey.survey_id"))
    survey_question_question_id = Column(Integer, ForeignKey("question.question_id"))
    survey_question_id = Column(Integer, primary_key = True)
   

engine = create_engine( 'sqlite:///database.db' )
Base.metadata.create_all(engine)
