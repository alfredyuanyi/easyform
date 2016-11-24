# coding: utf8
from django.conf.urls import url
from personalform import views as user_form_views
from easyform.settings import EXCEL_FILE, WORD_FILE

urlpatterns = [
    url(r'userlist/$', user_form_views.UserList),
    url(r'login/$', user_form_views.Login),
    url(r'logout/$', user_form_views.Logout),
    url(r'register/$', user_form_views.Register),
    url(r'usercenter/$', user_form_views.UserCenter),
    url(r'userinfo/$', user_form_views.UserInfo),
    url(r'userinfo/update/$', user_form_views.UserInfo),
    url(r'uploadform/excel/$', user_form_views.UploadForm, {'filetype': EXCEL_FILE}),
    url(r'uploadform/word/$', user_form_views.UploadForm, {'filetype': WORD_FILE}),
    url(r'downloadform/$', user_form_views.DownloadForm),
    url(r'createform/$', user_form_views.CreateForm),
    url(r'index/$', user_form_views.UserIndex),
    url(r'updateinfo/excel/$', user_form_views.updateinfo, {'filetype': EXCEL_FILE}),
    url(r'updateinfo/word/$', user_form_views.updateinfo, {'filetype': WORD_FILE}),

]