# Basic Config structure 
```sql
Host [pattern]
  Option1 value1
  Option2 value2
```

## Actual backend workflow in ssh 
```sql

**1. Regular SSH (like GitLab):**

    
Host gitlab.com
  HostName gitlab.com
  User git
  IdentityFile ~/.ssh/id_rsa

    

   
**Flow:**

    
graph LR
    A[Your Machine] -->|Direct SSH Connection| B[GitLab Server]



**2. AWS SSM Connection:**

    
Host i-* mi-*
    ProxyCommand sh -c "aws ssm start-session --target %h ..."

    

    
**Flow:**

    
graph LR
    A[Your Machine] -->|AWS SSM Service| B[AWS Systems Manager]
    B -->|Internal AWS Network| C[EC2 Instance]
```

### Proxy command breakdonw
```sql
aws ssm start-session \
    --target %h \                 # EC2 instance ID (i-xxx or mi-xxx)
    --document-name AWS-StartSSHSession \  # AWS SSM protocol
    --parameters 'portNumber=%p' \ # SSH port
    --profile AWSAdministratorAccess-718141767151 \ # AWS credentials
    --region us-east-1            # AWS region

```    

### Common Keywords:
```sql 
HostName      # Real hostname to connect to
User          # Username to log in as
IdentityFile  # Path to private key
Port          # SSH port number
ProxyCommand  # Command for custom connection method

Other Valid Keywords: 

AddKeysToAgent
AddressFamily
BatchMode
BindAddress
CanonicalDomains
CertificateFile
Compression
ConnectTimeout
ForwardAgent
LocalForward
ProxyJump
StrictHostKeyChecking
```

### Common usage in ssh config 

```sql
Dafault paths: 
Mac path ---> ~/.ssh/config
Windows path ---> c:\users\<username>\.ssh\config

Host example.com
  HostName example.com      # Actual hostname to connect to
  User myusername          # Username to log in with
  Port 22                  # SSH port (22 is default)
  IdentityFile ~/.ssh/key  # Path to private key
```

### Wildcards in host patterns
```sql
Host *                     # Matches all hosts
Host *.example.com        # Matches any subdomain
Host i-*                  # Matches EC2 instances (your case)

```
### Explanation of ssh ssm commands 
```sql 
Command: 
**host i-* mi-*
ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p' --profile AWSAdministratorAccess-718141767151 --region us-east-1"
**
When you run an SSH command like:

**ssh i-1234567890abc -p 22**

The values are automatically populated:

%h gets replaced with i-1234567890abc (the hostname you provided)
%p gets replaced with 22 (the port number, default is 22 if not specified)


**Here's how it works:**

    
# When you run
**ssh i-1234567890abc**

# The config expands to
aws ssm start-session \
    --target i-1234567890abc \  # %h is replaced with actual instance ID
    --parameters 'portNumber=22' # %p is replaced with port number
    ...


```

### Different scenarios for getting port values 
```sql
# Scenario 1: Default (no port specified)
ssh i-1234567890abc
# %p becomes 22 automatically

# Scenario 2: Explicit port
ssh -p 8022 i-1234567890abc
# %p becomes 8022

# Scenario 3: Port in config file
Host myserver
  Port 2222
  ProxyCommand ... 'portNumber=%p' ...
# %p becomes 2222

```
### ssh config content
```sql
# GitLab
Host gitlab.aws.dev
  HostName gitlab.aws.dev
  User git
  IdentityFile ~/.ssh/id_rsa

# GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa

Host ssh.gitlab.aws.dev
    User git
    IdentityFile ~/.ssh/id_rsa
    CertificateFile ~/.ssh/id_rsa-cert.pub
    IdentitiesOnly yes
    ProxyCommand none
    ProxyJump none
# SSH over Session Manager
host i-* mi-*
    ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p' --profile AWSAdministratorAccess-718141767151 --region us-east-1"

```


### Known Hosts Entries File (~/.ssh/known_hosts):

1. These are SERVER identities
2. Collected when you connect to servers
3. Created automatically when you first connect to a server
4. Compare the format of known host and public key geenrated

```sql
# Public Key (id_rsa.pub)
ssh-rsa [KEY] [EMAIL/COMMENT]

# Known Hosts Entry
[HOSTNAME] ssh-rsa [KEY]

```

### Your Public Key (typically in id_rsa.pub):

1. This is generated with commands liek --> ssh-keygen -t ed25519 -C "your_email@example.com"
2. This is YOUR identity
3. You share this with servers/services
4. Created by you using ssh-keygen
5. Typically it contains content like below:
   
```sql
ssh-rsa AAAAB3NzaC1... your.email@example.com
```

### Key differences:

```sql
Purpose:

Public key: Proves YOUR identity
Known hosts: Proves SERVER identity
Creation:

Public key: You create with ssh-keygen
Known hosts: Automatically collected during connections
Usage:

Public key: Upload to servers
Known hosts: Local verification of servers
```

### SSH connection with EMR


```bash
Commnad:
ssh -i   /Users/ymanan/Downloads/flinketlemr.pem hadoop@i-0ee2b597e4d29f644

Explanation:

ssh -i /Users/******/Downloads/flinketlemr.pem hadoop@i-0ee2b597e4d29f644
│   │           │                                  │     │
│   │           │                                  │     └── EC2 instance ID ( hostname)
│   │           │                                  └── Username(user) (hadoop for EMR)
│   │           └── Path to the .pem file
│   └── -i flag (specify identity file/private key)( Identity file)
└── SSH command


Same thing configured in the

Host emr-master
    HostName i-0ee2b597e4d29f644
    User hadoop
    IdentityFile /Users/******/Downloads/flinketlemr.pem
    Port 22  # optional as it's default

**If above config is configured, ssh commnad can be replaced as below :**
ssh emr-master

graph LR
    A[Your Machine] -->|First Connection| B[EMR Master Node]
    B -->|Sends Public Key| A
    A -->|Stores Key in known_hosts| C[known_hosts file]
```

### Probable issue and Solution with EMR 

##### 1. Try to connect
$ ssh -i key.pem hadoop@i-1234567890
> ERROR: REMOTE HOST IDENTIFICATION HAS CHANGED!
> Host key verification failed.

##### 2. Manual removal required
$ ssh-keygen -R i-1234567890

##### 3. Try connecting again
$ ssh -i key.pem hadoop@i-1234567890
> The authenticity of host 'i-1234567890' can't be established.
> Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

##### 4. New key automatically stored after you type 'yes'

# MWINIT setup 

![image](https://github.com/user-attachments/assets/188b5a04-7670-4cd0-bfbf-36bddb148036)

```bash
manan@88665a537eba cdk-dynamo-project % mwinit 
Welcome, ymanan

=======================================================================
If your security key's "On-Token PIN" status is "Enforced" in
https://register.midway-auth.amazon.com, you must use the "-f" or "--fido2"
option to authenticate with the key's on-token PIN.

We encourage using the "-f" or "--fido2" option for all users. The "-f"
option will become the default behavior in a future version.

For more information, please visit
https://w.amazon.com/bin/view/AWS_IT_Security/Helios/On-TokenPIN
=======================================================================

Please enter your Midway PIN: 
Please follow the instructions below to authenticate with your security key.

Security key to be used: Yubico Yubikey 4 OTP+U2F (FIDO1)
Touch the security key...
Successfully authenticated using WebAuthN, session cookie saved in /Users/ymanan/.midway/cookie
Successfully signed SSH public key "/Users/ymanan/.ssh/id_rsa.pub". The SSH certificate was saved in "/Users/ymanan/.ssh/id_rsa-cert.pub".
Successfully saved session token to MCS Keys Process


Explanation of what happened:

graph TD
    A[mwinit command] -->|Initiates| B[AWS Midway Authentication]
    B -->|Requires| C[Two-Factor Authentication]
    C -->|1. PIN Entry| D[Knowledge Factor]
    C -->|2. YubiKey Touch| E[Physical Factor]
    E -->|Success| F[Creates Certificates]
    F -->|1| G[Midway Session Cookie]
    F -->|2| H[SSH Certificate]
    F -->|3| I[MCS Token]


graph TD
    A[mwinit command] -->|Authenticates| B[AWS IAM Identity Center]
    B -->|Registers SSH key| C[AWS SSO Service]
    C -->|Creates Certificate| D[Signs your SSH key]
    D -->|Stores| E[Creates id_ecdsa-cert.pub]

This process:

Verifies your identity (2FA)
Creates temporary credentials
Sets up SSH access to AWS services
Establishes a trusted session
```


# Basics of Setting up SSH key and connecting from local to gitlab/github
# Gitlab SSH Key setup

**1. ✅ Step 1: Open Git Bash (or any terminal that supports SSH)**
If you don't have Git Bash installed, download it here:
👉 https://git-scm.com/downloads

After installing, right-click on your desktop or open Start Menu → Search “Git Bash” → Open it.

**2. ✅ Step 2: Generate SSH Key**
In Git Bash, run this command (replace your email):

```bash

ssh-keygen -t ed25519 -C "your_email@example.com"
If you get an error about ed25519 being unsupported, use this instead:

ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
You will see prompts:

Enter file in which to save the key (/c/Users/yourname/.ssh/id_ed25519):
👉 Press Enter to accept the default path.

Enter passphrase (empty for no passphrase):
👉 Optional: Type a passphrase, or press Enter twice to leave it empty.

You’ll get confirmation like:

Your identification has been saved in /c/Users/YourName/.ssh/id_ed25519
Your public key has been saved in /c/Users/YourName/.ssh/id_ed25519.pub
```

**3. ✅ Step 3: Start the SSH Agent**
Still in Git Bash, run:

```bash

eval "$(ssh-agent -s)"
Start the agent if not already running:


ssh-add ~/.ssh/id_ed25519
(Or use id_rsa if you chose RSA)
```

**4.  ✅ Step 4: Copy the Public Key to Clipboard**
Run this command to copy:

```bash

clip < ~/.ssh/id_ed25519.pub
```
Now your public SSH key is in your clipboard.

**5. ✅ Step 5: Add SSH Key to GitLab**
Go to GitLab: https://gitlab.com/

Sign in to your account.

In the top-right corner, click your profile picture → Edit profile.

On the left sidebar, go to SSH Keys.

Paste the key into the "Key" field.

Add a Title like “Windows Laptop SSH” and optionally set an expiration date.

Click Add key.

**6. ✅ Step 6: Test the SSH Connection**
In Git Bash, run:

bash
Copy
Edit
ssh -T git@gitlab.com
Expected output:

bash
Copy
Edit
Welcome to GitLab, @yourusername!
✅ Bonus: Set Git to Use SSH for GitLab
Make sure your Git remote uses the SSH URL. To check:

bash
Copy
Edit
git remote -v
If it shows https://, change it to SSH:

bash
Copy
Edit
git remote set-url origin git@gitlab.com:username/repository.git

# Explanation of gitlab to local Connection

1. 🔑 1. You Generated SSH Keys
When you ran ssh-keygen, two files were created:

File	Type	Purpose
id_ed25519 (or id_rsa)	Private	Stays on your local machine. Used to prove your identity.
id_ed25519.pub	Public	Shared with servers (like GitLab) so they can recognize you.

These two form a key pair used in public-key cryptography.

🔁 2. You Copied the Public Key to GitLab
When you paste the public key in GitLab:

GitLab stores it and links it to your user account.

Whenever a connection attempt is made, GitLab can challenge the connecting client to prove they hold the matching private key.

This is how SSH authentication works:

GitLab → sends a random challenge to your machine.

Your SSH client signs it using your private key.

GitLab verifies it using the public key you uploaded.

If it matches → you're authenticated.

🔐 GitLab never sees your private key. It only knows your public key.

👤 3. You Started the SSH Agent
The SSH Agent is a background process that holds your private keys in memory.

Why?

So you don't have to re-enter the passphrase every time you use SSH.

It supplies your key automatically when an SSH connection is made (e.g., for git clone, git push).

When you run:

bash
Copy
Edit
ssh-add ~/.ssh/id_ed25519
You're loading your private key into the agent. It will now respond to GitLab’s authentication challenge automatically.

🔌 4. GitLab Connection Flow (Simplified)
Here’s what happens when you run git clone git@gitlab.com:username/repo.git:

Git tries to connect to git@gitlab.com over SSH.

GitLab receives the connection request and checks:

Is there an SSH key on file for this user?

GitLab sends a challenge.

Your SSH agent signs it using your private key.

GitLab verifies the signature using the public key you uploaded.

✅ Access granted if the keys match.

No password is exchanged — it's all key-based.

🛑 5. Do You Need to Stop the SSH Agent?
Short answer: No, you don't have to stop it.
The agent is lightweight and doesn’t constantly run unless needed.

On Windows, it's managed by the OS as a background service.

If you're concerned about security or just not using Git/SSH, you can stop it manually:

powershell
Copy
Edit
Stop-Service ssh-agent


