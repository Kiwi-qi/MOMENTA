from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Department)
admin.site.register(DepartUser)