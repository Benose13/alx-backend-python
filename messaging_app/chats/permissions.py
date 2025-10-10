from rest_framework import permissions

class IsMessageOwner(permissions.BasePermission):
    """
    Allow access only to the sender or recipient of the message.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants in a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated for all API access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation or related message.
        - For Conversation objects: check participants field.
        - For Message objects: check sender/recipient or conversation participants.
        """
        user = request.user

        # If object is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If object is a Message, ensure user is sender, recipient, or part of conversation
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
            return user in conversation.participants.all() or user == obj.sender

        return False
