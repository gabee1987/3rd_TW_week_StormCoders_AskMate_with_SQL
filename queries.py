""" SQL handling Module"""


select_questions_for_display = """SELECT question.id, question.submission_time, question.view_number, question.vote_number,\
                                question.title, question.message, users.username, users.id\
                                FROM question\
                                LEFT JOIN users\
                                ON question.user_id=users.id\
                                ORDER BY question.submission_time DESC;"""

insert_new_question = """INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) \
                        VALUES(%s, %s, %s, %s, %s, %s, %s);"""

update_question_by_id = """UPDATE question SET view_number = view_number + 1\
                        WHERE id = %s;"""

select_question_by_id = """SELECT submission_time, view_number, vote_number, title, message, image FROM question\
                        WHERE id = %s;"""

select_question_by_questionid = """SELECT answer.id, answer.submission_time, answer.vote_number, answer.question_id, answer.message, users.username, answer.image\
                                FROM answer\
                                LEFT JOIN users\
                                ON answer.user_id=users.id\
                                WHERE question_id = %s;"""

delete_question_from_answers = """DELETE FROM answer WHERE question_id = %s;"""

delete_question_from_question = """DELETE FROM question WHERE id = %s;"""

delete_answer_from_answer = """DELETE FROM answer WHERE id = %s;"""

vote_up_question_by_id = """UPDATE question SET vote_number = vote_number + 1 WHERE id = %s;"""

vote_down_question_by_id = """UPDATE question SET vote_number = vote_number - 1 WHERE id = %s;"""

display_answer_by_id = """SELECT title, message FROM question WHERE id = %s;"""

insert_new_answer_to_database = """INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                                VALUES(%s, %s, %s, %s, %s, %s);"""

select_from_question = """SELECT question.title, question.id
                            FROM question
                            INNER JOIN users
                            ON question.user_id = users.id\
                            WHERE users.id = %s;"""

select_from_answer = """SELECT answer.message
                        FROM answer
                        INNER JOIN users
                        ON answer.user_id = users.id\
                        WHERE users.id = %s;"""


select_users = """SELECT id, first_name, last_name, username, birth_date, email, reputation\
                    FROM users\
                    ORDER BY id;"""

get_all_users = """SELECT username, id FROM users;"""


add_new_user = """INSERT INTO users (first_name, last_name, username, birth_date, email)\
                    VALUES(%s, %s, %s, %s, %s);"""
