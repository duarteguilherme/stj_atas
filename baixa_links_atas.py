import requests
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp
import async_timeout

anos = range(2011,2018)
meses = range(1,13)
dias = range(1,32)

datas = [ "{}/{}/{}".format(i, j, k) for k in anos for j in meses for i in dias ]

url = "http://ww2.stj.jus.br/processo/pauta/ver?data={}&aplicacao=calendario&popup=TRUE"

def escrever_arquivo(dicio):
    print(dicio)
    with open('dados.txt', 'a') as f:
        for i in ['data_sessao','hora','data','ata','turma']:
            f.write('"{}",'.format(dicio[i]))
        f.write('\n')

def limpa_classe(classe, info):
    info['hora'] = classe.find('span', attrs={'class':'clsCalendarioSessaoResumoHora'}).text
    info['data'] = classe.find('span', attrs={'class':'clsCalendarioSessaoResumoData'}).text
    try:
        info['ata'] = classe.find(attrs={'class':'clsCalendarioSessaoResumoAtaBotao'})['href']
    except:
        info['ata'] = ''
    info['turma'] = classe.find('span', attrs={'class':['clsCalendarioSessaoResumoOrdinariaClass', 'clsCalendarioSessaoResumoExtraOrdinariaClass']}).text
    escrever_arquivo(info)


 
def baixa_pagina(data_url):
    print(url.format(data_url))
    info = {}
    for i in range(500):
        try:
            pagina = requests.get(url.format(data_url)) 
            pagina = BeautifulSoup(pagina.text, 'html.parser')
            break
        except:
            pass
    info['data_sessao'] = pagina.find(id = "resumoTituloDataFormatada").text
    classes = pagina.find_all('div', attrs={'class':'clsCalendarioSessaoResumoLinha'})
    if classes is not None:
        for j in classes:
            limpa_classe(j, info)



for i in datas:
    baixa_pagina(i)
        
    
