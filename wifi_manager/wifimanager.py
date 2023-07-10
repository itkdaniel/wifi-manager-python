from dataclasses import dataclass
import os, platform

class WifiManager:

	def __init__(self,ssid=None,name=None):
		self.ssid = ssid
		self.name = name

	@staticmethod
	def displayAvailableNetworks():
		if platform.system() == "Windows":
			command = "netsh wlan show networks interface=Wi-Fi"
		elif platform.system() == "Linux":
			command = "nmcli dev wifi list"
		os.system(command)

	@staticmethod
	def connect(name=None, SSID=None):
		if platform.system() == "Windows":
			command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
		elif platform.system() == "Linux":
			command = "nmcli con up "+SSID
		os.system(command)

	@staticmethod
	def createNewConnection(name=None, SSID=None, key=None):
		config = """<?xml version=\"1.0\"?>
		<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
			<name>"""+name+"""</name>
			<SSIDConfig>
				<SSID>
					<name>"""+SSID+"""</name>
				</SSID>
			</SSIDConfig>
			<connectionType>ESS</connectionType>
			<connectionMode>auto</connectionMode>
			<MSM>
				<security>
					<authEncryption>
						<authentication>WPA2PSK</authentication>
						<encryption>AES</encryption>
						<useOneX>false</useOneX>
					</authEncryption>
					<sharedKey>
						<keyType>passPhrase</keyType>
						<protected>false</protected>
						<keyMaterial>"""+key+"""</keyMaterial>
					</sharedKey>
				</security>
			</MSM>
		</WLANProfile>"""
		if platform.system() == "Windows":
			command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
			with open(name+".xml", 'w') as file:
				file.write(config)
		elif platform.system() == "Linux":
			command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
		os.system(command)
		if platform.system() == "Windows":
			os.remove(name+".xml")

	@classmethod
	def run(self):
		try:
			self.displayAvailableNetworks()
			option = input('New connection (y/N)? ')
			if option =='N' or option == "":
				name = input('Name: ')
				self.connect(name,name)
				print('If not connected to this network, try connecting w correct creds')
			elif option == 'y':
				name = input('Name: ')
				key = getpass.getpass('Password: ')
				self.createNewConnection(name,name,key)
				self.connect(name,name)
				print('If not connected to this network, try connecting w correct creds')
			self.name = name
			self.ssid = name
		except KeyboardInterrupt as e:
			print('\nExiting...')
		else:
			self.network_name = ssid