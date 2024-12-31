from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/<str:user_id>/', views.user_profile_detail, name='user_profile_detail'),  # User profile details

    # Appointment URLs
    path('appointments/', views.appointment_view, name='appointment_list'),
    path('create-appointments/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:pk>/', views.appointment_view, name='appointment_detail'),

    # Feedback
    path('feedback/', views.submit_feedback, name='submit_feedback'),

    # Notification URLs
    path('create-notifications/', views.create_notification, name='create-notification'),
    path('notifications/', views.get_notifications, name='get-notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_as_read, name='mark-notification-read'),

    # Doctor URLs
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_list, name='doctor-detail'),
    path('create-doctors/', views.create_doctor, name='create_doctor'),

    # Chatbot Rules
    path('rules/', views.chat_rules, name='chat_rules'),
    path('create-rules/', views.add_chat_rules, name='add_chat_rule'),
    path('rules/<int:pk>/', views.chat_rules, name='chat_rule_detail'),  # Specific rule detail

    # Chat Sessions
    path('create-chat-sessions/', views.create_chat_session, name='create_chat_session'),
    path('chat-sessions/<int:pk>/', views.chat_session_detail, name='chat_session_detail'),
    path('chat-sessions/<int:session_id>/logs/', views.get_chatlog, name='get_chatlogs'),
    path('chat-sessions/<int:session_id>/create-logs/', views.create_chatlog, name='create_chatlog'),

    # Creating and updating user profile
    path('create-user-profile/', views.create_user_profile, name='create-user-profile'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

