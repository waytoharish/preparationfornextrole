Single task is per partition

🧮 Step 1: Estimate Data Size per Partition
If your input dataset is, say, 200 GB, and you partition it into 200 partitions, then:

```sql
200 GB / 200 = ~1 GB per partition (per task)
```

If each task processes 1 GB, and your transformation expands the data (e.g., join, explode), you might need 2–4 GB of
RAM per task.

🧮 Step 2: Use Spark Memory Sizing Formula

```java
Total executor memory = executor memory (e.g., 8g)
Usable memory for tasks = 0.6 * executor memory (due to Spark internal usage)

Example:

Executor memory = 8g
Spark reserves ~40% for storage, shuffle, broadcast, overhead
Usable = 0.6 * 8g = ~4.8g
So if each task needs ~1 GB, this executor can safely run 4 tasks in parallel.
```

🧰 Tuning Checklist
What to Tune| Config Example
Executor memory| spark.executor.memory=8g
Number of cores per executor |spark.executor.cores=4
Driver memory (local dev)| spark.driver.memory=4g
Number of partitions |rdd.repartition(200) or via --num-executors
Shuffle spill limit (advanced)    |spark.memory.fraction (default: 0.6)

✅ Summary Table
Scenario Root Cause Local Simulation How to Fix
Task OOM Too much memory in a single task ✅ Yes Use smaller partitions, increase executor memory
Executor OOM Too many parallel tasks ✅ Yes Reduce executor.cores, increase executor.memory
Collect OOM Driver tries to hold all data ✅ Yes Avoid .collect(), use .take() or .write()
