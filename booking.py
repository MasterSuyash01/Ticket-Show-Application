from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/suyashsrivastav/Desktop/Ticket-Show-Application/booking.db'
db = SQLAlchemy(app)

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

@app.route('/')
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
