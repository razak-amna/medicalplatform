from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Appointment, Feedback, Notification, Doctor, UserProfile, Rule, ChatSession, ChatLog
from .serializers import AppointmentSerializer, FeedbackSerializer, NotificationSerializer, DoctorSerializer, UserProfileSerializer, RuleSerializer, ChatSessionSerializer, ChatLogSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import random


# Home view
@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    data = {'message': "Medical Assistance Platform"}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({"error": "All fields are required (username, password, email)."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User  with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"message": "User  registered successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"detail": "Login successful.", "userId": user.id}, status=200)
    else:
        return Response({"detail": "Invalid credentials."}, status=401)

        
# Appointment Views
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def appointment_view(request, pk=None):
    if pk:
        # Handle logic for a single appointment
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        # Handle logic for listing all appointments
        if request.method == 'GET':
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)

    # Return 405 if the method is not allowed
    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_appointment(request):
    user = request.user
    
    # Extract data from the request
    data = request.data
    doctor_id = data.get('doctor_id')
    appointment_date = data.get('appointment_date')
    reason = data.get('reason')

    # Validate the input
    if not doctor_id or not appointment_date or not reason:
        return Response({"detail": "All fields (doctor_id, appointment_date, reason) are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if the doctor exists
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # Create the appointment
    appointment = Appointment.objects.create(
        user=user,
        doctor=doctor,
        appointment_date=appointment_date,
        reason=reason
    )
    
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



# Feedback Views
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_feedback(request):
    user = request.user
    # Add the user to the feedback data
    data = request.data.copy()  # Make a mutable copy of the data
    data['user'] = user.id  # Add the user ID to the data

    serializer = FeedbackSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Chatbot Views
@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_response(request):
    user_message = request.data.get('user_message', '')
    rules = Rule.objects.all()
    bot_response = "I'm sorry, I don't understand that."

    for rule in rules:
        if rule.keyword and rule.keyword.lower() in user_message.lower():
            bot_response = random.choice(rule.rule_content.split("\n"))
            break
    return Response({'bot_response': bot_response})

# Doctor Views
@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def doctor_list(request, pk=None):
    if request.method == 'GET':
        # Retrieve all doctors
        print("GET request to /doctors/")
        doctors = Doctor.objects.all()  # You can filter based on availability or other fields
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        print(f"Attempting to update doctor with ID: {pk}")
        try:
            doctor = Doctor.objects.get(pk=pk)  # Get the doctor by primary key (ID)
        except Doctor.DoesNotExist:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  
def create_doctor(request):
    data = request.data
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile Views
# @api_view(['GET', 'PUT'])
# @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
# def user_profile_detail(request, user_id=None):
#     user = request.user  # This will give you the logged-in user
#     # You can fetch more details if needed
#     user_data = {
#         "username": user.username,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#     }
#     return Response(user_data, status=200)

#     # Handle GET request (retrieve user profile)
#     if request.method == 'GET':
#         serializer = UserProfileSerializer(user_profile)
#         return Response(serializer.data)

#     # Handle PUT request (update user profile)
#     elif request.method == 'PUT':
#         serializer = UserProfileSerializer(user_profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])  # Require authentication
def user_profile_detail(request, user_id=None):
    user = request.user  # Get the logged-in user

    # Prepare user data
    user_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    if request.method == 'GET':
        return Response(user_data, status=200)

    elif request.method == 'PUT':
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({"detail": "Profile updated successfully."})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_profile(request):
    data = request.data
    try:
        user = request.user  # Use the authenticated user
        data['user'] = user.id
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Chat Session Views
@api_view(['GET'])
@permission_classes([AllowAny])
def chat_session_detail(request, pk):
    try:
        session = ChatSession.objects.get(id=pk)
    except ChatSession.DoesNotExist:
        return Response({"detail": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)
    except ChatSession.MultipleObjectsReturned:
        return Response({"detail": "Multiple chat sessions found for this ID."}, status=status.HTTP_400_BAD_REQUEST)

    # Continue with logic for the found session
    return Response(ChatSessionSerializer(session).data)

# Create a new chat session, checking if the user already has an active session
@api_view(['POST'])
@permission_classes([AllowAny])
def create_chat_session(request):
    user_id = request.data.get("user_id")
    
    # Check if the user already has an active session
    active_sessions = ChatSession.objects.filter(user_id=user_id, status="active")
    if active_sessions.exists():
        return Response({"detail": "User already has an active chat session."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new chat session
    new_session = ChatSession.objects.create(
        user_id=user_id,
        status="active",  # Assuming status is active when creating a new session
    )

    # Serialize and return the newly created chat session data
    serializer = ChatSessionSerializer(new_session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def chat_rules(request, pk=None):
    if request.method == 'GET':
        if pk is not None:  # For GET on specific rule
            try:
                rule = Rule.objects.get(pk=pk)
                serializer = RuleSerializer(rule)
                return Response(serializer.data)
            except Rule.DoesNotExist:
                return Response({"detail": "Rule not found."}, status=status.HTTP_404_NOT_FOUND)
        else:  # For GET all rules
            rules = Rule.objects.all()
            serializer = RuleSerializer(rules, many=True)
            return Response(serializer.data)

    if request.method == 'PUT':
        if pk is None:
            return Response({"detail": "Primary key (pk) is required for updating a rule."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rule = Rule.objects.get(pk=pk)
        except Rule.DoesNotExist:
            return Response({"detail": "Rule not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if pk is None:
            return Response({"detail": "Primary key (pk) is required for deleting a rule."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rule = Rule.objects.get(pk=pk)
        except Rule.DoesNotExist:
            return Response({"detail": "Rule not found."}, status=status.HTTP_404_NOT_FOUND)

        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Adding a chat rule
@api_view(['POST'])
@permission_classes([AllowAny])
def add_chat_rules(request):
    rule_data = request.data
    if not all(key in rule_data for key in ['rule_name', 'rule_type', 'rule_description', 'rule_content']):
        return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new rule entry
    new_rule = Rule.objects.create(
        rule_name=rule_data['rule_name'],
        rule_type=rule_data['rule_type'],
        rule_description=rule_data['rule_description'],
        keyword=rule_data.get('keyword', ''),  # Optional keyword
        rule_content=rule_data['rule_content']
    )
    return Response({"message": "Rule added successfully!", "rule_id": new_rule.id}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def create_chatlog(request, session_id):
    try:
        # Get the session object from the session ID
        chat_session = ChatSession.objects.get(id=session_id)
    except ChatSession.DoesNotExist:
        return Response({"detail": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)

    user_message = request.data.get('user_message')
    if not user_message:
        return Response({"detail": "User message is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Process the user message and get the bot response
    bot_response = get_bot_response(user_message)

    # Create the chat log
    chat_log = ChatLog.objects.create(
        session=chat_session,
        user_message=user_message,
        bot_response=bot_response
    )

    # Serialize and return the created chat log
    serializer = ChatLogSerializer(chat_log)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_chatlog(request, session_id):
    try:
        # Get the session object from the session ID
        session = ChatSession.objects.get(id=session_id)

        # Retrieve all chat logs associated with the session
        chat_logs = ChatLog.objects.filter(session=session)

        # Serialize the chat logs
        serializer = ChatLogSerializer(chat_logs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except ChatSession.DoesNotExist:
        return Response({"detail": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)



def get_bot_response(user_message):
    # Here, you can implement your chatbot logic based on the rules.
    # For simplicity, I'll just return a static response or you can integrate an AI service.

    if "hello" in user_message.lower():
        return "Hello! How can I assist you today?"
    elif "appointment" in user_message.lower():
        return "Sure! I can help you with appointment scheduling."
    elif "status" in user_message.lower():
        return "Its based on your scheduled time!" 
    else:
        return "I'm sorry, I didn't understand that. Can you rephrase?"



# Notification Views
@api_view(['GET'])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user

    # Retrieve all notifications for the authenticated user
    notifications = Notification.objects.filter(user=user)

    # Optionally filter by unread notifications
    unread = request.query_params.get('unread', None)
    if unread is not None:
        unread = unread.lower() == 'true'  # Convert to boolean
        notifications = notifications.filter(is_read=unread)

    # Serialize and return the notifications
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_notification(request):
    # Make sure the user is authenticated
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the message and other data from the request
    message = request.data.get("message", "")
    
    if not message:
        return Response({"detail": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new notification instance
    notification = Notification(user=user, message=message)
    notification.save()

    # Serialize and return the response
    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

    # Mark the notification as read
    notification.is_read = True
    notification.save()

    # Serialize and return the response
    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=status.HTTP_200_OK)