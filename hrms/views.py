from django.db import connection, transaction, IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from .models import *
from .serializers import *
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser

import traceback, sys, json, base64

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


class AttendanceViewset(mixins.ListModelMixin,
						mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin,
						viewsets.GenericViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]  
	permission_classes = [IsAuthenticated]
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer

	@transaction.atomic
	@action(methods=['GET'], detail=False, url_name=r'attendence', url_path="attendence",  permission_classes=[IsAuthenticated])
	def attendance(self, request):
		employee:Employee = request.user.employee
		attendances = Attendance.objects.filter(employee = employee)
		if(not attendances):
			attendance:Attendance = Attendance(
				employee = employee,
				start_at = datetime.now(),
				total_hours = 0
			)
			attendance.save()
			AttendancyHistory(attendance=attendance).save()
			return Response({'status': 'success'}, 201)

		attendance = attendances.first()
		AttendancyHistory(attendance=attendance).save()
		if(not attendance.start_at):
			# aje gutangura ibikorwa
			attendance.start_at = datetime.now()
			attendance.save()
			return Response({'status': 'success'}, 201)
		else:
			worked_time = datetime.now() - attendance.start_at.replace(tzinfo=None)
			attendance.total_hours = (attendance.total_hours or 0) + worked_time.total_seconds()
			attendance.start_at = None
			attendance.save()
			return Response({'status': 'success'}, 201) 


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
	# filter_backends = (filters.DjangoFilterBackend,)


class RoleViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated, ]
	queryset = Role.objects.all()
	serializer_class = RoleSerializer
	# filter_backends = (filters.DjangoFilterBackend,)

class AttendancyHistoryViewset(mixins.ListModelMixin,
						mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin,
						viewsets.GenericViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated, ]
	queryset = AttendancyHistory.objects.all()
	serializer_class = AttendancyHistoryserializer
	# filter_backends = (filters.DjangoFilterBackend,)
