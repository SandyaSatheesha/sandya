from django.shortcuts import render, redirect
from .models import Employee
from django.http import HttpResponse

# Create your views here.
def create_employee(request):
    #How to check incoming request is GET/POST???
    if request.method == 'GET':
        return render(request, 'empapp/employee_form.html')
    elif request.method == 'POST':
        # STEP-1: Read Employee input data
        empid = request.POST.get('emp_id')
        name = request.POST.get('emp_name')
        age = request.POST.get('emp_age')
        salary = request.POST.get('emp_salary')
        address = request.POST.get('emp_address')

        # STEP-2: Create "Employee Model" Object using Employee input data
        employee = Employee(empid=empid, name=name, age=age, salary=salary,
                            address=address)

        # STEP-3: call save() method on "Emplyee Model" Object
        employee.save()

        # STEP-4: Return response to the client saying that Employee Created successfully
        return HttpResponse("<h1 style='color: green'>Employee Created!!!</h1>")

def list_employees(request):
    #STEP-1: x = Get all employees from Database table(EMPLOYEE) ===> QuerySet
    ### employees = {emp1, emp2}
    employees_db = Employee.objects.all()

    # STEP-2 - Create Context object(dict) with QuerySet
    context_data = {
        "employees": employees_db
    }

    # STEP-3 - Send context object through render() function
    return render(request, 'empapp/list_emp.html', context=context_data)

def delete_emp(request):
    if request.method == 'GET':
        return render(request, 'empapp/del_emp_form.html')
    elif request.method == 'POST':
        #STEP-1: read the input employee id to be deleted 3
        id_input = request.POST.get('emp_pk')

        #STEP-2: Get Employee Object from DB based on input employee id... Employee Model Objct
        try:
            employee = Employee.objects.get(id=id_input)
            employee.delete()
            resp_msg = '<h1 style="color: green">Employee Deleted successfully!!!</h1>'
        except Exception:
            resp_msg = '<h1 style="color: red">Sorry, Employee with id {} did not find in the DB!!!</h1>'.format(id_input)
        return HttpResponse(resp_msg)

def ems(request):
    if request.method == 'GET':
        # STEP-1: x = Get all employees from Database table(EMPLOYEE) ===> QuerySet
        ### employees = {emp1, emp2}
        employees_db = Employee.objects.all()

        # STEP-2 - Create Context object(dict) with QuerySet
        context_data = {
            "employees": employees_db
        }

        # STEP-3 - Send context object through render() function
        return render(request, 'empapp/ems.html', context=context_data)
    elif request.method == 'POST':
        # STEP-1: Read Employee input data
        empid = request.POST.get('emp_id')
        name = request.POST.get('emp_name')
        age = request.POST.get('emp_age')
        salary = request.POST.get('emp_salary')
        address = request.POST.get('emp_address')

        # STEP-2: Create "Employee Model" Object using Employee input data
        employee = Employee(empid=empid, name=name, age=age, salary=salary,
                            address=address)

        # STEP-3: call save() method on "Emplyee Model" Object
        employee.save()

        # STEP-4: Return response to the client saying that Employee Created successfully
        # return HttpResponse("<h1 style='color: green'>Employee Created!!!</h1>")
        return redirect('/empapp/ems/')

def update_employee(request, pk):
    employee_db = Employee.objects.get(id=pk)

    employee_db.empid = request.POST.get("emp_id")#4455
    employee_db.name = request.POST.get("emp_name")
    employee_db.age = request.POST.get("emp_age")
    employee_db.salary = request.POST.get("emp_salary")
    employee_db.address = request.POST.get("emp_address")

    employee_db.save()
    return redirect('/empapp/ems/')

def delete_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    employee.delete()
    return redirect('/empapp/ems/')

def get_employee_by_id(request, pk):
    print("@@@@@@@@@@@@@@@@@@@@@@Inside get_employee_by_id")
    employee = Employee.objects.get(id=pk)
    employee_data = {'employee_info': employee}

    return render(request, 'empapp/emp_details_model.html', context=employee_data)
