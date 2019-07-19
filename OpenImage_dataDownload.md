download data (OpenImage V5 561GB)

1. awscli

   conda install awscli

2. run python script to download the training data

   ```bash
   nohup python3 DownloadData.py &
   ```

   change the save_dir to the proper directory to save the data

   change the size of the Pooling size of the multiprocessing to fasten downloading

3. run python script to download the labels and segmentations

   ```bash
   nohup python3 DownloadMetaData.py &
   ```

   change the save_dir to the proper directory to save the data

   