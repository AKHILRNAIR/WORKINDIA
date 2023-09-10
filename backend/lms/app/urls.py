from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_book/", views.add_book, name="add_book"),
    path("list_books/", views.list_books, name="list_books"),
    path("list_students/", views.list_students, name="list_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("list_issued_books/", views.list_issued_books, name="list_issued_books"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("edit_user_profile/", views.edit_user_profile, name="edit_user_profile"),
    path("register_student/", views.register_student, name="register_student"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.logout, name="logout"),
 
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:student_id>/", views.delete_student, name="delete_student"),
    
]