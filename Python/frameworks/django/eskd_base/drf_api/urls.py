from unicodedata import name
from django.urls import path, include
from rest_framework import routers, decorators
from . import views


router = routers.DefaultRouter()
router.register('blueprints', viewset=views.BlueprintAPI)
router.register('projects', viewset=views.ProjectAPI)
router.register('users', viewset=views.UserAPI)
router.register('public_users', viewset=views.PublicUserAPI)
router.register('info', viewset=views.InfoViewSet)
# router.register('info_v1', viewset=views.InfoViewSet)
# router.register('info_v2', viewset=views.InfoGenericViewSet)

urlpatterns = [ 
    path('', views.django_index),
    path('protected/', views.protected_view),
    path('', include(router.urls))
]
