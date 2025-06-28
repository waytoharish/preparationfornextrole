# Parallelism
Paralleism refers to how many tasks ( or threads) spark uses to process your data in parallel. I can be controlled in varour ways 

## 1. Default Parallelism ( Cluster level)
```python
spark . SparakSession.builder\
        .appName("MyApp")\
        .config("spark.default.parallelism","8")\
        .getOrCreate()
```
