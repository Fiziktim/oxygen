from flask import Flask, render_template, request, jsonify, redirect, url_for
#from flask_mongoengine import MongoEngine
import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
import bson
import random
import time

app = Flask(__name__)
bullshitery = True

cluster = MongoClient("mongodb+srv://fiziktim:<iIOTevbwbB9YMeEw@cluster0.u8nkh.azure.mongodb.net/questions_mdb?retryWrites=true&w=majority")
db = cluster["questions_mdb"]
collection = db["questions"]

'''
results = collection.find({})
for result in results:
    print(result["question"])
'''

#collection.find

#lastId = db.collection.find().sort[{"_id":-1}].limit(1)

#lastId = db.collection.find_one({"$max": "_id"})
#superUnoptimizedDBQuery

#lastId = collection.find_one({"$sort": {"_id": -1}}) #"$max"
#lastId = collection.find_one({"$sort": {"$_id": -1}})     #"$max"
#find().sort({fieldName:1/-1}).limit(-1)
#print(str(lastId[0]["_id"]) + " PUUUUUUUUUUUUUTE")


#for i in lastId:
#    print(str(i["_id"]) + " PUUUUUUUUUUUUUTE")

#app.config['MONGO_URI'] = mongodb+srv://fiziktim:<O2PN6frbiTEVocPTdw>@cluster0.u8nkh.azure.mongodb.net/<dbname>?retryWrites=true&w=majority

#db = MongoEngine()
#db.init_app(app)


#-- DB experimentation 

#-- /end DB experimentation

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        #if (request.form["mainFalse"]=="False" or request.form["mainTrue"]=="True") == False:
        requestMethod_firstChars = str(request.form)[22:]
        requestMethod_firstChars = requestMethod_firstChars[0:4]
        print("\nPUUUUUTE RequestMethod_firstChars = " + requestMethod_firstChars + "\n")
        if requestMethod_firstChars == "new_":
            new_question = request.form["new_question"]
            new_isTrue = request.form["htmlTruth"]
            if new_question != "":
                collection.insert_one({"question": new_question, "isTrue": new_isTrue})
            #db["users"].update({"$inc": {"number_of_questions_ever_submitted": 1}})
            #lastId = collection.find({"_id": "$max"})
            #for i in lastId:
            #    print(str(i["_id"]) + " PUUUUUUUUUUUUUTE")
            #new_question = request.form["True"]
            return redirect(url_for("pagex", testx=new_question))
            #return render_template("index.html")
        elif requestMethod_firstChars == "main": #The user clicked on "True" or "False"
            #if boutton == post_correspondant.isTrue:
                ###Bravo !
                #x =+ 1 in a row !!!!!
            #elif:
                #fail
                #Time to wait = 1 seconde time.sleep(5
                # return index
            random_id = random.randint(0, collection.count())
            question_to_display = collection.find_one({"_id": random_id})
            print(question_to_display["question"])
            #question_to_display = {"question" : "Chibros del bengalos ?"}
            return render_template("index.html", display_this_question=question_to_display["question"]) 
    else:
        random_id = random.randint(0, collection.count())
        question_to_display = collection.find_one({"_id": random_id})
        #return render_template("index.html")
        print(question_to_display["question"])
        return render_template("index.html", display_this_question=question_to_display["question"]) #Knows to look in the file "templates"


@app.route('/patapouf')
def chibre_du_bengale():
    if bullshitery == True:
        return '<h1>LES CHIBRES DU BENGAL SE DEPLACENT EN BANDE</h1>'
    else:
        return "Isn't that a sexy 4o4 tho ?"

@app.route('/test')
def test():
    return render_template('test.html', bIsActivated=bullshitery, uselessVariable=69, testList = ['Patrick, ', 'Michel, ', 'Gérard'], bullshitery=bullshitery)

@app.route('/admin')
def admin():
    if bullshitery == True:
        #return redirect("/PUUUUUUUUUUUUUUUTE")
        #or : 
        return redirect(url_for("pagex", testx="PUUUUUUUUUUUUTE"))
    else:
        return redirect(url_for("index"))

@app.route('/<testx>')
def pagex (testx):
    if bullshitery == True:
        return ('Bonjour, jeune <h1>' + testx + '</h1>')
    else:
        return ('Bonjour, jeune <h1>' + testx + '</h1>' + '\npss, 4o4 !'+ '\npss, 4o4')

if __name__ == '__main__':
    app.run(debug=True) #host='0.0.0.0', port=80, 

def backlog(): # You can make that shit vary of course
    # Done : print("make a quick pre-setup for db atoms")
    # Done : print("architect the structure of an atom")
    # Done : print("make the input function on the web page work")
    print("Quick ask to parents on how to send shit to a point colis. Check with Lluis to send the shit back to france")
    print("Check with rasmus when he can get someone. Then check with the dude.")
    print("do some quick shit on the rest of your wantodo")
    print("do more cool code")
    print("prepare bag")
    print("Dude, the one page app could be an app just showing you your knowledge tree getting more and more precise. " + "\nAnd you can share this with a 'how prepared for life are you quizz', which is basically the exact same thing as what I have just described, but you select what's important (cf gkeep) and tell people if they got these skills. "+"\nSounds like a lack of focus abit here no ?")


''' Ricardo Mendieta : Creative advertising
notes : 

"never look back at your slides" 

Nostalgia codak madmen salespitch

To sell your idea to a brand, talk the brand language.

Okay, if you're working with a brand, DO NOT have in your slides a competitor brand logo, or have a competito beer in your fridge...

"A client never buys the ideas, a client buys you."

You can ask a pr agency if you need to meet soeone. "We'll put you in the newspapers, you have to have this stuff on your social networks. And then you can try to get a meeting..."
Be really charming



A page for everyone on Oxygen (like a twitter wall, but where you only see the first question presented to you, where you can take a quizz from the knowledge of the person. (and get the most in a row))
Should say : "Teach the world something simple" - or - "Share your expertise" - or smthin like that (randomly, or A/B tested) - BETTER : "Share a small peice of your knowledge with people" - (Or "Share a glimse of your knowledge with people")

'''














#Atom and User architecture
'''
{"_id:": 26, "neutronId": 4, "protonsId": [4, 76, 159, 160, 161], "electronsId": [7, 63, 162, 165]}
or
{"_id:": 26, "neutronId": 4, "protonsId": [4, {"id:": 76, "probability": 0.73}, 159, 160, 161], "electronsId": [7, 63, 162, 165]} #The id + Probabilitty combo will probably 
or
{"_id:": 26, "neutronId": 4, "protonsId": [4, {"id:": 76, "opinions": [0, 0.25, 0.75, 0, 1, 0.25, 0, 0.25]}, 159, 160, 161], "electronsId": [7, 63, 162, 165], "tags": [{"tag": "economics", "opinions": [{"opinionId:" : 51304, "opinion": 0,75},{{"opinionId:" : 60217, "opinion": 1}}]},{}]} #The id + Probabilitty combo will probably 
or
#Recording what questions people have answered and when, and getting from this data, what question is where

{"_id": 0, "pseudoName": "Fiziktim", "questionsAnswered": [{"id": 42, "dateTime": "12h12-12/12/2069", "correctly": True},{"id": 69, "dateTime": "12h13-12/12/2069", "correctly": False}],"ipAdresses": [{"ip": 69.42.234.42, "fromDateTime": "12h12-12/12/2069", "toDateTime": "12h17-12/12/2069"},{"ip": 42.69.234.69, "fromDateTime": "15h12-13/12/2069", "toDateTime": "15h24-19/12/2069"}]}
'''




'''
for i in collection.find({}):
    question = i["question"]
    print(question)
    print(question[1])
    if str(question[1]) == "2":
        print("TO_CHANGE")
        new_question = question[2:]
        print(new_question)
        collection.update_one({"question": question}, {"$set": {"question": new_question}})
'''