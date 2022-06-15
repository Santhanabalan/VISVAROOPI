from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from django.db.models import Sum
from .models import *
from .forms import TaskForm, CreateUserForm, EmployeeForm
from .filters import TaskFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	tasks = Task.objects.all()
	employees = Employee.objects.all()

	total_employees = employees.count()

	total_tasks = tasks.count()
	completed = tasks.filter(status='Completed').count()
	pending = tasks.filter(status='Pending').count()

	context = {'tasks':tasks, 'employees':employees,
	'total_tasks':total_tasks,'completed':completed,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def userPage(request):
	tasks = request.user.employee.task_set.all()

	total_tasks = tasks.count()
	completed = tasks.filter(status='Completed').count()
	pending = tasks.filter(status='Pending').count()

	print('TaskS:', tasks)

	context = {'tasks':tasks, 'total_tasks':total_tasks,
	'completed':completed,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def accountSettings(request):
	employee = request.user.employee
	form = EmployeeForm(instance=employee)

	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def givenTasks(request):
	givenTasks = GivenTask.objects.all()
	current_price= GivenTask.objects.all().aggregate(Sum('price'))
	total_price= {'price':20000000}
	rem= total_price['price']-current_price['price__sum']
	remaining= {'remaining':rem}
	context = {'givenTasks':givenTasks ,'current_price':current_price,'total_price':total_price,'remaining':remaining}
	return render(request, 'accounts/givenTasks.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee(request, pk_test):
	employee = Employee.objects.get(id=pk_test)

	tasks = employee.task_set.all()
	task_count = tasks.count()

	myFilter = TaskFilter(request.GET, queryset=tasks)
	tasks = myFilter.qs 

	context = {'employee':employee, 'tasks':tasks, 'task_count':task_count,
	'myFilter':myFilter}
	return render(request, 'accounts/employee.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createTask(request, pk):
	TaskFormSet = inlineformset_factory(Employee, Task, fields=('givenTask', 'status'), extra=10 )
	employee = Employee.objects.get(id=pk)
	formset = TaskFormSet(queryset=Task.objects.none(),instance=employee)
	#form = TaskForm(initial={'employee':employee})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = TaskForm(request.POST)
		formset = TaskFormSet(request.POST, instance=employee)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/task_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)
	print('Task:', task)
	if request.method == 'POST':

		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/task_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteTask(request, pk):
	task = Task.objects.get(id=pk)
	if request.method == "POST":
		task.delete()
		return redirect('/')

	context = {'item':task}
	return render(request, 'accounts/delete.html', context)