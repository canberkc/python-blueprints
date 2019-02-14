from openpyxl import load_workbook


def get_workbook(file_path):
    return load_workbook(file_path)


def save_workbook(workbook, file_path):
    workbook.save(file_path)


def get_sheet_by_name(workbook, sheet_name):
    return workbook[sheet_name]


def modify_cell_position(sheet, row, col, input):
    cell_name = find_cell_name(sheet, row, col)
    modify_cell_by_name(sheet, cell_name, input)


def modify_cell_by_name(sheet, cell_name, input):
    sheet[cell_name] = input


def find_cell_name(sheet, row, col):
    ##TODO
    cell_name = ''
    return cell_name


path = 'C:/file.xlsx'
wb = get_workbook(path)
sheet = get_sheet_by_name(wb, 'sheet_name')
print('Title of this sheet is: ' + sheet.title)

