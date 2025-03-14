
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# from django.contrib.auth.models import Euser
from django.db import IntegrityError
from django.urls import reverse
from .models import Department, Leave, LeaveQuota, Role , Euser, TaskAssignment
from django.db import IntegrityError
from .models import Task
from django.utils import timezone 
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth import authenticate, login
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from .models import Department, Role, Euser  # ✅ Euser Import
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_date
from datetime import datetime
from django.contrib.messages import get_messages


# Check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Check if user is employee
def is_employee(user):
    return user.is_authenticated and not user.is_staff

# ✅ Admin Login View
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # ✅ Only Admin Allowed
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "Invalid Admin credentials!")
    
    return render(request, 'admin_login.html')  # Admin Login Page


def employee_login(request):
    storage = get_messages(request)  # ✅ Clear old messages before new login attempt
    list(storage)  # This will consume and clear old messages

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:  # ✅ Only Employee Allowed
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('/employee-dashboard')
        else:
            messages.error(request, "Invalid Employee credentials!")

    return render(request, 'employee_login.html')

from django.shortcuts import redirect

def dashboard_redirect(request):
    if request.user.is_staff:  
        return redirect('/admin_dashboard/')  # ✅ Admin साठी Redirect
    else:
        return redirect('/employee_dashboard/')  # ✅ Employee साठी Redirect


# ✅ Admin Dashboard View
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'home.html')

# ✅ Employee Dashboard View
@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, 'employee_home.html')

# ✅ Logout Function
@login_required
def logout_view(request):
    logout(request)  
    return redirect('/admin_dashboard')
    
User = get_user_model()  # ✅ `Euser` dynamic import करतो (Circular Import टाळतो)

def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)  # **इथे लॉगआउट फंक्शन वापरतोय**
    messages.success(request, "You have successfully logged out.")
    return redirect('/home')  # लॉगिन पेजवर रीडायरेक्ट

# def login(request):  # Optionally, rename to user_login(request) to avoid confusion
#     if request.method == "POST":
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)  # ✅ Using Django's built-in login function
#             messages.success(request, "Login successful!")
#             return redirect('/home')
#         else:
#             messages.error(request, "Invalid username or password. Please try again.")

#     return render(request, 'login.html')

def register_employee(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # ✅ Check if all fields are filled
        if not full_name or not email or not username or not password or not confirm_password:
            messages.error(request, "All fields are required!")
            return redirect('/register')

        # ✅ Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/employee_register')

        # ✅ Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('/employee_register')

        # ✅ Check if email is already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists!")
            return redirect('/employee_register')

        # ✅ Create the user
        name_parts = full_name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('/employee_login')

    return render(request, 'employee_register.html')




@login_required
def employee_detail(request):
    employees = Euser.objects.all()
    context = {'employees': employees}
    return render(request, 'employee_detail.html', context)



def add_employee(request):
    context={}
    if request.method == 'GET':
        departments = Department.objects.all()
        context['departments']=departments

        roles = Role.objects.all()
        context['roles']=roles
        return render (request, 'add_employee.html', context)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        date_of_joining = request.POST.get('date_of_joining')
        dept_id = request.POST.get('dept')  # ✅ Corrected key name
        role_id = request.POST.get('role')  # ✅ Corrected key name

        # print(first_name)
        # print(last_name)
        # print(username)
        # print(password)
        # print(email)
        # print(mobile)
        # print(date_of_joining)
        # print(dept_id)
        # print(role_id)
        
        

        if not dept_id or not role_id:
            return render(request, 'add_employee.html', {
                'error': "Please select a Department and Role!",
            })

        try:
            department = Department.objects.get(dept_id=dept_id)
            # role = Role.objects.get(role_id=role_id)
            role = Role.objects.get(role_id=int(role_id))

            user = Euser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                date_of_joining=date_of_joining,
                dept=department,  # ✅ Fixed Foreign Key Assignment
                role=role  # ✅ Fixed Foreign Key Assignment
            )
            user.set_password(password)
            user.save()

            return redirect('employee_detail')

        except IntegrityError:
            return render(request, 'add_employee.html', {
                'error': "An error occurred while saving. Try again.",
            })

    return render(request, 'add_employee.html')


def update_employee(request, emp_id):
    employee = get_object_or_404(User, id=emp_id)
    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == "POST":
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.username = request.POST['username']
        employee.email = request.POST['email']
        dept_id = request.POST.get('department')
        role_id = request.POST.get('role')

        # 🔹 Username Check (Conflict Avoidance)
        if User.objects.filter(username=employee.username).exclude(id=emp_id).exists():
            context = {
                'error': "Username already exists. Choose a different one.",
                'employee': employee,
                'departments': departments,
                'roles': roles
            }
            return render(request, 'edit_employee.html', context)  # ✅ File Name Updated

        # ✅ **Department & Role Update**
        if dept_id:
            employee.dept = Department.objects.get(id=dept_id)
        if role_id:
            employee.role = Role.objects.get(id=role_id)

        employee.save()  # ✅ Update Employee
        return redirect('employee_detail')  # 🔹 URL name check कर

    context = {
        'employee': employee,
        'departments': departments,
        'roles': roles
    }
    return render(request, 'edit_employee.html', context)  # ✅ File Name Updated



def delete_employee(request, emp_id):
    employee = get_object_or_404(User, id=emp_id)
    
    if request.method == "POST":
        employee.delete()
        return redirect('employee_detail')

    return render(request, 'delete_employee.html', {'employee': employee})



@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})


def add_department(request):
    if request.method == "POST":
        dept_name = request.POST.get('dept_name').strip()  # Remove extra spaces
        description = request.POST.get('description', '').strip()

        if not dept_name:  # Ensure department name is provided
            return render(request, 'add_department.html', {'error': 'Department name is required'})

        # Check if department name already exists
        if Department.objects.filter(dept_name=dept_name).exists():
            return render(request, 'add_department.html', {'error': 'Department name already exists'})

        try:
            Department.objects.create(dept_name=dept_name, description=description)
            return redirect(reverse('department_list'))  # Redirect to department list
        except IntegrityError:
            return render(request, 'add_department.html', {'error': 'Duplicate department entry'})

    return render(request, 'add_department.html')

def edit_department(request, dept_id):  # Accept dept_id as a parameter
    department = get_object_or_404(Department, dept_id=dept_id)

    if request.method == "POST":
        department.dept_name = request.POST['dept_name']
        department.description = request.POST['description']
        department.save()
        return redirect('department_list')  # Redirect after saving

    return render(request, 'edit_department.html', {'department': department})


def delete_department(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    department.delete()
    return redirect('department_list')


@login_required
def roll_list(request):
    roles = Role.objects.all()  # 'roles' नावाने data पाठवायचा
    return render(request, 'roll_list.html', {'roles': roles})  # 'roles' key वापरा


def addroll(request):
    if request.method == "POST":
        role_name = request.POST.get('role_name')
        description = request.POST.get('description')

        print(f"Received Data: {role_name}, {description}")  # Debugging

        # Check if role already exists
        if Role.objects.filter(role_name=role_name).exists():
            messages.error(request, "Role already exists!")
            print("Role already exists!")  # Debugging
        else:
            new_role = Role.objects.create(role_name=role_name, description=description)
            messages.success(request, f"Role '{new_role.role_name}' added successfully!")
            print(f"Saved Role: {new_role.role_name}")  # Debugging

            return redirect('roll_list')  # Redirect after adding role

    return render(request, 'add_roll.html')


@login_required
# 🔹 Task List (Read)
def task_list(request):
    tasks = Task.objects.all()  # ✅ Fetch all tasks
    return render(request, "task_list.html", {"tasks": tasks})  

# 🔹 Create Task
def create_task(request):
    if request.method == "POST":
        task_title = request.POST['task_title']
        task_description = request.POST['task_description']
        task_priority = request.POST['task_priority']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        task_type = request.POST['task_type']

        # ✅ Correct Task Creation
        Task.objects.create(
            task_title=task_title,
            task_description=task_description,
            task_priority=task_priority,
            start_date=start_date,
            end_date=end_date,
            task_type=task_type,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        return redirect('task_list')  # ✅ Redirect to Task List Page

    return render(request, 'create_task.html') 

# 🔹 Update Task
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == "POST":
        task.task_title = request.POST['task_title']
        task.task_description = request.POST['task_description']
        task.task_priority = request.POST['task_priority']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.task_type = request.POST['task_type']
        task.updated_at = timezone.now()
        task.save()
        return redirect('task_list')
    return render(request, 'edit_task.html', {'task': task})

# 🔹 Delete Task
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')


@login_required
def assign_task(request):
    if request.method == "POST":
        task_id = request.POST['task']
        employee_id = request.POST['employee']
        assigned_by_id = request.POST['assigned_by']
        status = request.POST['status']

        task = Task.objects.get(task_id=task_id)
        employee = Euser.objects.get(employee_id=employee_id)
        assigned_by = Euser.objects.get(employee_id=assigned_by_id)

        TaskAssignment.objects.create(
            task=task,
            employee=employee,
            assigned_by=assigned_by,
            status=status
        )

        messages.success(request, "Task assigned successfully!")
        return redirect('task_list')  

    tasks = Task.objects.all()
    employees = Euser.objects.all()
    return render(request, 'assign_task.html', {'tasks': tasks, 'employees': employees})



@login_required
def apply_leave(request):
    if request.method == "POST":
        employee = request.user  

        leave_type = request.POST.get('leave_type')
        reason = request.POST.get('reason')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        total_days = (end - start).days + 1

        leave = Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            reason=reason,
            start_date=start,
            end_date=end,
            total_days=total_days,
            status='Pending',
            approved_by=None
        )
        leave.save()

        print(f"Leave Created: {leave}")  # ✅ Debugging साठी Print करून पाहा  
        messages.success(request, "Leave request submitted successfully!")
        return redirect('leave_history')

    return render(request, 'apply_leave.html')






def leave_history(request):
    if request.user.is_superuser:
        leaves = Leave.objects.all()  # ✅ Admin Users ला सगळ्या Leave Requests दिसतील
    else:
        leaves = Leave.objects.filter(employee=request.user)  # ✅ Regular User ला फक्त त्याचेच Leaves दिसतील

    # print(f"Leaves Found: {leaves}")  # ✅ Debugging साठी Print करून पाहा  

    return render(request, 'leave_history.html', {'leaves': leaves})



def edit_leave(request, leaveid):
    """ Edit leave request (Admin/Employee) """
    # leave = get_object_or_404(Leave, id=leaveid)
    leave = get_object_or_404(Leave, leaveid=leaveid)  # ✅ Correct field name


    if request.method == 'POST':
        leave.leave_type = request.POST['leave_type']
        leave.reason = request.POST['reason']
        
        start_date = parse_date(request.POST['start_date'])
        end_date = parse_date(request.POST['end_date'])
        total_days = (end_date - start_date).days + 1  # ✅ Fix this
        
        leave.start_date = start_date
        leave.end_date = end_date
        leave.total_days = total_days  # ✅ Fix this
        leave.status = request.POST['status']
        leave.save()
        
        messages.success(request, "Leave updated successfully!")
        return redirect('leave_history')

    return render(request, 'edit_leave.html', {'leave': leave})


