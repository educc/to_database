import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, Course, Topic, Exam, Question, QuestionDetail, ExamQuestion


def create_course():
    return Course(
        name="Course1", 
        description="created by todb.py",
        createdBy="todb.py",
        createdDate=datetime.utcnow(),
        deleted=0,
        version=0)

def create_exam(mycourse):
    return Exam(
        course = mycourse,
        name="Exam1", 
        description="created by todb.py",
        examCode="some code",
        examApprovalTerm=100,
        examApprovalType="FIX.PERC",
        examStatusTypeId="ACTIVO",
        questions=0,
        duration=30,
        createdBy="todb.py",
        createdDate=datetime.utcnow(),
        deleted=0,
        version=0)

def create_topic(mycourse):
    return Topic(
            course = mycourse,
            name="Topic1",
            description="created by todb.py",
            weight=100,
            topicCode="some topiccode",
            createdBy="todb.py",
            createdDate=datetime.utcnow(),
            deleted=0,
            version=0)

def create_examquestion(myexam, myquestion):
    return ExamQuestion(
        exam = myexam, 
        question = myquestion,
        createdBy="todb.py",
        createdDate=datetime.utcnow(),
        deleted=0,
        version=0
    )

def create_question(mytopic, question_data):
    feedback = None
    if 'feedback' in question_data:
        feedback = question_data['feedback']
    return Question(
            topic = mytopic,
            description = question_data['question'].strip(),
            questionLevelTypeId = "BASICO",
            questionTypeId = None,
            descriptionAnswer = feedback ,
            questionCorrectAnswer = question_data['correct'].strip(),
            createdBy="todb.py",
            createdDate=datetime.utcnow(),
            deleted=0,
            version=0
        )

def create_question_options(myquestion,options_data):
    xlist = [] 
    for i, item in enumerate(options_data):
        option_item = QuestionDetail(
            question = myquestion,
            optionNumber = i+1,
            optionDescription = item.strip(),
            deleted=0,
            version=0,
            createdBy="todb.py",
            createdDate=datetime.utcnow(),
        )
        xlist.append(option_item)
    return xlist

def import_data(data):
    """
        example of 'data' argument
        [
            {
                "options":[
                    str,
                    str
                ],
                "question": str,
                "correct":str,
                "feedback": str
            },
    """
    
    session = Session(engine)

    try:
        course = create_course()
        exam = create_exam(course)
        topic = create_topic(course)

        nquestions = 0
        for question_obj in data:
            nquestions += 1
            question = create_question(topic,question_obj)

            if question.questionCorrectAnswer.count(',') > 0:
                question.questionTypeId = "OPC.MULT"
            else:
                question.questionTypeId = "OPC.UNICA"
            examquestion = create_examquestion(exam, question) 

            create_question_options(question, question_obj['options'])
        exam.questions = nquestions
        session.add(course)
        session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()

def main():
    print(sys.argv)
    if len(sys.argv) <= 1:
        print("need more params")
        print("todb.py filename_data.json")
    else:
        data = None
        with open(sys.argv[1]) as myfile:
            data = json.loads(myfile.read())
        import_data(data)

if __name__ == "__main__":
    main()

