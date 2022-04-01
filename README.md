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
# Merge de todas variantes GNOMAD com variantes LOF do GNOMAD

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

#EXTRAIR COLUNAS COM FREQUÊNCIAS

```r
#ABRIR ARQUIVO DE FREQ LOF MESCLADO DO BIPMED E NOMEAR COLUNAS
gnomad_exome = read.table("AF_LOF_GNOMAD/all_chr_merged.txt", header = F)

#ORDENAR POR CROMOSSOMO EM ORDEM CRESCENTE
gnomad_exome = gnomad_exome[order(gnomad_exome$V1, decreasing=c(FALSE)), ]

colnames(gnomad_exome) = c("chr", "pos", "id", "ref", "alt", "gene", "consequence", "filter_exome", 
                           "lof_quality", "lof_filter", "lof_flag", "af_gnomad", "ac_gnomad", "an_gnomad", 
                           "af_eas", "ac_eas", "an_eas", "af_nfe", "ac_nfe", "an_nfe", "af_afr", "ac_afr", 
                           "an_afr", "af_amr", "ac_amr", "an_amr", "af_asj", "ac_asj", "an_asj", "af_fin", 
                           "ac_fin", "an_fin", "af_sas", "ac_sas", "an_sas", "af_oth", "ac_oth", "an_oth")

#SALVAR ARQUIVO DE FREQ LOF MESCLADO
write.table(gnomad_exome,file="AF_LOF_GNOMAD/all_chr_merged_release.txt", row.names = F, col.names = T)
```
