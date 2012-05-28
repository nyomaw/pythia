'''
Created on 21 Mar 2012

@author: george
'''
import pylab#!@UnresolvedImport 
import numpy 

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from analysis.clustering.nmf import NMFClusterer
from evaluation.evaluators import ExtrinsicClusteringEvaluator
from analysis.clustering.algorithms import euclidean 
from analysis.dataset_analysis import DatasetAnalyser

def run_evaluation():
    ws = WarehouseServer()
    documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
    clusterers = [OrangeKmeansClusterer(k=39, ngram=1), 
                  DBSCANClusterer(epsilon=0.02, min_pts=3, distance=euclidean), 
                  NMFClusterer(rank=39, max_iter=65, display_N_tokens = 5, display_N_documents = 10)] 
    
    dataset_size = len(documents)
    da = DatasetAnalyser(documents)
    print da.avg_document_length()
    print da.vocabulary_size()
    print da.avg_vocabulary_size()
    print da.dataset_size()
    
    f_measures = []
    step = 5
    initial_document_size = 50
    for clusterer in clusterers:
        oc = clusterer
        f_list = []
        i=initial_document_size
        while (i < dataset_size): 
            ebe = ExtrinsicClusteringEvaluator(documents[:i])
            bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
            print bcubed_precision, bcubed_recall, bcubed_f
            f_list.append(bcubed_f)
            i += step
        f_measures.append(f_list)
               
    t = numpy.arange(initial_document_size, dataset_size, step)
    plots = []
    for measures_list in f_measures:
        plots.append(pylab.plot(t, measures_list))
    
    pylab.xlabel('Number of documents')
    pylab.ylabel('Bcubed F metric')
    pylab.legend(('kmeans', 'dbscan', 'nmf'), 'lower right', shadow=True)
    pylab.show()
    
import cProfile    
cProfile.run('run_evaluation()', 'different_data_sizes.profile')
