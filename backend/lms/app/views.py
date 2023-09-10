from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Book, IssuedBook, Student, expiry
from .forms import (
    BookForm,
    IssueBookForm,
    StudentRegistrationForm,
    UserLoginForm,
    PasswordChangeForm,
)
from datetime import datetime, timedelta, date

from django.db.models import Q
from django.http import Http404

#@login_required
def home(request):
    return render(request, "index.html")

@login_required
def add_book(request):
    alert = False  # Initialize alert as False by default

    if request.method == "POST":
        form = BookForm(request.POST)  # Use a form for input validation
        if form.is_valid():
            # Extract cleaned data from the form
            name = form.cleaned_data['book_name']
            author = form.cleaned_data['book_author']
            isbn = form.cleaned_data['book_isbn']
            category = form.cleaned_data['book_category']

            # Create a new Book instance
            book = Book.objects.create(
                name=name,
                author=author,
                isbn=isbn,
                category=category,
                available=True  # Set book availability to True initially
            )

            book.save()
            alert = True  # Set alert to True for success

    else:
        form = BookForm()  # Create an empty form for GET requests

    return render(request, "add_book.html", {'form': form, 'alert': alert})

@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {'books': books})

@login_required
def list_students(request):
    students = Student.objects.all()
    return render(request, "list_students.html", {'students': students})

@login_required
def issue_book(request):
    alert = False  # Initialize alert as False by default

    if request.method == "POST":
        form = IssueBookForm(request.POST)  # Use a form for input validation
        if form.is_valid():
            # Extract cleaned data from the form
            student_id = form.cleaned_data['student_id']
            isbn = form.cleaned_data['isbn']

            # Create a new IssuedBook instance
            issued_book = IssuedBook.objects.create(
                student_id=student_id,
                isbn=isbn,
                issued_date=datetime.today(),  # Set the issued date
                return_date=expiry(),  # Calculate the return date using your `expiry` function
            )

            issued_book.save()
            alert = True  # Set alert to True for success

    else:
        form = IssueBookForm()  # Create an empty form for GET requests

    return render(request, "issue_book.html", {'form': form, 'alert': alert})

@login_required
def list_issued_books(request):
    issued_books = IssuedBook.objects.all()
    book_details = []

    for issued_book in issued_books:
        days = (date.today() - issued_book.issued_date).days
        fine = 0

        if days > 14:
            fine = (days - 14) * 5

        book = Book.objects.get(isbn=issued_book.isbn)
        student = Student.objects.get(user=issued_book.student_id)

        book_detail = {
            'student_name': student.user.username,
            'student_id': student.user_id,
            'book_name': book.name,
            'isbn': book.isbn,
            'issued_date': issued_book.issued_date,
            'expiry_date': issued_book.return_date,
            'fine': fine,
        }

        book_details.append(book_detail)

    return render(request, "list_issued_books.html", {'issued_books': issued_books, 'book_details': book_details})

@login_required
def student_issued_books(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(Book.objects.filter(isbn=i.isbn))
        students = list(Student.objects.filter(user=i.student_id))
        i=0
        for l in books:
            t=(students[i].user,students[i].user_id,books[i].name,books[i].isbn,issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required
def user_profile(request):
    return render(request, "profile.html")

@login_required
def edit_user_profile(request):
    alert = False  # Initialize alert as False by default
    student = Student.objects.get(user=request.user)

    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        # Update the user-related fields
        request.user.email = email
        request.user.save()

        # Update the student model fields
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.save()

        alert = True  # Set alert to True for success

    return render(request, "edit_user_profile.html", {'student': student, 'alert': alert})


def register_student(request):
    if request.method == 'POST':
        print(0)
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            print(1)
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            login(request, user)
            return render(request, 'index.html')
    else:
        print(2)
        form = StudentRegistrationForm()
        return render(request, 'register_student.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def student_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
    else:
        form = UserLoginForm()
    return render(request, 'student_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')  # Replace 'admin_dashboard' with your admin dashboard URL
            else:
                messages.error(request, 'Invalid admin login credentials')
    else:
        form = UserLoginForm()
    return render(request, 'admin_login.html',{'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully')
    return redirect('list_books')

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully')
    return redirect('list_students')


