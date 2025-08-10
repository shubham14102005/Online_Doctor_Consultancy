from .import views
from django.urls import path


urlpatterns = [
     # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),


    path('dashboard/', views.dashboard, name='dashboard'),
    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'), 
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Appointments
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'), 

     path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),  
    path('appointments/<int:appointment_id>/confirm/', views.confirm_appointment, name='confirm_appointment'),

    # Prescriptions
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/create/<int:appointment_id>/', views.prescription_create, name='prescription_create'),

]