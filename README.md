# Pipeline para análise de dados genéticos

Ferramenta desenvolvido em `Python` para organizar as etapas de análise de dados genéticos e comparar com frequências alélicas do GnomAD v2 (GRCh37/hg19) https://gnomad.broadinstitute.org/. Caso não tenha o `PLINK 1.9` baixe-o em https://www.cog-genomics.org/plink/, pois algumas linhas de comandos são implementados utilizando o PLINK.

**Requisitos:**
`Linux`
`PLINK 1.9`
`Python 3.8.8 +`

# Obter arquivos WES do BIPMED

Os dados genéticos do exoma do BIPMED (GRCh37/hg19) está disponivel em https://www.ebi.ac.uk/ena/browser/view/PRJEB39251.

Executar o script `pipeline_dados_geneticos.py` via terminal `Linux` para realizar o controle de qualidade e cálculo de frequência alélica.

Certifique se o arquivo `BIPMED_WES_hg19.vcf.gz` está no mesmo `diretório` do script `pipeline_dados_geneticos.py`.

No terminal do linux execute o comando: 

```
python pipeline_dados_geneticos.py
```

# Obter arquivos de dados de exoma do gnomAD

O arquivo de texto `link_gnomad_exome.txt` contém os link para baixar os arquivos de exomas via terminal do linux

Abaixo o conteudo do `link_gnomad_exome.txt`:

```
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.22.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.21.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.20.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.19.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.18.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.17.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.16.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.15.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.14.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.13.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.12.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.11.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.10.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.9.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.8.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.7.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.6.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.5.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.4.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.3.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.2.vcf.bgz
https://storage.googleapis.com/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.1.vcf.bgz
```

Baixar arquivos de exomas do gnomAD no formato `VCF` via comando `wget` no terminal do `Linux`:

```
wget -i link_gnomad_exome.txt
```

# Extrair informações necessárias dos arquivos gnomAD

Utilizar o terminal do `Linux` para renomear a ID `vep` para `CSQ`, pois o `bcftools` não identifica a ID `vep` e salva em um novo arquivo `VCF` e `tbi`:

```
for i in $(seq 1 22); do gunzip -c gnomad.exomes.r2.1.1.sites.$i.vcf.bgz | sed "s/vep/CSQ/" | bgzip > chr$i.vcf.bgz && tabix -f -p vcf chr$i.vcf.bgz; done
```

O complemento `split-vep` do `bcftools` foi executado via terminal do `Linux` para extrair os campos desejados:

```
for i in $(seq 1 22); do bcftools +split-vep chr$i.vcf.bgz -F '%CHROM\t%POS\t%ID\t%REF\t%ALT\t%SYMBOL\t%Consequence\t%FILTER\t%AF\t%AF_eas\t%AF_nfe\t%AF_afr\t%AF_amr\t%AF_asj\t%AF_fin\t%AF_sas\t%AF_oth\n' -d > chr$i.txt; done
```
# Merge de todas variantes gnomAD com variantes LOF do gnomAD

O arquivo de variantes LOF `gnomad.v2.1.1.all_lofs.txt.bgz` disponivel no GNOMAD **não contém frequência alélica**.

Por isso, realizar merge entre todas variantes com variantes LOF (`gnomad.v2.1.1.all_lofs.txt.bgz`) para obter frequência alélica das variantes LOF utilizando o ambiente `R`:

```r
#ENTRADA DOS EXOMAS DO GNOMAD
for (i in 22:1){
gnomad_exome = read.table(paste0("chr",i,".txt"), header = F)

#SEPARAR OS DADOS APROVADOS NO TESTE DE QUALIDADE DE EXOMA
gnomad_exome = subset(gnomad_exome, gnomad_exome$V8 == "PASS")

#SEPARAR OS DADOS LOF COM ALTA CONFIABILIDADE E BAIXA CONFIABILIDADE
saida = subset(gnomad_exome, gnomad_exome$V9 == "HC" | gnomad_exome$V9 == "LC")

#ESCREVER TABELAS EM FORMATO TXT)
write.table(saida,file= paste0("chr",i,"_release.txt"), row.names = F, col.names = F)

#PARA CADA CICLO APAGAR DADOS
rm(gnomad_exome, saida)
}

#MERGE DE TODOS OS CHRS EM UM ÚNICO TXT
system("cat *.txt > all_chr_merged.txt")
```

# Extrair colunas de interesse do gnomAD

```r
#ABRIR ARQUIVO DE FREQ LOF MESCLADO DO GNOMAD
gnomad_exome = read.table("all_chr_merged.txt", header = F)

#ORDENAR POR CROMOSSOMO EM ORDEM CRESCENTE
gnomad_exome = gnomad_exome[order(gnomad_exome$V1, decreasing=c(FALSE)), ]

#NOMEAR AS COLUNAS
colnames(gnomad_exome) = c("chr", "pos", "id", "ref", "alt", "gene", "consequence", "filter_exome", 
                           "lof_quality", "lof_filter", "lof_flag", "af_gnomad", "ac_gnomad", "an_gnomad", 
                           "af_eas", "ac_eas", "an_eas", "af_nfe", "ac_nfe", "an_nfe", "af_afr", "ac_afr", 
                           "an_afr", "af_amr", "ac_amr", "an_amr", "af_asj", "ac_asj", "an_asj", "af_fin", 
                           "ac_fin", "an_fin", "af_sas", "ac_sas", "an_sas", "af_oth", "ac_oth", "an_oth")

#SALVAR ARQUIVO DE FREQ LOF MESCLADO
write.table(gnomad_exome,file="all_chr_merged_release.txt", row.names = F, col.names = T)
```
# Separar somente as variantes LOF com qualidade HC

```r
#CARREGAR OU INSTALAR PACOTE TIDYVERSE
if (!require("tidyverse")) {
  install.packages("tidyverse", dependencies = TRUE)
  library(tidyverse)
}

gnomad_exome = read.table("all_chr_merged_release.txt", header = T)

#SEPARAR AS VARIANTES COM MULTIPLAS CONSEQUENCIAS
gnomad_exome = separate(gnomad_exome, col = consequence, into = c("consequence"), sep = "&")

#SEPARAR SOMENTE AS VARIANTES COM CLASSES LOF
consequence = data.frame(lof_consequence = c("frameshift_variant", "stop_gained",
                                         "splice_donor_variant", "splice_acceptor_variant"))
saida_release = merge(gnomad_exome, consequence, by.x = "consequence", by.y = "lof_consequence")

#ORGANIZAR AS COLUNAS
saida_release = saida_release[,c(2:7, 1, 8:38)]

#ORDENAR COLUNAS
saida_release = saida_release[order(saida_release$chr, saida_release$gene, decreasing=c(FALSE)), ]

hc_gnomad_exome = subset(saida_release, saida_release$lof_quality == "HC")

hc_gnomad_exome$lof_filter = "."
hc_gnomad_exome$lof_flag = "."

#REMOVER DADOS DUPLICADOS
unique_gnomad = data.frame(unique(hc_gnomad_exome))

write.table(unique_gnomad,file="hc_chr_merged_release.txt", row.names = F, col.names = T)
```

# Extrair variantes LOF do gnomAD

```r
hc_gnomad_exome = read.table("hc_chr_merged_release.txt", header = T)

no_freq_gnomad = read.table("gnomad.v2.1.1.all_lofs.txt.bgz", header = T)

#COMBINAR VARIANTES DUPLICADAS
hc_gnomad_multi = hc_gnomad_exome %>%
  group_by(chr, pos, id, ref, alt, filter_exome, af_gnomad, ac_gnomad, an_gnomad, 
           af_eas, ac_eas, an_eas, af_nfe, ac_nfe, an_nfe, af_afr, ac_afr, 
           an_afr, af_amr, ac_amr, an_amr, af_asj, ac_asj, an_asj, af_fin, 
           ac_fin, an_fin, af_sas, ac_sas, an_sas, af_oth, ac_oth, an_oth) %>%
  summarise(gene = paste(gene, collapse = ","), consequence = paste(consequence, collapse = ","), .groups = "drop")

#MERGE ENTRE GNOMAD E GNOMAD LOF
merged = merge(hc_gnomad_multi, no_freq_gnomad, by.x = c("chr", "pos", "ref", "alt"), by.y = c("chrom","pos", "ref", "alt"))

merged$gene = NULL
merged$consequence = NULL
merged$gene_ids = NULL
merged$transcript_ids = NULL

#ORDENAR COLUNAS
merged = merged[order(merged$chr, decreasing=c(FALSE)), ]

write.table(merged,file="hc_gnomad_final.txt", row.names = F, col.names = T)
```
# Encontrar variantes em comum entre BIPMED e gnomAD

```r
lof_freq_gnomad = read.table("hc_gnomad_final.txt", header = T)

#ENTRADAS DAS FREQUÊNCIAS DAS POPULAÇÕES DO BIPMED
wes_bipmed = read.table("wes_AF.frq.strat", header = T)

#MERGE PARA ENCONTRAR VARIANTES EM COMUM
lof_gnomad_bipmed = merge(lof_freq_gnomad, wes_bipmed, by.x = c("chr", "id", "ref", "alt"), by.y = c("CHR", "SNP", "A2", "A1"))
lof_gnomad_bipmed_reverse = merge(lof_freq_gnomad, wes_bipmed, by.x = c("chr", "id", "ref", "alt"), by.y = c("CHR", "SNP", "A1", "A2"))

#MESCLAR AS COLUNAS
lof_gnomad_bipmed_release =  rbind(lof_gnomad_bipmed, lof_gnomad_bipmed_reverse)

#ORGANIZAR AS COLUNAS
lof_gnomad_bipmed_release = lof_gnomad_bipmed_release[,c(1:33,37:39,34:35)]

#RENOMEAR AS COLUNAS COM POPULAÇÕES BRASILEIRAS DO BIPMED
colnames(lof_gnomad_bipmed_release)[c(34:36)] = c("af_brs", "ac_brs", "an_brs")

#ORDENAR COLUNAS
lof_gnomad_bipmed_release = lof_gnomad_bipmed_release[order(lof_gnomad_bipmed_release$chr, decreasing=c(FALSE)), ]

write.table(lof_gnomad_bipmed_release,file="lof_gnomad_bipmed.txt", row.names = F, col.names = T)
```

# Encontrar variantes LOF associadas a Alzheimer por genes candidatos

```r
#GENES CANDIDATOS ALZHEIMER
genes_alzheimer = read.table("genes_alzheimer.txt", header = T)

#MERGE PARA SELECIONAR SOMENTE OS GENES CANDIDATOS EM BIPMED-GNOMAD
alzh_gnomad_bipmed = merge(lof_gnomad_bipmed, genes_alzheimer, by.x = "gene_symbols", by.y = "genes_alzheimer")
write.table(alzh_gnomad_bipmed,file="alzh_gnomad_bipmed.txt", row.names = F, col.names = T)

#MERGE PARA SELECIONAR SOMENTE OS GENES CANDIDATOS EM GNOMAD
alzh_gnomad = merge(hc_gnomad_final, genes_alzheimer, by.x = "gene_symbols", by.y = "genes_alzheimer")
write.table(alzh_gnomad,file="alzh_gnomad.txt", row.names = F, col.names = T)
```
