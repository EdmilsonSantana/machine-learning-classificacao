import pandas as pd
from collections import Counter

df = pd.read_csv('busca2.csv')

x_df = df[['home', 'busca', 'logado']]
y_df = df['comprou']

x_dummies_df = pd.get_dummies(x_df)
y_dummies_df = y_df

x = x_dummies_df.values
y = y_dummies_df.values

porcentagem_de_treino = 0.8
porcentagem_de_teste = 0.1

tamanho_de_treino = int(porcentagem_de_treino * len(y))
tamanho_de_teste = int(porcentagem_de_teste * len(y))
tamanho_de_validacao = len(y) - tamanho_de_treino - tamanho_de_teste

treino_dados = x[:tamanho_de_treino]
treino_marcacoes = y[:tamanho_de_treino]

fim_de_treino = tamanho_de_treino + tamanho_de_teste

teste_dados = x[tamanho_de_treino:fim_de_treino]
teste_marcacoes = y[tamanho_de_treino:fim_de_treino]

validacao_dados = x[fim_de_treino:]
validacao_marcacoes = y[fim_de_treino:]

# algoritmo que chuta um único valor 
acerto_base = max(Counter(validacao_marcacoes).values())
taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)
print("Taxa de acerto base: %f" % taxa_de_acerto_base)


def predict(nome, modelo, dados, marcacoes):
	resultado = modelo.predict(dados)
	acertos = (resultado == marcacoes)

	total_de_acertos = sum(acertos)
	total_de_elementos = len(teste_dados)
	taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

	msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
	print(msg)
	return taxa_de_acerto


def fit_and_predict(nome, modelo, treino_dados, 
	treino_marcacoes, teste_dados, teste_marcacoes):

	modelo.fit(treino_dados, treino_marcacoes)

	return predict(nome, modelo, teste_dados, teste_marcacoes)




from sklearn.naive_bayes import MultinomialNB
modelo_multinomial = MultinomialNB()

resultado_multinomial = fit_and_predict("MultinomialNB", modelo_multinomial, treino_dados, 
	treino_marcacoes, teste_dados, teste_marcacoes)

from sklearn.ensemble import AdaBoostClassifier
modelo_ada_boost = AdaBoostClassifier()

resultado_ada_boost = fit_and_predict("AdaBoostClassifier", modelo_ada_boost, treino_dados, 
	treino_marcacoes, teste_dados, teste_marcacoes)

if resultado_multinomial > resultado_ada_boost:
	vencedor = modelo_multinomial
else:
	vencedor = modelo_ada_boost

resultado_vencedor = predict("vencedor", vencedor, 
	validacao_dados, validacao_marcacoes)

print("Total de testes: %d" % len(validacao_dados))