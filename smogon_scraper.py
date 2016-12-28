from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome(executable_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
time.sleep(3)
driver.get("http://www.smogon.com/dex/xy/pokemon/")
time.sleep(3)

def csv_input(csvfile, rowVals):
	with open(csvfile, "ab") as outputFile:
			csvOutput = csv.writer(outputFile)
			print rowVals
			csvOutput.writerow(rowVals)

#parse html
def parse_html2(driver):
	pageSource = driver.page_source
	soup = BeautifulSoup(pageSource, 'html.parser')
	pokeEntry = soup.findAll('div', attrs={'class': 'PokemonAltRow'})
	for pokemon in pokeEntry:
		nameVal = pokemon.find("div", attrs={'class': 'PokemonAltRow-name'})
		nameSpan = nameVal.find("span").contents[1]
		name = nameSpan.get_text()
		#print name
		typeList = pokemon.find("div", attrs={'class': 'PokemonAltRow-types'}).findAll('a')
		# count for one or two types use a try statement
		try:
			type1 = typeList[0].get_text()
			type2 = typeList[1].get_text()
			typesTotal = "%s|%s" % (type1, type2)
		except IndexError:
			type1 = typeList[0].get_text()
			type2 = ""
			typesTotal = type1
		# collect both abilities
		abilities = pokemon.findAll('ul', attrs={'class': 'AbilityList'})
		try:
			ability1 = abilities[0].get_text()
			ability2 = abilities[1].get_text()
		except IndexError:
			ability1 = abilities[0].get_text()
			ability2 = ""
		#formatList = pokemon.find('div', attrs={'class': 'PokemonAltRow-tags'}).find('a').get_text()
		hp = pokemon.find('div', attrs={'class': 'PokemonAltRow-hp'}).find('span').get_text()
		atk = pokemon.find('div', attrs={'class': 'PokemonAltRow-atk'}).find('span').get_text()
		defense = pokemon.find('div', attrs={'class': 'PokemonAltRow-def'}).find('span').get_text()
		spAtk = pokemon.find('div', attrs={'class': 'PokemonAltRow-spa'}).find('span').get_text()
		speed = pokemon.find('div', attrs={'class': 'PokemonAltRow-spd'}).find('span').get_text()
		spdf = pokemon.find('div', attrs={'class': 'PokemonAltRow-spe'}).find('span').get_text()
		rowInputs = [name, typesTotal, type1, type2, ability1, ability2, hp, atk, defense, spAtk, speed, spdf]
		csv_input("smogon_pokemon.csv", rowInputs)
		"""
		with open("smogon_pokemon.csv", "wb") as outputFile:
			csvOutput = csv.writer(outputFile)
			csvOutput.writerow([name, typesTotal, type1, type2, ability1, ability2, hp, atk, defense, spAtk, speed, spdf])
		"""
		#print name, "type:", type1, type2, "\thp: ", hp, "\tatk:", atk, "\tdefense:", defense, "\tspAtk:", spAtk, "\tspd:", speed, "\tspDef:", spdf
		#print "abilities:", ability1, ability2
		"""
		with open("smogon_pokemon.csv", "wb") as outputFile:
			headerNames = ['Name', 'types', 'type1', 'type2', 'ability1', 'ability2', 'HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']
			csvOutput = csv.DictWriter(outputFile, fieldnames=headerNames)
		"""
	return name

#return namet
name = "blank"
while name != "Zygarde":
	name = parse_html2(driver)
	driver.execute_script("window.scrollBy(0, window.innerHeight);")
else:
	print "Finished scraping."
	driver.close()

"""
def parse_html(driver):
	pageSource = driver.page_source
	soup = BeautifulSoup(pageSource, 'html.parser')
	name = soup.findAll("div", attrs={'class': 'PokemonAltRow-name'})
	for vals in name:
		nameSpan = vals.find("span").contents[1]
		nameVal = nameSpan.get_text()
		print nameVal
"""
