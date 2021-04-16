#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
                       db='AirlineReservationSystem',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for the Customer's login
@app.route('/customerLogin')
def customerlogin():
	return render_template('customerLogin.html')

#Define route for the Booking Agent's login
@app.route('/agentLogin')
def agentLogin():
	return render_template('agentLogin.html')

#Define route for the Airline Staff's login
@app.route('/staffLogin')
def staffLogin():
	return render_template('staffLogin.html')

#Define route for the Customer's registration
@app.route('/customerRegistration')
def customerRegistration():
	return render_template('customerRegistration.html')

#Define route for the Booking Agent's registration
@app.route('/agentRegistration')
def agentRegistration():
	return render_template('agentRegistration.html')

#Define route for the Airline Staff's registration
@app.route('/staffRegistration')
def staffRegistration():
	return render_template('staffRegistration.html')

#Authenticates the Customer's Login
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customerLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE cus_email = %s and cus_password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('customerHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customerLogin.html', error=error)


#Authenticates the Booking Agent's Login
@app.route('/agentLoginAuth', methods=['GET', 'POST'])
def agentLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Booking_Agent WHERE agent_email = %s and agent_password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('agentHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('agentLogin.html', error=error)


#Authenticates the Airline Staff's Login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s and agent_password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('staffHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('staffLogin.html', error=error)

# Authenticates the Customer's registration
@app.route('/customerRegistrationAuth', methods=['GET', 'POST'])
def customerRegistrationAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	name = request.form['name']
	buildingNum = request.form['buildingNum']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone = request.form['phone']
	dob = request.form['dob']
	passportNum = request.form['passportNum']
	passportExp = request.form['passportExp']
	passportCountry = request.form['passportCountry']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE cus_email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This customer already exists"
		return render_template('customerRegistration.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, $s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, password, name, buildingNum, street, city, state, phone, dob, passportNum, passportExp, passportCountry))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the Booking Agent's registration
@app.route('/agentRegistrationAuth', methods=['GET', 'POST'])
def agentRegistrationAuth():
	#grabs information from the forms
	agentID = request.form['agentID']
	email = request.form['email']
	password = request.form['password']
	airline = request.form['airline']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Booking_Agent WHERE agent_email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This booking agent already exists"
		return render_template('agentRegistration.html', error = error)
	else:
		ins = 'INSERT INTO Booking_Agent VALUES(%s, %s, %s, %s)'
		cursor.execute(ins, (agentID, email, password, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the Airline Staff's registration
@app.route('/staffRegistrationAuth', methods=['GET', 'POST'])
def staffRegistrationAuth():
	#grabs information from the forms
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	password = request.form['password']
	username = request.form['username']
	dob = request.form['dob']
	phone = request.form['phone']
	airline = request.form['airline']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airline stafff member already exists"
		return render_template('staffRegistration.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (firstName, lastName, username, password, dob, phone, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
    # username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall()
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
	# return render_template('home.html', username=username, posts=data1)
	# return render_template('home.html', username=username)
	return render_template('home.html')

@app.route('/customerHome')
def customerHome():
	username = session['username']
	return render_template('customerHome.html')

@app.route('/agentHome')
def agentHome():
	username = session['username']
	return render_template('agentHome.html')

@app.route('/staffHome')
def staffHome():
	username = session['username']
	return render_template('staffHome.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
	# username = session['username']
	# cursor = conn.cursor();
	# blog = request.form['blog']
	# query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	# cursor.execute(query, (blog, username))
	# conn.commit()
	# cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 8888
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
