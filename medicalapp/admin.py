from django.contrib import admin
from .models import UserProfile, ChatSession, ChatLog, Rule, Appointment, Feedback, Notification, Doctor

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dob", "gender")
    search_fields = ("user__username", "gender")
    list_filter = ("gender",)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "started_at", "ended_at", "status")
    list_filter = ("status", "started_at")
    search_fields = ("user__username",)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "user_message", "timestamp")
    search_fields = ("session__user__username", "user_message", "bot_response")

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('rule_name', 'rule_type', 'rule_description', 'keyword')  # Fields to display in the list view
    search_fields = ('rule_name', 'rule_type', 'rule_description', 'keyword')  # Fields to search in the admin
    list_filter = ('rule_type',)  # Allows filtering by 'rule_type'
    ordering = ('rule_name',)  # Order by rule_name by default

    # You can customize the form used for adding/editing the rule
    fieldsets = (
        (None, {
            'fields': ('rule_name', 'rule_type', 'rule_description', 'rule_content')
        }),
    )

    # Optionally, you can also customize the view in the admin (e.g., how the data is displayed, inline models)
    # For example, you can define a custom method to display the 'rule_content' in a more readable format.

    def get_readonly_fields(self, request, obj=None):
        # Make the rule content read-only for admins
        if obj:
            return self.readonly_fields + ('rule_content',)
        return self.readonly_fields

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'contact_info', 'availability_schedule')
    search_fields = ('name', 'specialization', 'availability_schedule')
    list_filter = ('specialization',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "doctor", "appointment_date", "reason", "status")
    list_filter = ("status", "doctor", "appointment_date")
    search_fields = ("user__username", "doctor__name")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session", "rating", "created_at")
    search_fields = ("user__username", "feedback_text")
    list_filter = ("rating",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "sent_at", "is_read")
    search_fields = ("user__username", "message")
    list_filter = ("is_read", "sent_at")
