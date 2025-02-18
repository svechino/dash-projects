# 📊 Job Market Analysis Dashboard

![GitHub repo size](https://img.shields.io/github/repo-size/svechino/dash-projects?color=blue&style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/svechino/dash-projects?color=green&style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/svechino/dash-projects?style=for-the-badge)

🔎 **A Dash-based interactive web application that analyzes job market trends for Data Analysts.**
Built using **Dash, Plotly, Pandas, OpenAI API, and LangChain** to extract and visualize in-demand skills and salary trends.

🔥 **Live demo available here**: 👉 [**Live App**](https://job-market-frosty-rain-6871.fly.dev/) 🚀  

## **📸 Application Screenshot**
![Job Market Analysis Dashboard](https://github.com/svechino/dash-projects/blob/main/job_market/Screenshot.png)

## **🛠 Features**
✅ **Top In-Demand Skills:** Extracts and visualizes the most frequently required skills for Data Analysts.
✅ **Average Salary Analysis:** Displays salary distributions by city and state.  
✅ **Company Trends:** Compares how new and established companies post job vacancies.
✅ **Industry Distribution:** Shows the distribution of job postings across different industries. 
✅ **💡AI-Powered Skill Extraction:** Uses **OpenAI's GPT model via LangChain** to extract required skills from job descriptions 

## **🔗 Technologies Used
- **Dash & Plotly** → Interactive UI and visualizations
- **Pandas** → Data processing and transformation
- **Matplotlib & Seaborn** → Additional data exploration
- **OpenAI API & LangChain** → Extracting skills from job descriptions using NLP
- **Docker & Fly.io** → Deployment

---

## **🚀 How to Run Locally**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/svechino/dash-projects.git
cd dash-projects/job_market
```

### **2️⃣ Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### **3️⃣ Set Up OpenAI API Key
1. Create a .env file in the project folder:
```bash
touch .env
```
2. Add your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key-here
```


### **4️⃣ Run the Application**
```bash
python app.py
```
### **📍 The app will be available at:**
**👉 http://127.0.0.1:8080/**

