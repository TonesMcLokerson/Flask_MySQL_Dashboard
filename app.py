from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL 
from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, DateTimeField, IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Initialize MySQL
mysql = MySQL(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
	return render_template('home.html')

# About
@app.route('/about')
def about():
	return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()

#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)

# Register Form Class
class RegisterForm(Form):
	name = StringField( 'Name', [validators.Length(min=1, max=50)])
	username =StringField( 'Username', [validators.Length(min=4, max=25)])
	email =StringField( 'Email', [validators.Length(min=6, max=50)])
	password =PasswordField( 'Password',[ 
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])	
	confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data 
		password = sha256_crypt.encrypt(str(form.password.data)) 

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s) ", (name, email, username, password))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("You are now registered and can login", 'success')

		return redirect(url_for('login'))
	return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
        # Get Form Fields
		username = request.form['username']
		password_candidate = request.form['password']

		# Create cursor
		cur = mysql.connection.cursor()

		# Get user bu username
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
            # Get stored hash
			data = cur.fetchone()
			password = data['password']

			# Compare passwords
			if sha256_crypt.verify(password_candidate, password):
				#Passed
				session['logged_in'] = True
				session['username'] = username 

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error)
			# Close connection
			cur.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)

	return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	# Create cursor
	cur = mysql.connection.cursor()

	# Get Articles
	result = cur.execute("SELECT * FROM articles")

	articles = cur.fetchall()

	if result > 0:
		return render_template('dashboard.html', articles=articles)
	else:
		msg = 'No Articles Found'
		return render_template('dashboard.html')

	# Close Connection
	cur.close()

# Article Form Class
class ArticleForm(Form):
	title = StringField( 'Title', [validators.Length(min=1, max=200)])
	body =TextAreaField( 'Body', [validators.Length(min=30,)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data 
		body = form.body.data 

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute
		cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

		#Commit
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Article Created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_article.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title = %s, body = %s WHERE id = %s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)


# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

# Employees
@app.route('/employees')
@is_logged_in
def employees():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM employees")

    employees = cur.fetchall()

    if result > 0:
        return render_template('employees.html', employees=employees)
    else:
        msg = 'No Employees Found'
        return render_template('employees.html', msg=msg)
    # Close connection
    cur.close()

#Single Employee
@app.route('/employee/<string:id>/')
def employee(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get Employee
    result = cur.execute("SELECT * FROM employees WHERE id = %s", [id])

    employee = cur.fetchone()

    return render_template('employee.html', employee=employee)

# Employee Form Class
class EmployeeForm(Form):
	fname = StringField( 'First Name', [validators.Length(min=1, max=50)])
	lname = StringField( 'Last Name', [validators.Length(min=1, max=50)])
	address = StringField( 'Address', [validators.Length(min=1, max=100)])
	city = StringField( 'City', [validators.Length(min=1, max=50)])
	state = StringField( 'State', [validators.Length(min=2, max=25)])
	zipcode = StringField( 'Zip Code', [validators.Length(min=5, max=10)])
	phonenumber = StringField( 'Phone Number', [validators.Length(min=1, max=12)])
	email = StringField( 'Email', [validators.Length(min=6, max=100)])	
	dresssize = StringField( 'Dress Size', [validators.Length(min=4, max=10)])
	comments = TextAreaField( 'Comments', [validators.Length(min=1)])

# Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
@is_logged_in
def add_employee():
	form = EmployeeForm(request.form)
	if request.method == 'POST' and form.validate():
		fname = form.fname.data
		lname = form.lname.data
		address = form.address.data 
		city = form.city.data
		state = form.state.data
		zipcode = form.zipcode.data
		phonenumber = form.phonenumber.data
		email = form.email.data
		dresssize = form.dresssize.data
		comments = form.comments.data

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO employees(fname, lname, address, city, state, zipcode, phonenumber, email, dresssize, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ", (fname, lname, address, city, state, zipcode, phonenumber, email, dresssize, comments))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("Employee Successflly Uploaded", 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_employee.html', form=form)

# Accounts
@app.route('/accounts')
def accounts():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM accounts")

    accounts = cur.fetchall()

    if result > 0:
        return render_template('accounts.html', accounts=accounts)
    else:
        msg = 'No Employees Found'
        return render_template('accounts.html', msg=msg)
    # Close connection
    cur.close()

#Single Account
@app.route('/account/<string:id>/')
def account(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get Account
    result = cur.execute("SELECT * FROM accounts WHERE id = %s", [id])

    account = cur.fetchone()

    return render_template('account.html', account=account)

# Account Form Class
class AccountForm(Form):
	accountname = StringField( 'Account Name', [validators.Length(min=1, max=50)])
	accountaddress = StringField( 'Address', [validators.Length(min=1, max=75)])
	accountcity = StringField( 'City', [validators.Length(min=1, max=25)])
	accountcomments = TextAreaField( 'Comments', [validators.Length(min=1)])

# Add Account
@app.route('/add_account', methods=['GET', 'POST'])
@is_logged_in
def add_account():
	form = AccountForm(request.form)
	if request.method == 'POST' and form.validate():
		accountname = form.accountname.data
		accountaddress = form.accountaddress.data
		accountcity = form.accountcity.data
		accountcomments = form.accountcomments.data

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO accounts(accountname, accountaddress, accountcity, accountcomments) VALUES(%s, %s, %s, %s)",(accountname, accountaddress, accountcity, accountcomments))
		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("Account Successflly Uploaded", 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_account.html', form=form)

# Events
@app.route('/events')
def events():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM events")

    events = cur.fetchall()

    if result > 0:
        return render_template('events.html', events=events)
    else:
        msg = 'No Events Found'
        return render_template('events.html', msg=msg)
    # Close connection
    cur.close()

#Single Event
@app.route('/event/<string:id>/')
def event(id):
    # Create cursor
    cur = mysql.connection.cursor()   

    # Get Account
    result = cur.execute("SELECT * FROM events WHERE id = %s", [id])

    event = cur.fetchone()

    return render_template('event.html', event=event)

# Event Form Class
class EventForm(Form):
	program = StringField( 'Program', [validators.Length(min=1, max=50)])
	event_date = DateField( 'Date',format='%Y-%m-%d', validators=(validators.Optional(),))
	event_time = TextAreaField( 'Start Time', validators=(validators.Optional(),))
	end_time = TextAreaField( 'End Time', validators=(validators.Optional(),))  
	account = StringField( 'Account Name', [validators.Length(min=1, max=50)])
	sampler1 = StringField( 'Sampler', [validators.Length(min=1, max=50)])
	sampler2 = StringField( 'Sampler', [validators.Length(min=1, max=50)])
	teamlead = StringField( 'Team Lead?', [validators.Length(min=1, max=25)])
	comments = TextAreaField( 'Event Comments ', [validators.Length(min=1)])

# Add Event
@app.route('/add_event', methods=['GET', 'POST'])
@is_logged_in
def add_event():
	form = EventForm(request.form)
	if request.method == 'POST' and form.validate():
		program = form.program.data
		event_date = form.event_date.data
		event_time = form.event_time.data
		end_time = form.end_time.data
		account = form.account.data
		sampler1 = form.sampler1.data
		sampler2 = form.sampler2.data
		teamlead = form.teamlead.data
		comments = form.comments.data

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO events(program, event_date, event_time, account, sampler1, sampler2, teamlead, comments) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(program, event_date, event_time, account, sampler1, sampler2, teamlead, comments))
		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("Event Successflly Uploaded", 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_event.html', form=form)

# Edit Event
@app.route('/edit_event/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_event(id):
    # Create cursor
	cur = mysql.connection.cursor()

    # Get article by id
	result = cur.execute("SELECT * FROM events WHERE id = %s", [id])

	event = cur.fetchone()

	cur.close()
    # Get form
	form = EventForm(request.form)

	# Populate event form fields
	form.program.data = event['program']
	form.event_date.data = event['event_date']
	form.event_time.data = event['event_time']
	form.end_time.data = event['end_time']
	form.account.data = event['account']
	form.sampler1.data = event['sampler1']
	form.sampler2.data = event['sampler2']
	form.teamlead.data = event['teamlead']
	form.comments.data = event['comments']

	if request.method == 'POST' and form.validate():
		program = request.form['program']
		event_date = request.form['event_date']
		event_time = request.form['event_time']
		end_time = request.form['end_time']
		account = request.form['account']
		sampler1 = request.form['sampler1']
		sampler2 = request.form['sampler2']
		teamlead = request.form['teamlead']
		comments = request.form['comments']

        # Create Cursor
		cur = mysql.connection.cursor()
		app.logger.info(program)
        # Execute
		cur.execute ("UPDATE events SET program = %s, event_date = %s, event_time = %s, end_time = %s, account = %s, sampler1 = %s, sampler2 = %s, teamlead = %s, comments = %s WHERE id = %s",(program, event_date, event_time, end_time, account, sampler1, sampler2, teamlead, comments, id))
        # Commit to DB
		mysql.connection.commit()

		#Close connection
		cur.close()

		flash('Event Updated', 'success')

		return redirect(url_for('events'))

	return render_template('edit_event.html', form=form)

if __name__ == '__main__':
	app.secret_key = '5179'
	app.run(debug = True)