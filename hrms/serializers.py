from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class TokenPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['services'] = [group.name for group in self.user.groups.all()]
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.id
		data['fullname'] = self.user.first_name+" "+self.user.last_name
		data['email'] = self.user.email
		data['avatar'] = self.user.profile.avatar
		return data

class RegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

	class Meta:
		model = User
		fields = ('username','email', 'password', 'first_name', 'last_name')
		extra_kwargs = {
		    'first_name': {'required': True},
		    'last_name': {'required': True}
    	}

	def create(self, validated_data):
		user = User.objects.create(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

		user.set_password(validated_data['password'])
		user.save()

		return user
class ProfileSerializer(serializers.ModelSerializer): 
	def to_representation(self, obj):
		representation = super().to_representation(obj)
		representation['user'] = str(obj.user.email)
		return representation

	def get_id(self, obj):
		return obj.user.id

	class Meta:
		model = Profile
		fields = '__all__'
		read_only_fields = ['subscription_end_date']

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	profile = ProfileSerializer(required=True)
	email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

	class Meta:
		model = User
		exclude = "last_login","is_staff","date_joined","user_permissions"

class EmployeeSerializer(serializers.ModelSerializer): 

	def to_representation(self, obj):
		representation = super().to_representation(obj)
		representation['profile'] = ProfileSerializer(obj.profile, many=False).data
		return representation


	class Meta:
		model = Employee
		fields = '__all__'

		
class DepartmentSerializer(serializers.ModelSerializer): 
	def to_representation(self, obj):
		rep = super().to_representation(obj)
		rep['profile'] = ProfileSerializer(obj.profile, many=False).data
		rep['eepartment'] = ProfileSerializer(obj.eepartment, many=False).data
		rep['role'] = RoleSerializer(obj.role, many=False).data
		return rep

	class Meta:
		model = Department
		fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer): 
	def to_representation(self, obj):
		rep = super().to_representation(obj)
		rep['employeeSerializer'] = EmployeeSerializerSerializer(obj.employeeSerializer, many=False).data
		return rep
	class Meta:
		model = Attendance
		fields = '__all__'

class LeaveSerializer(serializers.ModelSerializer): 
	def to_representation(self, obj):
		rep = super().to_representation(obj)
		rep['employeeSerializer'] = EmployeeSerializerSerializer(obj.employeeSerializer, many=False).data
		return rep
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
	def to_representation(self, obj):
		rep = super().to_representation(obj)
		rep['employeeSerializer'] = EmployeeSerializerSerializer(obj.employeeSerializer, many=False).data
		return rep
	
	class Meta:
		model = Payment
		fields = '__all__'
