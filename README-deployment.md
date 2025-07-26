# 🚀 Deployment Guide for the "Fire Risk Prediction in Montreal" Live App

### 🔥 Application Overview
This project is **a production-ready web app** that predicts fire risk in Montreal using machine learning. It is built with **Flask**, deployed on **Render**, and fully integrated with **Google Cloud Storage (GCS)** for scalable data and model access.  

The project is version-controlled with **Git** and hosted on **GitHub** to support collaboration, reproducibility, and cloud deployment practices suitable for real-world ML engineering.

---

### 🔗 Quick Links:
[🚀 Live App](https://fire-risk-prediction-in-montreal.onrender.com) |
[📖 Project Details](README-detailed.md) |
[⚙️ Deployment Guide](fire-risk-app/README-deployment.md) |
[🎞️ Presentation Slides](https://drive.google.com/file/d/1lRE_yKjAF7jHVoCD7S1-z5ezxtrtlUYC/view?usp=sharing)

---

### 🔧 Prerequisites

To set up or understand the deployment, ensure the following tools and accounts are available:

- 🐍 Python 3.11+
- 🧰 Git installed
- 🖥️ Render account for web app deployment
- ☁️ Google Cloud account with a project and GCS bucket 
- 🔐 A service account key in JSON format with read access to the bucket

> 💡 Setup scripts are provided to automate environment configuration and credential linking.

---

### 📦 Model and Data Access

To follow production-grade ML deployment practices, this project **does not store models or datasets in the codebase**. Instead, all essential files are securely stored in **Google Cloud Storage (GCS)** and loaded dynamically at runtime.

For reproducibility, fire history data, spatial grid data and trained xgboost model can be downloaded via links below:

- 🔗 [Download fire risk data](https://drive.google.com/file/d/1U6BGWDvxeN1qBhKB1tlNH42kQt34D_oM/view?usp=sharing)
- 🔗 [Download grid data](https://drive.google.com/file/d/1BUvmI8e2VL4RKVSi3LkFlgPrtWx1HDBm/view?usp=sharing)
- 🔗 [Download model data](https://drive.google.com/file/d/15gUfpDLu-ze5GFWxlvrP4TCR-R3NcSUt/view?usp=sharing)  

> 🔐 These files are ignored by Git and not embedded in the app image. This reflects a cloud-native, stateless deployment design.

---

# ☁️ Production Deployment on Render

This application was deployed to **Render**, a fully managed cloud platform that automates building, deploying, and scaling Python applications.

The deployment process reflects **key stages** of a **production-ready** web application rollout:
- 🔐 Secure integration with **Google Cloud Storage (GCS)**
- ⚙️ Scalable application hosting using **Gunicorn + Flask**
- 🔧 Proper handling of secrets and environment variables
- 📦 Modular project structure designed for automation and CI/CD


## 🛠️   Phase 1 - GitHub Repository Setup
The first phase of the deployment process involved structuring the project repository to support reproducible builds, modular application logic, and cloud deployment integration.

**The project is hosted on GitHub at: [https://github.com/vlad-uve/Fire-Risk-Prediction-in-Montreal](https://github.com/vlad-uve/Fire-Risk-Prediction-in-Montreal)**

### 1.1 📂 Repository Structure
The repository is organized into clearly separated components to support maintainability and streamline deployment:

| Path                                 | Purpose                                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **`fire-risk-app/`**                 | Core Flask application; set as the root directory for Render builds                                                                |
| **`app_gcs.py`**               | Cloud-integrated entry point that streams model + data from GCS at runtime                                                         |
| **`requirements-app_gcs.txt`** | Dependency list used during Render builds (includes `google-cloud-storage`)                                                        |
| **`src/`**                           | Utility modules for data loading, mapping, and prediction                                                                          |
| **`model/`, `data/`**                | Local placeholders for model and dataset (both `.gitignore`d)                                                                      |
| **`static/`**                        | Front-end assets served by Flask:<br>• `images/background.jpg`<br>• `maps/default_pred_map.html`<br>• `maps/default_true_map.html` |
| **`templates/`**                     | Jinja2 templates — mainly `maps.html`, which renders the interactive map interface                                                 |


> This modular layout ensures that only the deployment-relevant files are monitored and built by Render, improving CI/CD efficiency.

### 1.2 CI/CD Integration with Render
The deployment is connected to **Render** using GitHub integration and configured with:

* **✅ Tracked branch:** `main` — only production-ready commits trigger deployments
* **📁 Root directory:** `fire-risk-app/` — limits the build context to the Flask app code only

> This setup ensures that only relevant changes (e.g., to app logic or templates) trigger a new build, while unrelated updates—such as to notebooks or documentation—are ignored.


## 🌐 Phase 2 - Google Cloud Storage (GCS) Configuration
This phase focused on configuring secure, cloud-native storage for model and data files using **Google Cloud Storage (GCS)**. Instead of embedding static assets within the codebase, the app loads them dynamically at runtime via GCS APIs. This makes the deployment stateless, modular, and scalable.


### 2.1 🪣 GCS Bucket Setup
A dedicated GCS bucket was created to host the model and data files:

| Setting            | Value                                |
| ------------------ | ------------------------------------ |
| **Bucket name**    | `fire-risk-gcs-bucket`               |
| **Region**         | `northamerica-northeast1` (Montréal) |
| **Storage class**  | Standard                             |
| **Access control** | Uniform bucket-level access          |


#### Folder layout inside the bucket:

```
fire-risk-gcs-bucket/
├── data/
│   ├── df_fires_history_risk.csv     # Fire risk history data
│   └── montreal_grid_v1.geojson      # 1km grid overlay for Montreal
│
└── model/
    └── xgb_model_v1.pkl              # Trained XGBoost classifier
```

### 2.2 🔐 Service Account and IAM Permissions
To enable secure access to GCS from the deployed app:

1. A **dedicated service account** was created in Google Cloud Console  
2. It was granted the following IAM role: `Storage Object Viewer (roles/storage.objectViewer)`
3. A **JSON key file** was generated and downloaded: `gcs_service_key.json`

> 🔐 The credential file is never committed to Git. Instead, it is uploaded to Render as a **secret file** and accessed securely during both build and runtime.


## 🚀 Phase 3 - Render Web Service Configuration

The final phase of the deployment involved configuring a **Render Web Service**. It hosts the Flask app and connects it to the Google Cloud Storage backend configured in Phase 2 and the GitHub repository set up in Phase 1.

### 3.1 🌍 Service Setup
These settings ensure that only the app-specific code `fire-risk-app` is deployed, using the minimal resources:

| Setting           | Value                          |
|-------------------|--------------------------------|
| **Name**          | Fire-Risk-Prediction-in-Montreal |
| **Language**      | Python 3                       |
| **Branch**        | `main`                         |
| **Region**        | Virginia (US East)             |
| **Root Directory**| `fire-risk-app/`               |
| **Instance Type** | Free (0.1 CPU, 512 MB RAM)     |

### 3.2 ⚙️ Build and Runtime Configuration

The application is deployed using **Gunicorn**, a production-grade WSGI server. Render automatically installs dependencies and runs the following configuration settings:

#### Build Command:

```
pip install -r requirements-app_gcs.txt
```

>This file `requirements-app_gcs.txt` includes all necessary libraries for deploying the flask application with GCS integration

#### Start Command:

```
gunicorn app_gcs:app --bind 0.0.0.0:$PORT
```

> The entry point `app_gcs.py` initializes the app and connects to GCS at runtime to retrieve model and data files

---

### 3.3 🔐 Credential Management

This allows the app to authenticate with Google Cloud without exposing credentials in code

#### Secret File:

The service account key (`gcs_service_key.json`) was uploaded to Render as a secret file, making it securely accessible by the app during both build and runtime.


#### Environment Variable:
``` 
GOOGLE_APPLICATION_CREDENTIALS=gcs_service_key.json
```

> This environment variable tells the Google Cloud SDK where to find the credentials file. When the Flask app starts, the SDK uses this path to authenticate with GCS and load the model and data securely.


### 3.4 ⚡ Runtime Behavior

Once deployed, the Flask application:

* Dynamically loads model and data from GCS
* Generates risk prediction maps using the current dataset
* Serves an interactive front-end via HTML templates and static content

> ✅ The deployment is fully cloud-native and avoids local state by externalizing all data.



### 3.5🗺️ Deployment Diagram

This diagram showcases the deployment pipeline and demonstrates a scalable, secure ML web app architecture using modern tools and cloud integration.

```
[GitHub Repo] ──► [Render Web Service]
                             │
                             └──► [Google Cloud Storage]
                                     ├── xgb_model_v1.pkl
                                     ├── df_fires_history_risk.csv
                                     └── montreal_grid_v1.geojson
```


### 3.6 🧪 (Optional) Deployment with Static Data

For quick demonstrations or when GCS access is not available, the application can be deployed using **static data and model files** instead of the cloud‑integrated workflow.

#### **Please follow these steps:**

#### 1. Upload the data files and the model in project folder

```
fire-risk-app/
├── data/
│   ├── df_fires_history_risk.csv
│   └── montreal_grid_v1.geojson
└── model/
    └── xgb_model_v1.pkl
```

#### 2. Open Render Web Service Settings and switch the file with necessary requirements to `requirements-app.txt`, which excludes dependencies for integration with GCS.

```
pip install -r requirements-app.txt
```

#### 3. Open Render Web Service Settings and switch the application entry point to `app.py`, which serves static data sourcing

```
gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 4. Redeploy

- Click “Manual Deploy” in the Render dashboard or push a commit to `main`.

 - Render rebuilds with the new commands; `app.py` now loads the model and data from the static (local) `model/` and `data/` folders, so no GCS access is required.


---

# 📂 Project Structure

```
├── files/ # Supporting files for documentation

├── fire-risk-app/ # 🔥 Core Flask app for prediction & visualization
│ ├── app_gcs.py # Main entry point for files from GCS
│ ├── app_static.py # Alternative entry point for locally saved files
│ │
│ ├── data/ # History of fire risk and spatial grid (Ignored in Git)
│ │ ├── df_fires_history_risk.csv
│ │ └── montreal_grid_v1.geojson
│ │
│ ├── model/ # Trained model (Ignored in Git)
│ │ └── xgb_model_v1.pkl
│ │
│ ├── static/ # Static assets (images, default and generated maps)
│ │ ├── images/
│ │ │ └── background.jpg
│ │ │
│ │ └── maps/
│ │   ├── default_pred_map.html
│ │   └── default_true_map.html
│ │
│ ├── templates/ # Jinja2 templates for rendering HTML
│ │ └── maps.html
│ │
│ ├── src/ # Core utilities: data loading, mapping, prediction
│ │ ├── data_utils.py
│ │ ├── map_utils.py
│ │ └── model_utils.py
│ │
│ ├── requirements-app_gcs.txt # Requirements for cloud deployment
│ └── requirements-app(with_gcs).txt # Aleternative Requirements for deployment with localy saved files
│
├── fire-risk-venv/ # Local virtual environment (Ignored in Git)
│
├── notebooks/ # Development notebooks
│
├── setup_scripts/ # Shell scripts for environment setup and GCS linking
│
├── gcs_service_key.json # Service account credentials (Ignored in Git)
│
├── README.md # Project overview
├── README-deployment.md # 📄 Deployment instructions (this file)
├── README-detailed.md # Extended description with technical context
│
├── requirements-dev.txt # Dev dependencies for notebooks or debugging
│
└── .gitignore # Specifies files/folders excluded from Git

```