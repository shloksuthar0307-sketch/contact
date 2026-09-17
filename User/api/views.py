from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from User.models import Contact, Tag, ContactSocialLink
from User.api.serializers import ContactSerializer, TagSerializer, ContactSocialLinkSerializer

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactSocialLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSocialLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactSocialLink.objects.filter(contact__user=self.request.user)
