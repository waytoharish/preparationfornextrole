# YARN coponents 

1. Resource Mananger
2. Node Manager
3. Application Manager

[ EC2 Worker Node ]
     |
     ├─ NodeManager (daemon)
     |
     ├─ Container 1 → Spark Executor JVM
     ├─ Container 2 → Spark Executor JVM
     ├─ Container 3 → ApplicationMaster (with driver, if cluster mode)
     └─ Container 4 → Spark Executor JVM

## Application Manager and Node Manager 

  +-----------------------------+
                    |     ResourceManager (RM)    |
                    |     (Global scheduler)      |
                    +-----------------------------+
                             ↑        ↑
                             |        |
         +------------------+        +------------------+
         |                                         |
+--------------------+                  +--------------------+
| NodeManager (Node 1)| <--- executor   | NodeManager (Node 2)| <--- AM
+--------------------+                  +--------------------+
         ↑                                         ↑
         |                                         |
  Starts and monitors                       Starts and monitors
  executor containers                       AM container

# Spark Components
1. driver
2. executor

# EMR Compoenents
1. Master Node
2. Core Node
3. Task Node


## ✅ Summary: Corrected Flow

1. You run spark-submit --master yarn --deploy-mode cluster
2. Spark contacts YARN ResourceManager
3. RM tells a NodeManager to launch a YARN container for ApplicationMaster
4. ApplicationMaster (AM) starts, Spark Driver runs inside it
5. AM negotiates with RM for executor containers
6. RM chooses NodeManagers to run those containers
7. Each NodeManager:
   a. Launches executor containers
   b. Monitors them
   c. Reports back to RM
   d. Driver coordinates the job using those executors


