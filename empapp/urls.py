from django.urls import path
from . import views

urlpatterns = [
    path('employee/', views.create_employee),
    path('list_emp/', views.list_employees),
    path('delete_emp/', views.delete_emp),
    path('ems/', views.ems),
    path('update_employee/<pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<pk>/', views.delete_employee, name='delete_employee'),
    # http://localhost:8000/delete_employee/11/

    # http://127.0.0.1:8000/empapp/get_employee/1234
    path('get_employee/<pk>/', views.get_employee_by_id, name='get_employee'),
]




