# ExomizerEvaluation
Script collection used to evaluate the performance of Exomizer.

# General Workflow

1. Exomizer analysis files are created using the sample structure file,VCF file and the HPO feature terms from a JSON file.
2. Exomizer is executed using a batchfile with all analysis files from step 1. For each case the hundred highest ranking genes are computed. 
3. For each case the rank of the disease gene is extracted from the results and the overall rank statistics are displayed.

# Usage/Installation Linux

To install the requirements run: 

```
pip3 install -r requirements.txt
```

Yaml which is also required can be installed using the instructions on: https://pyyaml.org/wiki/PyYAML


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
4. Extract the Exomizer version to the cloned repository (replace the folder exomier-cli-10.0.1).

5. Create a new directory ```data``` in the exomizer directory and move the additional data files from step 2 into ```data```

6. Changed the following lines of ```application.properties``` in the exomizer directory:
```
exomiser.data-directory= /home/jakob/Documents/PEDIA/ExomizerEvaluation/exomiser-cli-10.0.1/data #change this to your exomizer data directory (full path) 
exomiser.hg19.data-version=1805
```
7. Move annotated VCF files into the 1KG folder

8. Move JSON files (old format) into json_simulation.`

9. Adjust the directory information in ```config_SAMPLE``` if changed and rename it to ```config.ini```.

10. Edit ```analysis_file_structure.yml``` to configure Exomizer execution. The current version uses the Phenix priotization.

10. Execute the evaluation.py script:
```
python3 evaluation.py -f -e -r
```

11. (Optional) rerun the ranking or the exomization step:
```
python3 evaluation.py -e #rerun exomization
python3 evaluation.py -r #rerun ranking
```


