from django.contrib import admin

# Register your models here.
from CalorieTracker.models import *

admin.site.register(User)
admin.site.register(Food)
admin.site.register(Profile)
admin.site.register(ConsumedFood)
admin.site.register(Client)
