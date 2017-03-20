# coding: utf8

import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login,logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse

from django.core.exceptions import FieldDoesNotExist
from personalform.models import *
from personalform.forms import *
import json
from easyform.settings import MEDIA_URL, EXCEL_FILE, WORD_FILE, WEB_CRAWL, MEDIA_ROOT
from excelinfo import excel_to_python
from common import *
from fillexcel import *
from crawl import *
import demjson
# import simplejson

#
JAR_PATH = MEDIA_ROOT
JAR_NAME = 'Word.jar'

def file_iterator(filename, chunk_size=512):
	with open(filename) as f:
		while True:
			filestream = f.read(chunk_size)
			if filestream:
				yield filestream
			else:
				break
				pass
			pass
	pass


def UserList(request):
    users = User.objects.all()
    return HttpResponse('username = %s, email = %s' % (users[0].username, users[0].email))

def UsernameAjax(request):
	if request.method == 'POST':
		user_json = json.dumps(request.POST)
		username = user_json['username']
		pass
	else:
		return HttpResponse('illigal request method!')
	pass

def Login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			authUser = AuthUser.objects.create_user(username = data['username'], password= data['password'])
			authUser.save()
			loginUser = authenticate(username = data['username'], password = data['password'])
			if loginUser is not None:
				login(request, user = loginUser)
				return redirect('/user/index/')
				pass
			pass
		else:
			return render(request, 
					template_name='login.html',
					context={'form':form})
		pass
	elif request.method == 'GET':
		user = request.user
		if user.is_authenticated():
			return redirect(to='/user/index/')
			pass
		form = LoginForm(initial = {
			'username': '请输入用户名',
			'password': '请输入密码'
			})
		return render(request, 
            template_name = 'login.html',
            context = {'form': form})
	else:
		return HttpResponse("illigal request method!")

def Logout(request):
        user = request.user
	logout(request)
	AuthUser.objects.filter(username = user.username).delete()
	return redirect('/user/login/')
	pass

def Register(request):
    if request.method == 'GET':
        form = UserForm(initial = {'username': '请输入用户名',
			'email': '请输入可以联系到您邮箱地址'})
        request.session.set_test_cookie()
        return render(request, 
            template_name = 'register.html', context={'form': form})
        pass
    elif request.method == 'POST':
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()
			form = UserForm(request.POST)
			if form.is_valid():
				form_data = form.cleaned_data
				if User.objects.filter(username = form_data['username']).count() > 0:
					return HttpResponse("this username has been registered.try something else!")
				user = User.objects.create(username = form_data['username'],
					password = form_data['password'],
					email = form_data['email'])
				authUser = AuthUser.objects.create_user(username = user.username, password = user.password)
				authUser.save()
				loginUser = authenticate(username = user.username, password = user.password)
				if loginUser is not None:
					login(request, user = loginUser)
					user.save()
					return redirect('/user/index/')
					pass
				pass
			else:

				return render(request, 
					template_name='register.html',
					context={'form':form})
			pass
		else:
			return HttpResponse("请允许设置cookie后再试一遍。")
		pass       
    else:
        return HttpResponse("illegal request method!")
    pass
def UserInfo(request):
	if request.method == 'GET':
		request_user = request.user
		if request_user.is_authenticated():
			user = User.objects.get(username=request_user['username'])
			# what does user page do? zzz...
			pass
		else:
			return redirect(to='/user/login/')
		pass
	elif request.method == 'POST':
		# update user informations
		pass
	else:
		return HttpResponse('illigal request method!')
		pass
def UserCenter(request):
	if request.method == 'GET':
		request_user = request.user
		if request_user.is_authenticated():
			try:
				user = User.objects.get(username = request_user.username)
				pass
			except User.DoesNotExist:
				return HttpResponse('this user does not exist!')
				pass
			#数据如何处理未写
			return render(request, context={'m_user': user}, template_name = 'user.html')
		else:
			return redirect(to='/user/login/')
		pass
	else:
		return HttpResponse('illigal request method!')
        pass

def handle_uploaded_file(f, filepath):
    with open(filepath, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def UploadForm(request, filetype):
    if not request.user.is_authenticated():
        return redirect('/user/login/')
    if request.method == 'POST':
    	if filetype == EXCEL_FILE:
			form = UploadFileForm(request.POST, request.FILES)
		    	file_path = MEDIA_ROOT + request.FILES['file'].name
			handle_uploaded_file(request.FILES['file'], file_path)
			user_data = get_user_data(username = request.user.username)
			# print 'user_data'
			# print user_data
			excel_json = excel_to_python(fname=file_path, key = user_data)
			# print excel_json
			return render(request, 
				template_name = 'excel.html',
				context = {'data': excel_json, 'filepath': file_path})    	

    	elif filetype == WORD_FILE:
    		# do something for word file
		    	form = UploadFileForm(request.POST, request.FILES)
		    	file_path = MEDIA_ROOT + request.FILES['file'].name
			handle_uploaded_file(request.FILES['file'], file_path)
			flag = os.system('cd ' + JAR_PATH + '&& ' + 'java -jar ' + JAR_NAME + ' "Read" "' + file_path.encode('utf8') + '"')
			if flag != 0:
				return HttpResponse("server error!")
			json_class = json.JSONDecoder()
			# here has some problems, if lots of user request this method, maybe ...
			info = ''
			with open(JAR_PATH + 'middle.json', 'r') as f:
				info += f.read()
			word_info = json_class.decode(info)
			# word_info = eval(info)
			# print 'word_info: '
			# print word_info
			user_word_info = get_info_word(username = request.user.username, word_info = word_info)
			# print 'user_word_info: '
			# print user_word_info
			# print user_word_info.keys()[0]
			return render(request, 
				template_name = 'word.html',
				context = {'data': json.dumps(user_word_info), 'filepath': file_path})
			pass
	else:
			return Http404
    else:
        form = UploadFileForm()
    return render(request, template_name='uploadfile.html', context={'form': form})   
    pass

def CreateForm(request):

    pass
@csrf_exempt
def DownloadForm(request):
	filepath = request.GET['filepath']
	str_filepath = str(filepath.encode('utf8'))
	filename = str_filepath.split('/')[-1]
	response = StreamingHttpResponse(file_iterator(filename=filepath, chunk_size=512))
	response['Content-Type'] = 'application/octet-stream'
    	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    	return response
    	pass
@csrf_exempt
def updateinfo(request, filetype):
	if request.method == 'POST':
		if filetype == EXCEL_FILE:
			exceldata = []
			
			data = dict(request.POST)
			# print data
			lines = data['lines']
			try:
				merged = data['merged']
				pass
			except KeyError:
				merged = []
			
			tempdata =[]
			for m in merged:
				temp=[]
				for x in m.split(','):
					temp.append(int(x))
					pass
				tempdata.append(temp)
				pass
			# print tempdata
			# print int(lines[0])
			for x in xrange(0,int(lines[0])):
				exceldata.append(data[str(x)])
				pass
			fill_info_to_excel(request.POST['filepath'], exceldata, tempdata)
			
			for line in xrange(1,int(lines[0])):
				update_data = {}
				# print line
				for index in xrange(0,len(data['0'])):
					if data['0'][index] != '':
						update_data[data[str(line)][0] + '_' + data['0'][index]] = data[str(line)][index]
						pass
					else:
						continue
					pass
				# print 'update_data: ', update_data
				create_and_update_field(request.user.username, excel_data = update_data)
				pass
			
			# update excel informations
			return HttpResponse('succeed')			
			pass
		elif filetype == WORD_FILE:
			# do something for word file update
			tempdata = dict(request.POST)
			lines = tempdata['lines']
			# print 'tempdata: ', tempdata
			file_path = tempdata['filepath'][0]
			worddata = {}
			for line in xrange(0, int(lines[0])):
				worddata[tempdata[str(line)][0]] = tempdata[str(line)][1]
				pass
			print 'worddata: '
			print worddata
			f_info = ''
			with open(JAR_PATH + 'middle.json', 'r') as f_read:
				f_info += f_read.read()
			# json_class = json.JSONDecoder()
			print 'f_info: ', f_info
			f_data = json.loads(f_info)
			print 'f_data:    ', f_data
			jencode = json.JSONEncoder()
			for key in f_data.keys():
				f_data[key] = worddata[key]
				pass
			with open(JAR_PATH + 'middle.json', 'w') as f_write:
				f_write.write(jencode.encode(f_data))
			flag = os.system('cd ' + JAR_PATH + '&& ' + 'java -jar ' + JAR_NAME + ' "Write" "' + file_path.encode('utf8') + '"')
			if flag != 0:
				return HttpResponse("failed")
				pass
			create_and_update_word_field(username = request.user.username, word_data = worddata)
			return HttpResponse('succeed')
		elif filetype == WEB_CRAWL:
			exceldata = []
			
			data = dict(request.POST)
			print data
			lines = data['lines']
			# print int(lines[0])
			for x in xrange(0,int(lines[0])):
				exceldata.append(data[str(x)])
				pass
			# print 'exceldata: ', exceldata
			write_to_excel(request.POST['filepath'], exceldata)
			update_data = {}
			for line in xrange(0, int(lines[0])):
				for l_info in data[str(line)]:
					update_data[l_info[0]] = l_info[1]
					pass
			# for line in xrange(1,int(lines[0])):
			# 	update_data = {}
			# 	# print line
			# 	for index in xrange(0,len(data['0'])):
			# 		if data['0'][index] != '':
			# 			update_data[data[str(line)][0] + '_' + data['0'][index]] = data[str(line)][index]
			# 			pass
			# 		else:
			# 			continue
			# 		pass
				
				pass
			print 'update_data: ', update_data
			create_and_update_field(request.user.username, excel_data = update_data)
			# update excel informations
			return HttpResponse('succeed')			
			pass
		else:
			return Http404
		pass
	else:
		return HttpResponse('illigal request method!')
	pass
def UserIndex(request):
	if request.method == 'GET':
		request_user = request.user
		if request_user.is_authenticated():
			try:
				user = User.objects.get(username = request_user.username)
				pass
			except User.DoesNotExist:
				return redirect(to='/user/login/')
				pass
			#用户首页要干嘛，zz
			m_context = {'islogin': True}
			return render(request, template_name = 'main.html', context=m_context)
		else:
			m_context = {'islogin': False}
			return render(request, template_name = 'main.html', context=m_context)
		pass
	else:
		return HttpResponse('illigal request method!')
        pass

def WebCrawl(request):
	if request.method == "POST":
		request_user = request.user
		if request_user.is_authenticated():
			# url = request.POST['URL']
			biglist = ahhhhhhh(url='url', admin='admin', password='admin')
			m_context = demjson.encode(obj=biglist)
			file_path = MEDIA_ROOT + 'test.xls'
			return render(request, template_name = 'web.html', context = {'data': m_context, 'filepath': file_path})
			pass
		else:
			return redirect(to = 'user/login/')
		pass
	else:
		return HttpResponse('illigal request method')
	pass

