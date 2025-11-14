


# Job Application Tracker

A web-based application built with **Flask** and **SQLite/Azure SQL**, designed to help users track job applications efficiently. This project demonstrates full-stack Python development, CRUD operations, file uploads, and cloud-ready deployment practices.

---

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Add new job applications with details: date, company, role, source, CV, stages, status, and comments.
- Edit existing applications.
- Delete applications securely.
- Track application progress using stages.
- File upload support for CVs (`.pdf` and `.docx`).
- Status dropdown with visual indicators: **Accepted** (green) and **Rejected** (red).
- Responsive design for desktop and mobile.

---

## Demo
Include screenshots or a GIF of your app in action.  
Example:

![Job Application Form]<img width="1876" height="1031" alt="image" src="https://github.com/user-attachments/assets/3e804653-ff0d-4978-977c-baf3797b8eca" />
![Applications List] <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9222a6e2-9248-4832-90ea-d08202a0461e" />

---

## Technologies
- **Backend:** Python, Flask
- **Database:** SQLite (can be upgraded to Azure SQL for cloud deployment)
- **Frontend:** HTML5, CSS3 (responsive, no JS)
- **File Handling:** werkzeug for secure file uploads

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/oludarekenny/job-app-tracker.git
   cd job-app-tracker
   
2. Create a virtual environment:
   python3 -m venv appvenv
   source appvenv/bin/activate  # Linux/macOS

3. pip install -r requirements.txt
4. Run the app:
   python3 app.py


##**Usage**

- Go to the home page to add a new application.

- Navigate to the view page to see all submitted applications.

- Use Edit to update application details.

- Use Delete to remove an application.

- Uploaded CVs are stored in the /uploads folder.

   

