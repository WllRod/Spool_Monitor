import win32
import win32process
import win32con

s=win32process.STARTUPINFO()
win32process.CreateProcess(None, 'cmd.exe /c powershell -noexit "& ""C:\\Users\\teste.ps1""" > C:\\Users\\TI2\\Desktop\\teste.txt',None,None,True,win32con.CREATE_NEW_CONSOLE,None,'c:\\',s)