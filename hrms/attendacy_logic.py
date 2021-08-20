from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Attendance(models.Model):
	user = models.ForeignKey(User)
	start_at = models.DateTimeField(null=True)
	total_time = models.BigIntegerField()

class AttendanceHistory(models.Model):
	attendance = models.ForeignKey(Attendance)
	time = models.DateTimeField(null=True)

# ===================================================================

attendance = Attendance.objects.filter(user = request.user)
if(not attendance):
	attendance:Attendance = Attendance(...)
	attendance.save()

AttendanceHistory(attendance=attendance, time=datetime.now())
if(not attendance.start_at):
	# aje gutangura ibikorwa
	attendance.start_at = datetime.now()
	attendance.save()
	return Response(...)

worked_time = datetime.now() - attendance.start_at
attendance.total_time += worked_time
attendance.start_at = None
attendance.save()
return Response(...)