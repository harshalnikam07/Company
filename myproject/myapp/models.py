
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model 

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.dept_name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class Euser(AbstractUser):
    employee_id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="euser_groups",  # ✅ Conflict Fix केला
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="euser_permissions",  # ✅ Conflict Fix केला
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "employee"  # ✅ टेबलचं नाव "employee" ठेवलं




class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    TASK_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Team', 'Team'),
    ]

    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=300)
    task_priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES, default='Medium')
    start_date = models.DateField()
    end_date = models.DateField()
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES, default='Individual')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title

    class Meta:
        db_table = "task"  # Table Name



class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    assignment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Euser, on_delete=models.CASCADE, related_name="assigned_tasks")
    assigned_by = models.ForeignKey(Euser, on_delete=models.SET_NULL, null=True, related_name="tasks_assigned")
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.task.task_title} assigned to {self.employee.username}"

    class Meta:
        db_table = "task_assignment"  # ✅ टेबलचं नाव दिलं


    from django.contrib.auth import get_user_model

User = get_user_model()  # Employee Table ला Reference करण्यासाठी

# Leave Table
class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('PL', 'Paid Leave'),
        ('LWP', 'Leave Without Pay'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    leaveid = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaves", null=True, blank=True)  # ✅ Fix
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.employee.first_name} - {self.leave_type} ({self.status})"

    class Meta:
        db_table = "leave"

    def __str__(self):
        employee_name = self.employee.first_name if self.employee else "Anonymous"  
        return f"{employee_name} - {self.leave_type} ({self.status})"

# Leave Quota Table
class LeaveQuota(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('PL', 'Paid Leave'),
        ('LWP', 'Leave Without Pay'),
    ]

    quotaid = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_quotas")
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    total_quota = models.IntegerField()
    used_quota = models.IntegerField(default=0)
    remain_quota = models.IntegerField()

    def __str__(self):
        return f"{self.employee.first_name} - {self.leave_type} Quota"

    class Meta:
        db_table = "leave_quota"