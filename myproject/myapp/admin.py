from django.contrib import admin
from .models import Department, Role, Euser
from .models import Task, TaskAssignment
from .models import Leave, LeaveQuota



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'status', 'created_at', 'updated_at')
    search_fields = ('dept_name',)
    list_filter = ('status',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'created_at', 'updated_at')
    search_fields = ('role_name',)
    list_filter = ('created_at',)

@admin.register(Euser)
class EuserAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'username', 'email', 'mobile', 'dept', 'role', 'date_of_joining', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'username', 'email', 'mobile')
    list_filter = ('dept', 'role', 'created_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_title', 'task_priority', 'start_date', 'end_date', 'task_type', 'created_at', 'updated_at')
    list_filter = ('task_priority', 'task_type', 'start_date', 'end_date')
    search_fields = ('task_title', 'task_description', 'task_priority', 'task_type')
    ordering = ('-created_at',)  # Newest tasks first

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'task', 'employee', 'assigned_by', 'assigned_date', 'status', 'completed_at')
    list_filter = ('status', 'assigned_date')
    search_fields = ('task__task_title', 'employee__username', 'assigned_by__username')


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leaveid', 'employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'approved_by')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type', 'status')
    ordering = ('-start_date',)

@admin.register(LeaveQuota)
class LeaveQuotaAdmin(admin.ModelAdmin):
    list_display = ('quotaid', 'employee', 'leave_type', 'total_quota', 'used_quota', 'remain_quota')
    list_filter = ('leave_type',)
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type')
    ordering = ('employee',)