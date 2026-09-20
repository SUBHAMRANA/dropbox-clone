from django.contrib import admin
from .models import User, FileObject, AccessControlList

# Register the models so they appear in the Django admin panel
admin.site.register(User)
admin.site.register(FileObject)
admin.site.register(AccessControlList)