# -*- coding: utf-8 -*-
"""
Download Open Image training data v5

author: Le Yan
"""

import os
from multiprocessing import Pool

save_dir = '/data1/lyan/ImageAnalysis/20190714/OpenImage/Data/train/'

def download(i):
    fname = 'train_'+i+'.tar.gz'
    os.chdir(save_dir)
    os.system('aws s3 --no-sign-request cp s3://open-images-dataset/tar/'+fname+' ./')
    os.system('tar -xzvf '+fname+' -C ./')
    os.remove(fname)

if __name__ == '__main__':
    p = Pool(4)
    p.map(download, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'])
