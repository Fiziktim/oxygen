#version bourrin (mais où on se fait moins chier avec les freeze requirements): import flask, pymongo, json, bson, random, time, datetime, werkzeug
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
#from flask_mongoengine import MongoEngine
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import json
import bson
import random
import time

app = Flask(__name__)
app.secret_key = "d§èijhgcfd2456)" #For sessions. Used to encrypt session data.
bullshitery = True
#app.permanent_session_lifetime = timedelta(days=30) #erases permanent session data after 30 days (can also be set to minutes)

cluster = MongoClient("mongodb+srv://fiziktim:O2zcT4Zkj8pa1SeKzt@cluster0.u8nkh.azure.mongodb.net/questions_mdb?retryWrites=true&w=majority")
db = cluster["questions_mdb"]
collection = db["questions_new"]
collection_stats = db["stats"]
collection_tags = db["tags"]

def print_all_documentTags_CountIDs(): # WORKS
    results = collection_tags.find({})
    print("\n")
    for result in results:
        print(str(result["CountID"]) + " : " + str(result["Names"]["english"][0]))
    print("\n")

def find_tag_CountID_by_main_english_name(tagName): # WORKS
    results = collection_tags.find({'Names.english': tagName})
    for result in results:
        return result["CountID"]

def find_tag_name_by_array_CountID(CountID): # WORKS
    return collection_tags.find_one({"CountID":CountID})["Names"]["english"][0]

def backup_collection(collection_name,backup_collection_name): # WOEKS
    a_collection = db[collection_name]
    b_collection = db[backup_collection_name]
    to_backup = a_collection.find({})
    for result in to_backup:
        b_collection.insert_one(result)
# WORKS : backup_collection("questions_new", "questions_backup")

#db.collection.rename({"questions"})

def add_or_overrite_new_field_to_every_doc_in_collection(field, value_of_field): # WORKS
    i = 0
    results = collection.find({})
    for result in results:
        i += 1
        print(i)
        collection.update_one(result, {"$set":{str(field): value_of_field}})
        print(collection.find_one({"_id": result["_id"]}))

def remove_malicious_characters(string): # WORKS
    old_string = string
    new_string = ""
    for char in old_string:
        if char == "\"":
                char = "\\\""
        if char == ("\\"):
            char = ""
        #print(char, end="")
        new_string = new_string + char
    return new_string

def BaseFunctionToCopyACollectionToANewOneToChangeHowIDsBehaveLikeReplacingObjectIDsByHereCountIDs(): # Works
    results = collection.find({})
    superI = 0
    for result in results:
        superI = superI + 1
        print(result["_id"])
        result["CountID"] = superI
        result.pop("_id", None)
        db["questions_new"].insert_one(result)
        print(result)

def incNumberOfSubmittedQuestions(): # WORKS
    collection_stats.update_one({"instance":"main"},{"$inc":{"number_of_questions_ever_submitted": 1}})

def NumberOfSubmittedQuestions(): # WORKS
    return collection_stats.find_one({"instance":"main"})["number_of_questions_ever_submitted"]

def incNumberOfSubmittedTags(): # WORKS
    collection_stats.update_one({"instance":"main"},{"$inc":{"number_of_tags_ever_submitted": 1}})

def NumberOfSubmittedTags(): # WORKS
    return collection_stats.find_one({"instance":"main"})["number_of_tags_ever_submitted"]

#print("\n" + str(NumberOfSubmittedQuestions()) + "\n")

def add_new_main_tag(english_tag_name): # Works ?
    incNumberOfSubmittedTags()
    count = NumberOfSubmittedTags()
    collection_tags.insert_one({"CountID": count, "Names": {"english": [english_tag_name]}})
    #print(collection_tags.find_one({"CountID": count}))
    print(english_tag_name)

def erase_session_data(): # Works
    session.pop("in_a_row", None)

def fuse_two_tags_in_english(main_tag,tag_to_fuse):
    #Add tag_to_fuse to the array of main_tag
    #Remove the tag document of tag_to_fuse
    #For all tag docs that have a higher ["CountID"] than tag_to_fuse_document["CountID"], remove 1 to their ["CountID"]
    #Search for all docs in questions where tag_to_fuse_document["CountID"] is present. If main_tag_documment["CountID"] is present in the array, remove tag_to_fuse_document["CountID"], if not, transform tag_to_fuse_document["CountID"] into main_tag_document["CountID"]
    #Remove one to the total_number_of_tags in stats
    return "ass"

def return_all_present_tags_with_their_CountIDs_or_just_the_tags(option_both, all_tags):
    results = collection_tags.find({})
    all_present_tags = []
    countID_array = []
    for result in results:
        CountID = result["CountID"]
        #print(str(CountID) + " : " + str(result["Names"]["english"][0]))
        for language in result["Names"]:
            if all_tags :
                for i in result["Names"][language]:
                    all_present_tags.append(i)
                    countID_array.append(CountID)
        if not all_tags:
            all_present_tags.append(result["Names"]["english"][0])
            countID_array.append(CountID)
    if option_both:
        super_array = [all_present_tags, countID_array]
    else:
        super_array = all_present_tags
    return super_array

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        field_to_use_and_display = ""
        session.permanent = True
        if "in_a_row" in session:
            print("IN_A_ROW is in session and equals to = " + str(session["in_a_row"]))
        else:
            session["in_a_row"] = 0
            print("DEFINED in_a_row to 0")
        requestMethod_firstChars = str(request.form)[22:]
        requestMethod_firstChars = requestMethod_firstChars[0:4]
        print(requestMethod_firstChars)
        if requestMethod_firstChars == "new_": # Inputing a new question
            new_question = request.form["new_question"]
            if new_question != "":
                new_isTrue = request.form["htmlTruth"]
                new_tags_string = request.form["tags"]
                new_tags_string = new_tags_string + ","
                new_tag = ""
                new_tags = []
                tag_end_char = False
                for char in new_tags_string:
                    if char == ("," or ";"):
                        print("met a \"" + char + "\"")
                        if new_tag != "":
                            new_tags.append(new_tag)
                            tag_end_char = True
                        new_tag = ""
                    else:
                        if tag_end_char:
                            tag_end_char = False
                        else:
                            new_tag = new_tag + char
                print("\n" + str(new_tags) + "\n")
                super_array = return_all_present_tags_with_their_CountIDs_or_just_the_tags(True, True)
                old_tags = super_array[0]
                old_tags_CountIDs = super_array[1]
                question_tag_array = []
                for new_tag in new_tags:
                    tagsAreSimillar = False
                    for old_tag in old_tags:
                        if new_tag.lower() == old_tag.lower():
                            i = old_tags.index(old_tag)
                            question_tag_array.append(old_tags_CountIDs[i])
                            tagsAreSimillar = True
                            break
                    if tagsAreSimillar == False:
                        print("No Match for the tag : " + str(new_tag + "\n"))
                        add_new_main_tag(new_tag)
                        question_tag_array.append(find_tag_CountID_by_main_english_name(new_tag))
                        print("Added new tag as main_tag_english : " + str(new_tag))
                print(question_tag_array)
                number = int(NumberOfSubmittedQuestions())
                new_question = remove_malicious_characters(new_question) #Against Injection attacks and to allow chars like """
                collection.insert_one({"CountID": number, "question": new_question, "isTrue": new_isTrue, "ToDisplay": True, "Tags": question_tag_array})
                incNumberOfSubmittedQuestions()
                print("\nAdded new question as question number " + str(number) + "\n")
            return redirect(url_for("pagex", testx=new_question))
        elif requestMethod_firstChars == "main": #The user clicked on "True" or "False" at the top
            random_id = random.randint(0, collection.count_documents({}))
            print("RANDOM_ID : " + str(random_id))
            question_to_display = collection.find_one({"CountID": random_id})
            print(question_to_display["isTrue"])
            print(request.form["mainTruth"])
            if str(request.form["mainTruth"]) == str(question_to_display["isTrue"]):
                session["in_a_row"] += 1
                in_a_row = session["in_a_row"]
                print("GG")
                print("\nIN_A_ROW = " + str(session["in_a_row"]) + "\n")
            else:
                session.pop("in_a_row", None) #removes the in_a_row session data
                in_a_row = 0
                return "<h5 style='color:darkred'>Wrong answer. You start from the beginning.</h5>"
                #Time to wait = 1 seconde time.sleep(5
            #question_to_display = {"question" : "Chibros del bengalos ?"}
            print("\n\n\n-------")
            tag_collection = return_all_present_tags_with_their_CountIDs_or_just_the_tags(False, False)
            return render_template("index.html", display_this_question=question_to_display["question"], in_a_row=in_a_row, tag_collection=tag_collection)
        elif requestMethod_firstChars == "uppe":
            in_a_row = 0
            field_to_use_and_display = request.form["upper_tags_content"]
            random_id = random.randint(0, collection.count_documents({})) # THIS LINE IS REPEATED
            question_to_display = collection.find_one({"CountID": random_id}) # THIS LINE IS REPEATED
            tag_collection = return_all_present_tags_with_their_CountIDs_or_just_the_tags(False, False) # THIS LINE IS REPEATED
            print("\n" + field_to_use_and_display + "\n")
            return render_template("index.html", display_this_question=question_to_display["question"], in_a_row=in_a_row, tag_collection=tag_collection, field_to_use_and_display=field_to_use_and_display) # THIS LINE IS REPEATED

    else:
        random_id = random.randint(0, collection.count_documents({}))
        question_to_display = collection.find_one({"CountID": random_id})
        #return render_template("index.html")
        print(question_to_display["question"])
        if "in_a_row" not in session: in_a_row = 0
        else : in_a_row = session["in_a_row"]
        tag_collection = return_all_present_tags_with_their_CountIDs_or_just_the_tags(False, False)
        return render_template("index.html", display_this_question=question_to_display["question"], in_a_row=in_a_row, tag_collection=tag_collection) #Knows to look in the file "templates"

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
    # Done : print("Quick ask to parents on how to send shit to a point colis. Check with Lluis to send the shit back to france")
    # Done : print("Check with rasmus when he can get someone. Then check with the dude.")
    # Done : print("do some quick shit on the rest of your wantodo")
    # Done : print("do more cool code")
    # Done : print("prepare bag")
    # print("Dude, the one page app could be an app just showing you your knowledge tree getting more and more precise. " + "\nAnd you can share this with a 'how prepared for life are you quizz', which is basically the exact same thing as what I have just described, but you select what's important (cf gkeep) and tell people if they got these skills. "+"\nSounds like a lack of focus abit here no ?")
    print("Make the new questions available by creating a better id system")
    print("Do some basic UX design. AT LEAST for the first page. Something easy to use. Nice looking. Cool. And that would make an easy transition into the next features. Should be responsive (PWA).")
    print("It seems that ideally, i'd recode that shit. (maybe learn a bit more first). After doing a bit of UX")

backlog()


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

'''
THE DRAGON'S FORMULA : (By Dot Lung) The formula that allows you to grow an instagram / anything account 
1) Dialogue : 
- It's about the conversation that you are trying to position yourself in. What are you gonna talk about, what are you not. Plan that. 
- What does this dialogue look like in Messenger, Whatsapp, youtube, the more personalized, the more that you can listen to your ideal customer. The more trust you would trust.
- You need people to know you, to like you, to trust you. The more conversation you have, the more visibility you'll get on these news fields.
- Learn how to have conversation with people : how to ask open-handed questions to get people to ...
2) Relatability : 
- The more relatable you are, the more likes you will get. [more reliability = more likes]
- Content that makes people feel an emotion. Make them feel !
- "How are you going to use your craft to make it relatable, sharable, so that your message can be more visible"
3) Authenticity :
- Being true to yourself 
- Being who you really are (NOT faking it till you make it (you're gonna attract the wrong type of followers))
- Make people feel like you know them.
4) Giving Value : The entire backbone 
- "Give, give, give, give ask." Honestly, a good rule is give 10 times more than you take. (sales rule with )
5) Opinion : 
- Sharing your opinion is a great way to put conversation and controversy. (a lot of politics do that hardcore by putting supper polarizing stuff) : dudewithsign only does that in a fun way with pics with cardboards with messages, has 7.4 million subscribers
Vérifié
6) Niche :
- Make your content for a niche of people !!





Scaling your sales. Or scaling your communication : [ONLY WHILE you have all the first 6 figuered out]
- 
'''

'''
results = collection.find({})
for result in results:
    if result["CountID"] > 67:
        collection.update_one({"CountID":result["CountID"]}, {"$inc": {"CountID":1}})
'''
