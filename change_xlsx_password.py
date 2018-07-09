#This script changes the password of an Excel file

import os, sys
import win32com.client
def change_xlsx_password(filename, pw, pw_new = ''):
    xcl = win32com.client.Dispatch("Excel.Application")
    wb = xcl.Workbooks.Open(filename, False, False, None, pw)
    xcl.DisplayAlerts = False
    wb.SaveAs(filename, None, pw_new, '')
    xcl.DisplayAlerts = True
    xcl.Quit()