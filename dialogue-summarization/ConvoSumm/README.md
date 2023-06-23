# ConvoSumm
Data, code, and model checkpoints for the ACL 2021 paper [ConvoSumm: Conversation Summarization Benchmark and Improved Abstractive Summarization with Argument Mining](https://arxiv.org/pdf/2106.00829.pdf)!
</br>

## Data
The data can be accessed from this [Google Drive link](https://drive.google.com/drive/folders/1HfyCMa1fQ5DkzME9RQZkytZQfyDjE1EK?usp=sharing). </br>

The `data-non-processed` contains the original, non-processed data and is 27MB, while `data-processed` contains the data for vanilla, **-arg-filtered**, and **-arg-graph** experiments, as well as model outputs, and is 611 MB. </br>

Using the [gdrive cli](https://github.com/prasmussen/gdrive), download the folders with the following command </br>
```
gdrive download --recursive 1HfyCMa1fQ5DkzME9RQZkytZQfyDjE1EK
```

The data can also be downloaded from this [S3 bucket](https://s3.console.aws.amazon.com/s3/buckets/convosumm). </br>
```
aws s3 cp --recursive s3://convosumm/data/ ./data
```


## Code and Model Checkpoints
Please see this [README](https://github.com/Yale-LILY/ConvoSumm/blob/master/code/README.md) for code details. </br>

Model checkpoints can be downloaded from the S3 bucket (~80GB): </br> 
```
aws s3 cp --recursive s3://convosumm/checkpoints/ ./checkpoints
```

