from flask import Flask, render_template, request, redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import random
from flask import request
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required
from flask_login import LoginManager, UserMixin,logout_user 
import secrets
import matplotlib.pyplot as plt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/suyashsrivastav/Desktop/Ticket-Show-Application/booking.db'
db = SQLAlchemy(app)


# ---------- Landing Page ------------
@app.route('/')
def landingpage():
    return render_template('Landingpage.html')




# ---------- Admin Login Page ------------
@app.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect('Admin_dashboard')
        else:
            message = 'Invalid username or password.'
            return render_template('admin_login.html', message=message)
    else:
        return render_template('admin_login.html')


app.secret_key = secrets.token_hex(16)
class User(UserMixin,db.Model):
    __tablename__ = 'User'
    UserName = db.Column(db.String(80), primary_key=True, nullable=False)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Confirm_Password = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.Confirm_Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Confirm_Password, password)

    def get_id(self):
        return str(self.UserName)

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(UserName=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('user_login.html')

login_manager = LoginManager()
login_manager.login_view = 'user_login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))



@app.route('/user_logout', methods=['GET', 'POST'])
def user_logout():   
    logout_user()
    return redirect("user_login")    

#user page
@app.route('/New_user')
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
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return 'User created successfully'



# ---------- Contact Page ------------
@app.route('/contact')
def contact():
    return render_template('contact.html')


# ---------- Events Page ------------
@app.route('/events')
def Events():
    return render_template('Events.html')



# ----------- Ticket Booking -----------

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    venuename=db.Column(db.String(80),nullable=False)
    showname=db.Column(db.String(80),nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    booking_number = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name, date, time,venuename,showname, num_tickets):
        self.name = name
        self.date = date
        self.time = time
        self.venuename=venuename
        self.showname=showname
        self.num_tickets = num_tickets
        self.booking_number = self.generate_booking_number()

    def generate_booking_number(self):
        # Generate a random booking number
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        booking_number = ''.join(random.choice(chars) for i in range(6))
        return booking_number

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        show_id = request.form['venue']
        
        num_tickets = request.form['num_tickets']

        show=Show.query.get(show_id)
        num_tickets=int(num_tickets)
        if int(show.venue.Capacity)<num_tickets:
            return "HouseFull"
        show.venue.Capacity=str(int(show.venue.Capacity)-num_tickets)

        

        ticket = Ticket(name=name, date=date, time=time,venuename=show.venue.Venue,showname=show.name, num_tickets=num_tickets)
        db.session.add(ticket)
        db.session.commit()

        return render_template('confirmation.html', ticket=ticket)

    venues = Venue.query.all()
    shows = Show.query.all()
    return render_template('book_ticket.html',venues=venues,shows=shows)



class Venue(db.Model):
    
    Venue = db.Column(db.String(50),unique=True, primary_key=True)
    Location = db.Column(db.String(50))
    City = db.Column(db.String(50))
    Capacity = db.Column(db.String(50))



class Movies(db.Model):
    __tablename__ = 'Movies'
    Show_id = db.Column(db.Integer, primary_key=True, nullable=False)
    Moviename = db.Column(db.String(80), nullable=False)
    Rating = db.Column(db.String(120), nullable=False)
    Ticket_cost = db.Column(db.Integer, nullable=False)

@app.route('/movies')
def movies():
    movies = Movies.query.all()
    return render_template('movies.html', Movies=movies)


@app.route('/user_dashboard')
def user_dashboard():
    # get the search query from the URL parameter 'q'
    query = request.args.get('q')
    current_user = User.query.filter_by(UserName=session.get('user_id')).first()
    # if there is a search query, filter the venues by the query
    if query:
        venues = Venue.query.filter( Venue.Venue.contains(query) | Venue.Location.contains(query) | Venue.City.contains(query)).all()
    else:
        venues = Venue.query.all()
    shows = Show.query.all()

    return render_template('user_dashboard.html', venues=venues,current_user=current_user,shows=shows)

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        movies = Movies.query.filter(Movies.Moviename.contains(query)).all()
    else:
        movies = Movies.query.all()
    return render_template('movies.html', Movies=movies)



@app.route('/Admin_dashboard')
def Admin_dashboard():
    # get the search query from the URL parameter 'q'
    query = request.args.get('q')
    shows = Show.query.all()
    # if there is a search query, filter the venues by the query
    if query:
        venues = Venue.query.filter(
            
            Venue.Venue.ilike(f'%{query}%') |
            Venue.Location.ilike(f'%{query}%') |
            Venue.City.ilike(f'%{query}%')
        ).all()
    
    if query:
        shows=Show.query.filter(
            Show.name.ilike(f'%{query}%') 
        ).all()    
    
    else:
        venues = Venue.query.all()
        shows=Show.query.all()
    return render_template('Admin_dashboard.html', venues=venues,shows=shows)


@app.route('/add_venue', methods=['GET', 'POST'])
def add_venue():
    if request.method == 'POST':
        movie = request.form['Movie']
        venue = request.form['Venue']
        location = request.form['Location']
        city = request.form['City']
        capacity = request.form['Capacity']
        new_venue = Venue(Movie=movie, Venue=venue, Location=location, City=city, Capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()
        return redirect('/Admin_dashboard')
    return render_template('add_venue.html')

@app.route('/edit_venue/<Venue>', methods=['GET', 'POST'])
def edit_venue(venue):
    venue = Venue.query.filter_by(Venue=venue).first()
    if request.method == 'POST':
        venue.Venue = request.form['Venue']
        venue.Location = request.form['Location']
        venue.City = request.form['City']
        venue.Capacity = request.form['Capacity']
        db.session.commit()
        return redirect('/Admin_dashboard')
    return render_template('edit.html', venue=venue)

@app.route('/delete_venue/<venue>', methods=['GET', 'POST'])
def delete_venue(movie):
    venue = Venue.query.filter_by(Movie=movie).first()
    if request.method == 'POST':
        db.session.delete(venue)
        db.session.commit()
        return redirect('/Admin_dashboard')
    return render_template('delete.html', venue=venue)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.String,ForeignKey(Venue.Venue))
    name = db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    venue=db.relationship(Venue,backref="Shows")

@app.route('/add_show', methods=['GET', 'POST'])
def add_show():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        price = request.form['price']
        new_show = Show(name=name, time=time, price=price)
        db.session.add(new_show)
        db.session.commit()
        return 'Show added successfully!'
    else:
        venues=Venue.query.all()
        return render_template('add_show.html',venues=venues)

class Rating(db.Model):
    __tablename__="Ratings"
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(80))
    show_name = db.Column(db.String(80), nullable=False)
    venue_name = db.Column(db.String(80), nullable=False)
    ratings = db.Column(db.Integer, nullable=False)

@app.route('/rate_venue', methods=['POST'])
def rate_venue():
    venue_name = request.form.get('venue_name')
    show_name = request.form.get('show_name')
    rating = request.form.get('rating')
    
    # Retrieve the current user

    """currentuser = User.query.filter_by(UserName=current_user.UserName).first()"""
    
    # Create a new rating object and add it to the database
    rating = Rating(user_id=current_user.UserName, venue_name=venue_name, ratings=rating,show_name=show_name)
    db.session.add(rating)
    db.session.commit()
    
    # Redirect the user back to the dashboard
    return redirect(url_for('user_dashboard'))


@app.route('/my_bookings')
@login_required
def my_bookings():
    bookings = Ticket.query.filter_by(name=current_user.Name).all()
    return render_template('my_bookings.html', bookings=bookings)


@app.route('/edit_show/<show_name>', methods=['GET', 'POST'])
def edit_show(show_name):
    show = Show.query.filter_by(name=show_name).first()
    if request.method == 'POST':
        show.name = request.form['Name']
        show.time = request.form['Time']
        show.price = request.form['Price']
        db.session.commit()
        return redirect('/Admin_dashboard')
    return render_template('edit_show.html', show=show)


@app.route('/summary')
def generate_summary():
    # Query the Ticket table to retrieve the data
    shows = Ticket.query.all()
    
    # Create lists to store the show names and number of tickets sold
    show_names = []
    num_tickets_sold = []
    for show in shows:
        show_names.append(show.showname)
        num_tickets_sold.append(show.num_tickets)
    
    # Create the bar graph using matplotlib
    plt.plot(show_names, num_tickets_sold)
    plt.xlabel('Show')
    plt.ylabel('Number of Tickets Sold')
    plt.title('Ticket Sales Summary')
    plt.savefig("graph.png")

    return render_template('summary.html')




if __name__ == '__main__':
    app.run(debug=True)
