# ☕ BIG MO's Coffee Shop App 🚀

A simple, interactive coffee ordering web application built with Python Flask, Dockerized, and deployed to Azure App Service using GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD).

<img src="images/flowchart.png" alt="CI/CD Pipeline Flowchart showing code push, Docker build, ACR, and Azure App Service deployment" width="700" height="300"/>
---

## ✨ Introduction

Welcome to the GitHub repository for **BIG MO's Coffee Shop App!** This project serves as a practical demonstration of building a basic web application using Python Flask, packaging it into a Docker container, and automating its deployment to Microsoft Azure's App Service using GitHub Actions.

Initially conceived as a simple console-based interactive script, this project has evolved to showcase how to adapt a command-line application into a web-accessible service, providing a hands-on example of a modern CI/CD pipeline. It's an ideal starting point for anyone looking to understand:

* Basic Python web development with Flask.
* Containerization using Docker.
* Automated build and deployment workflows with GitHub Actions.
* Cloud deployment to Azure App Service for Containers.

## 🌟 Key Features

* **Interactive Coffee Menu:** Displays a list of available coffee items and their prices.
* **Session-Based Basket:** Users can add multiple items and quantities to a temporary shopping basket that persists for their browser session.
* **Item Removal:** Ability to remove specific items from the basket.
* **Total Cost Calculation:** Calculates the grand total for all items in the basket.
* **Web-Based Interface:** Powered by Flask, accessible via any web browser.
* **Dockerized Application:** Packaged into a lightweight Docker image for consistent environments and easy deployment.
* **Automated CI/CD:**
    * **Continuous Integration:** Every push to the `main` branch automatically triggers a build of the Docker image.
    * **Continuous Deployment:** The newly built image is automatically pushed to Azure Container Registry and deployed to Azure App Service.
* **Cloud Deployment:** Hosted on Azure App Service for Containers, providing a scalable and managed environment.
