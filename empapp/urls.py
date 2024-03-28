from django.urls import path
from . import views
urlpatterns = [
    path("create_emp/", views.create_employee, name="create_emp"),
    path("ems/", views.ems_home, name="ems"),
    path("update_emp/<pk>/", views.update_employee, name='update_emp'),
    path("delete_emp/<pk>/", views.delete_employee, name='delete_emp'),
]