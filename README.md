## App Requirements 

### 1) Core Features

* Users can **signup / login / logout**
* Only **authenticated users** can access feedback form
* Feedback form has **20 hardcoded questions + options**
* Form is split into **2 pages**

  * Page 1 → Q1–Q10
  * Page 2 → Q11–Q20
* On final submit: store all answers and show **success/complete page**

---

### 2) Tech & Packages

* Backend: **Flask**
* Auth: **flask_login package**
* Frontend: **Jinja2 templates**
* Validation & types: **Flask-Pydantic**
* Logging: **Loguru**
* DB: **SQLite**
* ORM: **SQLAlchemy**
* Architecture: **Blueprint modules + repository layer**

---

### 3) Auth Middleware

* Use `@login_required` on all feedback routes
* Redirect unauthorized users to `/auth/login`

---

### 4) Database Models (SQLAlchemy)

* **User**

  * id, username, email, password_hash

* **Answer**

  * id, answer_id, question_id, answer_value

* More if needed


---

### 5) Repository Layer (DB access only via repositories)

* `UserRepository`: create, fetch, verify password, etc.
* `AnswerRepository`: bulk insert answers, etc.
* More if needed
---

### 6) Blueprints

* `/auth` → signup, login, logout
* `/feedback` → page1, page2, submit, complete

---

### 7) Logging (Loguru)

Log key actions:

* signup attempt/result
* login attempt/result
* form submission start/end
* db save success/failure

---

### 8) Questions Structure

Hardcoded config like:

```python
QUESTIONS = [{"id": 1, "text": "...", "options": [...]}, ...]  # 20 total
```