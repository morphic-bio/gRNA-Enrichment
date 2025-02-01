The fastq files included in this repository were taken from the original study:

Rosen BP, Li QV, Cho HS, Liu D et al. Parallel genome-scale CRISPR-Cas9 screens uncouple human pluripotent stem cell identity versus fitness. Nat Commun 2024 Oct 17;15(1):8966. PMID: [39419994](https://www.ncbi.nlm.nih.gov/pubmed/39419994)

[NCBI GEO public access is located here.](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277069)

Only 4 out of the 8 samples are included here:
E8_T0
NE_GFP_high
NE_GFP_low
E8_control

Therefore 2 of the 4 screens are performed:
E8_screen (E8_T0 vs E8_control)
NE_screen (NE_GFP_high vs NE_GFP_low)

Fastq file names are their SRA SRR accession IDs (SRR____), each are associated with a sample.

Fastq files in this directory have been subsampled to 10000 read pairs using seqtk:
for file in *.fastq.gz; do
    seqtk sample -s100 "$file" 10000 | gzip > "${file%.fastq.gz}_sampled.fastq.gz"
done

Original larger files were removed, and the subsampled fastq files are renamed back to their original:
rename 's/_sampled.fastq.gz$/.fastq.gz/' *.fastq.gz

These files are meant to quickly test the workflow's functionality, not for accurately replicating original sample's results.

