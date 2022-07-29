from http.client import responses
import re
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# responses =[]; #this is a list of answer in one session

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 


debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """Select a survey"""

    return render_template("survey_start.html", survey= survey)


@app.route("/begin")
def start_survey():
            # """REDIRECT THE user to question/0"""
            # # return"yes"
            # return redirect ("/question/0")


    """Clear the sessions of previous responses or data"""
    session[RESPONSES_KEY] =[]

    return redirect ("/question/0")


@app.route ("/question/<int:qid>")
def display_question(qid):
            # # return "I am here"
            # """Display the question number {{qid}}"""

            #     #Protecting Questions:
            #     #If a user try to jump question withought answering some through browser
            #     #or if they try to access questions that doesn't exist redirect them to correct url

            # if (qid != len(responses)):
            #     qid =len(responses)
            #     # flash ("Survey questions needs to be answered in order") QQ
            #     return redirect (f"/question/{len(responses)}")

            # return render_template("questions.html", q=survey.questions[qid])
   
    """Display the question number {{qid}}"""
    
    #get the session info
    responses = session[RESPONSES_KEY]

    if responses is None:
        #there is no answer in the list
        #trying to access question page too soon
        #redirect to home page to begin the survey
        return redirect ("/")
    
    if len(responses) == len (survey.questions) :
        #they have answered all the questions and send them to thank you page
        return redirect ("/complete")

    if len(responses) != qid:
        #Trying to access questions out of order
        flash (f"Invalid question id: {qid}")
        return redirect (F"/question/{len(responses)}")

    #else send them to the question page and display the next question
    return render_template("questions.html", q=survey.questions[qid])

    



@app.route ("/answer", methods =["POST"])
def handle_question():
            # """append the response to responses list and redirect to next ques"""
            # ans = request.form["answer"]
            # # return ans
            # responses.append(ans);

            # #redirect to next ques
            # # return str(len(responses))
            # if len(responses) == len(survey.questions):
            #     """redirect them to a simple Thank you page"""
            #     return render_template("thankyou.html")

            # return redirect (f"/question/{len(responses)}")
    # print (f"***Q number is *** ")
    # print(f"session info {session[RESPONSES_KEY]}")


    """Save respoinse and redirect to next question"""

    #get the response choice
    choice = request.form["answer"];

    # Add the response to the session
    responses = session[RESPONSES_KEY]  #this basically creates an empty list refer to code ln 36 (only for 1st ques)
    responses.append (choice) #appeded the first choice as the
    session[RESPONSES_KEY] = responses; #now the current session will hold a list and is not empty anymore
    
    # print (f"***Q number is {len(responses)} *** ")
    # print(f"session info {session[RESPONSES_KEY]}")
    #Check if all the survey questions has been answered
    if len(responses) == len(survey.questions):
        #All the questions has been answered
        return redirect("/complete");
    
    else:
        #There are more questions that needs to be answered so redirect to next question
        # print (f"***now entering questions html with ques no {len(responses)} *** ")
        # print(f"session info {session[RESPONSES_KEY]}")
        return redirect(f"question/{len(responses)}")


@app.route ("/complete")
def complete():
    """survey complete. Show thank you page"""

    return render_template("thankyou.html")
