from importlib.util import source_hash
from rest_framework import serializers, reverse
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__' 
        # fields = ('first_name', 'last_name', 'patronymic', 'email')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__' 

    def validate_title(self, value): # unique validator and unique model field property analog
        qs = models.Project.objects.filter(title__exact=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} already exists")
        return value

class BlueprintSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = models.Blueprint
        fields = '__all__'
        # fields = ['user', 'title']
    
    def get_author(self, obj):
        return str(obj.author_id)


class ProjectInfoSerializer(serializers.ModelSerializer):
    blueprints = BlueprintSerializer(read_only=True, many=True)
    users = UserSerializer(read_only=True, many=True)

    url = serializers.SerializerMethodField(read_only=True)
    model_free_field = serializers.BooleanField(write_only=True)
    name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = models.Project
        # fields = '__all__'
        fields = [
            'pk',
            'title',
            'name',
            'url',
            'today',
            'model_free_field',
            'blueprints',
            'users',
        ]
    
    def create(self, validate_data):
        model_free_field = validate_data.pop('model_free_field')
        print("-"*60 + f'\ncreate with {model_free_field=}\n' + "-"*60)
        obj = super().create(validate_data)
        return obj 
    
    def get_url(self, obj):  # get_<field>
        request = self.context.get('request')
        if request:
            return reverse.reverse('project-detail', kwargs={"pk": obj.pk}, request=request)
        else:
            return None
    
    def validate_title(self, value):  # validate_<field>
        if models.Project.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(f'{value=} is busy!')
        return value

    # def get_blueprints(self, obj):
    #     # bp = models.Blueprint.objects.get(pk==)
    #     return BlueprintSerializer(bp, many=True).data

class PublicUserSerializer(serializers.ModelSerializer):
    projects_info = ProjectInfoSerializer(source='projects', read_only=True, many=True)
    class Meta:
        model = models.User 
        fields = ('pk', 'username', 'projects', 'projects_info')