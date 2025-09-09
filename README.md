# Flask PDF Generator

A simple Python Flask application that generates and streams PDF files using `xhtml2pdf`.

## 📦 Features

- Generate PDF from HTML
- Serve PDF as a download or inline view
- Easily integrate with Node.js, CAPM, or REST clients

## 🧰 Requirements

- Python 3.7+
- Flask
- xhtml2pdf

## Steps to create the project
1.  Create a MTA Project in SAP BAS 
2.  Create the conventional Flask project structure (with static/ and templates/ folders)
    ```python
    mkdir static templates
    ```
3.  Set up a Python virtual environment
    ```python
    python3 -m venv venv
    source venv/bin/activate
    ```
    "python3 -m venv venv" will create a folder named venv/ in your current directory, which contains your isolated Python environment. The first venv is a Python module, and the second venv is the name of the folder you’re creating. You can create multiple virtual environments for different projects, below code generate 2 enivornments for project a and b.
    ```python
    python3 -m venv venv-a 
    python3 -m venv venv-b
    ``` 
    Use "source venv/bin/activate" to activate the environment.

4. Install dependencies
    Install dependencies using the below approaches.
    ```python
    pip install flask xhtml2pdf 
            or
    pip install -r requirements.txt
    ```
5.  Save dependencies and packages
    Create requirements.txt file to track your dependencies. Use the commmand to create and populate the requirements file
    ```python
    pip freeze > requirements.txt
    ```
6. Create a simple Flask app (main.py - to return a PDF or JSON)
7. Deployment Config
    If deploying to SAP BTP Cloud Foundry, create files manifest.yml and Procfile manually.
    You can deploy using the SAP BTP CLI command, if enabled in your environment
    ```python
    cf push
    ```
8. Run the application
    ```python
    source venv/bin/activate
    python app.py
    ```
