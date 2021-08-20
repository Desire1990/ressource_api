from django.urls import path, include, re_path
from rest_framework import routers
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView

router = routers.DefaultRouter()
router.register("user",UserViewSet)
router.register("employee",EmployeeViewset)
router.register("department", DepartmentViewset)
router.register("attendance", AttendanceViewset)
router.register("attendancyHistory", AttendancyHistoryViewset)
router.register("leave", LeaveViewset)
router.register("bank", BankViewset)
router.register("payment", PaymentViewset)
router.register("role", RoleViewset)

app_name = 'hrms'     

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
]

 