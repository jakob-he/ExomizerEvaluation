#!/usr/bin/env python3
'''
Main script to evaluate exomizer performance.
'''
# standard libraries
import os
import subprocess
from argparse import ArgumentParser

# own libraries
from lib import exomizer, config, progressbar


def parse_arguments():
    '''Parsing command line arguments.'''
    parser = ArgumentParser(description=(
        "Evaluates the performances of exomizer on given VCF and JSON files using the Phenix priotization"))
    parser.add_argument("-f", "--createfiles",
                        help="create exomiser analysis files", action="store_true")
    parser.add_argument(
        "-e", "--exomizer", help="Create anaylsis batchfile and execute exomizer", action="store_true")
    parser.add_argument(
        "-r", "--ranks", help="Get ranks from result files", action="store_true")
    return parser.parse_args()


def createanafile(file, config_data):
    if file.endswith("gz"):
        jsonfile = exomizer.getjsonfile(
            file, config_data['directories']['json'])
        if jsonfile:
            exomizer.createanalysisfile(os.path.join(config_data['directories']['vcf'], file), jsonfile, config_data['files']
                                        ['samplefile'], config_data['directories']['analysisfiles'], config_data['directories']['results'])


def main():
    config_data = config.EvalExConfig()
    args = parse_arguments()
    # create analysisfiles for all vcf and json pairs 1KG
    if args.createfiles:
        # clear directories
        exomizer.resetdir(config_data['directories']['analysisfiles'])
        exomizer.resetdir(config_data['directories']['results'])

        vcffiles = []
        # create anaylsis files for each vcf file
        for file in os.listdir(config_data['directories']['vcf']):
            vcffiles.append(file)
        case_objs = progressbar.progress_bar("Create anaylsis files")(
            lambda file: createanafile(file, config_data))(vcffiles)

    # execute exomizer on batch file
    if args.exomizer:
        # create analysis batch file of all analysisfiles
        batchfile = exomizer.createbatchanalysis(
            config_data['directories']['analysisfiles'])
        config_data['exomizer']['exomizerdir'] = "exomiser-cli-10.0.1"
        FNULL = open(os.devnull, 'w')
        print("Executing Exomizer...")
        subprocess.run(["java", "-Xms4g", "-Xmx8g", "-jar", config_data['exomizer']['exomizerdir'] + ".jar",
                        "--analysis-batch", batchfile], cwd=config_data['exomizer']['exomizerdir'], stdout=FNULL, stderr=subprocess.STDOUT)
        print("Exomizer finished")

    # analyze results
    if args.ranks:
        print("Getting rank data")
        ranks = []
        for dir in os.listdir(config_data['directories']['results']):
            ranks.append(exomizer.getrank(
                dir, config_data['directories']['json'], config_data['directories']['results']))

        # print ranks as percentages
        exomizer.outputranks(ranks)


if __name__ == '__main__':
    main()
