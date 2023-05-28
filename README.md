# Event_management
# Meeting management

The Meeting Management App is a web application developed using Flask framework that allows users to manage events, meetings, and invitations within a company.

## Features

- Add users to events
- Create meetings for events
- Send invitations to users for meetings
- Track invitation status (Accepted, Rejected, Pending)

## Installation

1. Clone the repository:

2. Navigate to the project directory:

3. Install the dependencies:

4. Set up the database connection:
- Open `main.py` file.
- Update the `SQLALCHEMY_DATABASE_URI` configuration with your database connection string.

5. Run the application:

6. Access the app:
Open your web browser and visit `http://localhost:5000` to access the Meeting Management App.

## Usage

- Add users to events:
- Endpoint: `POST /events/<event_id>/users`
- Payload: `{ "user_id": 123 }`
- Add a user with the specified ID to the event with the given event ID.

- Create meetings for events:
- Endpoint: `POST /events/<event_id>/meetings`
- Payload: `{ "date": "2023-06-01", "time": "15:00" }`
- Create a new meeting for the event with the specified event ID, providing the date and time.

- Send invitations to users for meetings:
- Endpoint: `POST /meetings/<meeting_id>/invitations`
- Payload: `{ "inviter_id": 123, "invitee_id": 456 }`
- Send an invitation from the user with the inviter ID to the user with the invitee ID for the meeting with the given meeting ID.


## License

This project is licensed under the MIT License.
