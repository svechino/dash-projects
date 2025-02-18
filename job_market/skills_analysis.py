import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv("vacancies_with_skills.csv")

df = df.dropna(subset=["extracted_skills"])
df["extracted_skills"] = df["extracted_skills"].apply(lambda x: [skill.strip() for skill in x.split(",")])
generic_skills = {"data analysis", "analytics", "business intelligence", "data science", "[data analysis"}
all_skills = [skill for skill_list in df["extracted_skills"] for skill in skill_list]
all_skills = [skill for skill in all_skills if skill not in generic_skills]
skills_count = Counter(all_skills)
top_skills = skills_count.most_common(10)
top_skill_names = [x[0] for x in top_skills]
top_skill_counts = [x[1] for x in top_skills]
top_skills_df = pd.DataFrame(top_skills, columns=["skill", "count"])

plt.figure(figsize=(10, 5))
sns.barplot(x=top_skill_counts, y=top_skill_names, hue=top_skill_names, palette="Blues_r")
plt.xlabel("Frequency")
plt.ylabel("Skills")
plt.title("Top-10 requested skills for Data Analyst")
plt.show()

text = " ".join(all_skills)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)


plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Cloud of demand skills for Data Analyst")
plt.show()

df.to_csv("processed_vacancies.csv", index=False)
top_skills_df.to_csv("top_skills.csv", index=False)

print("🔹 Processed data has been saved as:")
print("- processed_vacancies.csv (all vacancies)")
print("- top_skills.csv (top 10 skills)")