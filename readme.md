# NL2SQL Extended
This repo is an extension to [NL2SQL-RULE](https://github.com/guotong1988/NL2SQL-RULE) repo.  
SQL(Structured Query Language) is a necessary and important query language in industrial domain for accessing and fetching required data from a database. However this required a syntax based language, SQL. This process can be made easy if questions in the form of natural language can be converted to SQL using deep learning technique. This repo achieves this using template-based classification approach method using BERT as backbone.

## Background
[NL2SQL-RULE](https://github.com/guotong1988/NL2SQL-RULE) is trained on [WikiSQL](https://github.com/salesforce/WikiSQL), which is a large dataset of simple queries(SELECT col-x FROM table-t WHERE conds-c, and t is not predicted, but given as input). However, such simple queries may not be sufficient to fulfill all the requirements. This repo extends the above work to include multiple SELECT columns and GROUP BY, along with queries having COUNT(*) syntax. The architecture for the added syntax is as follows:
1. SELECT multiple columns: Similar architecture to WHERE column prediction
2. SELECT number: Similar architecture to WHERE number prediction
3. SELECT agg: Similar architecture to WHERE operator prediction but with probability distribution over the 6 possibe aggregation rather than WHERE operators.
4. GROUP BY: Similar architecture to WHERE column prediction
5. COUNT(*): The headers at the input time are appended by a '\*' at the start. The model then predicts SELECT cols from the new set of headers. No changes to aggreagtion prediction is made. 

## Dataset
Since WikiSQL dataset does not have queries of the new syntax, [Spider](https://yale-lily.github.io/spider) dataset(having complex queries in the dataset) is used. However, the dataset has many complex queries, having syntax beyong the required syntax, like LIMIT, ORDER BY, HAVING, etc. Hence the required queries are filtered out and converted into the required form to run [output.py](NL2SQL-Guo/data_and_model/output_entity.py) which would include header and question knowledge the query data. The tables are also required to be extracted from databses provided by Spider. The obtained queries are merged with equal proportions from wikisql to increase the datapoints. Below are some metrics of the dataset used:  
<table>
    <tr>
        <th> - </th>
        <th>Total</th>
        <th>COUNT(*)</th>
        <th>GROUP BY</th>
    </tr>
    <tr>
        <td> Train</td>
        <td>3637</td>
        <td>642</td>
        <td>352</td>
    </tr>
    <tr>
        <td>Dev</td>
        <td>527</td>
        <td> 81</td>
        <td>40</td>
    </tr>
</table>  

For training or evaluating the model read the below instructions:
The merged WikiSQL and Spider datasets and required scripts are available [here](https://drive.google.com/file/d/14mfRe2Jx1_dG19bhWjVu1SiQaF_o3Zfd/view?usp=sharing)

The above dataset must be present in `/src/NL2SQL-Guo/data_and_model`. That is, finally directory must be as follows:
```
data_and_model  
|  
├───easy_spider                                                                                               │    └───knowledge_queries                                                                                    ....                                                                                                                      ├───spider                                                                                                              │   └───database                                                                                                          │       ├───academic                                                                                                      │       ├───activity_1                                                                                                    │       ├───aircraft                                                                                                      │       ├───allergy_1
 ....                                                                                                                                                                                                                                                 ├───spider_groupby                                                                                                      │   └───knowledge_queries                                                                                               └───spider_grpby_orderby 
```


## Results
| Model | Accuracy(w/o ft BERT) | Accuracy(ft BERT)
| ----------- | ----------- | ----- |
| SELECT NUM | 0.9895 | 0.9686 |
| SELECT COL | 0.9185 | 0.8810 |
| SELECT AGG | 0.9018 | 0.8830 |
| WHERE NUM | 0.9812 | 0.9895 |
| WHERE COL | 0.9582 | 0.9728 |
| WHERE OP |  0.9812 | 0.9874 |
| WHERE VAL(Indices) | 0.9311 | 0.9185 |
| WHERE VAL(String) | 0.9373 | 0.9436 |
| GROUP BY | **0.9707** | 0.9645 |
| COUNT(*) (header method)| 0.9770 | 0.9665 |
| COUNT(*) (pool method)| 0.8789 | **0.9832** |
| Exact Matching | 0.7766 | **0.7807** |

Notice the major difference in `COUNT(*) (pool method)` after fine tuning BERT. 


## How to use?
### Training 
Clone the repo and choose the required branch. `master` branch includes only the following extensions: 
1. SELECT multiple columns(that is, SELECT number, SELECT cols, SELECT agg)
2. COUNT(*)  

On the other hand, `groupby` branch also inlcudes GROUP BY syntax.  

**If you have a good GPU or want to just evaluate the model then `gpu` branch is the recommended one**

The [train.py](NL2SQL-Guo/train.py) script already has default parameters set to train the entire model along with fine tuning of BERT. The parameters can be provided in case the default behaviour is not required. Th dataset needs to be in proper format for training purposes, the query data as well as table data.  
 Training by default also requires pre-trained models(bert as well as non-bert model), and instructions for downloading them can be found [here](NL2SQL-Guo/README.md)  
Also by default, BERT is not fine-tuned while training, and the required arguments(defined in `train.py`) need to be changed for modifications from default behaviour.
## Released Models
The models are trained on single NVIDIA GeForce RTX 6000 GPU(~24 GB), training for 50 epochs lasted for ~2hrs. Below are some of the pre-trained models:
| Model Name | Link |
| ---------- | ---- |
| spider_multsel_cntstar_grpby_best.pt | [Link](https://drive.google.com/file/d/1VBdcTImJTYwDvHCB8aMckgCEYtLJ80mN/view?usp=sharing) |
| (non)bert_multsel_cntstar_grpby_bS16_lr0.00002.pt | [Link](https://drive.google.com/drive/folders/1_ep8leWhJ_mpbHuh-D2Gu7OeOv3VKBjh?usp=sharing) |

For using the above models, store the models in `saved_models`  directory at the same level as `train.py`. So the directory structure would look as follows:
```
train.py
|
saved_models
    |- bert_multsel_cntstar_grpby_bS16_lr0.00002.pt 
    |- nonbert_multsel_cntstar_grpby_bS16_lr0.00002.pt
```

## Limitations
1. MAX number of SELECT col = 4
2. Execution-guided decoding not implemented
3. Execution accuracy is not yet calculated. It requires merging Spider and WikiSQL databases

## Future Work
1. Including more syntax in the present work, like LIMIT, HAVING, ORDER BY, etc.
2. Implementing execution guided decooding
3. Finding execution accuracy of the present model

<!-- By Harsh-Sensei -->