# Parallelism
Paralleism refers to how many tasks ( or threads) spark uses to process your data in parallel. I can be controlled in varour ways 

## 1. Default Parallelism ( Cluster level)
```python
spark . SparakSession.builder\
        .appName("MyApp")\
        .config("spark.default.parallelism","8")\
        .getOrCreate()
```

## 2. Read Parallleism ( Input Partitioning)
When reading the data , controlling the number of partitions
```python
df = spark.read\
        .option("delimiter","\t")\
        .csv("path/to/file",schema = schema)\
        .repartition(10)
```

## 3. Repartitioning/Colescing 
Increase paralleism
```python
df = df.repartition(8) # More taks
```

Decrease parallism
```python
df = df.coalesce(8) # Less taks
```

4. Parallelism in spark submit
'''bash
spark-submit \
        --master local [4] \ #4 cores
        --conf spark.defeault.paralleism=8\
           your_script.py

# Summary 
| Level        | Config/Method                | Purpose                             |
|--------------|------------------------------|-------------------------------------|
| Cluster      | `spark.default.parallelism`  | Controls task count for RDD ops     |
| File Reading | `.repartition(n)`            | Controls input parallelism          |
| Execution    | `--master local[n]`          | Sets number of threads/cores        |
| Optimizing   | `.repartition()`, `.coalesce()` | Manually adjust partition count     |

