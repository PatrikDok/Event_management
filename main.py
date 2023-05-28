# main.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'access+pyodbc:///?odbc_connect=DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Patrik\Desktop\event management app\Event.accdb'
db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    events = db.relationship('Event', secondary='event_user')
    invitations_sent = db.relationship('Invitation', backref='inviter', foreign_keys='Invitation.inviter_id')
    invitations_received = db.relationship('Invitation', backref='invitee', foreign_keys='Invitation.invitee_id')

# Define the Company model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='company')

# Define the Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    users = db.relationship('User', secondary='event_user')
    meetings = db.relationship('Meeting', backref='event')

# Define the association table between Event and User models
event_user = db.Table('event_user',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Define the Meeting model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    invitations = db.relationship('Invitation', backref='meeting')

# Define the Invitation model
class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    inviter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Accepted, Rejected, Pending

@app.route('/events/<int:event_id>/users', methods=['POST'])
def add_user_to_event(event_id):
    try:
        # Retrieve the event from the database
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'message': 'Event not found'}), 404

        # Retrieve the user ID from the request payload
        data = request.get_json()
        user_id = data.get('user_id')

        # Retrieve the user from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Ensure the user and event belong to the same company
        if user.company_id != event.company_id:
            return jsonify({'message': 'User and event do not belong to the same company'}), 400

        # Check if the user is already associated with the event
        if user in event.users:
            return jsonify({'message': 'User is already associated with the event'}), 400

        # Add the user to the event and commit the changes
        event.users.append(user)
        db.session.commit()

        return jsonify({'message': 'User added to the event successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/events/<int:event_id>/meetings', methods=['POST'])
def create_meeting(event_id):
    try:
        # Retrieve the event from the database
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'message': 'Event not found'}), 404

        # Retrieve the meeting details from the request payload
        data = request.get_json()
        date = data.get('date')
        time = data.get('time')

        # Create a new meeting associated with the event
        meeting = Meeting(event_id=event.id, date=date, time=time)
        db.session.add(meeting)
        db.session.commit()

        return jsonify({'message': 'Meeting created successfully', 'meeting_id': meeting.id}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/meetings/<int:meeting_id>/invitations', methods=['POST'])
def create_invitation(meeting_id):
    try:
        # Retrieve the meeting from the database
        meeting = Meeting.query.get(meeting_id)
        if not meeting:
            return jsonify({'message': 'Meeting not found'}), 404

        # Retrieve the invitation details from the request payload
        data = request.get_json()
        inviter_id = data.get('inviter_id')
        invitee_id = data.get('invitee_id')

        # Retrieve the inviter and invitee from the database
        inviter = User.query.get(inviter_id)
        invitee = User.query.get(invitee_id)
        if not inviter or not invitee:
            return jsonify({'message': 'Inviter or invitee not found'}), 404

        # Check if the inviter and invitee belong to the same company
        if inviter.company_id != invitee.company_id:
            return jsonify({'message': 'Inviter and invitee do not belong to the same company'}), 400

        # Create a new invitation associated with the meeting
        invitation = Invitation(meeting_id=meeting.id, inviter_id=inviter.id, invitee_id=invitee.id, status='Pending')
        db.session.add(invitation)
        db.session.commit()

        return jsonify({'message': 'Invitation created successfully', 'invitation_id': invitation.id}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
