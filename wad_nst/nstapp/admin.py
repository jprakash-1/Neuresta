from django.contrib import admin
from .models import Profile,Feedback


# Registering our models here so that we can see model
# when we login to admin page.

admin.site.register(Profile)

class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Feedback,FeedbackAdmin)