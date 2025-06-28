# 🔁 Recovery Strategies in Spark When File Processing Fails Before Final Stage

If your **file processing job fails just before the last stage** (e.g., during final transformation or write), here's how you can avoid re-processing everything from scratch:

---

## ✅ 1. Enable Checkpointing (Resilience)

checkpoint saves your progress in a stable spot, so you can keep going without retracing every step. 

Use Spark’s **checkpointing** to save intermediate DataFrames to reliable storage like HDFS or S3:

```python
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")
df.checkpoint()
```

## ✅ 2. Persist/Cache Intermediate Steps
If you are doing expensive transformations , cahce the result 

```python 
df.cache()
```
Or:

```python
from pysparl import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)
```

## ✅ 3. Retrial mechanism in orchestration tool 
```bash

from airflow.operators.bash import BashOperator
from datetime import timedelta

t1 = BashOpertor(
    task_id = 'load_to_hdfs',
    retries = 3
    retry_delay = timedelta(minute =5)
    bash_command = 'spark-submit my_job.py'
)

