from django.contrib import admin

# Register your models here.
from .models import User,Events,Add_Blog,SeminarInformation

admin.site.register(User)
admin.site.register(Events)
admin.site.register(Add_Blog)
admin.site.register(SeminarInformation)