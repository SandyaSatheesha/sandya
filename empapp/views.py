from django.shortcuts import render, redirect
from .models import Employee
# Create your views here.
def ems_home(request):
    employees = Employee.objects.all();
    emp_data = {
        'employees': employees
    }
    #get all employee data from the table - query set obj (more than one obj)
    #create a dict obj & add employee data to the dict
    #send dict object to the emdhome.html througn contect object
    return render(request, "empapp/emshome.html", context=emp_data)

def create_employee(request):
    if request.method == 'GET':
        return render(request, "empapp/create_employee_form.html")
    elif request.method == 'POST':
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        age = request.POST.get('age')
        salary = request.POST.get('salary')
        address = request.POST.get('address')
        employee = Employee(empid=empid, name=name, age=age, salary=salary, address=address)
        employee.save()
        return redirect('/empapp/ems')
       # emp_dict = {
       #     "message": "Employee Created Successfully"
       # }
      #  return render(request, "empapp/success.html", context=emp_dict)

def update_employee(request, pk):
    employee_db = Employee.objects.get(id=pk)
    if request.method == 'GET':
        emp_dict = {
            "employee": employee_db
        }
        return render(request, "empapp/create_employee_form.html", context=emp_dict)
    elif request.method == 'POST':
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        age = request.POST.get('age')
        salary = request.POST.get('salary')
        address = request.POST.get('address')

        employee_db.empid = empid
        employee_db.name = name
        employee_db.age = age
        employee_db.salary = salary
        employee_db.address = address
        employee_db.save()
        return redirect("/empapp/ems")

def delete_employee(request, pk):
    employee_db = Employee.objects.get(id=pk)
    employee_db.delete()
    return redirect('/empapp/ems')





