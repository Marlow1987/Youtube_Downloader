import winreg
import os,sys,stat

#reg = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,'SOFTWARE\\TEST',reserved=0,access=winreg.KEY_WRITE)
#winreg.SetValueEx(reg,"test value",0,winreg.REG_DWORD,10)
reg = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,'SOFTWARE\\TEST',reserved=0,access=winreg.KEY_WRITE)
winreg.SetValueEx(reg,"test value",0,winreg.REG_DWORD,9)


