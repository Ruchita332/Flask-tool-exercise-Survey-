from http.client import responses
import re
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

responses =[];

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
    """REDIRECT THE user to question/0"""
    # return"yes"
    return redirect ("/question/0")

@app.route ("/question/<int:qid>")
def display_question(qid):
    # return "I am here"
    """Display the question number {{qid}}"""

    #Protecting Questions:
    #If a user try to jump question withought answering some through browser
    #or if they try to access questions that doesn't exist redirect them to correct url

    if (qid != len(responses)):
        qid =len(responses)
        # flash ("Survey questions needs to be answered in order") QQ
        return redirect (f"/question/{len(responses)}")

    return render_template("questions.html", q=survey.questions[qid])

@app.route ("/answer", methods =["POST"])
def save_response():
    """append the response to responses list and redirect to next ques"""
    ans = request.form["answer"]
    # return ans
    responses.append(ans);

    #redirect to next ques
    # return str(len(responses))
    if len(responses) == len(survey.questions):
        """redirect them to a simple Thank you page"""
        return render_template("thankyou.html")

    return redirect (f"/question/{len(responses)}")








