# 🤖 SmartLearn AI LLMOps System

## 💡 Overview
SmartLearn AI LLMOps System is a fully automated CI/CD and MLOps pipeline designed to streamline the deployment of AI-driven learning and quiz-generation applications.  
It integrates **GitHub**, **Jenkins**, **Docker Hub**, **ArgoCD**, **Groq AI**, **LangChain**, and **Kubernetes**, deployed on **AWS EC2 instances** using **NodePort** services.

This project demonstrates a complete AI/ML lifecycle — from **code commit → build → containerization → deployment → production inference** — powered by **Groq AI acceleration** and **LangChain orchestration**.

---

## 🧩 Features
- 🚀 End-to-end CI/CD automation using Jenkins, ArgoCD and Webhooks  
- 🧠 AI-powered quiz generator based on user-provided topics  
- ⚙️ LangChain for orchestrating LLM logic and structured question generation  
- ⚡ Groq AI LPUs for lightning-fast AI inference  
- ☸️ Kubernetes orchestration on AWS EC2 (NodePort)  
- 🐳 Dockerized architecture for portability  
- 🔗 GitHub Webhook integration for instant Jenkins triggers  
- ☁️ ArgoCD GitOps synchronization for automated deployments  
- 📊 Real-time evaluation and results generation inside the app  

---

## 🧠 Project Idea: SmartLearn AI Quiz Generator
The core idea of SmartLearn AI is to provide an **interactive AI-powered quiz generator**.  
Users input a topic, question type, difficulty level, and number of questions, and the app automatically generates a custom quiz using **LLMs through LangChain**.

### 🧩 Supported Question Types
- Multiple Choice  
- True/False  
- Fill in the Blank  
- Short Answer  
- Descriptive  
- Ordering  
- Multi-Select  
- Numerical  

After generating the quiz:
- Users can answer interactively.  
- The system evaluates responses and shows the score and feedback.  
- Results can be saved and downloaded as CSV.  

This AI quiz app is served via **Streamlit**, deployed through an automated CI/CD pipeline built with **Jenkins**, **Docker**, **ArgoCD**, and **Kubernetes**.

---

## 🚀 System Workflow
1. **Code Push to GitHub** → triggers **Webhook** → notifies **Jenkins**  
2. **Jenkins Pipeline** → pulls code, builds Docker image, pushes to Docker Hub  
3. **Docker Hub** → stores versioned images  
4. **ArgoCD** → monitors GitHub manifests and deploys to Kubernetes  
5. **Kubernetes Cluster (AWS EC2)** → runs the app using NodePort for public access  

---

## 🏗️ System Architecture
![System Architecture](System%20Architecture/SmartLearn%20AI%20System%20Architecture.jpg)

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/andrew-adel-labib/SmartLearn-AI-LLMOps-AIOps-Cloud-System-using-Groq-LangChain-Docker-Jenkins-ArgoCD-Minikube-AWS-EC2.git
cd SmartLearn-AI-LLMOps-AIOps-Cloud-System-using-Groq-LangChain-Docker-Jenkins-ArgoCD-Minikube-AWS-EC2
```

### 2️⃣ Launch AWS EC2 Instance
Use **Ubuntu 22.04 (t2.medium or higher)**

- When creating the EC2 instance, open ports:

| **Port**     | **Purpose**                  |
|:-------------:|:----------------------------:|
| 22            | SSH                          |
| 9595          | Jenkins                      |
| 31704         | ArgoCD                       |
| 9090          | SmartLearn App               |
| 30000–32767   | Kubernetes NodePort range    |

---

### 3️⃣ Install Dependencies
```bash
sudo apt update && sudo apt install -y docker.io kubectl minikube
sudo systemctl start docker
sudo systemctl enable docker
minikube start --driver=docker
```

---

## 🐳 Docker Build & Push Commands

| **Action** | **Command** | **Description** |
|-------------|-------------|-----------------|
| 🏗️ Build Image | `docker build -t <dockerhub-user>/smartlearn-ai:latest .` | Builds image using project Dockerfile |
| 🔐 Login | `docker login` | Authenticate with Docker Hub |
| ☁️ Push Image | `docker push <dockerhub-user>/smartlearn-ai:latest` | Upload image to Docker Hub |
| 🧩 Run Locally | `docker run -d -p 8080:8080 <dockerhub-user>/smartlearn-ai:latest` | Run the image locally for testing |

---

## ⚙️ Jenkins Integration (CI)

### 🧩 Run Jenkins as Docker Container on EC2

### 1️⃣ Pull Jenkins image 
```bash
sudo docker pull jenkins/jenkins:lts
```
### 2️⃣ Create persistent volume
```bash
sudo mkdir -p /home/ubuntu/jenkins_home
sudo chown 1000:1000 /home/ubuntu/jenkins_home
```
### 3️⃣ Run Jenkins container named "jenkins"
```bash
sudo docker run -d \
  --name jenkins \
  -p 9595:8080 \
  -p 50000:50000 \
  -v /home/ubuntu/jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

✅ Access Jenkins at:  
👉 `http://<EC2-Public-IP>:9595`

- Create a **Pipeline Job** and connect it to your GitHub repository.

---

### 🔑 Get Admin Password

```bash
sudo docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

👉 Copy this and paste it in the Jenkins setup screen.

---

### 🔗 GitHub Webhook Integration
1. Go to **GitHub → Settings → Webhooks → Add Webhook**
2. Set:
   - Payload URL: `http://<EC2-IP>:9595/github-webhook/`
   - Content type: `application/json`
   - Trigger: “Just the push event”
3. In Jenkins → Configure job → check **“GitHub hook trigger for GITScm polling.”**
4. Push a commit to GitHub — Jenkins should automatically start a new build.

---

### 🧱 Jenkinsfile Example
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<user>/<repo>.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t <dockerhub-user>/smartlearn-ai:latest .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u <dockerhub-user> --password-stdin'
                    sh 'docker push <dockerhub-user>/smartlearn-ai:latest'
                }
            }
        }
    }
}
```

---

## 🚀 ArgoCD Deployment (CD)

### 1️⃣ Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2️⃣ Expose ArgoCD Dashboard via NodePort (Accessible via EC2 Public IP)
```bash
kubectl patch svc argocd-server -n argocd \
  -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 8080, "nodePort": 31704}]}}'
```
Then open:  
👉 `https://<EC2-Public-IP>t:31704`

- Retrieve admin password:
```bash
kubectl get secret -n argocd argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

---

### 3️⃣ Connect Repository
In ArgoCD UI → Settings → Repositories → Connect Repo :
- Set **Sync Policy → Automatic**

### 4️⃣ Apply SmartLearn App Kubernetes Manifests
```bash
kubectl apply -f manifest/deployment.yml
kubectl apply -f manifest/service.yml
```

- Expose the app service publicly:
```bash
kubectl patch svc smartlearnai-service -n argocd \
  -p '{"spec": {"type": "NodePort", "ports": [{"port": 90, "targetPort": 90, "nodePort": 9090}]}}'
```

- Access your app at:  
👉 `http://<EC2-Public-IP>:9090`

---

## ☸️ Kubernetes NodePort Access
```bash
kubectl get svc -n argocd
```
- Example output
```pgsql
NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
argocd-server          NodePort    10.97.0.1      <none>        80:31704/TCP   10m
smartlearnai-service   NodePort    10.97.0.2      <none>        90:9090/TCP    5m
```
Access:  
👉 ArgoCD → `http://<EC2-IP>:31704`

👉 SmartLearn App → `http://<EC2-IP>:9090`

---

## 💻 Commands Summary

| **Action** | **Command** | **Description** |
|-------------|-------------|-----------------|
| 🏗️ Build Docker Image | `docker build -t <user>/smartlearn-ai:latest .` | Build Docker image |
| ☁️ Push to Docker Hub | `docker push <user>/smartlearn-ai:latest` | Push image |
| 🧠 Start Minikube | `minikube start --driver=docker` | Start local Kubernetes cluster |
| ⚙️ Apply Deployment | `kubectl apply -f manifest/deployment.yml` | Deploy pods |
| 🌐 Apply Service | `kubectl apply -f manifest/service.yml` | Expose via NodePort |
| 🔍 Check Pods | `kubectl get pods` | Verify running pods |
| 🔎 Get NodePort | `kubectl get svc` | Retrieve exposed port |

---

## 🧱 Tech Stack

| 🛠️ Tool / Service | 💡 Purpose | 🔍 Detailed Description |
|--------------------|------------|--------------------------|
| 🧠 **LangChain** | LLM Orchestration Framework | Connects large language models to backend logic, handling prompt chaining, question generation, and reasoning. |
| ⚡ **Groq AI** | AI Inference Accelerator | Provides ultra-fast inference for LLMs using LPUs (Language Processing Units). |
| 🐙 **GitHub** | Source Control | Hosts source code and triggers Jenkins builds through webhooks. |
| 🔗 **GitHub Webhook** | CI Automation | Sends automatic notifications to Jenkins when new code is pushed. |
| ⚙️ **Jenkins** | Continuous Integration | Automates build, testing, and Docker image generation. |
| 🐳 **Docker** | Containerization | Packages the app and its dependencies for consistent deployment. |
| 📦 **Docker Hub** | Image Registry | Stores and versions Docker images for Kubernetes pulls. |
| 🚀 **ArgoCD** | Continuous Deployment (GitOps) | Automatically syncs and deploys GitHub manifests to Kubernetes. |
| ☸️ **Kubernetes (Minikube)** | Orchestration | Manages containerized applications and scales them efficiently. |
| ☁️ **AWS EC2** | Cloud Infrastructure | Hosts Jenkins, ArgoCD, and Kubernetes clusters. |
| 🌐 **NodePort Service** | Networking | Exposes internal Kubernetes services externally for web access. |
| 🔧 **Kubectl** | CLI Management | Controls, manages, and monitors Kubernetes deployments. |
| 📄 **YAML Manifests** | Configuration | Defines deployments, services, replicas, and container specs. |

---

## 👤 Author
**Andrew Adel Labib**  
🧠 *NLP Engineer | GenAI Engineer*  
📧 **andrewadellabib77@gmail.com**  
🔗 [LinkedIn](https://www.linkedin.com/in/andrew-adel-b865b1244)
