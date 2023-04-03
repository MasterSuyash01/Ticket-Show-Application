from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/suyashsrivastav/Desktop/Ticket-Show-Application/booking.db'
db = SQLAlchemy(app)

# ---------- Landing Page ------------
@app.route('/')
def landingpage():
    return render_template('Landingpage.html')

# ---------- User Login Page ------------
@app.route('/user_login.html')
def user_login():
    return render_template('user_login.html')

# ---------- Admin Login Page ------------
@app.route('/admin_login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect('/dashboard?username='+username)
        else:
            return render_template('admin_login.html', message='Invalid username or password.')
    else:
        return render_template('admin_login.html')  


class User(db.Model):
    __tablename__ = 'User'
    UserName = db.Column(db.String(80), primary_key=True, nullable=False)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Confirm_Password = db.Column(db.String(80), nullable=False)

#----------------------to fix-----------------------------------------------------------#
# New_user page is not working.....
@app.route('/New_user.html')
def New_user():
    return render_template('New_user.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['password']
    
    user = User(UserName=username, Name=name, Email=email, Password=password, Confirm_Password=password)
    db.session.add(user)
    db.session.commit()
    
    return 'User created successfully'
#----------------------to fix-----------------------------------------------------------#



# ---------- Contact Page ------------
@app.route('/contact.html')
def contact():
    return render_template('contact.html')


# ---------- Events Page ------------
@app.route('/Events.html')
def Events():
    return render_template('Events.html')


# ---------- Home Page ------------
@app.route('/Landingpage.html')
def Home():
    return render_template('Landingpage.html')    


# ----------- Ticket Booking -----------

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    booking_number = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name, date, time, num_tickets):
        self.name = name
        self.date = date
        self.time = time
        self.num_tickets = num_tickets
        self.booking_number = self.generate_booking_number()

    def generate_booking_number(self):
        # Generate a random booking number
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        booking_number = ''.join(random.choice(chars) for i in range(6))
        return booking_number

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        num_tickets = request.form['num_tickets']

        ticket = Ticket(name=name, date=date, time=time, num_tickets=num_tickets)
        db.session.add(ticket)
        db.session.commit()

        return render_template('confirmation.html', ticket=ticket)

    return render_template('book_ticket.html')






if __name__ == '__main__':
    app.run(debug=True)









