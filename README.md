# BusinessLabs Student Registration Portal

This is a simple student registration portal built using Django. It has separate access for students and admins and stores student information in a SQLite database.

## Tech Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- SQLite

## What the project does

### Student

A student can:

- Register with their personal and academic details
- Upload an Aadhaar PDF
- Login using email and password
- View their profile
- Edit their profile
- Change their password
- Replace their Aadhaar document
- Reset their password using Forgot Password

### Admin

An admin can:

- Login through the same login page
- View all registered students
- Search students by name and class
- Filter students by age
- Open uploaded Aadhaar PDFs
- Edit student details
- Delete students

During admin editing, the student's name and email cannot be changed.

## Project Structure

```text
BusinessLabs/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── student_portal/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── accounts/
│
├── static/
│   └── css/
│
├── media/
│   └── aadhaar/
│
├── db.sqlite3
├── schema.sql
├── manage.py
└── README.md
```

## Running the Project

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install Django:

```bash
pip install django
```

Run the migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Admin Login

For testing, the admin account is:

**Email:** `admin@businesslabs.com`

**Password:** `Admin@123`

## Main Pages

```text
/                       Home
/signup/                Student Registration
/login/                 Login
/forgot-password/       Forgot Password
/student-dashboard/     Student Dashboard
/edit-profile/          Edit Student Profile
/admin-dashboard/       Admin Dashboard
```

## Database

The project currently uses SQLite.

The database file is:

```text
db.sqlite3
```

A SQL dump is also included:

```text
schema.sql
```

## Aadhaar Upload

Only PDF files are accepted for Aadhaar upload.

Uploaded files are given unique names on the server so that two students using the same original filename do not overwrite each other's files.

## CRUD

The project supports the basic CRUD operations:

- **Create** - Student registration
- **Read** - Student and Admin dashboards
- **Update** - Profile and student editing
- **Delete** - Admin can delete students

## Access Control

Students can access their own dashboard and profile.

Admins can access the student management dashboard.

A student cannot directly open the admin dashboard without an admin session.

## Validation

The application checks for:

- Duplicate student email
- PDF-only Aadhaar upload
- Password confirmation
- Logged-in user access
- Unique Aadhaar filenames

For a duplicate email, the following message is displayed:

```text
This email is already registered.
```
