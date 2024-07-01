from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from dateutil.parser import isoparse

app = Flask(__name__)

# I have added personalised MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dushyant@1170'
app.config['MYSQL_DB'] = 'meetify'

mysql = MySQL(app)

@app.route('/users/<int:user_id>/schedule', methods=['POST'])
def get_user_schedule(user_id):
    try:
        data = request.json
        start_time = isoparse(data['start_time'])
        end_time = isoparse(data['end_time'])

        booked_meetings = fetch_booked_meetings(user_id, start_time, end_time)
        free_slots = calculate_free_slots(start_time, end_time, booked_meetings)

        return jsonify({
            'booked_meetings': booked_meetings,
            'free_slots': free_slots
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def fetch_booked_meetings(user_id, start_time, end_time):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT start_time, end_time, timezone, meeting_type FROM meetings WHERE user_id = %s AND start_time >= %s AND end_time <= %s",
        (user_id, start_time, end_time)
    )
    meetings = []
    for row in cursor.fetchall():
        meeting = {
            'start_time': row[0].isoformat(),
            'end_time': row[1].isoformat(),
            'timezone': row[2],
            'meeting_type': row[3]
        }
        meetings.append(meeting)
    cursor.close()
    return meetings

def calculate_free_slots(start_time, end_time, booked_meetings):
    free_slots = [{
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration': (end_time - start_time).total_seconds() / 60
    }]

    for meeting in booked_meetings:
        meeting_start = isoparse(meeting['start_time'])
        meeting_end = isoparse(meeting['end_time'])

        updated_free_slots = []
        for slot in free_slots:
            slot_start = isoparse(slot['start_time'])
            slot_end = isoparse(slot['end_time'])

        free_slots = updated_free_slots

    return free_slots

@app.route('/users/<int:user_id>/dnd_start_time', methods=['PUT'])
def update_user_dnd_start_time(user_id):
    try:
        data = request.json
        dnd_start_time = datetime.fromisoformat(data['dnd_start_time'])

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET dnd_start_time = %s WHERE id = %s",
            (dnd_start_time, user_id)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User DND start time updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>/dnd_end_time', methods=['PUT'])
def update_user_dnd_end_time(user_id):
    try:
        data = request.json
        dnd_end_time = datetime.fromisoformat(data['dnd_end_time'])

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET dnd_end_time = %s WHERE id = %s",
            (dnd_end_time, user_id)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User DND end time updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>/preferred_timezone', methods=['PUT'])
def update_user_preferred_timezone(user_id):
    try:
        data = request.json
        preferred_timezone = data['preferred_timezone']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET preferred_timezone = %s WHERE id = %s",
            (preferred_timezone, user_id)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User preferred timezone updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        dnd_start_time = datetime.fromisoformat(data['dnd_start_time'])
        dnd_end_time = datetime.fromisoformat(data['dnd_end_time'])
        preferred_timezone = data['preferred_timezone']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, dnd_start_time, dnd_end_time, preferred_timezone) VALUES (%s, %s, %s, %s, %s)",
            (name, email, dnd_start_time, dnd_end_time, preferred_timezone)
        )
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return jsonify({'id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/meetings', methods=['POST'])
def create_meeting():
    try:
        data = request.json
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
        user_id = data['user_id']
        meeting_type = data['meeting_type']
        timezone = data['timezone']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO meetings (start_time, end_time, user_id, meeting_type, timezone) VALUES (%s, %s, %s, %s, %s)",
            (start_time, end_time, user_id, meeting_type, timezone)
        )
        mysql.connection.commit()
        meeting_id = cursor.lastrowid
        cursor.close()
        return jsonify({'id': meeting_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
