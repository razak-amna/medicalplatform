from rest_framework import serializers
from .models import Appointment, Feedback, Doctor, UserProfile, Rule, ChatSession, ChatLog, MedicalHistory, ChatHistory, Notification
from django.contrib.auth.models import User

# Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor',  'appointment_date', 'reason', 'status']
        extra_kwargs = {
            'doctor': {'required': True},
            'appointment_date': {'input_formats': ['%Y-%m-%d']},
            'appointment_time': {'input_formats': ['%H:%M']},
        }
    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)

# Feedback Serializer
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['rating', 'feedback_text']

# Doctor Serializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'dob', 'gender', 'phone_number', 'address', 'medical_history', 'chat_history']

# Rule Serializer
class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['rule_name', 'rule_type', 'rule_description', 'keyword', 'rule_content']

# Chat Session Serializer
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'started_at', 'ended_at', 'status']

    def create(self, validated_data):
        session = ChatSession.objects.create(**validated_data)
        session.started_at = timezone.now()  # Automatically set the current time for `started_at`
        session.save()
        return session

# Chat Log Serializer
class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['session', 'user_message', 'bot_response', 'timestamp']

# Medical History Serializer
class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['user', 'condition', 'treatment', 'date_of_diagnosis']

# Chat History Serializer
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['user', 'message', 'chat_type']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
