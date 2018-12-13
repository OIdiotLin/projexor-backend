from django.contrib import admin

from .models import *

# Admin site settings
admin.site.site_header = 'Projexor 后台管理'

# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(UserInProject)
admin.site.register(Task)
admin.site.register(UserInTask)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Resource)
admin.site.register(File)
