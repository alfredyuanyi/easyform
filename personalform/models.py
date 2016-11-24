# coding: utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length = 30, blank = False, unique = True)
	password = models.CharField(max_length = 30, blank = False)
	email = models.EmailField(max_length=50)
	def __unicode__(self):
		return self.username
		pass
	class Meta:
		ordering = ['username']
		verbose_name = '用户'
		verbose_name_plural = '用户'
	pass

class Info(models.Model):
	username = models.CharField(max_length=30, blank=False)
	excel_field = models.CharField(max_length=250)
	excel_value = models.CharField(max_length=250)
	def __unicode__(self):
		return self.excel_field
		pass
	class Meta:
		ordering = ['username']
		verbose_name='用户excel信息'
		verbose_name_plural = '用户excel信息'
	

class WordInfo(models.Model):
	username = models.CharField(max_length=30, blank=False)
	word_field = models.CharField(max_length=250)
	word_value = models.CharField(max_length=250)
	def __unicode__(self):
		return self.word_field
		pass
	class Meta:
		ordering = ['username']
		verbose_name='用户word信息'
		verbose_name_plural = '用户word信息'	


