import socket
import requests
from netaddr import *
class bcolors:
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

def pegaip():
	ips = raw_input(bcolors.OKBLUE+"[+] - Insira a rede: "+bcolors.ENDC)
	for ip in IPNetwork(ips):
		ip = str(ip)
		for port in (80,8080):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(0.3)
			t = s.connect_ex((ip,port))
			s.close()
			if t == 0:
				result = '%s:%d' %(ip,port)
				print bcolors.OKBLUE+'[+] - Endereco: '+result+bcolors.ENDC
				checaip(result)
def checaip(result):
	try:
		ip = 'http://'+result
		c = requests.get(ip,timeout=0.3)
		print bcolors.WARNING+'[+] - 1 - Tentativa de encontrar fabricante'+bcolors.ENDC
		if c.headers['www-authenticate']: 
			server = c.headers['www-authenticate'].split("=")[1].split('"')[1]
			print bcolors.OKGREEN+'[+] - 1 - Fabricante encontrado '+server+bcolors.ENDC
			fabricante = open('fabricantes/'+server+'.txt','a')
			fabricante.write(ip+'\n')
			print

		elif not c.headers['www-authenticate']:
			print bcolors.WARNING+'[+] - 2 - Tentativa de encontrar fabricante'+bcolors.ENDC
			value = c.text.find("<title>")
			if value != -1:
				c = requests.get(ip,timeout=0.3)
				server = c.text[value:-1].split()[0].split('>')[1].split('<')[0]
				print bcolors.OKGREEN+'[+] - 2 - Fabricante encontrado '+server+bcolors.ENDC
				fabricante = open('fabricantes/'+server+'.txt','a')
				fabricante.write(ip+'\n')
				print
			else:
				c = requests.get(ip,timeout=0.3)
				print bcolors.WARNING+'[+] - 3 - Tentativa de encontrar fabricante'+bcolors.ENDC
				value = c.text.find("<TITL>")
				if value != -1:
					server = c.text[value:-1].split()[0].split('>')[1].split('<')[0]
					print bcolors.OKGREEN+'[+] - 3 - Fabricante encontrado '+server+bcolors.ENDC
					fabricante = open('fabricantes/'+server+'.txt','a')
					fabricante.write(ip+'\n')
					print

	except:
		print bcolors.FAIL+'[+] - Fabricante nao encontrado, salvo em semregistro.txt'+bcolors.ENDC
		semregistro = open('fabricantes/semregistro.txt','a')
		semregistro.write(ip+'\n')
		print

pegaip()
