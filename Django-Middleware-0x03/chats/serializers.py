from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)
    role = serializers.CharField(max_length=20)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'password',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def validate_email(self, value):
        """Ensure no duplicate emails exist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Hash the password and create a new user."""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
    

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender_name = serializers.SerializerMethodField()  # derived field example

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_name',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['sent_at']

    def get_sender_name(self, obj):
        """Return sender's full name."""
        return f"{obj.sender.first_name} {obj.sender.last_name}" if obj.sender else None


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages and participants."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()  # another use of SerializerMethodField

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'message_count',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def get_message_count(self, obj):
        """Return the number of messages in the conversation."""
        return obj.messages.count()
