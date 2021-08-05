from django.db import models
import random
from django.utils import timezone
import datetime
import time
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

STATUS = (
	('PRESENT', 'PRESENT'),
	('ABSENT', 'ABSENT'),
	('UNAVAILABLE', 'UNAVAILABLE')
)

MARRIED = 'Married'
SINGLE = 'Single'
DIVORCED = 'Divorced'
WIDOW = 'Widow'
WIDOWER = 'Widower'

MALE = 'male'
FEMALE = 'female'
OTHER = 'other'
NOT_KNOWN = 'Not Known'

GENDER = (
	(MALE,'Male'),
	(FEMALE,'Female'),
	(OTHER,'Other'),
	(NOT_KNOWN,'Not Known'),
	)

MR = 'Mr'
MRS = 'Mrs'
MSS = 'Mss'
DR = 'Dr'
SIR = 'Sir'
MADAM = 'Madam'


FULL_TIME = 'Full-Time'
PART_TIME = 'Part-Time'
CONTRACT = 'Contract'
INTERN = 'Intern'


OLEVEL = 'O-LEVEL'
SENIORHIGH = 'Senior High'
JUNIORHIGH = 'Junior High'
TERTIARY = 'Tertiary'
PRIMARY = 'Primary Level'
OTHER = 'Other'




TITLE = (
	(MR,'Mr'),
	(MRS,'Mrs'),
	(MSS,'Mss'),
	(DR,'Dr'),
	(SIR,'Sir'),
	(MADAM,'Madam'),
	)

EMPLOYEETYPE = (
	(FULL_TIME,'Full-Time'),
	(PART_TIME,'Part-Time'),
	(CONTRACT,'Contract'),
	(INTERN,'Intern'),
	)

EDUCATIONAL_LEVEL = (
	(SENIORHIGH,'Senior High School'),
	(JUNIORHIGH,'Junior High School'),
	(PRIMARY,'Primary School'),
	(TERTIARY,'Tertiary/University/Polytechnic'),
	(OLEVEL,'OLevel'),
	(OTHER,'Other'),
	)



class Department(models.Model):
	'''
	 Department Employee belongs to. eg. Transport, Engineering.
	'''
	name = models.CharField(max_length=125)
	description = models.CharField(max_length=125,null=True,blank=True)
	created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
	updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


	class Meta:
		verbose_name = _('Department')
		verbose_name_plural = _('Departments')
		ordering = ['name','created']
	
	def __str__(self):
		return self.name



class Role(models.Model):
	'''
		Role Table eg. Staff,Manager,H.R ...
	'''
	name = models.CharField(max_length=125, unique = True)
	description = models.CharField(max_length=125,null=True,blank=True)

	created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
	updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


	class Meta:
		verbose_name = _('Role')
		verbose_name_plural = _('Roles')
		ordering = ['name','created']


	def __str__(self):
		return self.name



class Employee(models.Model):
	STATUS = (
		(MARRIED,'Married'),
		(SINGLE,'Single'),
		(DIVORCED,'Divorced'),
		(WIDOW,'Widow'),
		(WIDOWER,'Widower'),
		)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar  = models.ImageField(null=True, blank=True)
	is_valid = models.BooleanField(default = False)

	department = models.ForeignKey(Department,on_delete=models.CASCADE, null=True)
	role =  models.ForeignKey(Role,verbose_name =_('Role'),on_delete=models.CASCADE,null=True,default=None)
	emp_id = models.CharField(max_length=64, default='emp'+str(random.randrange(100,999,1)))
	mobile = models.CharField(max_length=15)
	title = models.CharField(_('Title'),max_length=64,default=MR,choices=TITLE,blank=False,null=True)
	status = models.CharField(_('Marital Status'),max_length=10,default=SINGLE,choices=STATUS,blank=False,null=True)
	address = models.CharField(max_length=100, default='')
	gender = models.CharField(choices=GENDER, max_length=10)
	banque = models.ForeignKey("Bank", on_delete=models.CASCADE)
	compte = models.CharField(max_length=255)
	joined = models.DateTimeField(default=timezone.now, editable=False)
	birthday = models.DateField(_('Birthday'),blank=False,null=False)
	education = models.CharField(_('Education'),help_text='highest educational standard ie. your last level of schooling',max_length=20,default=SENIORHIGH,choices=EDUCATIONAL_LEVEL,blank=False,null=True)
	employeetype = models.CharField(_('Employee Type'),max_length=15,default=FULL_TIME,choices=EMPLOYEETYPE,blank=False,null=True)	
	salary = models.FloatField()

	def __str__(self):
		return f'{self.user.username}' 

  
   

class Attendance (models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
	date = models.DateField(auto_now_add=True)

	def save(self,*args, **kwargs):
		super(Attendance,self).save(*args, **kwargs)
	
	def __str__(self):
		return 'Attendance -> '+str(self.date) + ' -> ' + str(self.employee)

class Leave (models.Model):
	STATUS = (('approved','APPROVED'),('unapproved','UNAPPROVED'),('decline','DECLINED'))
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
	start = models.DateTimeField(default=timezone.now)

	def __str__(self):

class Recruitment(models.Model):
	first_name = models.CharField(max_length=25)
	last_name= models.CharField(max_length=25)
	position = models.CharField(max_length=15)
	email = models.EmailField(max_length=25)
	phone = models.CharField(max_length=11)

	def __str__(self):
		return self.first_name +' - '+self.position


class Bank(models.Model):
	# access table: employee.bank_set.
	# employee = models.ForeignKey('Employee',help_text='select employee(s) to add bank account',on_delete=models.CASCADE,null=True,blank=False)
	name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
	account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
	# branch = models.CharField(_('Branch'),help_text='which branch was the account issue',max_length=125,blank=True,null=True)
	# salary = models.DecimalField(_('Starting Salary'),help_text='This is the initial salary of employee',max_digits=16, decimal_places=2,null=True,blank=False)

	# created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
	# updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


# 	class Meta:
# 		verbose_name = _('Bank')
# 		verbose_name_plural = _('Banks')
# 		ordering = ['-name','-account']
	class Meta:
		verbose_name = _('Bank')
		verbose_name_plural = _('Banks')
		ordering = ['-name','-account']


# 	def __str__(self):
# 		return ('{0}'.format(self.name))



class Payment(models.Model):
	employee = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = 'employee_payment')
	bank = models.ForeignKey(Bank, on_delete = models.CASCADE, related_name = 'employee_bank')
	date = models.DateTimeField(default=timezone.now, editable=False)

	def __str__(self):
		return f'{self.date}'



# gestions des biens et quotation ensembles 
