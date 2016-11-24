import xlwt
import xlrd
from xlutils.copy import copy


# def fill_info_to_excel(fname, info_dict):
#   rb = xlrd.open_workbook(fname)
#   wb = copy(rb)
#   ws = wb.get_sheet(0)
#   for i in range(len(info_dict)):
#       for j in range(len(info_dict[0])):
#         print(i,j,info_dict[i][j])
#         ws.write(i,j,info_dict[i][j])
#   wb.save(fname)


def fill_info_to_excel(fname, dict):
  rb = xlrd.open_workbook(fname)
  wb = copy(rb)
  ws = wb.get_sheet(0)
  for i in range(len(dict)):
      for j in range(len(dict[0])):
        ws.write(i,j,dict[i][j])
  wb.save(fname)