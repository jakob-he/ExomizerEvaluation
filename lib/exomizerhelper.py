#!/usr/bin/env python3
'''
General helper functions used to evaluate the exomizer performance.
'''
# standard libraries
import json
import os
import datetime
import time
import shutil

#3rd party libraries
import yaml
import pandas

def createanalysisfile(vcf, jsonfile ,analysissanmplefile, outputdir , resultdir):
    '''Creates and dumps an Exomizer analysis file.'''
    #delete previous analyisfiles and results
    # get absolute file/directory paths; necessary for exomizer execution
    thispath = os.path.normpath(os.path.join(os.path.dirname( __file__ ), '..'))
    vcf = os.path.join(thispath,vcf)
    resultdir = os.path.join(thispath,resultdir)

    caseid = (os.path.basename(vcf).split(".")[0])

    #get features from JSON file
    with open(jsonfile,"r") as inputjson:
        jsondata = json.load(inputjson)
    features = jsondata['features']

    #get data from sample anaylsis file
    with open(analysissanmplefile,"r") as samplefile:
        data=yaml.load(samplefile)

    #create result dir if not yet present
    resultdir = os.path.join(resultdir,caseid)
    if not os.path.exists(resultdir):
        os.makedirs(resultdir)

    #fill anaylsis file with features and vcf destination
    data['analysis']['vcf'] = vcf
    data['analysis']['hpoIds'] = features
    data['outputOptions']['outputPrefix'] = resultdir + '/' + caseid

    #dump analysis files
    with open(os.path.join(outputdir,caseid+".yml"),"w") as analysisfile:
        yaml.dump(data,analysisfile)

def getjsonfile(vcf,jsondir):
    caseid = (os.path.basename(vcf).split(".")[0])
    jsonfile = os.path.join(jsondir,caseid+".json")
    if os.path.isfile(jsonfile):
        return jsonfile

def createbatchanalysis(dir):
    '''creates a batchanalysisfile of all files contained in a specific directory'''
    files = ""
    thispath = os.path.normpath(os.path.join(os.path.dirname( __file__ ), '..'))
    for file in os.listdir(dir):
        if(file.endswith('.yml')):
            file = os.path.join(thispath,dir,file)
            files = files + file + "\n"
    batchfile = os.path.join(dir,"batchanalysis.txt")
    with open(batchfile,"w") as batchanalysis:
        batchanalysis.write(files)
    return os.path.join(thispath,batchfile)

def getrank(caseid,jsondir,resultdir):
    '''searches for the rank of a disease gene in the exomizer results'''
    #get disease gene
    with open(os.path.join(jsondir,caseid + ".json")) as jsonfile:
        data = json.load(jsonfile)

    try:
        try:
            diseasegene = data['genomic_entries'][0]['variants']['gene']['gene_id']
        except KeyError:
            diseasegene = data['genomic_entries'][0]['gene']['gene_id']
    except Exception:
        diseasegene = None

    #search for diseas gene in result data
    resultdir = os.path.join(resultdir,caseid)
    resultdata = pandas.read_csv(os.path.join(resultdir,caseid+"_AD.genes.tsv"), sep='\t', header=0)

    rank = resultdata.loc[resultdata['ENTREZ_GENE_ID']==diseasegene]['ENTREZ_GENE_ID']

    if rank.empty:
        return 100
    else:
        return rank.index[0]

def resetdir(dir,backupdir):
    '''Compresses and saves the content of a directory'''
    #compress current content
    thispath = os.path.normpath(os.path.join(os.path.dirname( __file__ ), '..'))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    backupdir = os.path.join(thispath,backupdir)
    shutil.make_archive(os.path.join(backupdir,timestamp), 'zip', base_dir=os.path.join(thispath,dir))
    #delete current content
    for root, dirs, files in os.walk(dir):
        for f in files:
            if not f.endswith(".zip"):
                os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def outputranks(ranks):
    '''prints the percentages of positions given to diesease genes'''
    #plot results
    first = 0
    bestten = 0
    besthundred = 0
    worse = 0
    ranks = [rank for rank in ranks if rank is not None]
    for rank in ranks:
        if rank == 0:
            first = first + 1
        elif rank < 10:
            bestten = bestten + 1
        elif rank < 100:
            besthundred = besthundred +1
        else:
            worse = worse + 1


    print("Rank 1:\t", first/len(ranks), "\n")
    print("Rank 2-10:\t", bestten/len(ranks), "\n")
    print("Rank 11-100:\t", besthundred/len(ranks), "\n")
    print("Rank 100+:\t",worse/len(ranks))

    accuracies = []
    rank_names = []
    for i in range(0,100):
        accuracies.append(sum((1 for rank in ranks if rank <= i))/len(ranks))
        rank_names.append(f'rank {i+1}')
    results_df = pandas.DataFrame(data = {'accuracies':accuracies}, index = rank_names)
    with open("accuracies.csv","w") as output:
        results_df.to_csv(output)
