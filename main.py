'''
AskMate Q&A website
by StormCoders
'''
from flask import Flask, request, redirect, render_template, flash
from db_manager import *
import psycopg2
from datetime import datetime
from queries import *

app = Flask(__name__)
app.secret_key = 'Stormcoders AskMate website is awesome'


@app.route('/')
@app.route('/index')
def index():
    '''
        Displays the questions as a table.
    '''
    table_headers = [
                    '#ID',
                    'Submission time',
                    'View number',
                    'Vote number',
                    'Title',
                    'Message',
                    'User',
                    'View',
                    'Delete',
                    'Vote Up',
                    'Vote Down'
                    ]
    query = select_questions_for_display
    view_questions = query_execute(query)
    return render_template('index.html', table_headers=table_headers, view_questions=view_questions)


@app.route('/question/new')
def new_question():
    '''
        Displays the question form page.
    '''
    return render_template('question_form.html')


@app.route('/new_question', methods=['POST'])
def add_new_question():
    '''
        Adds new question to the database.
    '''
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    question_title = request.form['q_title']
    question_message = request.form['q_message']
    query = insert_new_question
    data_to_modify = (dt, 0, 0, question_title, question_message, 0, 1)
    query_execute(query, data_to_modify, 'no_data')
    return redirect("/")


@app.route('/question/<q_id>', methods=['GET', 'POST'])
def display_question(q_id=None):
    '''
        Displays the question from the database, selected by q_id.
    '''
    q_table_headers = [
                    'Submission Time',
                    'View number',
                    'Vote number',
                    'Title',
                    'Message',
                    'Image'
                    ]
    a_table_headers = [
                    'ID',
                    'Submission Time',
                    'Vote number',
                    'Question Id',
                    'Message',
                    'Image',
                    'Delete'
                    ]
    question_id = [q_id]
    query = update_question_by_id
    query_execute(query, question_id, 'no_data')
    query = select_question_by_id
    view_question = query_execute(query, question_id)
    query = select_question_by_questionid
    view_answers = query_execute(query, question_id)
    return render_template(
                        'question.html',
                        q_id=q_id,
                        view_question=view_question,
                        q_table_headers=q_table_headers,
                        a_table_headers=a_table_headers,
                        view_answers=view_answers
                        )


@app.route('/question/<q_id>/delete')
def delete_question(q_id=None):
    '''
        Deletes the appropriate question.
        Removes a row from the table.
    '''
    query = delete_question_from_answers
    data_to_modify = [q_id]
    query_execute(query, data_to_modify, 'no_data')

    query = delete_question_from_question
    data_to_modify = [q_id]
    query_execute(query, data_to_modify, 'no_data')
    return redirect('/')


@app.route('/answer/<q_id>/<a_id>/delete')
def delete_answer(q_id=None, a_id=None):    # This function isn't working right now!!!
    '''
        Deletes the appropriate answer.
        Removes a row from the table.
    '''
    query = delete_answer_from_answer
    data_to_modify = [a_id]
    query_execute(query, data_to_modify, 'no_data')
    return redirect('/question/' + q_id)


@app.route('/question/<q_id>/vote-up')
def vote_up_question(q_id=None):
    '''
        Takes a vote up in the appropiate question.
        Adds 1 to the number in file.
    '''
    query = vote_up_question_by_id
    data_to_modify = [q_id]
    query_execute(query, data_to_modify, 'no_data')
    return redirect("/")


@app.route('/question/<q_id>/vote-down')
def vote_down_question(q_id=None):
    '''
        Takes a vote down in the appropiate question.
        Substracs 1 from the number in file.
    '''
    query = vote_down_question_by_id
    data_to_modify = [q_id]
    query_execute(query, data_to_modify, 'no_data')
    return redirect("/")


@app.route('/question/<q_id>/new-answer')
def display_answer(q_id=None):
    '''
        Displays the answer form page.
    '''
    query = display_answer_by_id
    data_to_modify = [q_id]
    view_questions = query_execute(query, data_to_modify)
    return render_template('answer_form.html', q_id=q_id, view_questions=view_questions)


@app.route('/question/new-answer/<q_id>', methods=['POST'])
def add_new_answer(q_id=None):
    """
    Add the new answer to database.
    """
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answer_message = request.form["answer_message"]
    query = insert_new_answer_to_database
    data_to_modify = (dt, 0, q_id, answer_message, 0)
    query_execute(query, data_to_modify, 'no_data')
    return redirect("/question/" + q_id)


@app.route('/registration')
def registration():
    '''
        Displays the registration page.
    '''
    return render_template('registration.html')


@app.route('/add_registration', methods=['POST'])
def add_registration():
    '''
        Adds the new user to the database.
    '''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    birth_date = request.form['bday']
    email = request.form['email']
    query = """INSERT INTO users (first_name, last_name, username, birth_date, email)\
                VALUES(%s, %s, %s, %s, %s);"""
    data_to_modify = (first_name, last_name, username, birth_date, email)
    query_execute(query, data_to_modify, 'no_data')
    return redirect("/")


@app.route("/user/<user_id>")
def display_user_page(user_id=None):
    user_id = [user_id]

    query = select_from_question
    selected_question_datas = query_execute(query, user_id)

    query = select_from_answer
    selected_answer_datas = query_execute(query, user_id)

    return render_template(
                            'user_page.html',
                            selected_answer_datas=selected_answer_datas,
                            selected_question_datas=selected_question_datas
                            )


@app.route('/all-user')
def all_user():
    '''
        Displays the all-user page.
    '''
    table_headers = [
                    'Id',
                    'First name',
                    'Last name',
                    'Username',
                    'Birth Date',
                    'Email',
                    'Reputation',
                    'View'
                    ]
    query = select_users
    list_users = query_execute(query, 'all_data')
    return render_template('all_user.html', table_headers=table_headers, list_users=list_users)


@app.errorhandler(404)
def page_not_found(error):
    return 'Missing', 404


if __name__ == '__main__':
    app.run(debug=True)
