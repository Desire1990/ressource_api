from django.db import connection, transaction, IntegrityError
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters import rest_framework as filters

import traceback, sys, json, base64

from .models import *
from .serializers import *

def getToken(jwt:str)->list:
	liste = token.split(".")[:-1]
	new_liste = []

	for group in liste:
		missing = len(group) % 4
		if missing: group += '=' * missing
		content = base64.standard_b64decode(group)
		new_liste.append(json.loads(content))
		
	return new_liste

class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer

class UserViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, IsAdminUser]
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = request.data
		user = User(
			username = data.get("username"),
			first_name = data.get("first_name"),
			last_name = data.get("last_name")
		)
		user.set_password("password")
		
		user.save()
		serializer = UserSerializer(user, many=False)
		return Response(serializer.data, 201)

	def update(self, request, *args, **kwargs):
		user = request.user
		data = request.data
		username = data.get("username")
		if username : user.username = username
		password = data.get("password")
		if password : user.set_password(password)
		user.save()
		serializer = UserSerializer(user, many=False)
		return Response(serializer.data, 201)

	def patch(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		user = self.get_object()
		user.is_active = False
		user.save()
		return Response({'status': 'success'}, 204)


class DepartmentViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer

class ProfileViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

class EmployeeViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer

class AttendanceViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer

class LeaveViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Leave.objects.all()
	serializer_class = LeaveSerializer
	filterset_fields = ('user', )

class BankViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Bank.objects.all()
	serializer_class = BankSerializer

class PaymentViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated, ]
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	filter_backends = (filters.DjangoFilterBackend,)


class RoleViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated, ]
	queryset = Role.objects.all()
	serializer_class = RoleSerializer
	filter_backends = (filters.DjangoFilterBackend,)

