import socket
import requests

def pegaip():
        file = raw_input('[+] - Digite o caminho do arquivo que contem o arquivos com os IP's')
        ips = file.readlines()
        print "[+] - Working..."
        for ip in ips:
                ip = ip.strip()
                for port in [80,8080]:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.3)
                        t = s.connect_ex((ip,port))
                        s.close()
                        if t == 0:
                                result = '%s:%d' %(ip,port)
                                print '[+] - Endereco: '+result
                                checaip(result)
def checaip(result):
        try:
                ip = 'http://'+result.strip()
                print '[+] - Tentativa de encontrar fabricante'
                c = requests.get(ip)
                header = c.headers
                if header['www-authenticate'] != None:
                        server = header['www-authenticate'].split("=")[1].split('"')[1]
                        print '[+] - Fabricante encontrado '+server
                        fabricante = open('fabricantes/'+server+'.txt','a')
                        fabricante.write(ip+'\n')
                else:
                        print '[+] - Fabricante nao encontrado'
                        semregistro = open('fabricantes/semregistro.txt','a')
                        semregistro.write(ip+'\n')
                print
        except:
                print '[+] - Fabricante nao encontrado'
                semregistro = open('fabricantes/semregistro.txt','a')
                semregistro.write(ip+'\n')

pegaip()
