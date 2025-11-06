# SmartLearn-AI-LLMOps-AIOps-Cloud-System-using-Groq-LangChain-Docker-Jenkins-ArgoCD-Minikube-AWS-EC2

SmartLearn AI LLMOps and AIOps Intelligent Automation System Using Groq LPU, LangChain, Streamlit, Docker, Jenkins, ArgoCD, GitOps, Kubernetes Minikube and AWS EC2 for Scalable Cloud-Native Deployment

# 🤖 SmartLearn AI LLMOps System

## 🧠 Overview

SmartLearn AI LLMOps System is a **fully automated CI/CD and MLOps pipeline** designed to streamline deployment of AI-driven applications. The system integrates **GitHub, Jenkins, Docker Hub, ArgoCD, and Kubernetes** to deliver seamless continuous integration and deployment on **AWS EC2** instances using **NodePort services**.

This project demonstrates how to manage the lifecycle of an AI/ML application — from **code commit → build → containerization → deployment → production monitoring** — through a robust and automated infrastructure.

---

## 🚀 System Workflow

1. **Code Push to GitHub** → Triggers a **Webhook** that notifies Jenkins.
2. **Jenkins Pipeline** → Pulls latest code, builds Docker image, pushes to Docker Hub.
3. **Docker Hub** → Stores versioned container images.
4. **ArgoCD** → Monitors GitHub repository for manifest changes and deploys automatically.
5. **Kubernetes Cluster on AWS EC2** → Runs the deployed containerized application with a **NodePort** service for external access.

---

## 🧩 Features

* Automated **CI/CD pipeline** with Jenkins and GitHub Webhooks.
* Containerized deployments with **Docker**.
* **ArgoCD-based GitOps** deployment to Kubernetes.
* **AWS EC2-hosted cluster** using Minikube or kubeadm.
* Exposed **NodePort** services for public access.
* Scalable, modular, and reproducible infrastructure.

---

## ⚙️ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd SmartLearn-AI-LLMOps-System
```

### 2. Launch AWS EC2 Instance

* Use an Ubuntu-based EC2 instance (t2.medium or higher recommended).
* Open required **Security Group Ports**:

  * `22` (SSH)
  * `8080` (Jenkins)
  * `30000-32767` (Kubernetes NodePort range)

### 3. Install Dependencies

```bash
sudo apt update && sudo apt install -y docker.io docker-compose kubectl minikube
```

Enable Docker service:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Start Minikube:

```bash
minikube start --driver=docker
```

---

## 🐳 Docker Build & Push Commands

### Build Docker Image

```bash
docker build -t <dockerhub-username>/smartlearn-ai:latest .
```

**Explanation:** Builds the Docker image using the project’s Dockerfile and tags it with your Docker Hub username.

### Push Image to Docker Hub

```bash
docker login
# Enter your Docker Hub credentials
docker push <dockerhub-username>/smartlearn-ai:latest
```

**Explanation:** Pushes the locally built image to your Docker Hub repository for later deployment by Kubernetes.

---

## 🧱 Jenkins Integration (CI)

### Configure Jenkins

1. Install Jenkins on EC2:

   ```bash
   sudo apt install openjdk-11-jre -y
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt update && sudo apt install jenkins -y
   ```

2. Access Jenkins via `http://<EC2-Public-IP>:8080`

3. Create a **Pipeline Job** connected to your GitHub repo.

4. Add a **GitHub Webhook** to trigger builds on push events.

### Jenkinsfile Example

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
                sh 'docker build -t <dockerhub-username>/smartlearn-ai:latest .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'DOCKER_HUB_PASS')]) {
                    sh 'echo $DOCKER_HUB_PASS | docker login -u <dockerhub-username> --password-stdin'
                    sh 'docker push <dockerhub-username>/smartlearn-ai:latest'
                }
            }
        }
    }
}
```

---

## 🔗 GitHub Webhook Integration with Jenkins

### 1. Purpose

The GitHub Webhook allows **automated Jenkins builds** whenever code is pushed to your repository — removing the need to manually trigger jobs after every change.

### 2. Configuration Steps

1. Go to your **GitHub repository → Settings → Webhooks → Add Webhook**.
2. Set the **Payload URL** to your Jenkins endpoint:

   ```
   http://<EC2-Public-IP>:8080/github-webhook/
   ```
3. Choose **Content type:**

   ```
   application/json
   ```
4. Select:

   ```
   Just the push event
   ```
5. Click **Add Webhook**.

### 3. Jenkins Setup

* In Jenkins, ensure the **“GitHub Integration”** and **“GitHub API”** plugins are installed.
* Inside your Jenkins pipeline job, go to:
  **Configure → Build Triggers → Check “GitHub hook trigger for GITScm polling”**.

Now every push to your GitHub repo will **automatically start a Jenkins pipeline build**.

### 4. Verification

You can test the webhook connection by committing any small change (like editing the README) — Jenkins should automatically start a new build.

---

## 🎯 ArgoCD Deployment (CD)

### Deploy ArgoCD on Kubernetes

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Access ArgoCD UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Then open: `https://localhost:8081`

### Connect to GitHub Repository

* Add your repo URL in ArgoCD UI.
* Set **Sync Policy** to *Automatic*.

### Apply Kubernetes Manifests

```bash
kubectl apply -f manifest/deployment.yml
kubectl apply -f manifest/service.yml
```

**Explanation:**

* `deployment.yml`: Defines the container deployment and replicas.
* `service.yml`: Exposes the app via NodePort for external access.

---

## ☸️ Kubernetes NodePort Access

Get service details:

```bash
kubectl get svc
```

Access app at:

```
http://<EC2-Public-IP>:<NodePort>
```

Example:

```
http://13.58.24.122:30007
```

---

## 💻 Commands Summary

| Action             | Command                                         | Description                   |
| ------------------ | ----------------------------------------------- | ----------------------------- |
| Build Docker Image | `docker build -t <user>/smartlearn-ai:latest .` | Build image locally           |
| Push Image         | `docker push <user>/smartlearn-ai:latest`       | Push to Docker Hub            |
| Start Minikube     | `minikube start --driver=docker`                | Initialize Kubernetes cluster |
| Apply Deployment   | `kubectl apply -f manifest/deployment.yml`      | Deploy app pods               |
| Apply Service      | `kubectl apply -f manifest/service.yml`         | Expose app via NodePort       |
| Check Pods         | `kubectl get pods`                              | Verify pods are running       |
| Get NodePort       | `kubectl get svc`                               | Retrieve external access port |

---

## 🧩 Tech Stack

| Tool                      | Purpose                 | Usage/Configuration                               |
| ------------------------- | ----------------------- | ------------------------------------------------- |
| **GitHub**                | Source control          | Stores source code & triggers Jenkins via Webhook |
| **Jenkins**               | CI Tool                 | Automates build, test, and Docker image creation  |
| **Docker**                | Containerization        | Packages application into portable images         |
| **Docker Hub**            | Image Registry          | Stores versioned container images                 |
| **ArgoCD**                | GitOps Deployment       | Monitors GitHub and auto-syncs to Kubernetes      |
| **Kubernetes (Minikube)** | Container Orchestration | Runs workloads & manages pods                     |
| **AWS EC2**               | Cloud Infrastructure    | Hosts Jenkins, ArgoCD, and Kubernetes cluster     |
| **NodePort Service**      | Network Access          | Exposes the app to public traffic                 |
| **Kubectl**               | CLI Management Tool     | Manages K8s resources (pods, svc, deployments)    |
| **YAML Manifests**        | Deployment Definitions  | Define K8s configurations for automation          |

---

## 📁 Project Structure

```
SmartLearn-AI-LLMOps-System/
│
├── manifest/
│   ├── deployment.yml
│   └── service.yml
│
├── Jenkinsfile
├── Dockerfile
├── requirements.txt
├── src/
│   ├── generator/
│   └── utils/
│
└── README.md
```

---

## 👤 Author

**Andrew Adel Labib**
🧠 NLP Engineer | GenAI Engineer
📧 [andrewadellabib7blackbuzzard@gmail.com](mailto:andrewadellabib7blackbuzzard@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/andrew-adel-b865b1244)

---

This `README.md` provides a complete end-to-end overview of how to build, integrate, and deploy the **SmartLearn AI LLMOps System** on AWS EC2 using Jenkins, Docker Hub, ArgoCD, and Kubernetes with NodePort exposure.
