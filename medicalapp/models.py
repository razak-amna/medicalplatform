from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("Other", "Other")])
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.JSONField(blank=True, null=True)  
    chat_history = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Ended", "Ended")], default="Active")

    def __str__(self):
        return f"ChatSession #{self.id} for {self.user.username}"

class ChatLog(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="logs")
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Session #{self.session.id} at {self.start_time}"

class Rule(models.Model):
    rule_name = models.CharField(max_length=100, default='Default Rule Name')
    rule_type = models.CharField(max_length=50)  # e.g., 'intent', 'response', etc.
    rule_description = models.TextField(blank=True, null=True)
    rule_content = models.TextField(default='')  # Store rules as JSON (e.g., intents, responses)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.rule_name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)  
    availability_schedule = models.JSONField(blank=True, null=True)  # To store doctor's schedule

    def __str__(self):
        return f"{self.name} - {self.specialization}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, related_name="appointments")
    appointment_date = models.DateTimeField()
    appointment_time = models.DateTimeField(default=timezone.now)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Canceled", "Canceled")],
        default="Scheduled"
    )
    reason = models.TextField(blank=True, null=True)  # Reason for the appointment

    def __str__(self):
        doctor_name = self.doctor.name if self.doctor else 'No doctor assigned'
        return f"{self.user.username} - {doctor_name} - {self.appointment_date}"


class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255)
    treatment = models.CharField(max_length=255)
    date_of_diagnosis = models.DateField()

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_type = models.CharField(max_length=50)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks", null=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="feedback", null=True, blank=True)
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField()  # Ensuring only positive ratings
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.user.username} - Rating: {self.rating}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if the notification has been read
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Notification to {self.user.username} - Read: {self.is_read}"