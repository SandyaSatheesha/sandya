from django.urls import path
from . import views
urlpatterns = [
    path("employee/", views.employee_crud),
    path("employee/<pk>/", views.employee_crud),
]
