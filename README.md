# Remote Virtual Laboratory Platform

A professional, production-ready educational SaaS platform for remote Arduino and Raspberry Pi experiments using virtual simulation, optimized for native local execution.

## 🌟 Key Features
- **Integrated Wokwi Simulator**: Perform real embedded systems experiments in the browser.
- **Multilingual Support**: Available in English, Uzbek (O'zbek), and Russian (Русский).
- **Gamified Learning**: Earn points and badges for completing experiments.
- **Teacher Admin Panel**: Create experiments, review submissions, and grade student work.
- **Modern UI/UX**: Professional dashboard inspired by leading SaaS products.
- **Role-Based Access**: Specialized views for Students and Teachers.

## 🛠️ Technology Stack
- **Backend**: Python, Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Babel, Flask-Bcrypt
- **Frontend**: Bootstrap 5, Vanilla JS, Jinja2, CSS3 (Modern SaaS design)
- **Database**: SQLite (default) / PostgreSQL ready

## 🚀 Native Local Setup

1. **Clone and Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file based on `.env.example`.

3. **Initialize Database & Seed Data**:
   ```bash
   python seed.py
   ```

4. **Run the Application**:
   ```bash
   python run.py
   ```
   Visit: `http://localhost:5000`

## 🧪 Experiments
The platform comes pre-loaded with 8 experiments:
1. **LED Blink** (Arduino)
2. **Button Controlled LED** (Arduino)
3. **Traffic Light System** (Arduino)
4. **Temperature Sensor DHT11** (Arduino)
5. **Ultrasonic Distance Sensor** (Arduino)
6. **LED Control using MicroPython** (Pi Pico)
7. **Temperature Monitoring** (Pi Pico)
8. **Light Sensor System** (Pi Pico)

## 👤 Credentials (Default Seed Data)
- **Teacher**: `admin@lab.com` / `admin123`
- **Student**: `student@lab.com` / `student123`
