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
        user = request.user

        # Check if the object is a Conversation
        if hasattr(obj, 'participants'):
            # Only participants can view or modify the conversation
            return user in obj.participants.all()

        # Check if the object is a Message
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
            # Participants of the conversation can view the message
            if request.method in permissions.SAFE_METHODS:
                return user in conversation.participants.all()
            
            # For update/delete requests (PUT, PATCH, DELETE),
            # Only the sender or conversation participants can modify/delete
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return user == obj.sender or user in conversation.participants.all()

        # Default deny
        return False