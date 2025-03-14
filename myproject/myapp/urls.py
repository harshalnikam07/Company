from django.urls import include, path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from .views import admin_dashboard, employee_dashboard



urlpatterns = [
    path('employee_login/', views.employee_login, name='employee_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('home', views.home),
    # path('employee_detail', views.employee_detail),
    path('employee_detail', views.employee_detail, name='employee_detail'),  
    path('add_employee', views.add_employee),
    # path('login', views.login),
    path('logout/', views.user_logout, name='logout'),
    path('departments/', views.department_list, name='department_list'),
    path('add_department/', views.add_department),
    path('edit_department/<int:dept_id>/', views.edit_department, name='edit_department'),  # ✅ Edit Route
    path('delete_department/<int:dept_id>/', views.delete_department, name='delete_department'),  # ✅ Delete Route
    # path('roll', views.roll_list),
    path('roll_list/', views.roll_list, name='roll_list'),
    path('addroll', views.addroll),
    path('update_employee/<int:emp_id>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('tasks/', views.task_list, name='tasks'),
    path('create_tasks', views.create_task, name='create_tasks'),
    path('update_tasks/<int:task_id>/', views.update_task, name='update_tasks'),  # ✅ Update Task
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),  # ✅ Delete Task
    path('assign-task/', views.assign_task, name='assign-task'),
    path('task-list/', views.task_list, name='task_list'),
    path('register_employee/', views.register_employee, name='register_employee'),
    # path('register_admin/', views.register_admin, name='register_admin'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave-history/', views.leave_history, name='leave_history'),  # ✅ Fix name
    path('edit-leave/<int:leaveid>/', views.edit_leave, name='edit_leave'),

]