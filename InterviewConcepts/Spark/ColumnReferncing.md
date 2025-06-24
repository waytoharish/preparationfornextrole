### 🔁 Column Referencing in PySpark

| Method               | Example                          | Best For                          |
|----------------------|----------------------------------|-----------------------------------|
| `df["col"]`          | `df["value"]`                    | Simple access, expressions        |
| `df.col`             | `df.value`                       | Clean syntax (no special chars)   |
| `col("col")`         | `col("value")`                   | Flexible, function-friendly       |
| `selectExpr()`       | `df.selectExpr("col + 1")`       | SQL-like transformations          |
| `expr()`             | `expr("col IS NULL")`            | SQL expressions in code           |
| `alias()`            | `df["value"].alias("val")`       | Renaming columns                  |
| Nested access        | `col("nested.field")`            | Struct/nested column access       |


In PySpark, there are several ways to refer to columns when working with DataFrames. Here’s a comprehensive list with examples and best practices.

✅ 1. Using String Indexing (df["col"])
python
Copy
Edit
df["value"]
Common and intuitive.

Can be chained: df["value"].isNull()

✅ Good for: Simple expressions and column access.

✅ 2. Using Dot Notation (df.col)
python
Copy
Edit
df.value
Similar to accessing attributes.

More concise.

⚠️ Limitations:

Doesn't work if column names have spaces, dots (.), or special characters.

✅ 3. Using col() Function
python
Copy
Edit
from pyspark.sql.functions import col

col("value")
The most flexible and powerful.

Use in expressions like:

python
Copy
Edit
df.select(col("value").alias("new_value"))
✅ Best for: Complex expressions, chaining, and when passing columns to functions.

✅ 4. Using df.selectExpr() with SQL expressions
python
Copy
Edit
df.selectExpr("value as new_value", "id + 1 as id_plus_one")
Write SQL-style expressions as strings.

✅ Best for: Quick transformations with SQL-like syntax.

✅ 5. Using df["col"].alias("new_name")
python
Copy
Edit
df.select(df["value"].alias("new_value"))
Assign a new name (alias) to a column.

Works like SQL’s AS.

✅ 6. Using F.expr() for complex SQL expressions
python
Copy
Edit
from pyspark.sql.functions import expr

df.select(expr("value IS NULL").alias("is_null"))
✅ Best for: Evaluating SQL expressions in PySpark code.

✅ 7. Accessing Nested Columns
If you have a struct or nested schema:

python
Copy
Edit
df.select("address.city")
# OR
col("address.city")
If dot notation fails (e.g., with spaces or special chars):

python
Copy
Edit
df.select(col("`address.city`"))
