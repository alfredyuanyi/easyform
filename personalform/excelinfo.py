# coding: utf8
import xlwt
import xlrd
import demjson


def excel_to_python(fname, key):
  bk = xlrd.open_workbook(fname, formatting_info=True)
  print 'qucoanima'
  try:
    sh = bk.sheet_by_name("Sheet1")
  except:
    pass

  nrows = sh.nrows
  ncols = sh.ncols

  cols_width = []
  rows_height = []

  for i in range(ncols):
    cols_width.append(sh.computed_column_width(i))

  for i in range(nrows):
    rows_height.append(sh.rowinfo_map[i].height)

  row_list = []

  for i in range(0, nrows):
      row_data = sh.row_values(i)
      row_list.append(row_data)

  for i in range(len(row_list)):
      for j in range(len(row_list[0])):
        for k in range(len(key)):
          m = key[k][0].split('_')
          print 'm[0]: ', m[0]
          print 'm[1]: ', m[1]
          if (m[0] == row_list[i][0] and m[1] == row_list[0][j]):
            row_list[i][j] = key[k][1]
            print 'row_list: ', row_list

  merged = []
  # for index in sh.merged_cells:
  #   rlo, rhi, clo, chi = index
  #   merged[(rlo, rhi, clo, chi)] = (rlo, clo, rhi - rlo, chi - clo)
  for (rlow,rhigh,clow,chigh) in sh.merged_cells:
      merged.append([rlow,clow,rhigh-rlow,chigh-clow])

  dict = {}
  dict['nrows'] = nrows
  dict['ncols'] = ncols
  dict['row_list'] = row_list
  dict['cols_width'] = cols_width
  dict['rows_height'] = rows_height
  dict['merged'] = merged
  # print(dict)
  json = demjson.encode(dict)
  return json
