from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'email', 'id')
    list_display_links = ('id', 'last_name', )
    search_fields = ('last_name', )
    fieldsets = (
        ("Personal Info", {'fields': (('username', 'password'), ('first_name', 'last_name', 'patronymic'), 'email', 'projects')}),
        ("Admin Info", {'fields': ('is_superuser', 'is_staff', 'is_active', ('date_joined', 'last_login'), 'user_permissions', 'groups')}),
    )


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    # list_display_links = ('title', )
    search_fields = ('title', )
    list_editable = ('title', )


@admin.register(models.Blueprint)
class BlueprintAdmin(admin.ModelAdmin):
    list_display = ('title', 'decimal_number', 'file', 'updated', 'created')
    list_display_links = ('title', 'decimal_number')
    search_fields = ('title', )
    list_filter = ('updated', 'created')


# @admin.register(models.ProjectBlueprint)
# class ProjectBlueprintAdmin(admin.ModelAdmin):
#     list_display = ('project_id', 'blueprint_id')


# @admin.register(models.ProjectUser)
# class ProjectUsersAdmin(admin.ModelAdmin):
#     list_display = ('project_id', 'author_id')
