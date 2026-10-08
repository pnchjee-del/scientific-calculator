# PNC 3D Handheld Scientific & Statistical Calculator

A realistic, colorful 3D handheld calculator web application built with Python Flask, HTML5, CSS3, and JavaScript. Optimized for both **Personal Computers** and **Android devices** (smartphones & tablets), with complete step-by-step statistical calculations and deviation tables.

---

## Features
- **PNC 3D Handheld Interface**: Tactile 3D button depression, sculpted casing, simulated solar panel, and recessed LCD screen.
- **Scientific Keypad**: Trigonometric functions (`sin`, `cos`, `tan`), logarithms (`log`, `ln`), powers (`^`), roots (`√`), brackets, and constants (`π`, `e`).
- **Statistical Calculation Engine**:
  - Sample Size ($n$), Sum ($\sum x$), Sum of Squares
  - Arithmetic Mean ($\bar{x}$)
  - Median ($M$)
  - Mode ($Mo$) with unimodal, bimodal, and multimodal detection
  - Range ($Max - Min$)
  - Sample Standard Deviation ($s$) & Population Standard Deviation ($\sigma$)
  - Sample Variance ($s^2$) & Population Variance ($\sigma^2$)
  - Mean Absolute Deviation (MAD)
  - Quartiles ($Q_1$, $Q_2$, $Q_3$) and Interquartile Range (IQR)
- **Step-by-Step Solutions**: Detailed formulas, step-by-step substitutions, frequency distribution tables, and a full deviation matrix table.
- **Responsive on PC & Android**: Haptic vibration feedback on Android, PWA installable, physical keyboard shortcuts on PC.

---

## Deployment on Render (render.com)

This repository includes all required configuration files (`requirements.txt`, `Procfile`, `render.yaml`) for 1-click deployment on [Render](https://render.com).

### Step 1: Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new).
2. Run these commands in your project folder:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect the settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
5. Click **Deploy Web Service**.

Your live URL will be ready at: `https://<your-service-name>.onrender.com`!

---

## Local Development
```bash
pip install -r requirements.txt
python app.py
```
- Open on PC: `http://localhost:5000`
- Open on Android: `http://<your-local-ip>:5000` (shown in terminal)

