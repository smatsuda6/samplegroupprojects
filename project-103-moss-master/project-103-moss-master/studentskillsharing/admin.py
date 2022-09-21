from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from studentskillsharing.models import Comment, Profile, Skill, Post


class UserInline(admin.StackedInline):
    model = settings.AUTH_USER_MODEL
    can_delete = False
    verbose_name_plural = 'Profiles'
    #fk_name = 'user'


class CustomUser(UserAdmin):
    inlines = (UserInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUser, self).get_inline_instances(request, obj)


#admin.site.unregister(User)
admin.site.register(User, CustomUser)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Skill)
admin.site.register(Comment)
