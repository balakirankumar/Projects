from flask import Flask, render_template, request
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


chatbot = ChatBot(
    'Buddy',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry.Please contact balakirankumar999@gmail.com',
        'maximum_similarity_threshold': 1.0
        }
    ],
    database_uri='sqlite:///db_2.sqlite3')

training_data_college = open('training_data/College.txt').read().splitlines()
training_data_gretting = open('training_data/grettings.txt').read().splitlines()
training_data_more = open('training_data/more.txt').read().splitlines()


training_data = training_data_college + training_data_gretting + training_data_more

trainer = ListTrainer(chatbot)
trainer.train(training_data) 

trainer_corpus = ChatterBotCorpusTrainer(chatbot)

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/",methods=['GET','POST'] )
def home():
    if request.method=='POST' :
        mail=request.form.get('Your Email')
        os.system(f"python mail.py {mail}")
        return render_template("Ngit.html")
    return render_template("Ngit.html")

list1=["College Timings","Exam Notifications","Mids", "Cie",
"Branches","3-1 Materials","Soft Computing","Operating System","Artificial Intelligence","Computer Networks","Web And Internet Technologies","Automata Language And Computations",
"Software Engineering","Notice Board","Admissions","Ivth Sem Results","Results","Acdamic Info","Can You Tell Me About Acdamic Info","Exams Timtetable","Google",
"Infrastructure","Cse First Year Syllabus","Cse Second Year Syllabus","Cse Third1 Year Syllabus","It First Year Syllabus","It Second Year Syllabus","It Third1 Year Syllabus","Lab Externals","Phone Number",
"Eamcet Code","Address","What Is Fs?","Fs","What Is Sonet?","Sonet","What Is Cwd?","What Is Trishul?","Cwd","Trishul","Location","What Is Bec?","Bec","Placements","Transport","Images","Campus Images",
"3rd Year Online Class Recordings","Current College Schedule","Principal","College Timings","Chemistry Faculty","Physics Faculty","Hi","Who Are You?","Hello","What You Do?","Do You Know Hindi?","What Should I Ask You?","Byeeeee","Bye","Ttyl","Thank You",
"Who Created You?","Hello, I Am","What's Up?","I Am Fine","How Are You?","What Is Your Name?","Ok",
]
@app.route("/bot")
def bot():
    return render_template("bot.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userText = userText.title()
    # print(userText)
    if userText in list1:
        # print("got it")
        return str(chatbot.get_response(userText))
    
    return str(chatbot.get_response("Default Responce"))


