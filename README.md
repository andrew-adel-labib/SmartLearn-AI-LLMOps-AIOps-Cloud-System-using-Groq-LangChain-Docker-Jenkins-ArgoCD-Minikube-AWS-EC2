<h1 align="left">🤖 SmartLearn AI LLMOps System</h1>

<h2 style="color:#007BFF;">🧠 Overview</h2>

SmartLearn AI LLMOps System is a fully automated CI/CD and MLOps pipeline designed to streamline the deployment of AI-driven learning and quiz-generation applications.  
It integrates **GitHub**, **Jenkins**, **Docker Hub**, **ArgoCD**, **Groq AI**, **LangChain**, and **Kubernetes**, deployed on **AWS EC2 instances** using **NodePort** services.

This project demonstrates a complete AI/ML lifecycle — from **code commit → build → containerization → deployment → production inference** — powered by **Groq AI acceleration** and **LangChain orchestration**.

---

<h2 style="color:#28a745;">🧩 Features</h2>

- 🚀 End-to-end CI/CD automation using Jenkins, ArgoCD & Webhooks  
- 🧠 AI-powered quiz generator based on user-provided topics  
- ⚙️ LangChain for orchestrating LLM logic and structured question generation  
- ⚡ Groq AI LPUs for lightning-fast AI inference  
- ☸️ Kubernetes orchestration on AWS EC2 (NodePort)  
- 🐳 Dockerized architecture for portability  
- 🔗 GitHub Webhook integration for instant Jenkins triggers  
- ☁️ ArgoCD GitOps synchronization for automated deployments  
- 📊 Real-time evaluation and results generation inside the app  

---

<h2 style="color:#e67e22;">🧠 Project Idea: SmartLearn AI Quiz Generator</h2>

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

<h2 style="color:#17a2b8;">🚀 System Workflow</h2>

- **Code Push to GitHub** → triggers **Webhook** → notifies **Jenkins**  
- **Jenkins Pipeline** → pulls code, builds Docker image, pushes to Docker Hub  
- **Docker Hub** → stores versioned images  
- **ArgoCD** → monitors GitHub manifests and deploys to Kubernetes  
- **Kubernetes Cluster (AWS EC2)** → runs the app using NodePort for public access  

---

<h2 style="color:#9b59b6;">⚙️ Setup & Installation</h2>

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/SmartLearn-AI-LLMOps-System.git
cd SmartLearn-AI-LLMOps-System
```

### 2️⃣ Launch AWS EC2 Instance

Use Ubuntu 22.04 (t2.medium or higher)

Open ports:

- 22 (SSH)

- 8080 (Jenkins)

- 30000–32767 (NodePort range)

### 3️⃣ Install Dependencies
```bash
sudo apt update && sudo apt install -y docker.io docker-compose kubectl minikube
sudo systemctl start docker
sudo systemctl enable docker
minikube start --driver=docker
```
<h2 style="color:#f39c12;">🐳 Docker Build & Push Commands</h2>
| Action      | Command                                                            | Description                           |
| ----------- | ------------------------------------------------------------------ | ------------------------------------- |
| Build Image | `docker build -t <dockerhub-user>/smartlearn-ai:latest .`          | Builds image using project Dockerfile |
| Login       | `docker login`                                                     | Authenticate with Docker Hub          |
| Push Image  | `docker push <dockerhub-user>/smartlearn-ai:latest`                | Upload image to Docker Hub            |
| Run Locally | `docker run -d -p 8080:8080 <dockerhub-user>/smartlearn-ai:latest` | Run the image locally for testing     |

<h2 style="color:#2ecc71;">⚙️ Jenkins Integration (CI)</h2>
🧩 Install Jenkins
```bash
sudo apt install openjdk-11-jre -y
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update && sudo apt install jenkins -y
```

Access Jenkins at:
👉 http://<EC2-Public-IP>:8080

Create a Pipeline Job and connect it to your GitHub repository.

<h2 style="color:#c0392b;">🔗 GitHub Webhook Integration</h2>

Go to GitHub → Settings → Webhooks → Add Webhook

Set:

Payload URL: http://<EC2-IP>:8080/github-webhook/

Content type: application/json

Trigger: “Just the push event”

In Jenkins → Configure job → Check “GitHub hook trigger for GITScm polling.”

Push a commit to GitHub — Jenkins should automatically start a new build.

<h2 style="color:#16a085;">🧱 Jenkinsfile Example</h2>
```bash
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
<h2 style="color:#d35400;">🚀 ArgoCD Deployment (CD)</h2>
### 1️⃣ Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
### 2️⃣ Access ArgoCD Dashboard
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Then open:
👉 https://localhost:8081

### 3️⃣ Connect Repository

Add GitHub repo inside ArgoCD UI

Set Sync Policy → Automatic

### 4️⃣ Apply Kubernetes Manifests
```bash
kubectl apply -f manifest/deployment.yml
kubectl apply -f manifest/service.yml
```

Access your app at:
👉 http://<EC2-Public-IP>:<NodePort>

<h2 style="color:#2980b9;">☸️ Kubernetes NodePort Access</h2>
```bash
kubectl get svc
```

Access:
👉 http://<EC2-Public-IP>:<NodePort>

Example:
👉 http://13.58.24.122:30007

<h2 style="color:#8e44ad;">💻 Commands Summary</h2>
Action	Command	Description
Build Docker Image	docker build -t <user>/smartlearn-ai:latest .	Build Docker image
Push to Docker Hub	docker push <user>/smartlearn-ai:latest	Push image
Start Minikube	minikube start --driver=docker	Start local Kubernetes cluster
Apply Deployment	kubectl apply -f manifest/deployment.yml	Deploy pods
Apply Service	kubectl apply -f manifest/service.yml	Expose via NodePort
Check Pods	kubectl get pods	Verify running pods
Get NodePort	kubectl get svc	Retrieve exposed port
<h2 style="color:#e74c3c;">🧱 Tech Stack</h2>
🛠️ Tool / Service	💡 Purpose	🔍 Detailed Description
🧠 LangChain	LLM Orchestration Framework	Connects large language models to backend logic, handling prompt chaining, question generation, and reasoning.
⚡ Groq AI	AI Inference Accelerator	Ultra-fast, low-latency inference for LLM models using LPUs.
🐙 GitHub	Source Control	Hosts code, manages versioning, and triggers Jenkins builds via Webhooks.
🔗 GitHub Webhook	CI Automation	Automatically triggers Jenkins pipelines on code push.
⚙️ Jenkins	Continuous Integration	Automates build, testing, and Docker image creation.
🐳 Docker	Containerization	Packages the app and dependencies into a portable image.
📦 Docker Hub	Image Registry	Stores versioned Docker images for Kubernetes pulls.
🚀 ArgoCD	Continuous Deployment (GitOps)	Syncs manifests automatically to Kubernetes for live deployment.
☸️ Kubernetes (Minikube)	Orchestration	Deploys, manages, and scales containerized workloads.
☁️ AWS EC2	Cloud Infrastructure	Hosts Jenkins, ArgoCD, and Kubernetes cluster.
🌐 NodePort Service	Networking	Exposes services externally from EC2.
🔧 Kubectl	CLI Management	Manages and monitors Kubernetes deployments.
📄 YAML Manifests	Configuration	Defines deployments, replicas, and services.

<h2 style="color:#34495e;">👤 Author</h2>

Andrew Adel Labib
🧠 NLP Engineer | GenAI Engineer
📧 andrewadellabib7blackbuzzard@gmail.com
🔗 LinkedIn
