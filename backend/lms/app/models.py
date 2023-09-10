from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    category = models.CharField(max_length=50)

    def _str_(self):
        return f"{self.name} [{self.isbn}]"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def _str_(self):
        return f"{self.user} [{self.branch}] [{self.classroom}] [{self.roll_no}]"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(default=expiry)

    def _str_(self):
        return f"Issued Book: {self.book.name} by {self.book.author} to {self.student.user.username}"