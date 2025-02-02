# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)    
   Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
Docker
Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
Kubernetes
Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.
The name Kubernetes originates from Greek, meaning helmsman or pilot. K8s as an abbreviation results from counting the eight letters between the "K" and the "s". Google open-sourced the Kubernetes project in 2014. Kubernetes combines over 15 years of Google's experience running production workloads at scale with best-of-breed ideas and practices from the community.


FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.
The key features are:
Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
Fast to code: Increase the speed to develop features by about 200% to 300%. *
Fewer bugs: Reduce about 40% of human (developer) induced errors. *
Intuitive: Great editor support. Completion everywhere. Less time debugging.
Easy: Designed to be easy to use and learn. Less time reading docs.
Short: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
Robust: Get production-ready code. With automatic interactive documentation.
Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.


SQLAlchemy
The SQLAlchemy SQL Toolkit and Object Relational Mapper is a comprehensive set of tools for working with databases and Python. It has several distinct areas of functionality which can be used individually or combined together. Its major components are illustrated below, with component dependencies organized into layers:

Above, the two most significant front-facing portions of SQLAlchemy are the Object Relational Mapper (ORM) and the Core.
Core contains the breadth of SQLAlchemy’s SQL and database integration and description services, the most prominent part of this being the SQL Expression Language.




FastAPI with SQLAlchemy
FastAPI doesn't require you to use a SQL (relational) database.
But you can use any relational database that you want.
Here we'll see an example using SQLAlchemy.
You can easily adapt it to any database supported by SQLAlchemy, like:
PostgreSQL
MySQL
SQLite
Oracle
Microsoft SQL Server, etc.
In this example, we'll use SQLite, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.
Later, for your production application, you might want to use a database server like PostgreSQL


Alembic
Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine. This tutorial will provide a full introduction to the theory and usage of this tool.
To begin, make sure Alembic is installed as described at Installation. As stated in the linked document, it is usually preferable that Alembic is installed in the same module / Python path as that of the target project, usually using a Python virtual environment, so that when the alembic command is run, the Python script which is invoked by alembic, namely your project’s env.py script, will have access to your application’s models. This is not strictly necessary in all cases, however in the vast majority of cases is usually preferred.


Swagger UI
Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption.
Dependency FreeThe UI works in any development environment, be it locally or in the web

Human FriendlyAllow end developers to effortlessly interact and try out every single operation your API exposes for easy consumption

Easy to NavigateQuickly find and work with resources and endpoints with neatly categorized documentation

All Browser SupportCater to every possible scenario with Swagger UI working in all major browsers

Fully CustomizableStyle and tweak your Swagger UI the way you want with full source code access

Complete OAS SupportVisualize APIs defined in Swagger 2.0 or OAS 3.*


# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: 
To ensure one job runs only after another job is complete, you can use the needs or dependencies keyword.
needs: Specifies an explicit dependency on another job, ensuring the dependent job runs only after its requirements are complete. This is useful when you have a specific order. 
dependencies: Ensures the output artifacts of one job are available to another. It doesn't necessarily enforce the order, but it's often used for dependencies on artifacts.

- How to change the image used in a task: 
To change the Docker image for a specific job, use the image: keyword within the job definition.
    
- How do you start a task manually:
To set a job to be started manually (like a deployment), use the when: manual keyword. You can also specify if a manual job should be optional with allow_failure: true.

- The Script part of the config file - what is it good for?
The script: section contains the commands that GitLab CI/CD should run when the job executes. This is where you define the specific operations for a job, like building code, running tests, deploying software, etc.

- If I want a task to run for every branch I put it into the stage ??
To run a task for every branch, use the only: keyword with a pattern that matches branches.

- If I want a task to run for every merge request I put it into the stage ??
To run a task for every merge request, use the only: keyword with a specific condition for merge requests.

- If I want a task to run for every commit to the main branch I put it into the stage ??
To run a task for every commit to the main branch, specify the branch in the only: keyword.

# flake8 / flakeheaven

- What is the purpose of flake8?
Flake8 is a Python tool used to enforce coding style guidelines, check for programming errors, and detect code smells. It combines the functionality of several other tools:

PyFlakes: For detecting logical errors.
pycodestyle (formerly known as Pep8): For ensuring adherence to the PEP 8 style guide.
mccabe: For checking the complexity of the code.

- What types of problems does it detect
Flake8 detects several types of problems, including:

Syntax errors
Indentation errors
Line length violations
Unused imports and variables
Improper use of whitespace
Logical errors such as using undefined variables
Code complexity issues

- Why should you use a tool like flake8 in a serious project?
Using Flake8 in a serious project provides several benefits:

Consistency: Ensures that all code adheres to a consistent style, making it easier to read and maintain.
Error Detection: Helps catch errors early in the development process, reducing the likelihood of bugs.
Code Quality: Promotes best practices and improves overall code quality.
Efficiency: Saves time during code reviews by automatically checking for style and syntax issues.

## Run flake8 on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *Dockerflake8*
- enter Program: *docker*
- enter Arguments: 
    *exec -i 1337_pizza_web_dev flakeheaven lint /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *$ProjectFileDir$*

If you like it convenient: Add a button for flake8 to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->Dockerflake8

### Run flake8 on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run flake8 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->Dockerflake8 

# GrayLog

- What is the purpose of GrayLog?
Graylog is a centralized log management tool that allows you to collect, index, and analyze log data. Its purposes include:

Aggregating logs from various sources into a single location.
Providing real-time insights into application and system behavior.
Facilitating troubleshooting and debugging by enabling powerful search and filter capabilities.
Monitoring and alerting based on specific log patterns or thresholds.

- What logging levels are available?
Common logging levels available in Graylog (and many other logging systems) are:

DEBUG: Detailed information, typically of interest only when diagnosing problems.
INFO: Confirmation that things are working as expected.
WARN: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
ERROR: Due to a more serious problem, the software has not been able to perform some function.
CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

- What is the default logging level?
The default logging level can vary depending on the system or configuration, but often the default level is INFO.

- Give 3-4 examples for logging commands in Python:
  ```python
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
  ```

# SonarQube

- What is the purpose of SonarQube?

SonarQube is an open-source platform designed to continuously inspect code quality. It identifies bugs, vulnerabilities, and code smells, enforces coding standards, tracks technical debt, and integrates with CI/CD pipelines to provide ongoing feedback to developers. This helps maintain a clean, secure, and maintainable codebase.

- What is the purpose of the quality rules of SonarQube?

Quality rules in SonarQube serve to automate the code review process by establishing guidelines for coding practices, ensuring code consistency, and identifying specific issues such as potential bugs, security vulnerabilities, and code smells. These rules help developers understand where improvements or refactoring are needed, maintaining high standards of code quality across the project.

- What is the purpose of the quality gates of SonarQube?

Quality gates in SonarQube set pass/fail criteria for code quality, preventing code that doesn't meet these standards from progressing through the development pipeline. They encourage continuous improvement by setting progressively stricter criteria, provide immediate feedback to developers, and support compliance with regulatory standards. This ensures that only code meeting required quality levels is merged or deployed, reducing the risk of defects in production.

## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 