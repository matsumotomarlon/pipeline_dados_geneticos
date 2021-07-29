#!/usr/bin/env python
# coding: utf-8

# # Requisitos: Python 3, Plink 1.9, VCFtools

# In[ ]:


#Comandos para instalar pacotes, caso não tenha o pacote instalado retire a tag "#" e execute os comandos abaixo:
#!py -m pip install numpy
#!py -m pip install pandas
#!py -m pip install seaborn
#!py -m pip install matplolib


# In[1]:


import numpy as np #biblioteca utilizada para trabalhar com vetores
import pandas as pd #biblioteca para trabalhar com dataframes (planilhas excel)
#import seaborn as sns #biblioteca utilizada para criar gráficos mais "bonitos"
#import matplotlib.pyplot as plt #biblioteca para criar gráficos "comuns" ao estilo Matlab
import os


# In[ ]:


#Tratamento de dados WES com Plink
cmd = "plink --vcf wes_hg19.vcf.gz --make-bed --out wes_hg19 --double-id --biallelic-only strict"

os.system(cmd)


# In[ ]:


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


# In[ ]:


#Renomear as asmotras da primeira coluna para BRS
for linha in novo_conteudo:
    linha[0] = "BRS"


# In[ ]:


#Escrever e salvar no computador o arquivo de saida
with open(arquivo_saida, "w") as saida:
    for linha in novo_conteudo:
        linha = " ".join(linha)
        linha = linha + "\n"
        saida.write(linha)
saida.close()


# In[ ]:


#wes_hg19_fam = pd.read_table("wes_hg19.fam", header = None, sep = " ")

#wes_hg19_fam


# In[ ]:


#for linha in wes_hg19_fam[0]:
#    wes_hg19_fam[0] = "BRS"
    
#wes_hg19_fam.to_csv("wes_hg19.fam", index = False, header = None, sep = " ")


# In[2]:


novo_conteudo = []

with open("wes_hg19.bim", "r") as f:
    conteudo = f.readlines()
    
    for linha in conteudo:
        linha = linha.strip("\n")
        linha = linha.strip("\r")
        linha = linha.split("\t")
        novo_conteudo.append(linha)
f.close()


# In[4]:


#Renomear os ID que estão com "." para o numero do cromossomo e posição
for linha in novo_conteudo:
    if linha[1] == ".":
        linha[1] = "chr" + linha[0] + "_" + linha[3]


# In[6]:


#Escrever e salvar no computador o arquivo de saida
with open("wes_hg19_no_blank_id.bim", "w") as saida:
    for linha in novo_conteudo:
        linha = "\t".join(linha)
        linha = linha + "\n"
        saida.write(linha)
saida.close()


# In[192]:


#concatenar as colunas dos alelos referencias com alelos alternativos
gen = []
teste = []
gen_quality = ["GC","CG","AT","TA"]

for linha in novo_conteudo:
    genotipo = [linha[4] + linha[5]]
    linha = linha + genotipo
#df_c = pd.concat([novo_conteudo.reset_index(drop=True), df_b], axis=1)


# In[188]:





# In[ ]:


#Definir diretorio de arquivo de entrada
#wes_hg19_bim = pd.read_table("wes_hg19.bim", header = None)


# In[ ]:


#renomear as variantes sem ID de identificação
    
#wes_hg19_bim[1] = wes_hg19_bim[1].replace(["."], ["Chr" + wes_hg19_bim[0].astype(str) + "_" + wes_hg19_bim[3].astype(str)])


# In[ ]:


#wes_hg19_bim.to_csv("wes_hg19_no_blank_id.bim", index = False, header = None, sep = "\t")


# In[ ]:


#Tratamento de dados de arranjos de SNPs com Plink
#cmd = "plink --bfile array_raw.gz --maf 0.01 --make-bed --out saida_filtered_maf"
#os.system(cmd)


# In[ ]:


cmd = "plink --vcf ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz --make-bed --out thousand_genome_chr22_extract --biallelic-only strict --allow-extra-chr"
os.system(cmd)

#i = 0
#for i in range(22):
#    cmd = "plink --vcf ALL.chr",i,".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz --make-bed --out thousand_genome_chr",i,"_extract --biallelic-only strict --allow-extra-chr"
#    os.system(cmd)


# In[ ]:


#cmd = "ls thousand_genome_chr*log | cut -d'.' -f1 > mergelist.txt"
#os.system(cmd)


# In[ ]:




