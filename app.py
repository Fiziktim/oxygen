#version bourrin (mais où on se fait moins chier avec les freeze requirements): import flask, pymongo, json, bson, random, time, datetime, werkzeug
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
#from flask_mongoengine import MongoEngine
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import json
import bson
import random
import time
import unicodedata

app = Flask(__name__)
app.secret_key = "d§èijhgcfd2456)" #For sessions. Used to encrypt session data. #THO UNSAFE, BECAUSE REALLY EASY TO DECRYPT : https://blog.miguelgrinberg.com/post/how-secure-is-the-flask-user-session --- Hash sensitive or hackable data. FOR NOW : VULNERABILITY 
bullshitery = True
linkitery = False
#app.permanent_session_lifetime = timedelta(days=30) #erases permanent session data after 30 days (can also be set to minutes)

cluster = MongoClient("mongodb+srv://fiziktim:O2zcT4Zkj8pa1SeKzt@cluster0.u8nkh.azure.mongodb.net/questions_mdb?retryWrites=true&w=majority")
db = cluster["questions_mdb"]
collection = db["questions_new"]
collection_stats = db["stats"]
collection_tags = db["tags"]
collection_users = db["users"]
PYTHONHASHSEED = 2821220674

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

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

def obvious_print(to_print):
    print('\n\n\nPUUUUUUUUUUUUUUUUUUUUTE : ' + str(to_print) + ' \n\n\n')

def add_or_overrite_new_field_to_every_doc_in_collection(field, value_of_field): # WORKS
    i = 0
    results = collection.find({})
    for result in results:
        i += 1
        print(i)
        collection.update_one(result, {"$set":{str(field): value_of_field}})
        print(collection.find_one({"_id": result["_id"]}))

def remove_malicious_characters(string, removeSpeChars = False): # WORKS
    string = str(string)
    string = string.strip(' ').strip('\\').strip('\r').strip('\t')

    if removeSpeChars:
        classical_chars = 'abcdefghijklmnopqrstuvwxyz-'
        classical_chars = list(classical_chars)
        for char in string.lower():
            if char not in classical_chars:
                string = string.replace(char, '')
    
    return string

def isEmailLegitimate(emailAdress):
    str(emailAdress)
    correctness = 0
    atDone = False
    lastDotDone = False
    if emailAdress[:1] == "@": #if emailAdress[:1] in ("@", "."):
        obvious_print("The first character is either @ or .")
        return False
    for char in emailAdress:
        if char == "@":
            if atDone == False:
                correctness += 1
                atDone = True
            else:
                return False
        elif char == "." and atDone and not lastDotDone:
            if lastDotDone == False:
                correctness += 1
                lastDotDone = True
        elif char == " ": #elif char in ("°", "é", "\'", "\"", "^", "¨", "$", "€", "*", "°", "#", "&")
            return False
    if correctness == 2:
        return True
    else:
        return False

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
            obvious_print("new_ request")
            new_question = request.form["new_question"]
            if new_question != "": 
                new_isTrue = request.form["htmlTruth"]
                new_source = remove_malicious_characters(request.form["source"])
                new_source_type = remove_malicious_characters(request.form["source_type"])
                try:
                    new_author = remove_malicious_characters(request.form["source_author"])
                except ValueError as ve:
                    obvious_print(ve)
                    new_author = None
                session["source_path"] = [{"new_source":new_source,"new_source_type":new_source_type,"new_author":new_author}]

                #####
                try:
                    new_source_2 = remove_malicious_characters(request.form["source_2"])
                    new_source_type_2 = remove_malicious_characters(request.form["source_type_2"])
                    try:
                        new_author_2 = remove_malicious_characters(request.form["source_author_2"])
                    except:
                        new_author_2 = None
                    
                    session["source_path"].append({"new_source":new_source_2,"new_source_type":new_source_type_2,"new_author":new_author_2})

                except:
                    pass
                #####

                new_tags_string = remove_malicious_characters(request.form["tags"])
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

                # Removes most perfect duplicates from input questions
                current_doc = {"CountID": number, "question": new_question, "isTrue": new_isTrue, "ToDisplay": True, "Tags": question_tag_array, "source_path": session["source_path"]} # After, we'll add a source chain
                if "inserted_questions" not in session:
                    session["inserted_questions"] = []
                if hash(str(current_doc["question"])) not in session["inserted_questions"]:
                    collection.insert_one(current_doc) # VULNERABILITY You can still get spammed with duplicates tho, if you don't watch out, this is only checking if they are duplicate in the session
                    session["inserted_questions"].append(hash(str(current_doc["question"]))) # Removed Vulnerability : Dunno how sessions work, but maybe you could get the session data of someone and know which questions they inserted. You still can but it's hashed now. You're welcome 
                    obvious_print( str(hash(str(current_doc["question"]))) + " is not in " + str(session["inserted_questions"]))
                else:
                    obvious_print( str(hash(str(current_doc["question"]))) + " is in " + str(session["inserted_questions"]))
                    return "<p>This question has already been inserted</p>"
                
                #obvious_print( str(session) + "\n" + str(session["inserted_questions"]) + "\n" + str(hash(str(current_doc["question"]))) ) #########

                incNumberOfSubmittedQuestions()
                print("\nAdded new question as question number " + str(number) + "\n")
            #return render_template("/")
            return redirect(url_for("pagex", testx=new_question))
        elif requestMethod_firstChars == "main": #The user clicked on "True" or "False" at the top
            obvious_print("main request")
            print("\n" + session["upper_tag"] + "\n")
            '''
            try:
                find_tag_CountID_by_main_english_name(request.form["upper_tags_content"])
            except:
                return "unexistant tag"'''



            #random_id = random.randint(0, collection.count_documents({}))
            #print("RANDOM_ID : " + str(random_id))
            #question_to_display = collection.find_one({"CountID": random_id})

            #question_to_display = collection.aggregate([{ '$sample': { 'size': 1 } }])

            tag_countID = find_tag_CountID_by_main_english_name(session['upper_tag'])
            print("TAG COUNTID : " + str(tag_countID))
            question_to_display = collection.aggregate([{ '$match': { 'Tags': tag_countID } },{ '$sample': { 'size': 1 } }])
            for finite in question_to_display:
                question_to_display = finite
            #obvious_print(find_tag_CountID_by_main_english_name(session['upper_tag']))

            main_source = "The ultimate mexican teacher"

            print(question_to_display["isTrue"])
            print(request.form["mainTruth"])
            obvious_print(main_source)
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
            return render_template("index.html", display_this_question=question_to_display["question"], in_a_row=in_a_row, tag_collection=tag_collection, main_source=main_source)
        elif requestMethod_firstChars == "uppe":
            obvious_print("uppe request")
            in_a_row = 0
            session["upper_tag"] = request.form["upper_tags_content"]
            random_id = random.randint(0, collection.count_documents({})) # THIS LINE IS REPEATED
            question_to_display = collection.find_one({"CountID": random_id}) # THIS LINE IS REPEATED
            tag_collection = return_all_present_tags_with_their_CountIDs_or_just_the_tags(False, False) # THIS LINE IS REPEATED
            print("\n" + session["upper_tag"] + "\n")
            return render_template("index.html", display_this_question=question_to_display["question"], in_a_row=in_a_row, tag_collection=tag_collection, field_to_use_and_display=session["upper_tag"], source_path=session["source_path"]) # THIS LINE IS REPEATED
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

@app.route('/<testx>')
def pagex(testx):
    return "Wesh" + testx

'''
@app.route('/<userName>')
@app.route('/<userName>/<fromAccountCreation>') #You can find a way to make the "fromAccountCreation" argument invisible
def userX(userName, fromAccountCreation=False): # Irrelevant, we need a email verification process.
    obvious_print("From account creation" + str(fromAccountCreation))
    if fromAccountCreation == False:
        username_list = collection_users.distinct('username', {}, {})
        if userName in username_list:
            return ('<h3>This is the home page of ' + userName + '</h3>') #You also need to make these a unique shot
        else:
            return "<p>This content is unavailable, or not anymore.<br><br><a href='/'>Get back to Oxygen</a></p>"
    else:
        return ('<h3>This is the home page of ' + userName + '</h3>') #You also need to make these a unique shot
'''

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ""
    if 'email_fkeep' not in session:
        session['email_fkeep'] = ""
    if request.method == 'POST':
        session['email_fkeep'] = remove_malicious_characters(request.form['email'])
        hashedPassword = hash(request.form['password'])
        obvious_print("Website POST :" + str(hashedPassword))
        user_doc = collection_users.find_one({'email':session['email_fkeep']})
        try:
            databaseHashedPassword = user_doc['hashed_password']
            obvious_print("Database :" + str(databaseHashedPassword))
            if databaseHashedPassword == hashedPassword:
                session["user_first_name"] = user_doc['first_name']
                session["user_last_name"] = user_doc['last_name']
                obvious_print(session)
                return "Login Sucessful"
            else:
                error = "Invalid Password"
                #return "<p>Wrong password. <a href='/login'>Back to logging in.</a></p>"
        except:
            error = "An account with this email does not exist yet."
            #return "<p>An account with this email does not exist yet.<br><br><!--If you don't have an account, you can create one it by clicking <a href='/create_an_account'>create account</a>.--><br><br>--> <a href='/login'>Back to logging in.</a> <--</p>"
    return render_template('login.html', error=error, email_field=session['email_fkeep'])

@app.route('/create_an_account', methods=['POST', 'GET'])
def create_an_account():
    error = ""
    if 'first_name_fkeep' not in session:
        session['first_name_fkeep'] = ""
    if 'last_name_fkeep' not in session:
        session['last_name_fkeep'] = ""
    if 'email_fkeep' not in session:
        session['email_fkeep'] = ""
    if request.method == 'POST':
        obvious_print("Request.method Passed. It's a POST.")
        obvious_print(request.form) #Hackable (password)
        session['first_name_fkeep'] = remove_malicious_characters(request.form['first_name'], True)
        session['last_name_fkeep'] = remove_malicious_characters(request.form['last_name'], True)
        session['email_fkeep'] = remove_malicious_characters(request.form['email'])
        session['username'] = strip_accents((session['first_name_fkeep'] + "_" + session['last_name_fkeep']).lower())
        hashedPassword = hash(request.form['password'])
        if session['first_name_fkeep'] == "" or session['last_name_fkeep'] == "" or session['email_fkeep'] == "" or hashedPassword == 0:
            return 'ARTHUR BORDEL !!!!!'
        #Then, we check if username exists already in list
        username_list = collection_users.distinct('username', {}, {})
        if session['username'] in username_list:
            session['username'] = session['username'] + "_0"
            userNameIncrement = 0
            while session['username'] in username_list:
                userNameIncrement += 1
                session['username'] = session['username'][:-1] + str(userNameIncrement)
        #Then, we check if email already exists in list.
        email_list = collection_users.distinct('email', {}, {})
        if not isEmailLegitimate(session['email_fkeep']):
            error = "Invalid email adress"
        elif session['email_fkeep'] in email_list:
            #return "<p>An account with this email already exists.<br><br><!--If you already have an account, you can access it by clicking <a href='/login'>login</a>.--><br><br>--> <a href='/create_an_account'>Back to creating my account.</a> <--</p>"
            error = "An account with this email adress already exists"
        else:
            collection_users.insert_one({"first_name": session['first_name_fkeep'], "last_name": session['last_name_fkeep'], "username": session['username'] ,"email": session['email_fkeep'], "hashed_password": hashedPassword, "verified_email":False})
            return "Here, we pretend that you're receiving an email confirmation. Once you have received it and clicked on the link, you can <a href='login'>Log in</a>."
            #return redirect(url_for("userX", userName="session['username']", fromAccountCreation=True)) # This will be obsolete
    return render_template('create_an_account.html', error=error, first_name_field=session['first_name_fkeep'], last_name_field=session['last_name_fkeep'], email_field=session['email_fkeep']) ####################################

@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')

@app.route('/admin')
def admin():
    if bullshitery == True:
        #return redirect("/PUUUUUUUUUUUUUUUTE")
        #or : 
        return redirect(url_for("pagex", testx="PUUUUUUUUUUUUTE"))
    else:
        return redirect(url_for("index"))

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

def cyber_security_warnings():
    print("\n\n")
    print("Cyber Security Warnings :")
    print("We use the classic python hash function. That's probably not a good thing.\nBecause people can hash passwords and know what's on our databases. If they manage to change the hashed password on the database, they can choose exactly the password they want.")
    print("\n\n")

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
