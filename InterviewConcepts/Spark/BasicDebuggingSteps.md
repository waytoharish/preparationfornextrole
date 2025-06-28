

# 🔍 1. Data Skew
What: Some partitions contain a lot more data than others.

Symptom: Most tasks finish quickly; a few run forever or are stuck.

Check: Use Spark UI → Stages → Look for one or two tasks running longer than the rest.

```json
Fix:

1. Use salting or repartition.

2. Use skew hints if supported (in SQL).

3. Avoid joins on highly skewed keys.
```

# 🔧 2. Executor/Cluster Resource Contention
What: Not enough memory, CPU, or IO bandwidth.

Symptom: Executors slow or die; GC overhead >90%.

**Check: Spark UI → Executors tab → Look for:**

1. High task failure

2. GC time

3. Idle executors

**Fix:**

1. Increase executor memory or cores

2. Use persist() carefully to avoid OOM

3. Scale up or scale out your cluster


# 🗂️ 3. Large Input File / Slow Source
What: File is larger than expected or source (S3, HDFS) is slow.

Symptom: Long time in stage 0 (reading stage).

Check: Input file size / network throughput / API latency.

**Fix:**

1. Optimize input file size (avoid 1 huge file).

2. Use partitioned read (like .option("recursiveFileLookup", "true")).

3. For streaming: check event lag and trigger interval.

# 🚧 4. Job Hanging Due to Deadlocks / Infinite Loops
What: Your UDF or transformation contains an infinite loop or external call that hangs.

Symptom: Stage gets submitted but never finishes.

**Fix:**

1. Check any UDFs or external API calls in your transformations.

2. Use logs and add timeouts.

# 📉 5. Driver Bottleneck
What: Driver is overwhelmed (e.g., collecting large datasets).

Symptom: Using .collect(), .show(), or .toPandas() on large data.

**Fix:**

1. Avoid collect() on large datasets.

2. Use take(n) or save data to disk.

# 📈 6. Output Write Bottlenecks
What: Writing to slow destination (e.g., S3, HDFS, DB).

Symptom: Job hangs at last stage (write).

**Fix:**

1. Check write mode, retry policy, and destination health.

2. Use partitioned writes or reduce output file size.


# 🔁 7. Shuffling Issues
What: Heavy shuffles due to wide transformations (groupBy, join, etc.).

Symptom: Disk spilling or hanging tasks during shuffle stages.

Check: Spark UI → Look at shuffle read/write sizes.

**Fix:**

Tune shuffle partitions:

```python

spark.conf.set("spark.sql.shuffle.partitions", "200")

✅ What is spark.sql.shuffle.partitions?
This setting controls how many partitions are created after a shuffle.

Default: 200 (in Spark 3.x)

More partitions → more parallelism

Too many partitions → overhead (task scheduling, small files)

Too few partitions → not enough parallelism, long tasks, data skew

```
Avoid unnecessary wide transformations.


| Condition                      | Why to Increase                                           |
|-------------------------------|-----------------------------------------------------------|
| Large dataset (e.g. >10 GB)   | More data needs more parallelism                          |
| Shuffle stage taking long     | Tasks might be processing too much data individually      |
| Shuffle files very large      | Each partition's file is too big to handle efficiently    |
| Task duration highly uneven   | Data skew — some tasks take 10x longer than others        |



| Total Data Size After Shuffle | Recommended Shuffle Partitions |
|-------------------------------|-------------------------------|
| ~1 GB                         | 100–200                       |
| ~10 GB                        | 200–500                       |
| ~100 GB                       | 500–2000                      |
| ~1 TB                         | 2000–5000                     |
