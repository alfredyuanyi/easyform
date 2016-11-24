# coding: utf8
from django.contrib import admin
from personalform.models import *
from django.contrib.auth.models import User as AuthUser
# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'password')
	list_filter = ('username',)
	ordering = ('username',)
	pass

class InfoAdmin(admin.ModelAdmin):
	list_display = ('username', 'excel_field', 'excel_value')
	list_filter = ('username',)
	ordering = ('username',)
	pass
class WordInfoAdmin(admin.ModelAdmin):
	list_display = ('username', 'word_field', 'word_value')
	list_filter = ('username',)
	ordering = ('username',)
	pass
admin.site.register(WordInfo, WordInfoAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Info, InfoAdmin)