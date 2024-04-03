import json
import urllib.request
import sqlite3
from contextlib import closing
import gzip


user_agent = 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36'
headers = {
	'User-Agent': user_agent,
	'countrycode': '304',
	'authorization': 'Bearer',
	'langcode': '2',
	'accept': 'application/json, text/javascript, */*; q=0.01',
	'content-type': 'application/json',
}
data = {
	#'soft': 'Sw',
	'soft': 'Sc', #Vi
}

#Ranked battles list/ retrieve 5 seasons : how to differenciate double or single
url = 'https://api.battle.pokemon-home.com/tt/cbd/competition/internet/list'

req = urllib.request.Request(url, json.dumps(data).encode(), headers)
body = ''
with urllib.request.urlopen(req) as res:
	body = json.load(res)
with open("sample.json", "w") as outfile:
	json.dump(body, outfile)
#end Ranked battles list

#getting the playable Pokémon from these lists
for season_id in body['list']:
	rst = body['list'][season_id]['rst']
	ts1 = body['list'][season_id]['ts1']
	ts2 = body['list'][season_id]['ts2']
	url = f'https://resource.pokemon-home.com/battledata/ranking/scvi/{season_id}/{rst}/{ts2}/pokemon'
	req = urllib.request.Request(url, headers=headers)
	#req.add_header('Accept-encoding', 'gzip')
	pdetail = ''
	#data = gzip.GzipFile(fileobj=urllib.request.urlopen(req)).read()
	#content = data.decode("utf-8")
	try:
		res = urllib.request.urlopen(req)
		pdetail = json.load(res)
		with open('Pokemon_'+season_id+'_'+str(rst)+'_'+str(ts2)+'.json', "w") as outfile:
			json.dump(pdetail, outfile)
	except:
		print("POKEMON issue with season_id "+season_id)
#end getting pokémon

#getting trainers
for season_id in body['list']:
	rst = body['list'][season_id]['rst']
	ts1 = body['list'][season_id]['ts1']
	ts2 = body['list'][season_id]['ts2']
	try:
		for i in range(1, 2):
			url = f'https://resource.pokemon-home.com/battledata/ranking/scvi/{season_id}/{rst}/{ts1}/traner-{i}'
			req = urllib.request.Request(url, headers=headers)
			req.add_header('Accept-encoding', 'gzip')
			pdetail = ''
			data = gzip.GzipFile(fileobj=urllib.request.urlopen(req)).read()
			content = data.decode("utf-8")
			pdetail = json.loads(content)
			with open('Trainer_'+season_id+'_'+str(rst)+'_'+str(ts1)+'_'+str(i)+'.json', "w") as outfile:
				json.dump(pdetail, outfile)
	except:
		print("TRAINERS issue with season_id "+season_id)
#getting Pokémon rankings
for season_id in body['list']:
	rst = body['list'][season_id]['rst']
	ts1 = body['list'][season_id]['ts1']
	ts2 = body['list'][season_id]['ts2']
	try:
		for i in range(1, 6):
			url = f'https://resource.pokemon-home.com/battledata/ranking/scvi/{season_id}/{rst}/{ts2}/pdetail-{i}'
			req = urllib.request.Request(url, headers=headers)
			#req.add_header('Accept-encoding', 'gzip')
			pdetail = ''
			#data = gzip.GzipFile(fileobj=urllib.request.urlopen(req)).read()
			#content = data.decode("utf-8")
			with urllib.request.urlopen(req) as res:
				pdetail = json.load(res)
				#with open(season_id+'_'+str(rst)+'_'+str(ts2)+'_'+str(i)+'.json', "w") as outfile:
				with open(season_id+'_'+str(rst)+'_'+str(ts1)+'_'+str(i)+'.json', "w") as outfile:
					json.dump(pdetail, outfile)
	except:
		print("RANKINGS issue with season_id "+season_id)