🔍 Summary: What is eqNullSafe?
In Spark, df["col"].eqNullSafe(value) (or col <=> value in SQL) compares two values for equality, treating NULL = NULL
as true. This differs from standard SQL equality (=), where NULL = NULL is always false or unknown.

✅ How does eqNullSafe work in a join?
Let’s look at your two DataFrames:

df1
sql
Copy
Edit
+---+-----+
| id|value|
+---+-----+
| 1| foo|
| 2| null|
+---+-----+
df2
sql
Copy
Edit
+-----+
|value|
+-----+
| bar|
| null|
+-----+
Join using eqNullSafe:
python
Copy
Edit
df3 = df1.join(df2, df1["value"].eqNullSafe(df2["value"]))
Join logic:

'foo' <=> 'bar' = false

'foo' <=> null = false

null <=> 'bar' = false

null <=> null = true

So the only row that will match is where both value columns are null.

Output of df3:
sql
Copy
Edit
+---+-----+-----+
| id|value|value|
+---+-----+-----+
| 2| null| null|
+---+-----+-----+
Only one row matches!

🤯 What if you use regular equality (=) instead?
python
Copy
Edit
df4 = df1.join(df2, df1["value"] == df2["value"])
In this case:

'foo' == 'bar' = false

'foo' == null = null (excluded)

null == 'bar' = null (excluded)

null == null = null (excluded)

So nothing matches → output will be empty.

🔍 So does eqNullSafe “replace NULL with false”?
Not exactly.

Here’s how eqNullSafe works:

If both sides are NULL, it returns true.

If one side is NULL and the other isn't, it returns false.

If both are non-null: behaves like regular ==.

So:

It doesn’t "replace" NULL with false, but it defines how NULLs behave in comparisons—giving you true when both sides are
null (unlike regular SQL).

✅ When to use eqNullSafe?
Use it when you:

Want to match null values in joins or filters.

Need to avoid excluding rows just because they contain nulls in join keys.

Let me know if you want a visual truth table or performance tips when using eqNullSafe.
