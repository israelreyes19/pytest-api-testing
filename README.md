# **User Management API \- Automated Test Suite & CI/CD Pipeline**

This repository contains the end-to-end (E2E) automated test framework for the **User Management API**, built with **Python**, **Pytest**, and **Requests**, integrated with **Allure Reports** and **GitHub Actions**.

## **Architecture & Design Decisions**

* **Language & Framework:** Python 3.11 with Pytest for clean fixture management and flexible test parametrizations.  
* **HTTP Client Abstraction:** Custom APIClient class handling URL routing, environment contexts (dev / prod), failure hooks, and authorization headers (Authentication).  
* **Environment Dynamic Routing:** Dynamic base URL switching driven by the \--env CLI flag.  
* **Parallel CI Matrix Pipeline:** GitHub Actions matrix running dev and prod stages simultaneously with fail-fast: false, ensuring one failing environment stage does not block the other.  

## **Prerequisites & Local Setup**

* **Start the API Docker Container:**  
  docker run \-p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest

* **Set up Virtual Environment & Install Dependencies:**  
  python3 \-m venv .venv  
  source .venv/bin/activate  
  pip install \-r requirements.txt

## **Running Tests Locally**

Run the automated tests against the desired environment:

\# Run tests for Dev environment  
pytest \--env=dev

\# Run tests for Prod environment  
pytest \--env=prod

\# Run tests using the full path to virtual environment  
.venv/bin/python \-m pytest \--env=dev \--alluredir=allure-results

To view the Allure report locally in your browser:

allure serve allure-results

## **CI/CD Pipeline & Reports**

The GitHub Actions workflow .github/workflows/api-tests.yml:

1. Launches the application Docker container inside the runner.  
2. Executes the test suite in parallel for both dev and prod environments.  
3. Generates and publishes the interactive **Allure Report** to GitHub Pages automatically.

## **Identified Bugs & Contract Violations**

Discrepancies found between the actual application behavior and the OpenAPI specification (sdet\_challenge\_api.yml) are documented in detail in BUGS.md.