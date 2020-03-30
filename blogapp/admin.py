from django.contrib import admin

# Register your models here.
from blogapp.models import *
from usetapp.models import *

admin.site.register(Banner)
admin.site.register(BlogCategory)
admin.site.register(Tags)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendlyLink)

admin.site.register(BlogUser)
admin.site.register(EmailVerifyRecord)