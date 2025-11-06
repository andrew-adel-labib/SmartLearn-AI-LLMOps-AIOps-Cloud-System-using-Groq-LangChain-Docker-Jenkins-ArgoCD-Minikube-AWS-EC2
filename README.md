# 🤖 SmartLearn AI LLMOps System

## 🧠 Overview

SmartLearn AI LLMOps System is a **fully automated CI/CD and MLOps pipeline** integrating modern DevOps and AI engineering tools — **GitHub, Jenkins, Docker Hub, ArgoCD, Groq AI, LangChain, and Kubernetes** — deployed on **AWS EC2** using **NodePort services**.

This project demonstrates a complete AI application lifecycle from **code commit → build → containerization → deployment → inference acceleration** through a robust, intelligent automation system.

---

## 🧩 Features

- 🚀 **End-to-end CI/CD** automation with Jenkins, ArgoCD, and Webhooks  
- 🧠 **AI-driven inference** with **Groq AI LPUs** for high-speed performance  
- 🧩 **LangChain-powered orchestration** for LLM logic and automation  
- ☸️ **Kubernetes** for scalable container management  
- ☁️ **AWS EC2** cluster hosting Jenkins, ArgoCD, and K8s  
- 🐳 **Dockerized architecture** for consistent builds  
- 🔗 **GitHub Webhook** integration for automated triggers  
- 🌐 **NodePort** service exposing the app publicly  

---

## 🧱 Tech Stack

| 🛠️ Tool / Service | 💡 Purpose | 🔍 Detailed Description |
|--------------------|-------------|--------------------------|
| 🧠 **LangChain** | LLM Orchestration Framework | Manages and chains together language model operations, memory, and tools to handle SmartLearn AI logic flow. |
| ⚡ **Groq AI** | AI Inference Accelerator | Provides lightning-fast, low-latency inference for deployed AI models using Groq LPUs (Language Processing Units). |
| 🐙 **GitHub** | Source Control | Hosts project code and manages versioning; acts as the CI trigger source through webhooks. |
| 🔗 **GitHub Webhook** | CI Automation | Notifies Jenkins automatically when commits are pushed, triggering build and deployment pipelines. |
| ⚙️ **Jenkins** | Continuous Integration | Pulls code, builds Docker images, and pushes to Docker Hub through pipeline automation. |
| 🐳 **Docker** | Containerization Platform | Packages application into portable images for seamless deployment across environments. |
| 📦 **Docker Hub** | Image Registry | Stores versioned Docker images created by Jenkins for deployment in Kubernetes. |
| 🚀 **ArgoCD** | Continuous Deployment (GitOps) | Continuously synchronizes GitHub manifests with Kubernetes deployments, ensuring real-time updates. |
| ☸️ **Kubernetes (Minikube)** | Container Orchestration | Manages containers, pods, and services; supports scaling and fault tolerance. |
| ☁️ **AWS EC2** | Cloud Infrastructure | Hosts the Jenkins server, ArgoCD controller, and Kubernetes cluster on cloud infrastructure. |
| 🌐 **NodePort Service** | Network Exposure | Makes Kubernetes services accessible from the internet using static NodePort mapping. |
| 🔧 **Kubectl** | Kubernetes CLI Tool | Used for applying, managing, and monitoring Kubernetes resources. |
| 📄 **YAML Manifests** | Configuration Management | Define Kubernetes deployments and services for automated rollout. |

---

## ⚙️ Setup & Usage

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/SmartLearn-AI-LLMOps-System.git
cd SmartLearn-AI-LLMOps-System
```

### 2. Launch EC2 Instance
- Choose Ubuntu 22.04 (t2.medium or higher)
- Configure **Security Group Ports:**
  - 22 (SSH)
  - 8080 (Jenkins)
  - 30000–32767 (NodePort Range)

### 3. Install Dependencies
```bash
sudo apt update && sudo apt install -y docker.io kubectl minikube
sudo systemctl enable docker && sudo systemctl start docker
minikube start --driver=docker
```

---

## 🧰 Docker Commands

| Action | Command | Description |
|--------|----------|-------------|
| Build Image | `docker build -t <user>/smartlearn-ai:latest .` | Build the project Docker image. |
| Run Container | `docker run -d -p 8080:8080 <user>/smartlearn-ai:latest` | Run image locally for testing. |
| Login | `docker login` | Authenticate with Docker Hub. |
| Push Image | `docker push <user>/smartlearn-ai:latest` | Upload image to Docker Hub. |

---

## ⚙️ Jenkins Pipeline (CI)

1. Create a Jenkins Pipeline Job.  
2. Add your repository URL and credentials.  
3. Configure Webhook from GitHub:  
   - Payload URL: `http://<EC2-IP>:8080/github-webhook/`  
   - Content type: `application/json`  
   - Trigger: *Just the push event*  

**Sample Jenkinsfile**
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
        stage('Push Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_PASS')]) {
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

### Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Access ArgoCD
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```
Then open in browser: `https://localhost:8081`

### Deploy App
```bash
kubectl apply -f manifest/deployment.yml
kubectl apply -f manifest/service.yml
```

**Access App:**  
```
http://<EC2-Public-IP>:<NodePort>
```

---

## 🧱 Project Structure
```
SmartLearn-AI-LLMOps-System/
│
├── manifest/
│   ├── deployment.yml
│   └── service.yml
├── Jenkinsfile
├── Dockerfile
├── src/
│   ├── generator/
│   └── utils/
└── README.md
```

---

## 👤 Author

**Andrew Adel Labib**  
🧠 NLP Engineer | GenAI Engineer  
📧 [andrewadellabib7blackbuzzard@gmail.com](mailto:andrewadellabib7blackbuzzard@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/andrew-adel-b865b1244)
