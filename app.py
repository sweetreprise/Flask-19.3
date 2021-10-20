from flask import Flask, render_template, redirect, request, flash, url_for
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def survey_start():
    """show homepage for survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions 

    return render_template('home.html', title = title, instructions = instructions)

@app.route('/questions/<int:num>')
def show_questions(num):
    """routes user to questions in the survey.
    if user attempts to access invalid questions, or questions no in order,
    they will be redirected
    """
    length_of_survey = len(satisfaction_survey.questions)
    length_of_responses = len(responses)

    if num == length_of_responses and length_of_responses != length_of_survey:
        question = satisfaction_survey.questions[num].question
        choose_yes = satisfaction_survey.questions[num].choices[0]
        choose_no = satisfaction_survey.questions[num].choices[1]

    elif num > length_of_responses or num < length_of_responses:
        flash('Invalid url', 'error')

        return redirect(f'/questions/{length_of_responses}')
        
    else:
        return redirect('/thankyou')

    return render_template('question.html', question = question, yes = choose_yes, no = choose_no, num = num)

@app.route('/answer')
def submit_answer():
    """stores user's answers in responses list, then redirects to next question"""
    ans = request.args['answer']
    num = request.args['num']
    responses.append(ans)

    return redirect(f'/questions/{int(num) + 1}')

@app.route('/thankyou')
def thank_user():
    """directs user to thank you page upon survey completion"""
    return render_template('thankyou.html')







