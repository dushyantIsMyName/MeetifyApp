A sophisticated Meeting Scheduling App, Meetify.

--> While running the application, use a MySQL DB and priorly create 2 tables: Users and Meetings with the following schemas:

--> Users:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    dnd_start_time DATETIME,
    dnd_end_time DATETIME,
    preferred_timezone VARCHAR(255)
);

--> Meetings:

CREATE TABLE meetings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meeting_type ENUM('online', 'offline'),
    start_time DATETIME,
    end_time DATETIME,
    timezone VARCHAR(255),
    notification_interval VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

--> Example create new user CURL to hit on postman:

curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Bob Smith",
           "email": "bob.smith@example.com",
           "dnd_start_time": "2024-07-02T08:00:00+00:00",
           "dnd_end_time": "2024-07-02T17:00:00+00:00",
           "preferred_timezone": "Europe/London"
         }'

--> Example create new meeting CURL to hit on postman:

curl -X POST http://localhost:5000/meetings \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Quarterly Review",
           "description": "Reviewing performance and goals for the quarter",
           "start_time": "2024-07-03T09:00:00+00:00",
           "end_time": "2024-07-03T11:00:00+00:00",
           "user_id": 2,
           "meeting_type": "online",
           "timezone": "IST"
         }'

--> Example get_user_schedule CURL to hit on postman:

curl -X POST http://localhost:5000/users/2/schedule \
     -H "Content-Type: application/json" \
     -d '{
           "start_time": "2024-07-01T00:00:00+00:00",
           "end_time": "2024-07-07T23:59:59+00:00"
         }'



Thanks for reading, cheers :)
