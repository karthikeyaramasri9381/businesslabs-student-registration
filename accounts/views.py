from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from .models import Admin, Student


def home(request):
    return render(request, "accounts/home.html")


def signup(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        qualification = request.POST.get("qualification")
        interests = request.POST.getlist("interests")
        student_class = request.POST.get("student_class")
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")
        aadhaar = request.FILES.get("aadhaar")

        if Student.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/signup.html",
                {"error": "This email is already registered."}
            )

        if not aadhaar or not aadhaar.name.lower().endswith(".pdf"):
            return render(
                request,
                "accounts/signup.html",
                {"error": "Aadhaar document must be a PDF."}
            )

        Student.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            date_of_birth=date_of_birth,
            gender=gender,
            qualification=qualification,
            interests=", ".join(interests),
            student_class=student_class,
            subject=subject,
            marks=marks,
            aadhaar=aadhaar
        )

        return redirect("login")

    return render(request, "accounts/signup.html")


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            admin = Admin.objects.get(email=email)

            if check_password(password, admin.password):
                request.session.flush()
                request.session["admin_id"] = admin.id
                return redirect("admin_dashboard")

        except Admin.DoesNotExist:
            pass

        try:
            student = Student.objects.get(email=email)

            if check_password(password, student.password):
                request.session.flush()
                request.session["student_id"] = student.id
                return redirect("student_dashboard")

        except Student.DoesNotExist:
            pass

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid email or password."}
        )

    return render(request, "accounts/login.html")


def student_dashboard(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    return render(
        request,
        "accounts/student_dashboard.html",
        {"student": student}
    )


def edit_profile(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":

        student.full_name = request.POST.get("full_name")
        student.date_of_birth = request.POST.get("date_of_birth")
        student.gender = request.POST.get("gender")
        student.qualification = request.POST.get("qualification")
        student.interests = ", ".join(
            request.POST.getlist("interests")
        )
        student.student_class = request.POST.get("student_class")
        student.subject = request.POST.get("subject")
        student.marks = request.POST.get("marks")

        password = request.POST.get("password")

        if password:
            student.password = make_password(password)

        aadhaar = request.FILES.get("aadhaar")

        if aadhaar:

            if not aadhaar.name.lower().endswith(".pdf"):
                return render(
                    request,
                    "accounts/edit_profile.html",
                    {
                        "student": student,
                        "error": "Aadhaar document must be a PDF."
                    }
                )

            student.aadhaar = aadhaar

        student.save()

        return redirect("student_dashboard")

    return render(
        request,
        "accounts/edit_profile.html",
        {"student": student}
    )


def logout_view(request):
    request.session.flush()
    return redirect("login")


def calculate_age(date_of_birth):

    today = timezone.now().date()

    age = today.year - date_of_birth.year

    if (today.month, today.day) < (
        date_of_birth.month,
        date_of_birth.day
    ):
        age -= 1

    return age


def admin_dashboard(request):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("login")

    students = Student.objects.all().order_by("id")

    name = request.GET.get("name", "").strip()
    student_class = request.GET.get("student_class", "").strip()
    min_age = request.GET.get("min_age", "").strip()
    max_age = request.GET.get("max_age", "").strip()

    if name:
        students = students.filter(full_name__icontains=name)

    if student_class:
        students = students.filter(student_class__icontains=student_class)

    today = timezone.now().date()

    if min_age.isdigit():
        min_age_value = int(min_age)

        max_birth_date = date(
            today.year - min_age_value,
            today.month,
            today.day
        )

        students = students.filter(
            date_of_birth__lte=max_birth_date
        )

    if max_age.isdigit():
        max_age_value = int(max_age)

        min_birth_date = date(
            today.year - max_age_value - 1,
            today.month,
            today.day
        ) + timedelta(days=1)

        students = students.filter(
            date_of_birth__gte=min_birth_date
        )

    student_list = []

    for student in students:
        student.age = calculate_age(student.date_of_birth)
        student_list.append(student)

    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "students": student_list,
            "name": name,
            "student_class": student_class,
            "min_age": min_age,
            "max_age": max_age,
        }
    )


def admin_edit_student(request, student_id):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":

        # Name and Email are intentionally not changed here.

        student.date_of_birth = request.POST.get("date_of_birth")
        student.gender = request.POST.get("gender")
        student.qualification = request.POST.get("qualification")
        student.interests = ", ".join(
            request.POST.getlist("interests")
        )
        student.student_class = request.POST.get("student_class")
        student.subject = request.POST.get("subject")
        student.marks = request.POST.get("marks")

        password = request.POST.get("password")

        if password:
            student.password = make_password(password)

        aadhaar = request.FILES.get("aadhaar")

        if aadhaar:

            if not aadhaar.name.lower().endswith(".pdf"):
                return render(
                    request,
                    "accounts/admin_edit_student.html",
                    {
                        "student": student,
                        "error": "Aadhaar document must be a PDF."
                    }
                )

            student.aadhaar = aadhaar

        student.save()

        return redirect("admin_dashboard")

    return render(
        request,
        "accounts/admin_edit_student.html",
        {"student": student}
    )


def admin_delete_student(request, student_id):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("admin_dashboard")

    return render(
        request,
        "accounts/delete_student.html",
        {"student": student}
    )


def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        admin = Admin.objects.filter(email=email).first()

        if admin:
            if new_password != confirm_password:
                return render(
                    request,
                    "accounts/forgot_password.html",
                    {
                        "error": "Passwords do not match.",
                        "email": email
                    }
                )

            admin.password = make_password(new_password)
            admin.save()

            return render(
                request,
                "accounts/forgot_password.html",
                {
                    "success": "Password reset successfully. You can login now."
                }
            )

        student = Student.objects.filter(email=email).first()

        if student:

            if new_password != confirm_password:
                return render(
                    request,
                    "accounts/forgot_password.html",
                    {
                        "error": "Passwords do not match.",
                        "email": email
                    }
                )

            student.password = make_password(new_password)
            student.save()

            return render(
                request,
                "accounts/forgot_password.html",
                {
                    "success": "Password reset successfully. You can login now."
                }
            )

        return render(
            request,
            "accounts/forgot_password.html",
            {"error": "Email address not found."}
        )

    return render(request, "accounts/forgot_password.html")