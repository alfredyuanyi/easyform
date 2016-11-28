import xlwt
import xlrd
from xlutils.copy import copy




def fill_info_to_excel(fname, dict,merged):
  rb = xlrd.open_workbook(fname)
  wb = copy(rb)
  ws = wb.get_sheet(0)
  for i in range(len(dict)):
      for j in range(len(dict[0])):
        ws.write(i,j,dict[i][j])
  for i in range(len(merged)):
    # print merged[i][0],merged[i][2]+merged[i][0],merged[i][1],merged[i][1]+merged[i][3],dict[merged[i][0]][merged[i][1]]
    ws.write_merge(merged[i][0],merged[i][2]+merged[i][0]-1,merged[i][1],merged[i][1]+merged[i][3]-1,dict[merged[i][0]][merged[i][1]])
  wb.save(fname)

def write_to_excel(fname,res):
  filename = xlwt.Workbook()
  sheet = filename.add_sheet("sheet1")
  for i in range(len(res)):
      for j in range(len(res[i])):
      	# print 'res[i][j]: ', res[i][j]
        sheet.write(i,j,res[i][j])
  filename.save(fname)
