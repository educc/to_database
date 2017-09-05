import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, Course, Topic, Exam, Question, QuestionDetail, ExamQuestion
import base64
import codecs

def create_course(data):
    return Course(
        name=data["course_name"], 
        courseCode=data["course_code"],
        cost=data['course_cost'],
        description="created by todb.py",
        createdBy="todb.py",
        language="EN",
        courseStatusTypeId="ACTIVE",
        createdDate=datetime.utcnow(),
        deleted=0,
        version=0)

def create_exam(mycourse,data):
    return Exam(
        course = mycourse,
        name=data['name'],
        examCode=data['code'],
        description="created by todb.py",
        examApprovalTerm=100,
        examApprovalType="FIX.PERC",
        examStatusTypeId="ACTIVE",
        questions=0,
        duration=data['duration'],
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
            description = get_question_desc(question_data['question']),
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

def get_question_desc(questionstr:str):
    result = questionstr.strip()
    if result.startswith('base64,'):
        allbytes = bytes(result[7:], "utf-8")
        result = base64.decodebytes(allbytes)
    return result


def import_data(data):
    """  require a specific json format, see example.json """
    session = Session(engine)
    nexam = 1
    nquestions = 0

    try:
        course = create_course(data)
        topic = create_topic(course)

        for exam_obj in data['exams']:
            exam = create_exam(course, exam_obj)

            nquestions = 0
            for question_obj in exam_obj['questions']:
                nquestions += 1
                question = create_question(topic,question_obj)

                if question.questionCorrectAnswer.count(',') > 0:
                    question.questionTypeId = "OPC.MULT"
                else:
                    question.questionTypeId = "OPC.UNICA"
                examquestion = create_examquestion(exam, question) 

                create_question_options(question, question_obj['options'])
            #end
            exam.questions = nquestions
            nexam += 1
        #end-for

        session.add(course)
        session.commit()
    except Exception as ex:
        print(f"Error on exam {nexam} and question {nquestions} ")
        print(ex)
        session.rollback()

def main():
    print(sys.argv)
    if len(sys.argv) <= 1:
        print("need more params")
        print("todb.py filename_data.json")
    else:
        data = None
        with codecs.open(sys.argv[1],"r","UTF-8") as myfile:
            data = json.loads(myfile.read())
        import_data(data)

if __name__ == "__main__":
    main()

