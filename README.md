# 🤖 Persistent AI Chatbot: AWS Bedrock + MySQL + Docker

A production-ready, conversational AI application that remembers. This chatbot moves beyond simple in-memory demos by implementing a persistent memory layer using MySQL and high-performance reasoning via the **Amazon Nova** model series.

---

## 🌟 Key Features

* **Advanced Reasoning**: Powered by **Amazon Nova Lite v1.0** via AWS Bedrock for fast, intelligent responses.
* **Long-Term Memory**: Uses `SQLChatMessageHistory` to store and retrieve full conversation threads from a MySQL database, enabling seamless multi-session dialogues.
* **Enterprise Architecture**: Decoupled frontend (Streamlit) and backend (LangChain) logic.
* **Full Observability**: Integrated with LangChain's debug and verbose modes to trace exact prompt construction and token usage in your terminal.
* **Cloud Native**: Ready for both local development with **Docker Compose** and production-grade orchestration with **Kubernetes**.
* **Security First**: Credential management via `.env` files and Kubernetes Secrets.

---

## 🏗️ Architecture

The application is structured into four distinct layers:

1.  **Frontend**: Streamlit-based UI handles session management and real-time rendering.
2.  **Orchestration**: LangChain (v0.3.0+) manages the flow between user input, memory retrieval, and AI invocation.
3.  **Persistence**: MySQL stores raw chat history indexed by `session_id`.
4.  **Intelligence**: AWS Bedrock executes the LLM inference using regional inference profiles for high availability.

`[User] -> [Streamlit UI (8501)] -> [LangChain Backend] <-> [MySQL DB (3306)]`
`                                       |`
`                                       v`
`                              [AWS Bedrock (Nova Lite)]`

---

## 📋 Prerequisites

* **AWS Account**: Bedrock access granted for **Amazon Nova Lite** in `eu-west-1`.
* **Docker Desktop**: For containerized deployment.
* **Python 3.10+**: For local development.
* **AWS CLI**: Configured with credentials that have `AmazonBedrockFullAccess`.

---

## 🚀 Getting Started

### 1. Docker Setup (Recommended)
This is the fastest way to launch the full stack (App + Database).

1.  **Clone the Repo**:
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
2.  **Environment Setup**:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and provide your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `DB_PASSWORD`.
3.  **Launch**:
    ```bash
    docker-compose up --build
    ```
    Access the UI at: `http://localhost:8501`

### 2. Kubernetes Deployment
For simulating production environments:
1.  **Setup Secrets**:
    Create a `secret.yaml` from `secret.yaml.example` with your real credentials.
2.  **Deploy**:
    ```bash
    kubectl apply -f secret.yaml
    kubectl apply -f mysql-deployment.yaml
    kubectl apply -f app-deployment.yaml
    kubectl apply -f app-service.yaml
    ```

---

## 📂 File Structure

| File | Description |
| :--- | :--- |
| `ChatBackend.py` | Core logic: LangChain orchestration, DB connection, and Bedrock setup. |
| `chatfrontend.py` | Streamlit UI and session management. |
| `Dockerfile` | Python 3.10-slim environment with `langchain-aws` optimization. |
| `docker-compose.yml` | Multi-container setup for the app and MySQL services. |
| `requirements.txt` | Dependency list (pinned to LangChain v0.3.0+). |
| `*-deployment.yaml` | Kubernetes manifests for enterprise-grade deployment. |

---

## 🛠️ Usage & Troubleshooting

* **Logs**: Check your terminal or Docker logs to see the AI's "thought process" in real-time.
* **Validation Errors**: Ensure your `AWS_REGION` in the `.env` matches the region where you have model access.
* **Database**: History is persistent! Even if you stop the containers, your messages remain in the `db_data` volume.