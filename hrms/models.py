from django.db import models
import random
from django.utils import timezone
import datetime
import time
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .manager import LeaveManager

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
SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'

LEAVE_TYPE = (
	(SICK,'Sick Leave'),
	(CASUAL,'Casual Leave'),
	(EMERGENCY,'Emergency Leave'),
	(STUDY,'Study Leave'),
)

DAYS = 30






class Department(models.Model):
	'''
	 Department Employee belongs to. eg. Transport, Engineering.
	'''
	name = models.CharField(max_length=125, unique=True)
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
	mobile = models.CharField(max_length=15)
	title = models.CharField(_('Title'),max_length=64,default=MR,choices=TITLE,blank=False,null=True)
	status = models.CharField(_('Marital Status'),max_length=10,default=SINGLE,choices=STATUS,blank=False,null=True)
	address = models.CharField(max_length=100, default='')
	gender = models.CharField(choices=GENDER, max_length=10)
	joined = models.DateTimeField(default=timezone.now, editable=False)
	birthday = models.DateField(_('Birthday'),blank=False,null=False)
	education = models.CharField(_('Education'),help_text='highest educational standard ie. your last level of schooling',max_length=20,default=SENIORHIGH,choices=EDUCATIONAL_LEVEL,blank=False,null=True)
	employeetype = models.CharField(_('Employee Type'),max_length=15,default=FULL_TIME,choices=EMPLOYEETYPE,blank=False,null=True)	
	salary = models.FloatField()

	def __str__(self):
		return f'{self.user}' 

	@property
	def get_full_name(self):
		fullname = ''
		firstname = self.firstname
		lastname = self.lastname
		othername = self.othername

		if (firstname and lastname) is None:
			fullname = firstname +' '+ lastname
			return fullname
		elif othername:
			fullname = firstname + ' '+ lastname +' '+othername
			return fullname
		return

  
   

class Attendance (models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	Approved_by = models.CharField(max_length = 50, help_text = 'Approved by ...')
	hours = models.FloatField(blank=True, null=True, editable=False)

	def save(self, *args, **kwargs):
		if self.start_time and self.end_time:
			self.hours = (self.end_time - self.start_time).seconds // 3600
		super(Attendance, self).save(*args, **kwargs)


	
	def __str__(self):
		return 'Attendance -> '+str(self.hours) +'h'' -> ' + str(self.employee)

	def calcul_heureMensuelle(self):
		pass

	# def save(self, *args, **kwargs):
	# 	start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
	# 	end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
	# 	total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(start_time,'%H:%M:%S'))
	# 	hours = total_time
	# 	super(Attendance, self).save(*args, **kwargs)


class Leave(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	startdate = models.DateField(verbose_name=_('Start Date'),help_text='leave start date is on ..',null=True,blank=False)
	enddate = models.DateField(verbose_name=_('End Date'),help_text='coming back on ...',null=True,blank=False)
	leavetype = models.CharField(choices=LEAVE_TYPE,max_length=25,default=SICK,null=True,blank=False)
	reason = models.CharField(verbose_name=_('Reason for Leave'),max_length=255,help_text='add additional information for leave',null=True,blank=True)
	defaultdays = models.PositiveIntegerField(verbose_name=_('Leave days per year counter'),default=DAYS,null=True,blank=True)
	status = models.CharField(max_length=12,default='pending') #pending,approved,rejected,cancelled
	is_approved = models.BooleanField(default=False) #hide
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	Approved_by = models.CharField(max_length=50, null=True, blank=False)
	# objects = LeaveManager()



	@property
	def pretty_leave(self):
		leave = self.leavetype
		user = self.user
		employee = user.employee_set.first().user.username
		return ('{0} - {1}'.format(employee,leave))



	@property
	def leave_days(self):
		days_count = ''
		startdate = self.startdate
		enddate = self.enddate
		if startdate > enddate:
			return 0
		dates = (enddate - startdate)
		return dates.days
		



	@property
	def leave_approved(self):
		return self.is_approved == True




	@property
	def approve_leave(self):
		if not self.is_approved:
			self.is_approved = True
			self.status = 'approved'
			self.save()


	@property
	def unapprove_leave(self):
		if self.is_approved:
			self.is_approved = False
			self.status = 'pending'
			self.save()

	@property
	def leaves_cancel(self):
		if self.is_approved or not self.is_approved:
			self.is_approved = False
			self.status = 'cancelled'
			self.save()






class Recruitment(models.Model):
	first_name = models.CharField(max_length=25)
	last_name= models.CharField(max_length=25)
	position = models.CharField(max_length=15)
	email = models.EmailField(max_length=25)
	phone = models.CharField(max_length=11)

	def __str__(self):
		return self.first_name +' - '+self.position


class Bank(models.Model):
	name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
	account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
	

	class Meta:
		verbose_name = _('Bank')
		verbose_name_plural = _('Banks')
		ordering = ['-name','-account']


	def __str__(self):
		return ('{0}'.format(self.name))



class Payment(models.Model):
	employee = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = 'employee_payment')
	attendance = models.ForeignKey(Attendance, on_delete= models.CASCADE)
	bank = models.ForeignKey(Bank, on_delete = models.CASCADE, related_name = 'employee_bank')
	date = models.DateTimeField(default=timezone.now, editable=False)
	monthSalary = models.FloatField(editable=False)

	
	def __str__(self):
		return f'{self.date} {self.employee.salary}'

	def heures(self):
		pass #comment  trouver le nombre d'heures pendant un mois noteees nbh tenu pour calculer les salaires


	def heureMensuelle(nbh):
		if nbh<160:
			result = nbh
		elif  nbh<200:
			result = 160 + (nbh-160)*1.25
		else:
			result = 160+(40*1.25)+(nbh-200)*1.5



	def save(self, *args, **kwargs):
		if self.employee and self.attendance:
			# self.monthSalary = self.employee.salary*heureMensuelle
			self.monthSalary = self.employee.salary*self.attendance.hours
		super(Payment, self).save(*args, **kwargs)


	



# gestions des biens et quotation ensembles 