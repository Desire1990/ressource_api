from django.urls import path, include, re_path
from rest_framework import routers
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView


router = routers.DefaultRouter()
router.register("user",UserViewset)
router.register("employee",EmployeeViewset)
router.register("department", DepartmentViewset)
router.register("attendance", AttendanceViewset)
router.register("leave", LeaveViewset)
router.register("bank", BankViewset)
router.register("payment", PaymentViewset)
router.register("profile", ProfileViewset)
router.register("role", RoleViewset)

urlpatterns = [
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls')),
	path('login/', TokenPairView.as_view()),
	path('refresh/', TokenRefreshView.as_view()),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
            VerifyEmailView.as_view(), name='account_confirm_email'),
]
