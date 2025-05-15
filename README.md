### Cloning the Repository

1. Clone the repository using the command below:

```bash
git clone https://github.com/bharat-dir96/Tour-Packages-API.git
```

2. Move into the project directory:

```bash
cd Tour-Packages-API
```

3. Create a virtual environment:

```bash
python -m venv envname
```

4. Activate the virtual environment:

```bash
envname\Scripts\activate  # On Windows
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

### Running the App

#### 🚀 To Run the Backend

1. Move to the backend folder:

```bash
cd backend
```

2. Run the Django development server:

```bash
python manage.py runserver
```

> ⚠ The backend server will start at: `http://127.0.0.1:8000/`

**Available API Endpoints:**

* `GET /api`
* `GET /api/packages`
* `GET /api/packages/:code`

---

#### 💻 To Run the Frontend

1. Move to the frontend folder:

```bash
cd irctc-clone
```

2. Install the frontend dependencies:

```bash
npm install
```

3. Start the Vite development server:

```bash
npm run dev
```

> ⚠ The frontend server will start at: `http://localhost:5173/`

---
