from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(VoteRecord)
admin.site.register(VoteRecord_only)
# Register your models here.
