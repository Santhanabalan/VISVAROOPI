#***(1)Returns all employees from employee table
employees = Employee.objects.all()

#(2)Returns first employee in table
firstemployee = Employee.objects.first()

#(3)Returns last employee in table
lastemployee = Employee.objects.last()

#(4)Returns single employee by name
employeeByName = Employee.objects.get(name='Peter Piper')

#***(5)Returns single employee by name
employeeById = employee.objects.get(id=4)

#***(6)Returns all orders related to employee (firstemployee variable set above)
firstEmployee.order_set.all()

#(7)***Returns orders employee name: (Query parent model values)
order = Order.objects.first() 
parentName = order.employee.name

#(8)***Returns products from products table with value of "Out Door" in category attribute
products = Product.objects.filter(category="Out Door")

#(9)***Order/Sort Objects by id
leastToGreatest = Product.objects.all().order_by('id') 
greatestToLeast = Product.objects.all().order_by('-id') 


#(10) Returns all products with tag of "Sports": (Query Many to Many Fields)
productsFiltered = Product.objects.filter(tags__name="Sports")

'''
(11)Bonus
Q: If the employee has more than 1 ball, how would you reflect it in the database?
  
A: Because there are many different products and this value changes constantly you would most 
likly not want to store the value in the database but rather just make this a function we can run
each time we load the employees profile
'''

#Returns the total count for number of time a "Ball" was ordered by the first employee
ballOrders = firstEmployee.order_set.filter(product__name="Ball").count()

#Returns total count for each product orderd
allOrders = {}

for order in firstEmployee.order_set.all():
	if order.product.name in allOrders:
		allOrders[order.product.name] += 1
	else:
		allOrders[order.product.name] = 1

#Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}


#RELATED SET EXAMPLE
class ParentModel(models.Model):
	name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
	parent = models.ForeignKey(ParentModel)
	name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
#Returns all child models related to parent
parent.childmodel_set.all()

