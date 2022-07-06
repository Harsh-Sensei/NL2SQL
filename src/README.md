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


## Results
| Model | Accuracy(This) |
| ----------- | ----------- |
| SELECT NUM | 0.9895 |
| SELECT COL | 0.9185 |
| SELECT AGG | 0.9018 |
| WHERE NUM | 0.9812 |
| WHERE COL | 0.9582 |
| WHERE OP |  0.9812 |
| WHERE VAL(Indices) | 0.9311 |
| WHERE VAL(String) | 0.9373 |
| GROUP BY | 0.9707 |
| COUNT(*) | 0.9770 |
| Exact Matching | 0.7766 |

## How to use?
### Training

### Evaluation

### Using pre-trained models

## Released Models

## Limitations

## Future Work


<!-- By Harsh-Sensei -->