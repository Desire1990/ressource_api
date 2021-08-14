from django.db import connection, transaction, IntegrityError
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django_filters import rest_framework as filters

import traceback, sys, json, base64

from .models import *
from .serializers import *
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser


class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create':
			permission_classes = [AllowAny]
		elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
			permission_classes = [IsLoggedInUserOrAdmin]
		elif self.action == 'list' or self.action == 'destroy':
			permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]



class DepartmentViewset(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, JWTAuthentication)
	permission_classes = [IsAuthenticated, ]
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer


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
