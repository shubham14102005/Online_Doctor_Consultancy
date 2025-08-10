from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Doctor, Patient, Appointment, Prescription


from .forms import (
    CustomUserCreationForm,
    DoctorForm,
    PatientForm,
    AppointmentForm,
    PrescriptionForm,
    CustomLoginForm,
    
)

# --------------------- Home View ---------------------
def index(request):
    return render(request, 'index.html')

# --------------------- User Registration ---------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.save()

          
            if user.user_type == 'doctor':
                Doctor.objects.create(
                    user=user,
                    specialization=form.cleaned_data.get('specialization', ''),
                    experience=form.cleaned_data.get('experience', 0),
                    consultation_fee=form.cleaned_data.get('consultation_fee', 0),
                    availability=form.cleaned_data.get('availability', ''),
                    contact_info=form.cleaned_data.get('contact_info', ''),
                )
                login(request, user)
                return redirect('doctor_dashboard')  
            elif user.user_type == 'patient':
                Patient.objects.create(
                    user=user,
                    contact_info=form.cleaned_data.get('contact_info', ''),
                    gender=form.cleaned_data.get('gender', 'M'),
                    age=form.cleaned_data.get('age', 0),
                )
                login(request, user)
                return redirect('patient_dashboard') 

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home') 
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    if request.method in ["POST", "GET"]: 
        logout(request)
        return redirect('login') 
    return redirect('home') 
# --------------------- Dashboard ---------------------

def dashboard(request):
    return render(request, 'index.html')  

# --------------------- Doctor Views ---------------------
@login_required
def doctor_dashboard(request):
    
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    return render(request, 'doctor_dashboard.html', {'doctor': doctor, 'appointments': appointments})

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('specialization')
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

# --------------------- Patient Views ---------------------
@login_required
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    return render(request, 'patient_dashboard.html', {'patient': patient, 'appointments': appointments})

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})

# --------------------- Appointment Views ---------------------
@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = get_object_or_404(Patient, user=request.user)
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})

@login_required
def appointment_list(request):
    if request.user.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor__user=request.user)
    elif request.user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient__user=request.user)
    else:
        appointments = Appointment.objects.all()

    return render(request, 'appointment_list.html', {'appointments': appointments})

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.user == appointment.doctor.user:
        appointment.status = 'Confirmed'
        appointment.save()

    return redirect('appointment_detail', appointment_id=appointment.appointment_id)


@login_required
def book_appointment(request, doctor_id):
  
    doctor = get_object_or_404(Doctor, user_id=doctor_id)
    
  
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.status = 'Pending'  
            appointment.save()
            return redirect('patient_dashboard') 
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form, 'doctor': doctor, 'patient': patient})
# --------------------- Prescription Views ---------------------

@login_required
def prescription_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

   
    if request.user != appointment.doctor.user:
        return redirect('dashboard')  

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.doctor = appointment.doctor
            prescription.patient = appointment.patient
            prescription.save()
            return redirect('doctor_dashboard') 
    else:
        form = PrescriptionForm()

    return render(request, 'prescription_form.html', {'form': form, 'appointment': appointment})
  
@login_required
def prescription_list(request):
    if request.user.user_type == 'doctor':
        prescriptions = Prescription.objects.filter(doctor__user=request.user)
    elif request.user.user_type == 'patient':
        prescriptions = Prescription.objects.filter(patient__user=request.user)
    else:
        prescriptions = Prescription.objects.none()  

    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

