# coding: utf8

from personalform.models import *

'''
excel_data type: list
'''
def get_user_data(username):
	# result_data = {}
	# for row in Info.objects.filter(username=username):
	# 	if row.excel_field in excel_data:
	# 		result_data[row.excel_field] = row.excel_value
	# 		pass
	# 	pass
	# for data in excel_data:
	# 	if data not in result_data.keys():
	# 		result_data[data] = ''
	# 		pass
	# 	pass
	# return result_data
	result_data = {}
	rows = Info.objects.filter(username = username)
	for index in xrange(0, rows.count() - 1):
		result_data[index] = (rows[index].excel_field, rows[index].excel_value)
		pass
	return result_data
	pass

def create_and_update_field(username, excel_data):
	for field in excel_data.keys():
		obj, created = Info.objects.update_or_create(
			username = username,
			excel_field = field,
			defaults = {'excel_value': excel_data[field]})
		pass
	pass




























# from django.db import connection, connections
# from django.db import transaction


# # check field in model or not ****************************************************8
# # try:
# #     User._meta.get_field('haha')
# # except FieldDoesNotExist:
# #     print 'haha does not exist'
# @transaction.atomic()
# def get_user_field():
# 	with connections['information'].cursor() as m_cursor:
# 		sql = "SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'userform_user'";
# 		m_cursor.execute(sql)
# 		rows = m_cursor.fetchall()
# 	user_field_list = list(rows)
# 	return user_field_list
# 	pass
# # find fields in excel_fields which already has value in user model
# # user_field_list type : list, excel_fields type : dict
# def exist_field_in_excel(user_field_list, excel_fields):
# 	exist_fields = []
# 	for field in user_field_list:
# 		if field in excel_fields.keys():
# 			exist_field.append(field)
# 			pass
# 	return exist_fields
# 	pass
# # according to exist_fields, update excel_info.
# def fill_excel_blank(username, exist_fields, excel_info):
# 	user = User.objects.get(username = username)
# 	for field in exist_fields:
# 		excel_info[field] = user.field
# 	return excel_info
# 	pass

# # user_field_list type: list, excel_field type: dict
# def get_and_update_new_field(user_field_list, excel_fields_and_values):
# 	new_field = {}
# 	updata_field = {}
# 	for field in excel_fields_and_values.keys():
# 		if field not in user_field_list:
# 			new_field[field] = excel_fields_and_values[field]
# 			pass
# 		else:
# 			if excel_fields_and_values[field] != '':
# 				updata_field[field] = excel_fields_and_values[field]
# 				pass
# 	return (new_field, updata_field)
# 	pass
# # new_field type: dict
# @transaction.atomic
# def create_new_field(username, new_field):
# 	with connection.cursor() as m_cursor:
# 		for field in new_field:
# 			sql = 'alter table userform_user add %s text' %field
# 			m_cursor.execute(sql)


# 	pass
# @transaction.atomic
# def update_user_field_value(username, update_fields):
# 	with connection.cursor() as m_cursor:
# 		for field in update_fields:
# 			# 更新字段sql
# 			sql = 'update table userform_user set %s = %s where username = %s' %(field, update_fields[field], username)
# 			m_cursor.execute(sql)
# 			# 检查sql执行结果	
# 	pass