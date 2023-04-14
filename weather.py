#!/usr/bin/python3

import requests
import json
from datetime import datetime
import sys

h = {"User-Agent": "weather"}

base_url = "https://api.weather.gov"

test_coords = "45.903658,-68.924333"

def loadConfig():
	with open("config.json", "r") as conf:
		c = conf.read()
		return json.loads(c)

def getZone(coords):
	resp = requests.get(base_url+"/points/"+coords, headers=h)

	jd = json.loads(resp.text)
	return jd

def getDailyForecast(url, num_days):
	resp = requests.get(url, headers=h)
	first = json.loads(resp.text)	

	# endpoint returns 2 weather updates per day (day/night)
	for i in range(1, (num_days*2)+1): #len(first['properties']['periods'])):
		p = first['properties']['periods'][i]
		time = p["name"]
		temp_str = str(p['temperature'])
		humidity = str(p['relativeHumidity']['value'])
		fcast_text = p['detailedForecast'] 

		print(time+" "+temp_str+p["temperatureUnit"])
		print("Humidity: "+humidity+"%")
		print(fcast_text)
		print()

def getHourlyForecast(url, num_hours):	
	resp = requests.get(url+"/hourly", headers=h)
	data = json.loads(resp.text)


	for i in range(1, num_hours+1):#len(data['properties']['periods'])):
		p = data['properties']['periods'][i]
		time = datetime.fromisoformat(p['startTime'])
		weekday = datetime.strftime(time, '%A') 
		date = datetime.strftime(time, '%b %d')	
		hour = datetime.strftime(time, '%H:%M')
		wind = p['windDirection']+" "+p['windSpeed']


		print(hour+": "+str(p['temperature'])+"F")
		print(p['shortForecast'])
		print("Wind: "+wind)
		print(weekday+", "+date)
		print()

def getAlerts(cid):
	resp = requests.get(base_url+"/alerts/active/zone/"+cid, headers=h)
	data = json.loads(resp.text)
	print(data)
	"""
	for i in range(len(data['features'][0]['properties'])):
		p = data['features'][0]['properties'][i]
		print(p)
	"""

def parseInput(cid):
	if len(sys.argv) == 2:
		if sys.argv[1] == 'hourly':
			getHourlyForecast(cast, int(sys.argv[2]))
		elif sys.argv[1] == 'daily':
			getDailyForecast(cast, int(sys.argv[2]))
		elif sys.argv[1] == 'alerts':
			getAlerts(cid)
		else:
			print("Bad input")
	else:
		# help menu
		print("Not enough arguments")


if __name__ == "__main__":
	config = loadConfig()
	zoneinfo = getZone(config['coordinates'])
	cast = zoneinfo['properties']['forecast']
	county_url = zoneinfo['properties']['county']
	countyId = county_url[len(county_url)-6:len(county_url)]
	parseInput(countyId)
	#getFutureForecast(cast, 3)
	#getTodaysForecast(cast, 5)

