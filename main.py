# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import json
import re


app = Flask(__name__)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with open('user.json','r') as file:
            users = json.load(file)
        if username in users and users[username][0] == password:
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg , username=username)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/delete_blog', methods =['GET', 'POST'])
def delete_blog():
    msg = ''
    if request.method == 'POST' and 'id' in request.form:
        blog_id = request.form['id']
        with open('blogs.json','r') as file:
            blogs = json.load(file)
        if blog_id in blogs:
            msg = 'Deteted Successfully !'
            del blogs[blog_id]
            with open('blogs.json','w') as file:
                json.dump(blogs,file)
            return render_template('delete_blog.html', msg = msg)
        else:
            msg = 'Incorrect Id !'
    return render_template('delete_blog.html', msg = msg)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/print_blogs')
def print_blogs():
    with open('blogs.json','r') as file:
        blogs = json.load(file)
    return render_template('print_blogs.html' , blogs=blogs)

@app.route('/create_blog', methods =['GET', 'POST'])
def create_blog():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'title' in request.form and 'description' in request.form :
        blog_id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        with open('user.json','r') as file:
            blogs = json.load(file)
        if blog_id in blogs:
            msg = 'Blog already exists with this id please try with another id !'
        elif not blog_id or not title or not description:
            msg = 'Please fill out the form !'
        else:
            blogs[blog_id] = [title,description]
            with open('blogs.json','w') as file:
                json.dump(blogs,file)
            msg = 'Blog Successfully Created !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('create_blog.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with open('user.json','r') as file:
            users = json.load(file)
        if username in users:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            users[username] = [password,email]
            with open('user.json','w') as file:
                json.dump(users,file)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
if __name__ == "__main__":
    app.run()
