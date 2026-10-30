# CareConnect – Clinic Appointment Booking API

CareConnect is a REST API built with **Django** and **Django REST Framework** for managing doctors and booking clinic appointments. Patients get an automatically assigned **token number** and **time slot** based on the doctor and the date they choose.

## Features

- Create, view, update and delete doctor records
- Book appointments and list existing appointments
- Automatic **token numbering** per doctor, per day
- Automatic **15-minute time slots** starting at 10:00 AM, with the lunch break (12:30 PM – 1:30 PM) skipped
- Bookings are rejected once the day's slots are full (last slot ends at 5:00 PM)
- Duplicate-booking validation: the same phone number cannot book twice on the same date
- Request validation through DRF serializers

## Tech Stack

- Python
- Django
- Django REST Framework
- Database: SQLite (Django default) <!-- TODO: update if you use MySQL -->
- API testing: `APIDOC.http` (VS Code REST Client) or any API client

## Data Models

**Doctor**

| Field | Type | Notes |
|---|---|---|
| doctor_name | Text | |
| specialization | Text | |
| experience | Positive integer | Years |
| hospital | Text | |
| consultation_fee | Positive integer | |
| available | Boolean | Defaults to `true` |

**Appointment**

| Field | Type | Notes |
|---|---|---|
| patient_name | Text | |
| phone | Text | |
| doctor_id | Integer | ID of the doctor |
| appointment_date | Date | `YYYY-MM-DD` |
| problem | Text | Optional |
| token_number | Integer | Assigned automatically |
| appointment_time | Time | Assigned automatically |
| status | Text | Defaults to `pending` |
| created_at | Date and time | Set automatically |

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/doctors/` | List all doctors |
| POST | `/doctors/` | Add a doctor |
| GET | `/doctors/<id>/` | Get one doctor |
| PUT | `/doctors/<id>/` | Update a doctor |
| DELETE | `/doctors/<id>/` | Delete a doctor |
| GET | `/appointments/` | List all appointments |
| POST | `/appointments/` | Book an appointment |

### Example: add a doctor

```http
POST /api/doctors/
Content-Type: application/json

{
    "doctor_name": "Ansa",
    "specialization": "Oncology",
    "experience": 3,
    "hospital": "Lakeshore",
    "consultation_fee": 700
}
```

### Example: book an appointment

```http
POST /api/appointments/
Content-Type: application/json

{
    "patient_name": "Manu",
    "phone": "9897417712",
    "doctor_id": 3,
    "appointment_date": "2026-10-29",
    "problem": "Fever"
}
```

Successful response (the first booking of the day for that doctor):

```json
{
    "Status": "Booked Successfully",
    "Token Number": 1,
    "Appointment Time": "10:00:00"
}
```

More sample requests are in [`APIDOC.http`](APIDOC.http).

## How Booking Works

1. The request is validated by the serializer. If the same phone number already has an appointment on that date, it is rejected with `"Already Booked!"`.
2. The API finds the latest appointment for that doctor on that date.
3. If there is none, the booking gets **token 1** at **10:00 AM**.
4. Otherwise, the token number increases by one and the time moves forward by **15 minutes**.
5. If the next slot would fall at 12:30 PM, it moves to 1:30 PM (lunch break).
6. If the next slot would be 5:00 PM, the day is full and the booking is rejected.

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/jisnapm/CareConnect.git
cd CareConnect

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install django djangorestframework

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Run the server
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.

## Project Structure

```
CareConnect/
├── clinic/
│   ├── models.py        # Doctor and Appointment models
│   ├── serializers.py   # Serializers and duplicate-booking validation
│   ├── views.py         # API views and token/slot booking logic
│   └── urls.py          # API routes
├── APIDOC.http          # Sample API requests
├── manage.py
└── README.md
```

## What I Learned

- Designing REST APIs with Django REST Framework (models, serializers, class-based views)
- Writing business logic for scheduling: token assignment and time-slot generation
- Validating requests with serializers and handling errors

## Future Improvements

- Link appointments to doctors with a foreign key, and check that the doctor exists and is available
- Return proper HTTP status codes (`201 Created`, `400 Bad Request`)
- Add authentication and permissions for patients and staff
- Add appointment update and cancellation endpoints
- Handle simultaneous bookings safely when assigning token numbers
- Add unit tests and pagination
