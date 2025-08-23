import pdfplumber
import json
import threading
import os

def scrapper():
    PATH_SUMULAS = os.getenv("PATH_RAW_FILE")
    PATH_JSON = os.getenv("PATH_JSON")

    try:
        pdf = pdfplumber.open(PATH_SUMULAS)
    except Exception as e:
        print("Erro ao abrir arquivo do STJ : " + e)

    print("Iniciando extração de dados do arquivo pdf ...")

    # Separação dos excertos e catalogação por súmula
    def adicionarExcertoDocumentos(sumula, raw_texto, enunciado, count): 
        excertos = str(raw_texto.split("\n\n")).split('"')
        
        print("Adicionando excerto {:d} {:s}".format(count, sumula))

        excerto = ""
        adicionar = False # Flag para evitar acúmulo de excertos

        # Excertos estão divididos nos excertos de fato e nos autores
        # Para criar os documentos é necessário juntar um excerto com um autor
        for e in excertos:
            if e.find("INTEIRO TEOR DAS SÚMULAS") == -1 and len(e.strip()) > 5:
                if (e.strip()[0].find("(") > 5 or e.strip()[0].find("(") == -1) and not(adicionar):
                    excerto += e
                    adicionar = True

                else:
                    excerto += e

                    objeto_documento = {
                        "page_content": excerto,
                        "metadata" : {
                            "source": sumula,
                            "enunciado": enunciado.strip(),
                        }
                    }

                    documentos.append(objeto_documento)
                    excerto = ""
                    adicionar = False

    count = 0

    documentos = [] # Array de dicionários com excertos separados
    raw_sumulas = "" # Ex : Sumula 10
    raw_excertos = "" # Conjunto de todos os excertos da sumula 10
    raw_enunciado = "" # Enunciado da Sumula 10

    INDEX_INICIAL = 38 # Página da primeira súmula (pg 39)
    INDEX_FINAL = len(pdf.pages) # Página do último excerto da última súmula

    # Acrônimos para facilitar a leitura
    EPO = "Excerto dos Precedentes Originários:"
    PRE = "Precedentes"
    EN = "Enunciado:"

    for i in range(INDEX_INICIAL, INDEX_FINAL):
        
        t = threading.Thread()

        # Extraindo dados básicos da página (Texto Cru da Página e Coluna da Esquerda)
        pagina = pdf.pages[i]
        raw_texto = pagina.extract_text()
        esquerda = pagina.crop((0, 0, 0.55 * pagina.width, 0.8 * pagina.height))
        texto_esquerda = esquerda.extract_text()

        posInicial = raw_texto.find(EPO) # Index da seção de Excertos

        # Se houver enunciados na página, extrair.
        if texto_esquerda.find(EN) != -1:
            limite_inferior = texto_esquerda.find(EN)+len(EN)
            limite_superior = texto_esquerda.find("Referências Legislativas:")

            raw_enunciado = texto_esquerda[limite_inferior:limite_superior]

        # Se houver início da seção de excertos : 
        # Se houver final da seção de excertos deve-se extrair o conteúdo entre o título da seção de excertos e o título da seção de precedentes
        # Se houver final da seção deve-se adicionar o conteúdo no array de documentos
        # Se não houver final da seção de excertos deve-se extrair todo o conteúdo após o título da seção de excertos
        if posInicial != -1:
            posFinal = raw_texto[posInicial+len(EPO):].find(PRE)

            raw_sumulas = pagina.extract_text_lines()[2].get("text") # Extração do número da Súmula

            posInicial += len(EPO)
            textoAdicionar = ""
            if posFinal != -1:
                
                textoAdicionar += raw_texto[posInicial:]
                textoAdicionar = textoAdicionar[:textoAdicionar.find(PRE)]
                raw_excertos = textoAdicionar 

                t = threading.Thread(target=adicionarExcertoDocumentos, args=(raw_sumulas, raw_excertos, raw_enunciado, count))
                t.start()   

                count += 1
                raw_excertos = ""

            else:
                textoAdicionar += raw_texto[posInicial:]
                raw_excertos = textoAdicionar

                t = threading.Thread(target=adicionarExcertoDocumentos, args=(raw_sumulas, raw_excertos, raw_enunciado, count))
                t.start()  

                raw_excertos = ""
                count += 1 

        # Se não houver início da seção de excertos : 
        # Se houver final da seção de excertos deve-se extrair todo o conteúdo até o título da seção de precedentes
        # Se houver final da seção de excertos deve-se adicionar o conteúdo no array de documentos
        # Se não houver final da seção de excertos deve-se extrair todo o conteúdo da página   
        else:
            posFinal = raw_texto.find(PRE)

            textoAdicionar = ""
            if posFinal != -1:
                textoAdicionar = raw_texto[:posFinal]
                raw_excertos = textoAdicionar

                t = threading.Thread(target=adicionarExcertoDocumentos, args=(raw_sumulas, raw_excertos, raw_enunciado, count))
                t.start()  

                raw_excertos = ""
                count += 1 
            else:
                textoAdicionar += raw_texto
                raw_excertos = textoAdicionar

                t = threading.Thread(target=adicionarExcertoDocumentos, args=(raw_sumulas, raw_excertos, raw_enunciado, count))
                t.start()  

                raw_excertos = ""
                count += 1 

    print("Iniciando criação de arquivo JSON...")

    documentsFile = open(PATH_JSON, "w", encoding="UTF-8")
    json.dump(documentos, documentsFile, indent=4)

    print("Arquivo JSON criado com sucesso.")