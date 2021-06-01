from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name= 'dashboard'),
    path('signup/', views.signup, name='signup'), 
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'), 
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'), 
    path('admission/', views.AdmissionView.as_view(), name='admission'), 
    path('account_verify/email=<email>', views.resendEmail, name='resendemail')


]

