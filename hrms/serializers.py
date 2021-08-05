from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


	

class TokenPairSerializer(TokenObtainPairSerializer):
	
	@classmethod
	def get_token(cls, user):
		token = super(TokenPairSerializer, cls).get_token(user)

		# Add custom claims
		token['username'] = user.username
		return token

	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['services'] = [group.name for group in self.user.groups.all()]
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.id
		data['fullname'] = self.user.first_name+" "+self.user.last_name
		data['email'] = self.user.email
		return data


		
class EmployeeSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Employee
		fields = '__all__'
		fields = ('avatar','is_valid','department','role','mobile','title','status','address','gender','joined','birthday','education','employeetype','salary')



class UserSerializer(serializers.HyperlinkedModelSerializer):
	employee = EmployeeSerializer(required=True)

	class Meta:
		model = User
		fields = ('username','email', 'first_name', 'last_name', 'password', 'employee')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		employee_data = validated_data.pop('employee')
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		Employee.objects.create(user=user, **employee_data)
		return user

	def update(self, instance, validated_data):
		employee_data = validated_data.pop('employee')
		employee = instance.employee

		instance.email = validated_data.get('email', instance.email)
		instance.save()

		employee.address = employee_data.get('address', employee.address)
		employee.gender = employee_data.get('gender', employee.gender)
		employee.joined = employee_data.get('joined', employee.joined)
		employee.birthday = employee_data.get('birthday', employee.birthday)
		employee.education = employee_data.get('education,', employee.education)
		employee.avatar = employee_data.get('avatar,', employee.avatar)
		employee.mobile = employee_data.get('mobile,', employee.mobile)
		employee.birthday = employee_data.get('birthday,', employee.birthday)
		employee.gender = employee_data.get('gender,', employee.gender)
		employee.status = employee_data.get('status,', employee.status)
		employee.title = employee_data.get('title,', employee.title)
		employee.joined = employee_data.get('joined,', employee.joined)
		employee.salary = employee_data.get('salary,', employee.salary)
		employee.employeetype = employee_data.get('employeetype,', employee.employeetype)
		employee.save()

		return instance




class DepartmentSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Department
		fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Attendance
		fields = '__all__'

class LeaveSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Leave
		fields = '__all__'

class RecruitmentSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Recruitment
		fields = "__all__"
class RoleSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Role
		fields = "__all__"

class BankSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Bank
		fields = '__all__'
		
class PaymentSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Payment
		fields = '__all__'
