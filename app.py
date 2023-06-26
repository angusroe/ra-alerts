import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import config
import random
from time import sleep

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'awoongaboonga1234567890'

@app.route('/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':

        name = request.form['name']
        phone_number = request.form['phonenumber']
        client_url = request.form['url']
        if not phone_number:
            flash('Please enter a valid UK phonenumber')
        if not client_url:
            flash('Please enter valid RA URL')
        
        if len(client_url)>0:
            url = config.add_https_schema(client_url)
        else:
            return render_template('form.html')
        
        # check if they already have alerts for this event
        if config.already_signed_up(phone_number,url):
            return render_template('success.html')

        # check if we already have the url in the database
        result = config.already_exists(url)
        if result:
            is_event = result[3]
            if is_event == 1:
                event_date = result[2]
                config.add_event(name, phone_number, url, event_date)
                return render_template('success.html')
            elif is_event == 0:
                flash('Please enter valid RA URL - tickets must be available to purchase directly from the RA website')
                return render_template('form.html')

        # if we don't already have the url in the events table
        result = config.create_page_soup(url)
        page_soup = result[0]
        response_status = result[1]
        if response_status > 204:
            return render_template('error.html')
        event = config.validate_RA_tickets(page_soup)

        # check if it is a real RA event
        if event == False:
            config.insert_not_event(url)
            flash('Please enter valid RA URL - tickets must be available to purchase directly from the RA website')
        else:
            config.insert_is_event(name, phone_number, url, page_soup)
            return render_template('success.html')

    return render_template('form.html')

        # conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute('SELECT * FROM webform WHERE url = (?) AND phonenumber = (?)',
        #             (url,phone_number))
        # result = cur.fetchone
        # if result is  None:
        #     conn.close()
        #     return render_template('success')

        # cur.execute('SELECT * FROM events WHERE url = (?)',
        #              (url,))
        # result = cur.fetchone()
        # if result is not None: # if we already have thge reusult in our database it reduces excess get requests
        #     is_event = result[3]
        #     if is_event == 1: 
        #         event_date = result[2]
        #         conn.execute('INSERT INTO webform (name, phonenumber, url, event_date) VALUES (?, ?, ?, ?)',
        #                      (name, phone_number, url, event_date))
        #         conn.commit()
        #         conn.close()
        #         return redirect(url_for('success'))
        #     elif is_event == 0:
        #         flash('Please enter valid RA URL - tickets must be available to purchase directly from the RA website')
        #         conn.close()
        #         return render_template('form.html')
        # conn.close()

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

# if __name__ == '__main__':
#     app.run()