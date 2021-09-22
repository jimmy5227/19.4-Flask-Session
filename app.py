from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'HelloWorld'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []
questionsArray = surveys.satisfaction_survey.questions


@app.route('/')
def index():
    RESPONSES.clear()
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions
    return render_template('start.html', title=title, instructions=instructions)


@app.route(f'/questions/<questionnum>')
def questions(questionnum=0):
    questionnum = int(questionnum)
    if questionnum not in range(len(questionsArray)) and len(RESPONSES) < len(questionsArray):
        flash('That is not a valid survey question')
        return redirect(f'/questions/{len(RESPONSES)}')
    elif len(RESPONSES) not in range(len(questionsArray)):
        return redirect('/thanks')
    else:
        question = surveys.satisfaction_survey.questions[len(
            RESPONSES)].question
        return render_template('questions.html', question=question)


@app.route('/answer', methods=['POST'])
def answer():
    choice = request.form.get('answer')
    RESPONSES.append(choice)
    return redirect(f'/questions/{len(RESPONSES)}')


@app.route('/thanks')
def thanks():
    return 'Thank you!'
