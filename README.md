# Pipeline para análise de dados genéticos

Ferramenta desenvolvido em `Python` para organizar as etapas de análise de dados genéticos e comparar com frequências alélicas do GnomAD v2 (GRCh37/hg19) https://gnomad.broadinstitute.org/. Caso não tenha o `PLINK 1.9` baixe-o em https://www.cog-genomics.org/plink/, pois algumas linhas de comandos são implementados utilizando o PLINK.

**Requisitos:**
`Linux`
`PLINK 1.9`
`Python 3.8.8`

# Obter arquivos WES do BIPMED

Os dados genéticos do exoma do BIPMED (GRCh37/hg19) está disponivel em https://www.ebi.ac.uk/ena/browser/view/PRJEB39251.

Executar o script `pipeline_dados_geneticos.py` via terminal para realizar o controle de qualidade e calculo de frequência alélica.

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

Baixar arquivos de exomas do gnomAD no formato `VCF` via comando `wget` no terminal do `Linux`

```
wget -i link_gnomad_exome.txt
```

# Extrair informações necessárias dos arquivos gnomAD

Utilizar o terminal do `Linux` para renomear a ID `vep` para `CSQ`, pois o `bcftools` não identifica a ID `vep` para realizar a extração dos campos.

```
for i in $(seq 1 22); do gunzip -c gnomad.exomes.r2.1.1.sites.$i.vcf.bgz | sed "s/vep/CSQ/" | bgzip > chr$i.vcf.bgz && tabix -f -p vcf chr$i.vcf.bgz; done
```

O complemento `split-vep` do `bcftools` foi executado via terminal do `Linux` para extrair os campos desejados:

```
for i in $(seq 1 22); do bcftools +split-vep chr$i.vcf.bgz -f '%CHROM\t%POS\t%ID\t%REF\t%ALT\t%AF\t%SYMBOL\t%Consequence\t%FILTER\n' -d > chr$i.txt; done
```
