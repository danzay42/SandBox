import uuid
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import validators


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patronymic = models.CharField(max_length=15, blank=True)
    projects = models.ManyToManyField('Project', blank=True)

    def __str__(self) -> str:
        if self.patronymic:
            return f"{self.last_name} {self.first_name[0]}.{self.patronymic[0]}."
        else:
            return f"{self.first_name} {self.last_name}" 

    class Meta:
        ordering = ('first_name', 'last_name')


class Project(models.Model):
    # title = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=40)

    # @property
    # def blueprints(self, obj):
    #     return Blueprint.objects.filter(pk=obj.pk).count
    
    @property
    def today(self):
        return datetime.datetime.today()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title', )


class Blueprint(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='blueprints/')
    decimal_number = models.CharField(max_length=30, unique=True, validators=[validators.validate_decimal_number])

    origin = models.ForeignKey('Blueprint', on_delete=models.SET_NULL, blank=True, null=True)
    author_id = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False) 

    projects = models.ManyToManyField('Project', through='ProjectBlueprint')

    def __str__(self) -> str:
        return self.title  

    class Meta:
        ordering = ('title', 'decimal_number', 'created', 'updated')


class ProjectBlueprint(models.Model):  # explicit vay to create many_to_many table
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    blueprint = models.ForeignKey('Blueprint', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True, editable=False)


# class ProjectUser(models.Model):  # explicit vay to create many_to_many table
#     project_id = models.ForeignKey('Project', on_delete=models.CASCADE)
#     author_id = models.ForeignKey('User', on_delete=models.CASCADE)

