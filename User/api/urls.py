from django.urls import path, include
from rest_framework.routers import DefaultRouter
from User.api.views import ContactViewSet, TagViewSet, ContactSocialLinkViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'social-links', ContactSocialLinkViewSet, basename='social-link')

urlpatterns = [
    path('', include(router.urls)),
]
