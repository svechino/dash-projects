import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv('Data_Analyst Job.csv')

# Data loading and checking:
print(df.head())
print(df.info())
print(df.isnull().sum())
print(f"Data duplicates: {df.duplicated().sum()}")

# Renaming columns:
df.columns = (
    df.columns.str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)
print(df.columns)

# EDA
# Processing salary:
def extract_salary(salary):
    match = re.findall(r"\d+", str(salary))
    if len(match)==2:
        min_salary = (int(match[0]) * 1000)/12
        max_salary = (int(match[1]) * 1000)/12
        avg_salary = (min_salary + max_salary)/2
        return min_salary, max_salary, avg_salary
    return None, None, None

df[["min_salary", "max_salary", "avg_salary"]] = df["salary_estimate"].apply(lambda x: pd.Series(extract_salary(x)))
print(df[["min_salary", "max_salary", "avg_salary"]].describe())

plt.figure(figsize=(10, 5))
sns.histplot(df['avg_salary'].dropna(), bins=30, kde=True)
plt.xlabel("Average Salary ($)")
plt.ylabel("Vacancies Number")
plt.title("Salary Distribution")
plt.show()

# Processing location:
df["city"] = df["location"].apply(lambda x: x.split(",")[0])
df["state"] = df["location"].apply(lambda x: x.split(",")[1])
top_cities = df["city"].value_counts().head(10)
top_states = df["state"].value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_cities.index, y=top_cities.values, hue=top_cities.index, palette="Blues_r", legend=False)
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Vacancies Number")
plt.title("Top-10 cities by vacancies of Data Analyst")
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=top_states.index, y=top_states.values, hue=top_cities.index, palette="Blues_r")
plt.xticks(rotation=45)
plt.xlabel("State")
plt.ylabel("Vacancies Number")
plt.title("Top-10 states by vacancies of Data Analyst")
plt.show()

# Processing companies:
top_companies = df["company_name"].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_companies.index, y=top_companies.values, hue=top_companies.index, palette="Blues_r")
plt.xticks(rotation=90)
plt.xlabel("Company Name")
plt.ylabel("Vacancies Number")
plt.title("Top-10 companies by vacancies of Data Analyst")
plt.show()

# Correlation between rating and average salary:
plt.figure(figsize=(10,5))
sns.scatterplot(x=df["rating"], y=df["avg_salary"], alpha=0.5)
plt.xlabel("Company rating")
plt.ylabel("Average Salary ($)")
plt.title("How company rating influences on salary?")
plt.show()

# Text cleaning:
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def text_clean(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)
df["clean_description"] = df["job_description"].apply(text_clean)
print(df[["job_description", "clean_description"]].head())

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def extract_skills(text):
    promt = f"""
    Analyze the following job description and extract a list of key skills.  
    Provide only the list of skills, separated by commas, without any explanations.  

    Job description:  
    {text}
    """
    response = llm.invoke([HumanMessage(content=promt)])
    return response.content.strip()

import time

batch_size = 500  # Обрабатываем 500 вакансий за раз

for i in range(0, len(df), batch_size):
    print(f"Обрабатываем {i}–{i + batch_size} вакансий...")
    df.loc[i:i + batch_size - 1, "extracted_skills"] = df.loc[i:i + batch_size - 1, "clean_description"].apply(
        lambda x: extract_skills(str(x)))

    # Сохраняем прогресс
    df.to_csv("vacancies_with_skills.csv", index=False)

    # Делаем паузу, чтобы избежать лимитов OpenAI
    time.sleep(5)



