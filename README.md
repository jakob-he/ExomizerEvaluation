# ExomizerEvaluation
Script collection used to evaluate the performance of Exomizer using JSON and VCF files.

# Usage/Installation Linux

1. Clone this repository
```
git clone https://github.com/jakobhertzberg/ExomizerEvaluation
```
2. Get the latest precompiled Exomizer version: 
```
wget https://data.monarchinitiative.org/exomiser/latest/exomiser-cli-10.1.0-distribution.zip
```
3. Get the necessary data files:
```
wget  https://data.monarchinitiative.org/exomiser/latest/1805_hg19.zip
wget  https://data.monarchinitiative.org/exomiser/latest/1802_phenotype.zip 
```
4. Move the exomizer to the cloned repository (replace the examplatory folder exomier-cli-10.0.1)

5. Create a new directory ```data``` in the exomizer directory and move the additional data files from step 2 into ```data```

6. Changed the following lines of ```application.properties``` in the exomizer directory:
```
exomiser.data-directory= /home/jakob/Documents/PEDIA/ExomizerEvaluation/exomiser-cli-10.0.1/data #change this to your exomizer data directory (full path) 
exomiser.hg19.data-version=1805
```
7. Move annotated VCF files into the 1KG folder

8. Move JSON files into json_simulation. The JSON files have to satisfy <b>one</b> of the follwing criteria:
  - the disease gene is in ```['genomic_entries']['variants']['gene']['gene_id']```
  - the disease gene is in ```['genomic_entries']['gene']['gene_id']```

9. Adjust the directory information in ```config_SAMPLE``` if changed and rename it to ```config.ini```.

10. Edit ```analysis_file_structure.yml``` to configure Exomizer execution.

10. Execute the evaluation.py script:
```
python3 evaluation.py -f -e -r
```

11. (Optional) rerun the ranking or the exomization step:
```
python3 evaluation.py -e #rerun exomization
python3 evaluation.py -r #rerun ranking
```


