from django import forms
from .models import Doctor, Patient, User, Appointment, Prescription
from django.contrib.auth.forms import UserCreationForm


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience', 'consultation_fee', 'availability', 'contact_info']


class CustomUserCreationForm(UserCreationForm):
    specialization = forms.CharField(required=False)
    experience = forms.IntegerField(required=False, min_value=0, initial=0)
    consultation_fee = forms.IntegerField(required=False, min_value=0, initial=0)
    availability = forms.CharField(required=False)
    contact_info = forms.CharField(required=False)
    age = forms.IntegerField(required=False, min_value=0, initial=0)
    gender = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'user_type', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == "doctor":
            if not cleaned_data.get("specialization"):
                self.add_error("specialization", "Specialization is required for doctors.")
            if cleaned_data.get("experience") is None:
                self.add_error("experience", "Experience is required for doctors.")
            if cleaned_data.get("consultation_fee") is None:
                self.add_error("consultation_fee", "Consultation fee is required for doctors.")
        if user_type == "patient":
            if not cleaned_data.get("age"):
                self.add_error("age", "Age is required for Patients.")
            if not cleaned_data.get("contact_info"):
                self.add_error("contact_info", "Contact is required for Patients.")
            if not cleaned_data.get("gender"):
                self.add_error("gender", "Gender is required for Patients.")
            
        return cleaned_data
    
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'contact_info']

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'required'
        })
    )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [ 'medications', 'notes']
        widgets = {
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
