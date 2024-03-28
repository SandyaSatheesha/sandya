from django.shortcuts import render
import json
from django.http import HttpResponse
from . models import Employee
from django.core.serializers import serialize
from kafka import KafkaProducer
from json import dumps
# Create your views here.

def parse_output(emp_json):
    # convert json to dict
    emp_meta = json.loads(emp_json)
    emp_list = []
    for meta_obj in emp_meta:
        emp = meta_obj['fields']
        emp['id'] = meta_obj['pk']
        emp_list.append(emp)

    emps_json = json.dumps(emp_list)
    return emps_json

def employee_crud(request, pk=None):
    if request.method == 'GET':
        if pk is None:
            # step 1: get all employee object from db  (query set --> is a database)
            emp_qs = Employee.objects.all()

            # step 2: convert queryset object  into json
            emps_json = parse_output(serialize('json', emp_qs))
            return HttpResponse(emps_json, content_type="application/json")
        else:
            # We need to write logic to get employee by id from database
            #step 1: get emp object from db  based on pk
            emp = Employee.objects.get(id=pk)
            #step 2: convert object to python  dict : manually
            emp_dict = {
                'id': emp.id,
                'empid': emp.empid,
                'name': emp.name,
                'age': emp.age,
                'salary': emp.salary,
                'address': emp.address,
            }
            #step 3: convert dict object into json -->json.dumps()
            emp_json = json.dumps(emp_dict)
            #resp_dict = {'message': 'GET By ID method got called!'}
            return HttpResponse(emp_json, content_type="application/json")
    elif request.method == 'POST':
        # step1 read the input data
        emp_input_json = request.body
        # step2
        emp_input_dict = json.loads(emp_input_json)
        '''
        {
            "empid": 1001,
            "name": 'sandya',
            "age": 23,
            "salary": 50000,
            "address": 'chennai',
        }
        '''

        #step3
        employee = Employee(empid=emp_input_dict['empid'], name=emp_input_dict['name'], age=emp_input_dict['age'],
                            salary=emp_input_dict['salary'], address=emp_input_dict['address'])
        employee.save()
        send_message(emp_input_dict)
        resp_dict = {'message': 'Employee Created!!!'}
        return HttpResponse(json.dumps(resp_dict), content_type="application/json")

    elif request.method == 'PUT':
        # step 1: REad employee data to be updated --request.body-->json
        emp_input_json = request.body

        # step 2: convert Json to dict --> json.loads()===> dict
        emp_input_dict = json.loads(emp_input_json)

        # step 3: get Employee from DB by pk ==>Employee.objects.get(id=pk)
        emp_db = Employee.objects.get(id=pk)

        # step 4: update Employee DB objects  with input dict data
        emp_db.empid = emp_input_dict["empid"]
        emp_db.name = emp_input_dict["name"]
        emp_db.age = emp_input_dict["age"]
        emp_db.salary = emp_input_dict["salary"]
        emp_db.address = emp_input_dict["address"]

        # step 5: call the save method  on top of DB object
        emp_db.save()

        # step 6: send the response back to the client saying employee db is updates successgully
        resp_dict = {'message': 'Employee with {} updated successfully!'.format(emp_db.empid)}
        return HttpResponse(json.dumps(resp_dict), content_type="application/json")



    elif request.method == 'DELETE':
        employee = Employee.objects.get(id=pk)
        empid = employee.empid
        employee.delete()
        resp_dict = {'message': 'Employee with {}, Deleted Successfully!!!'.format(empid)}
        return HttpResponse(json.dumps(resp_dict), content_type="application/json")

def send_message(employee):
    print('@@@@@@@@ Kafka Producer Sending a message!!!')
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    producer.send('EMPLOYEE_TOPIC', value=employee)
    producer.flush()
    print('@@@@@@@@ Kafka Producer <<<SENT>>> a message!!!')