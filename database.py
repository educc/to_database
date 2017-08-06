from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

connectstr: str = ""
with open('connectstring.txt') as myfile:
    connectstr = myfile.readline().strip()

engine = create_engine(connectstr)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Course = Base.classes.course
Topic = Base.classes.topic
Exam = Base.classes.exam
ExamQuestion = Base.classes.examquestion
Question = Base.classes.question
QuestionDetail = Base.classes.questiondetail
