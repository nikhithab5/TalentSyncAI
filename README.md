# TalentSync AI 🚀

An AI-powered job portal built using Django that helps job seekers upload resumes, analyze job descriptions, and find the best matching opportunities.

## Features

* User Authentication

  * Sign up and login
  * Google OAuth Login
  * Password reset support

* Resume Management

  * Upload resumes in PDF format
  * View uploaded resumes
  * Resume storage for each user

* AI Job Fit Analyzer

  * Paste any job description
  * Compare it against uploaded resumes
  * Display matching and missing skills
  * Generate a match score

* Job Management

  * Browse jobs
  * Save jobs
  * Apply for jobs
  * Track applications

* Recruiter Features

  * Recruiter dashboard
  * Interview scheduling
  * Recruiter notes

## Technologies Used

* Python
* Django
* SQLite
* Bootstrap 5
* HTML
* CSS
* Django Allauth
* Google OAuth

## Installation

```bash
git clone https://github.com/nikhithab5/TalentSyncAI.git
cd TalentSyncAI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Future Enhancements

* AI resume scoring
* ATS compatibility checker
* Interview preparation assistant
* Smart job recommendations

## Author

Developed by **Nikhitha Pragallapati**

GitHub: https://github.com/nikhithab5
