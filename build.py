#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe, sys, os
import subprocess

sys.argv.append('py2exe')

#REFERENCIA http://wiki.wxpython.org/Py2exe%20with%20Python2.6
########### http://osdir.com/ml/python.py2exe/2007-06/msg00018.html
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>Test Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.30729.4918"
            processorArchitecture="X86"
            publicKeyToken="1fc8b3b9a1e18e3b"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''
RT_MANIFEST = 24

setup(
	options = {
		'py2exe': {
			'bundle_files': 1, 
			'compressed': True,
			'optimize': 1,
			'dll_excludes': ['w9xpopen.exe']
		}
	},
	windows = [{	
			'script'	: "main.py",#Nome do arquivo.py para ser compilado
			'name'		: "pyBotnet", #Defina com suas variáveis
			'description'	: "Botnet Desenvolvida em Python", #Defina com suas variáveis
			'version'	: "1.0", #Defina com suas variáveis
			'company_name'	: "Unknowns", #Defina com suas variáveis
			'copyright'	: "Copyright 2016 Unknowns Systems Incorporated", #Defina com suas variáveis
			'icon_resources': [(1, "icons\\python.ico")], #Icone - Comente essa linha caso nao queira um icone, ou troque para o icone da pasta icons para qual icone desejar
			#'other_resources' : [(RT_MANIFEST, 1, manifest_template)], #Descomente essa linha para o programa rodar com Privilegio de adminstrador
	}],
	zipfile = None,
)
"""
Codado by Moisés Oliver
"""
print "\nAquivo compilado com sucesso:\n\n\
Rodando UPX em subprocess\n\
-> Empacotando o execultavel\n\
-> Modo de compressao ultra-brute\n\
-> Isso pode demorar um pouco\n"
#Aqui o exe sera comprimido com o upx
tam_antes = os.path.getsize("dist\main.exe")

local = os.getcwd()
command = local + "\upx.exe --ultra-brute", "dist\main.exe"
processo = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
processo.wait()

tam_depois = os.path.getsize("dist\main.exe")
tam_z = tam_antes - tam_depois

print "Tamanho Antes: %s kb" % tam_antes
print "Tamanho Novo : %s kb" % os.path.getsize("dist\main.exe")



