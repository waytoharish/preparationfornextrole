🔍 What does “Stage retry due to task crash” mean?
This error generally shows up in Spark logs like:

WARN TaskSetManager: Lost task 0.0 in stage 3.0 (TID 45, executor 1, host): java.lang.Exception: Task failed due to ...
INFO TaskSetManager: Starting task 0.1 in stage 3.0 (TID 46, executor 1, host) as a retry

🧠 Spark Architecture Recap
Component Role
Driver Creates jobs/stages/tasks, manages retries
Executor Runs the actual tasks (functions) on partitions

Each Stage is made up of Tasks, one per data partition. If any one task fails, Spark retries it by default (usually up
to 4 times).

🔥 Common Reasons for Task Crash (Stage Retry)
Root Cause | What happens? | Can it be simulated locally?
Out of Memory (OOM)    | Task uses too much memory |✅ Yes
Divide by Zero / Data Bug |Bad input causes exception |✅ Yes
UDF Exception |UDF fails silently or with error |✅ Yes
Corrupted Data |Task fails reading a file |✅ Yes
Executor Failure |Machine/network failure |❌ Not locally, but can be simulated in a cluster

🔥 SCENARIO1 : Task Crashes Due to OOM
Aspect | Detail
Root Cause | A task processes a partition too large to fit in memory (e.g., large array, join, collect)
What Happens |JVM throws java.lang.OutOfMemoryError, or PySpark throws MemoryError
Simulatable |Locally? ✅ Yes — we’ll create a case below
