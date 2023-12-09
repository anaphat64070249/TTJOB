from ..services.EmployeeService import Employees;

from flask import Blueprint, request

employee = Blueprint('employee', __name__);

employeeService = Employees();

@employee.route("/all", methods=['GET'])
def getAll():
    return employeeService.getEmployees();

@employee.route("/create", methods=["POST"])
def create():
    body = request.values.to_dict();
    files = request.files.to_dict();
    reply = employeeService.create(body, files);
    return reply;

@employee.route("/infoAndEmp/all", methods=["GET"])
def getInfoAndEmp_all():
    return employeeService.getInfomationAndEmployee_All();

@employee.route("/<emp_id>", methods=["GET"])
def getEmployee_by_id(emp_id: int):
    return employeeService.getEmployee_by_emp_id(emp_id);

@employee.route("/infoAndEmp/<emp_id>", methods=["GET"])
def getInfoAndEmp_by_id(emp_id: int):
    return employeeService.getInfoAndEmployee_by_id(emp_id);

@employee.route("/address/<emp_id>", methods=["GET"])
def getAddress_by_id(emp_id: int):
    return employeeService.getAddress_by_id(emp_id);

@employee.route("/fullName/<emp_id>", methods=["GET"])
def getFullName(emp_id: int):
    return employeeService.getAccount_getFullName(emp_id);