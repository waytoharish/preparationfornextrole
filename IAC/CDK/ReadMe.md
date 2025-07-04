# Steps to be followed:

1. Create specific directory and intialize blank cdk project 

```bash
mkdir <directory_name>
cd <directory_name>
cdk init
```
*Result:* It will create all the required cdk files and folders in this library

2. Create virtual env and install all the requirements

3. Update your stack file (e.g., my_dynamodb_project/my_dynamodb_project_stack.py):

4. Update the app.py file in your project root:

5. Project structure should look lke 

```pgsql
my-dynamodb-project/
├── README.md
├── app.py
├── my_dynamodb_project/
│   ├── __init__.py
│   └── my_dynamodb_project_stack.py
├── requirements.txt
├── source.bat
├── cdk.json
└── setup.py

```

6. Bootstrap the project 
```bash
cdk bootstrap aws://211125709716/ap-south-1
```

7. cdk deploy

# Explaination 

1. CDKToolkit Stack
    a. Yes, cdk bootstrap creates a CDKToolkit stack which is required only once per account/region
    b. This stack creates essential resources:
        i. An S3 bucket (to store deployment artifacts)
        ii. IAM roles (for CDK to deploy resources)
        iii. It's like setting up the infrastructure to deploy infrastructure
 ```pgsql   
Account (First time)
└── cdk bootstrap
    └── Creates CDKToolkit Stack
        ├── S3 Bucket
        ├── IAM Roles
        └── Other bootstrap resources
```

2. CDK Deploy Flow

 ```pgsql   
cdk deploy
└── Reads app.py
    └── app.py instantiates your Stack class
        └── Creates CloudFormation template
            └── Deploys to AWS


Example workflow:

    
# 1. app.py is the entry point
app = cdk.App()  # Creates CDK app instance

# 2. Creates stack instance
CdkDynamoProjectStack(app, "CdkDynamoProjectStack")

# 3. Synthesizes CloudFormation template
app.synth()


# Stack naming 
 The string can be different from class name
CdkDynamoProjectStack(app, "MyCustomStackName")  # This is fine
CdkDynamoProjectStack(app, "ProductionStack")    # This is also fine

# This string becomes the CloudFormation stack name in AWS


```

3. App and Stack Relationship
    
### App is a Construct type
app = cdk.App()  # Creates root construct

### Stack inherits from Construct
class CdkDynamoProjectStack(Stack):  # Stack extends Construct
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        # scope is the parent construct (app in this case)

    
### Python Concepts Used
    
def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    

    
Key Python concepts:

Class inheritance (super())
Type hints (scope: Construct)
Variable arguments (**kwargs)
Constructor (__init__)


Here's a visual representation of how it all works together:

 ```pgsql     
Deployment Process
├── app.py (Entry Point)
│   └── Creates App instance
│       └── Creates Stack instance
│           └── Synthesizes CloudFormation
│               └── Deploys to AWS
│
Infrastructure Hierarchy
├── App (Root Construct)
│   └── Stack (Your stack)
│       └── Resources (DynamoDB, etc.)
│
Class Hierarchy
├── Construct (Base class)
│   └── Stack (Inherits from Construct)
│       └── Your Stack (Inherits from Stack)
```  

    
#### Practical Example:

```python    
# app.py
from aws_cdk import App
from my_stack import MyStack

# Create the app instance (root construct)
app = App()

# Create multiple stacks if needed
MyStack(app, "DevStack")
MyStack(app, "ProdStack")

# Synthesize CloudFormation template
app.synth()

# my_stack.py
from aws_cdk import Stack
from constructs import Construct

class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        # Your resources go here
        # Each resource is a construct
        table = dynamodb.Table(
            self,           # scope (the stack)
            'MyTable',      # construct ID
            # ... other parameters
        )

    

    
# When building CDK pipelines, remember:

# Every resource is a Construct
# Constructs form a tree structure
# Each Construct needs:
# Scope (parent Construct)
# ID (unique within scope)
# Properties (configuration)
# This tree structure allows CDK to:

# Track dependencies
# Generate CloudFormation
# Manage resource lifecycle
# Handle permissions and security

```


### Explanation of releation between Stack and App

```pgsql
Question: 
class accepts only 1 input --> CdkDynamoProjectStack(Stack)

But whenever it is called , 3 inputs are provided.
CdkDynamoProjectStack(app, "CdkDynamoProjectStack",)

unable to relate to this



Let me break down the Python class inheritance and constructor concept used here:

    
# Basic Python class inheritance example first
class Parent:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Child(Parent):    # Child inherits from Parent
    def __init__(self, a, b):
        super().__init__(a, b)  # Calls Parent's __init__

    

    
Now, let's look at your CDK code:

    
# What's actually happening in CDK
from aws_cdk import Stack          # This is the Parent class
from constructs import Construct

class CdkDynamoProjectStack(Stack):  # Your class inherits from Stack
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)  # Calls Stack's __init__

    

    
When you write:

    
CdkDynamoProjectStack(app, "CdkDynamoProjectStack")

    

    
Here's the flow:

    
# 1. Parent Stack class definition (simplified)
class Stack:
    def __init__(self, scope: Construct, id: str, **kwargs):
        self.scope = scope
        self.id = id
        # ... other initialization

# 2. Your class inherits from Stack
class CdkDynamoProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        # This line calls the parent (Stack) constructor
        super().__init__(scope, construct_id, **kwargs)
        
        # Here you can add your resources
        table = dynamodb.Table(self, "MyTable",...)

# 3. When you create an instance
app = cdk.App()
CdkDynamoProjectStack(
    app,                        # scope: where to create the stack
    "CdkDynamoProjectStack",    # construct_id: name of the stack
)

    

    
Let's make it even clearer with a simple analogy:

    
# Simple analogy
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

class Car(Vehicle):  # Car inherits from Vehicle
    def __init__(self, brand, model):
        super().__init__(brand, model)  # Calls Vehicle's __init__

# Creating a car
my_car = Car("Toyota", "Camry")  # Passes 2 parameters even though Car(Vehicle)

    

    
In CDK terms:

    
# Your stack is like defining a specific type of vehicle
class CdkDynamoProjectStack(Stack):
    def __init__(self, scope, construct_id):
        super().__init__(scope, construct_id)
        
        # This is like adding features to your vehicle
        table = dynamodb.Table(
            self,           # the stack instance itself
            "MyTable",      # name for this resource
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            )
        )

# Creating the stack is like creating a specific vehicle
app = cdk.App()
my_stack = CdkDynamoProjectStack(
    app,                        # where to create it (like which factory)
    "CdkDynamoProjectStack"     # what to call it (like the VIN number)
)

    

    
Visual representation:

    
Stack (Parent Class)
    │
    │── __init__(scope, id, **kwargs)
    │
    └── CdkDynamoProjectStack (Your Class)
            │
            └── __init__(scope, id, **kwargs)
                    │
                    └── super().__init__(scope, id, **kwargs)
                            │
                            └── Creates stack in AWS

    

    
When you instantiate:

    
CdkDynamoProjectStack(app, "CdkDynamoProjectStack")
│
├── scope: app (where to create the stack)
│
└── construct_id: "CdkDynamoProjectStack" (what to name it)

    

    
The parameters:

scope: The parent construct (usually the app)
construct_id: Unique identifier for this stack
**kwargs: Optional additional parameters
This is a fundamental pattern in CDK where:

Every construct (including Stack) needs a scope and an id
The scope creates parent-child relationships
The id must be unique within that scope

```


# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
