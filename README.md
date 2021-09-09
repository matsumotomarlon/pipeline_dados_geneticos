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
# Merge todas variantes GNOMAD com variantes LOF do GNOMAD

O arquivo de variantes LOF `gnomad.v2.1.1.all_lofs.txt.bgz` disponivel no GNOMAD **não contém frequência alélica**.

Por isso, realizar merge entre todas variantes com variantes LOF (`gnomad.v2.1.1.all_lofs.txt.bgz`) para obter frequência alélica das variantes LOF utilizando o ambiente `R`:

```r
# ABRIR ARQUIVO COM TODOS OS LOF DO GNOMAD
gene_data = read.table("gnomad.v2.1.1.all_lofs.txt.bgz", header = T)

#EXTRAIR COLUNA COM SIMBOLOS DOS GENES
symbols_gene = data.frame(unique(gene_data$gene_symbols))
colnames(symbols_gene) = c("gene_symbols")

for (i in 1:22){
#ENTRADA DOS EXOMAS DO GNOMAD
gnomad_exome = read.table(paste0("chr",i,".txt"), header = F)

#MERGE ENTRE EXOMAS GNOMAD E LOF GNOMAD
saida = merge(gnomad_exome, symbols_gene, by.x = "V7", by.y = "gene_symbols")

#FILTRAR OS EXOMAS COM QUALIDADE PASS
saida = subset(saida, saida$V9 == "PASS")

#MERGE POR CLASSES DE VARIANTES
consequence = data.frame(consequence = c("frameshift_variant", "stop_gained", "splice_donor_variant", "splice_acceptor_variant"))
saida_release = merge(saida, consequence, by.x = "V8", by.y = "consequence")

#ESCREVER TABELAS EM FORMATO TXT DOS GENES ALVOS
write.table(saida_release,file= paste0("chr",i,"_release.txt"), row.names = F, col.names = F)

rm (gnomad_exome, saida, saida_release)
}

#MERGE DE TODOS OS CHRS
system("cat LOF_AF_PASS/*.txt > chr_release_merged.txt")

#ABRIR ARQUIVO DE FREQ LOF MESCLADO DO BIPMED E NOMEAR COLUNAS
gnomad_exome = read.table("LOF_AF_PASS/chr_release_merged.txt", header = F)
gnomad_exome = gnomad_exome[,c(3:8, 2:1, 9:17)]

colnames(gnomad_exome) = c("chr", "pos", "id", "ref", "alt", "af_pop_total", "gene", "consequence", 
                           "filter_exome", "af_eas", "af_nfe", "af_afr", "af_amr", 
                           "af_asj", "af_fin", "af_sas", "af_oth")

#SALVAR ARQUIVO DE FREQ LOF MESCLADO
write.table(gnomad_exome,file="LOF_AF_PASS/chr_release_merged.txt", row.names = F, col.names = T)

```
