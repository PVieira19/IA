"""
Created on Thu May 16 16:36:32 2019

@autor: Manuel, Lety, Jorge
@trabalho: Métodos de Procura
"""
import json

class cidade:
    def __init__(self,nome):
        self.nome = nome
        self.vizinhos = []

    def adicionarCidade(self,cidade,distancia):
        if self.nome != cidade.nome:
            flag = False
            for c in self.vizinhos:
                if c.cidade.nome == cidade.nome:
                    flag = True
                    break
            if flag == False :
                dc = distanciaCidade(cidade,distancia)
                self.vizinhos.append(dc)
                cidade.adicionarCidade(self,distancia)

    def printVizinhos(self):
        for v in self.vizinhos:
            print(v.cidade.nome + ": "+ str(v.dist))

class distanciaCidade:
    def __init__ (self,cidade,distancia):
        self.cidade = cidade
        self.distancia = distancia
        
class cidadeDistanciaLinhaReta:
    def __init__(self,nome,distancia):
        self.nome = nome
        self.distancia = distancia

listaCidades = []
listaCidadesLR = []

def findCidade(nome):
    global listaCidades
    for cidade in listaCidades:
        if cidade.nome == nome:
            return cidade
        
def findCidadeLR(nome):
    global listaCidadesLR
    for cidade in listaCidadesLR:
        if cidade.nome == nome:
            return cidade

def loadJsonCidade():
    global listaCidades
    cidadesJSON = None
    with open('cidades.json','r',encoding='utf-8')  as f:
        cidadesJSON = json.load(f)
    print("a carregar cidades do ficheiro cidades.json...")
    for cityJSON in cidadesJSON:
        c = findCidade(cityJSON["nome"])
        if not c: 
            c = cidade(cityJSON["nome"])
            listaCidades.append(c)
            c.printVizinhos()
        
        for vizinho in cityJSON["vizinhos"]:
            cc = findCidade(vizinho["nome"])
            if not cc :
                cc = cidade(vizinho["nome"]) 
                listaCidades.append(cc)
            c.adicionarCidade(cc,vizinho["distancia"])

def loadJsonCidadeLR():
    global listaCidadesLR
    cidadesJSON = None
    with open('cidadesLR.json','r',encoding='utf-8')  as f:
        cidadesJSON = json.load(f)
    print("a carregar cidades do ficheiro cidadesLR.json...")    
    for cityJSON in cidadesJSON:
        c = cidadeDistanciaLinhaReta(cityJSON["nome"],cityJSON["distancia"])
        listaCidadesLR.append(c)
    

def procuraProfundiade(partida,destino):
    caminho = ""
    contador = 0
    historico = []
    p = findCidade(partida)
    d = findCidade(destino)
    if not p:
        print("cidade de partida não encontrada")
        exit()
    if not d:
        print("cidade destino não existe")
        exit()
    historico.append(p)
    
    while len(historico) > 0:
        cidadeAtual = historico.pop(0)
        caminho = caminho + cidadeAtual.nome +  " -> "
        #print(str(contador), caminho)
        if cidadeAtual.nome == d.nome:
            print("Destino alcançado!")
            print("Foram necessárias [" + str(contador) + "] iterações")
            print("Caminho percorrido: " + caminho)
            return
        else:
            historico.clear()
            for vizinho in cidadeAtual.vizinhos:
                historico.append(vizinho.cidade)
                contador = contador + 1

def procuraCustoUniforme(partida,destino):
    historico = []
    p = findCidade(partida)
    if not p:
        print("A cidade de partida não existe!")
        exit()
    d = findCidade(destino)
    if not d:
        print("A cidade de destino não existe!")
        exit()
    temp = { 'percurso' : [p], 'total' : 0}
    historico.append(temp)
    contador = 0
    while len(historico) > 0:
        percursoPrioritario = 0
        valorPrioritario = historico[0]['total']
        i = 0
        for c in historico:
            if c['total'] < valorPrioritario:
                percursoPrioritario = i
                valorPrioritario = c['total']
            i = i + 1
        maiorPrioridade = historico.pop(percursoPrioritario)
        percurso = maiorPrioridade['percurso']
        cidadeAtual = percurso[len(percurso)-1]
        
        if cidadeAtual.nome == destino:
            print("Destino alcançado!")
            print("Foram necessárias [" + str(contador) + "] iterações")
            print("Distancia: [" + str(maiorPrioridade['total']) + "] kms")
            caminho = ""
            for c in maiorPrioridade['percurso']:
                caminho = caminho + c.nome + " -> "
            print("Caminho percorrido: " + caminho)
            break
        else:
            listaVizinhos = cidadeAtual.vizinhos
            for v in listaVizinhos:
                cidadesLista = []
                for c in percurso:
                    cidadesLista.append(c)
                cidadesLista.append(v.cidade)
                novaDist = maiorPrioridade['total'] + v.distancia
                novoPercurso = { 'percurso' : cidadesLista, 'total' : novaDist }
                historico.append(novoPercurso)
        contador = contador + 1

def procuraSofrega(partida,destino="Faro"):
    p = findCidade(partida)
    if not p:
        print("A cidade de partida não existe!")
        exit()
    caminho = []
    caminho.append(p)
    i = 0
    while caminho[len(caminho)-1].nome != destino:
#        print(str(i),caminho[len(caminho)-1].nome)
        historico = []
        for v in caminho[len(caminho)-1].vizinhos:
            city = findCidadeLR(v.cidade.nome)
            historico.append(city)        
        tempM = historico[0].nome
        tempD = historico[0].distancia
        for c in historico:
            if c.distancia < tempD:
                tempM = c.nome
                tempD = c.distancia
        caminho.append(findCidade(tempM))
        i = i + 1
#    print(str(i),caminho[len(caminho)-1].nome)
    percurso = ""
    for c in caminho:
        percurso = percurso + c.nome + " -> "
    print("Destino alcançado!")
    print("Foram necessárias [" + str(i) + "] iterações")
    print("Caminho percorrido: " + percurso)

def procuraAstar(partida,destino="Faro"):
    p = findCidade(partida)
    d = findCidadeLR(partida).distancia
    if not p:
        print("A cidade de partida não existe!")
        return
    for vizinhos in p.vizinhos:
        if vizinhos.cidade.nome == "Faro":
            #return vizinhos.distancia
            print("Distancia "+str(vizinhos.distancia))
    historico = []
    temp = { 'percurso' : [p], 'total' : 0, 'distLReta' : d }
    historico.append(temp)
    contador = 0
    while len(historico) > 0:
#        print(str(contador),end=' ')
#        for e in  sorted(historico, key=lambda g: g['distLReta'])  :
#            print(e['percurso'][len(e['percurso'])-1].nome,end=' ')
#            print(e['total'],end=' ')
#        print()
        distLReta = historico[0]['distLReta']
        melhorPercurso = 0;
        i = 0;
        for p in historico:
            if p['distLReta'] < distLReta:
                distLReta = p['distLReta']
                melhorPercurso = i
            i = i + 1
        percurso = historico.pop(melhorPercurso)
        cidadeAtual = percurso['percurso'][len(percurso['percurso'])-1]
        if cidadeAtual.nome == destino:
            print("Destino alcançado!")
            print("Foram necessárias [" + str(contador) + "] iterações")
            caminho = ""
            for c in percurso['percurso']:
                caminho = caminho + c.nome + " -> "
            print("Caminho percorrido: " + caminho)
            break
        else:
            for v in cidadeAtual.vizinhos:
                novaDistanciaLR = findCidadeLR(v.cidade.nome).distancia
                novosVizinhos = []
                for c in percurso['percurso']:
                    novosVizinhos.append(c)
                novosVizinhos.append(v.cidade)
                distancia = percurso['total']+v.distancia
                temp = { 'percurso' : novosVizinhos, 'total' : distancia, 'distLReta' : novaDistanciaLR+distancia }
                historico.append(temp)
            contador = contador + 1
            
loadJsonCidade()
loadJsonCidadeLR()
#procuraProfundiade("Porto", "Viseu")     
#procuraCustoUniforme("Vila Real", "Faro")
#procuraSofrega("Coimbra","Faro")
#procuraAstar("Coimbra","Faro")
def cidade_inicio_funcao():
    cidade_inicio_=''
    print("Qual a cidade origem ?")
    cidade_inicio_ = input()
    return cidade_inicio_

def cidade_destino_funcao():
    cidade_destino_=''
    print("Qual a cidade destino ?")
    cidade_destino_=input()
    return cidade_destino_

def metodos_procura_funcao_definir():
    metodo_=''
    print("Qual o método de procura?\n1-Procura em Profundidade Primeiro\n2-Procura Custo Uniforme\n3-Procura Sofrega\n4-Procura A*")
    metodo_ = input()
    return metodo_

#if __name__ == "__main__":
'''Main'''
print("########################################################################################")
cidade_inicio=''
cidade_destino=''
print("-----------------------Definir Origem e Destino-----------------------")
cidade_inicio=cidade_inicio_funcao()
cidade_destino=cidade_destino_funcao()

while True:
    metodo=''
    metodo=metodos_procura_funcao_definir()
    print("########################################################################################")
    if metodo=="1": #procura em largura primeiro
        print("----------------Procura em Profundidade Primeiro---------------")
        print("Origem: "+ cidade_inicio)
        print("Destino: "+cidade_destino)
        print("----------------------------------------------------------")
        procuraProfundiade(cidade_inicio, cidade_destino)     
        #chamar a função do metodo de procura primeiro com as cidades como parametro
    elif metodo=="2": #procura custo uniforme
        print("----------------Procura Custo Uniforme---------------")
        print("Origem: " + cidade_inicio)
        print("Destino: " + cidade_destino)
        print("----------------------------------------------------------")
        procuraCustoUniforme(cidade_inicio, cidade_destino)
        # chamar a função do metodo de custo uniforme com as cidades como parametro
    elif metodo=="3": #procura sofrega
        print("----------------Procura Sofrega---------------")
        print("Origem: " + cidade_inicio)
        print("Destino: Faro")
        print("----------------------------------------------------------")
        procuraSofrega(cidade_inicio,"Faro")
        #chamar a função do metodo de procura sofrega com as cidades como parametros
    else:
        print("----------------Procura A*---------------")
        print("Origem: " + cidade_inicio)
        print("Destino: " + cidade_destino)
        print("----------------------------------------------------------")
        procuraAstar(cidade_inicio,"Faro")
        #chamar a função do metodo de A* com as cidades como parametros


