import json
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.forms.models import model_to_dict
from rest_framework import decorators, response, generics, views, mixins, viewsets, permissions, authentication
from . import models, serializer, permissions as custom_permissions, mixins as custom_mixins


class BlueprintAPI(viewsets.ModelViewSet):
    queryset = models.Blueprint.objects.all()
    serializer_class = serializer.BlueprintSerializer
    # permission_classes = (custom_permissions.IsOwnerOrReadOnly, )


class ProjectAPI(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializer.ProjectSerializer


class UserAPI(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserSerializer
    # permission_classes = (permissions.IsAdminUser, )


class PublicUserAPI(viewsets.ModelViewSet, custom_mixins.CustomMixin):
    queryset = models.User.objects.filter(is_staff=True).order_by('username')
    serializer_class = serializer.PublicUserSerializer


class InfoViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializer.ProjectInfoSerializer

    # def perform_create(self, serializer):
    #     model_free_field = serializer.validated_data.pop('model_free_field')
    #     print("-"*60 + f'\ncreate with {model_free_field=}\n' + "-"*60)
    #     return super().perform_create(serializer)


# class InfoGenericViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = models.Project.objects.all()
#     serializer_class = serializer.ProjectInfoSerializer


def django_index(request: HttpRequest) -> HttpResponse:
    data = {}
    data['headers'] = dict(request.headers)
    data['body'] = str(request.body)
    data['etc'] = str(request.user)
    data['MIME-type'] = request.content_type

    data['models_info'] = {
        "users": models.User.objects.count(),
        "blueprints": models.Blueprint.objects.count(),
        'projects': models.Project.objects.count(),
    }
    data["first_user"] = model_to_dict(models.User.objects.all().first(), fields=['pk', 'username'])
    return JsonResponse(data)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
def protected_view(request: HttpRequest) -> HttpResponse:
    data = {}
    data['headers'] = dict(request.headers)
    data['body'] = str(request.body)
    data['user'] = str(request.user)
    data['MIME-type'] = request.content_type
    data['message'] = 'This is protected view'
    return response.Response(data)