from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # assuming obj has a participants field (ManyToMany with User)
        return request.user in obj.participants.all()


class IsMessageOwner(permissions.BasePermission):
    """
    Allow access only to the sender or recipient of the message.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient
