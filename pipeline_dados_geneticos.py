#Comandos para instalar pacotes, caso não tenha o pacote instalado retire a tag "#" e execute os comandos abaixo:
#!py -m pip install numpy
#!py -m pip install pandas
#!py -m pip install seaborn
#!py -m pip install matplolib

#import numpy as np #biblioteca utilizada para trabalhar com vetores
#import pandas as pd #biblioteca para trabalhar com dataframes (planilhas excel)
import os #necessário para executar comandos via terminal

#Tratamento de dados WES com Plink
cmd = "plink --vcf wes_hg19.vcf.gz --make-bed --out wes_hg19 --double-id --biallelic-only strict"
os.system(cmd)

#Abrir o arquivo e remover espaços e quebra de linhas
novo_conteudo = []

with open("wes_hg19.fam", "r") as f:
    conteudo = f.readlines()
    
    for linha in conteudo:
        linha = linha.strip("\n")
        linha = linha.strip("\r")
        linha = linha.split(" ")
        novo_conteudo.append(linha)
f.close()

#Renomear as asmotras da primeira coluna para BRS
for linha in novo_conteudo:
    linha[0] = "BRS"
    
#Escrever e salvar no computador o arquivo de saida
with open("wes_hg19.fam", "w") as saida:
    for linha in novo_conteudo:
        linha = " ".join(linha)
        linha = linha + "\n"
        saida.write(linha)
saida.close()

#Abrir o arquivo e remover espaços e quebra de linhas
novo_conteudo = []

with open("wes_hg19.bim", "r") as f:
    conteudo = f.readlines()
    
    for linha in conteudo:
        linha = linha.strip("\n")
        linha = linha.strip("\r")
        linha = linha.split("\t")
        novo_conteudo.append(linha)
f.close()

#Renomear os ID que estão com "." para o numero do cromossomo e posição
for linha in novo_conteudo:
    if linha[1] == ".":
        linha[1] = "chr" + linha[0] + "_" + linha[3]
        
#Escrever e salvar no computador o arquivo de saida
with open("wes_hg19.bim", "w") as saida:
    for linha in novo_conteudo:
        linha = "\t".join(linha)
        linha = linha + "\n"
        saida.write(linha)
saida.close()

#controle de qualidade do WES
cmd = "plink --bfile wes_hg19 --geno 0.05 --mind 0.05 --hwe 0.01 --make-bed --out wes_filtered"
os.system(cmd)

#calcular a frequência alélica de WES do BIPMED
cmd = "plink --bed wes_filtered.bed --bim wes_filtered.bim --fam wes_filtered.fam --freq --family --out wes_AF"
os.system(cmd)
