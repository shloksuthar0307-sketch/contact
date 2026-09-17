from rest_framework import serializers
from User.models import User, Tag, Contact, ContactSocialLink, ContactActivity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'password',
            'profile_image', 'phone_number', 'bio', 'company', 'job_title',
            'timezone', 'is_email_verified', 'updated_at'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'last_contacted_at')

    def validate_tags(self, tags):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            for tag in tags:
                if tag.user != request.user:
                    raise serializers.ValidationError("You can only assign tags that belong to you.")
        return tags


class ContactSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSocialLink
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_contact(self, contact):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if contact.user != request.user:
                raise serializers.ValidationError("You can only add links to your own contacts.")
        return contact


class ContactActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactActivity
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def validate_contact(self, contact):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if contact.user != request.user:
                raise serializers.ValidationError("You can only log activities for your own contacts.")
        return contact
