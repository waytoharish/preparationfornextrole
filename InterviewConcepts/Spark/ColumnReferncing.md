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
