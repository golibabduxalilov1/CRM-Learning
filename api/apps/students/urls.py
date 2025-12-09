from django.urls import path
from . import views

urlpatterns = [
    path("", views.StudentListCreateView.as_view(), name="student-list"),
    path("<int:pk>/", views.StudentDetailView.as_view(), name="student-detail"),
]
