import pandas as pd 
import os
import numpy as np
import re
import requests

dados = pd.read_csv('dados.txt', header=None)
dados.columns = ['dia_escrito', 'hora','data','link','turma','naosei']
dados = dados[pd.notnull(dados['link'])]


def limpa_link(link):
	link = link.split(',')
	documento = re.sub("'", "", re.sub("javascript:quandoClicaAbreAta\('", "", link[0]))
	data = re.sub("'", "", re.sub("'\).+", "", link[-1]))
	url = "https://ww2.stj.jus.br/processo/dj/documento?seq_documento=" + documento + '&data_pesquisa=' + data + 'parametro=42'
	nome_documento = documento + re.sub('/','_', data)
	return {'url': url, 'documento': nome_documento}

def baixa_pdf(ata):
	conteudo = requests.get(ata['url']).content
	if not os.path.exists('pdfs'):
		os.makedirs('pdfs')
	with open('pdfs/' + ata['documento'] + '.pdf', 'wb') as f:
		f.write(conteudo)



for i in range(dados.shape[0]):
	ata = limpa_link(dados['link'].iloc[i])
	print(ata)
	baixa_pdf(ata)