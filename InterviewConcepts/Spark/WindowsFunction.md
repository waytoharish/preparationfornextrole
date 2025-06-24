**📘 PySpark Window Functions — A Practical Learning Guide
🚪 What Is a Window Function?**
A window function performs a calculation across a set of table rows that are somehow related to the current row — without collapsing the result into a single row like groupBy() does.

Think of it as “grouping without reducing.”

🧰 1. Components of a Window Function
To use window functions in PySpark, you define a window specification using the Window class, which has three optional parts:

| Part                 | Description                         
|----------------------|----------------------------------|
| partitionBy()          | Like GROUP BY (divides rows into groups)| 
| orderBy()             | Orders rows within each partition        | 
| rowsBetween()        | Defines frame relative to current row     | 
| rangeBetween()       | Defines frame relative to current row     | 



🧪 2. Common Window Functions
From pyspark.sql.functions:

Function	Description
row_number()	Assigns a unique row number
rank()	Assigns rank (with gaps for ties)
dense_rank()	Like rank(), but no gaps
lag() / lead()	Access previous/next row’s value
sum() / avg() / count()	Rolling aggregates
first() / last()	First or last value in partition

🔧 3. Simple Example — Ranking Customers by Purchase
```python

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("region").orderBy("purchase_amount")

df.withColumn("rank_in_region", row_number().over(window_spec))
Partitioned by region

Ordered by purchase_amount
```
Assigns a rank per region

📦 4. Example — Rolling 7-Day Total

```python

from pyspark.sql.window import Window
from pyspark.sql.functions import sum

window_spec = Window.orderBy("date").rangeBetween(-7, 0)

df.withColumn("7_day_total", sum("sales").over(window_spec))
For each row, looks at values from 7 days before to the current row
```
Computes a rolling sum

⏳ 5. Difference Between rowsBetween and rangeBetween
| Function      | Works On       | Use Case                     |
|---------------|----------------|------------------------------|
| `rowsBetween` | Row position   | E.g., previous 2 rows        |
| `rangeBetween`| Row values     | E.g., last 7 days (time range) |


🛠 6. Practical Use Cases
Use Case	Window Function Used
Rank customers by spending	rank() or dense_rank()
Running total or average	sum() / avg()
Compare current to previous row	lag()
Detect first/last event in a group	first() / last()
Rolling time-based windows	rangeBetween()

🔑 Best Practices
Always use orderBy() with window functions — even if you don’t partition.

Use .alias() to name your computed columns.

Use .partitionBy() for grouping logic that persists across multiple rows.

📘 Resources to Practice
Dataset ideas: transactions, logs, purchases, events

Functions to try: row_number(), lag(), sum(), dense_rank()

Try real-world challenges: customer retention, top-N per group, session tracking
