import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import re
import ast
from collections import Counter
import numpy as np

# Load dataset
df = pd.read_csv("processed_vacancies.csv")

# Compute average salary by city and state (top-10)
salary_by_city = df.groupby("city")["avg_salary"].mean().reset_index()
salary_by_city = salary_by_city.sort_values(by="avg_salary", ascending=False).head(10)
salary_by_state = df.groupby("state")["avg_salary"].mean().reset_index()
salary_by_state = salary_by_state.sort_values(by="avg_salary", ascending=False).head(10)

top_skills_df = pd.read_csv("top_skills.csv")
top_skills_df = top_skills_df.sort_values(by="count", ascending=False)  # Ensure correct sorting

# Сity options for dropdown
city_options = [{"label": "All Cities", "value": "all"}] + [
    {"label": city, "value": city} for city in df["city"].dropna().unique()
]

vacancies_by_year = df.dropna(subset=["founded"])
vacancies_by_year = vacancies_by_year["founded"].value_counts().reset_index()
vacancies_by_year.columns = ["Year Founded", "Vacancies"]
vacancies_by_year = vacancies_by_year[vacancies_by_year["Year Founded"] > 0]
vacancies_by_year = vacancies_by_year.sort_values(by="Year Founded")

df["industry"] = df["industry"].replace("-1", np.nan)
industry_counts = df.dropna(subset=["industry"])
industry_counts = industry_counts["industry"].value_counts().nlargest(10).reset_index()
industry_counts.columns = ["Industry", "Vacancies"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Analysis of In-Demand Skills and Salaries for Data Analysts",
                        className="text-center mb-4"), width=12)
    ),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Top-10 In-Demand Skills", className="card-title"),
                    html.Label("Select City:"),
                    dcc.Dropdown(id="city-selector", options=city_options,
                                 value="all", clearable=False),
                    dcc.Graph(id="top-skills")
                ])
            ], className="shadow-sm")
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Salary by City and State", className="card-title"),
                    html.Label("Select Data:"),
                    dcc.Dropdown(
                        id="location-type",
                        options=[{"label": "Cities", "value": "city"},
                                 {"label": "States", "value": "state"}],
                        value="city",
                        clearable=False
                    ),
                    dcc.Graph(id="salary-chart")
                ])
            ], className="shadow-sm")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Do Older Companies Post More Job Listings?", className="card-title"),
                    dcc.Graph(figure=px.line(vacancies_by_year, x="Year Founded", y="Vacancies",
                                             title="Do Older Companies Post More Job Listings?",
                                             markers=True, line_shape="spline",
                                             labels={"Year Founded": "Company Founded Year", "Vacancies": "Number of Job Listings"},
                                             color_discrete_sequence=["dodgerblue"]))
                ])
            ], class_name="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Top-10 Industries by Data Analyst Vacancies", className="card-title"),
                    dcc.Graph(id="industry-distribution",
                              figure=px.pie(industry_counts, names="Industry",
                                            values="Vacancies", title="Top-10 Industries by Data Analyst Vacancies",
                                            hole=0.3, color_discrete_sequence=px.colors.sequential.Viridis))
            ])
        ], class_name="shadow-sm")
    ], width=6)
])
], fluid=True)

@app.callback(
    Output("top-skills", "figure"),
    Input("city-selector", "value")
)

def updated_skills_chart(selected_city):
    if selected_city == "all":
        filtered_df = top_skills_df
        title = "Top-10 In-Demand Skills (All Cities)"
    else:
        city_df = df.dropna(subset=["city", "extracted_skills"])
        city_df = city_df[city_df["city"] == selected_city]

        if city_df.empty:
            return px.bar(title=f"No data available for {selected_city}")

        generic_skills = {"data analysis", "analytics", "business intelligence", "data science"}


        def parse_skills(x):
            try:
                return ast.literal_eval(x) if isinstance(x, str) else x
            except:
                return []

        city_df["extracted_skills"] = city_df["extracted_skills"].apply(parse_skills)

        all_skills = [skill.strip().lower() for skill_list in city_df["extracted_skills"] for skill in skill_list]
        all_skills = [skill for skill in all_skills if skill not in generic_skills]

        if not all_skills:
            return px.bar(title=f"No skills found for {selected_city}")

        skills_count = Counter(all_skills)
        top_skills = skills_count.most_common(10)

        filtered_df = pd.DataFrame(top_skills, columns=["skill", "count"])
        filtered_df["skill"] = filtered_df["skill"].astype(str).str.strip()
        filtered_df = filtered_df.dropna()

        filtered_df["skill"] = filtered_df["skill"].apply(lambda x: re.sub(r"[^a-zA-Z0-9\s]", "", x))
        filtered_df = filtered_df.sort_values(by="count", ascending=False)
        title = f"Top-10 In-Demand Skills in {selected_city}"

    fig = px.bar(filtered_df, x="count", y="skill", orientation="h",
                 color="count", color_continuous_scale="Viridis",
                 labels={"count": "Frequency", "skill": "Skill"},
                 title=title,
                 category_orders={"skill": filtered_df["skill"].tolist()} if not filtered_df.empty else {})

    return fig

@app.callback(
    Output("salary-chart", "figure"),
    Input("location-type", "value")
)
def update_salary_chart(location_type):
    if location_type == "city":
        filtered_df = salary_by_city
        title = "Average Salary by City"
    else:
        filtered_df = salary_by_state
        title = "Average Salary by State"

    filtered_df = filtered_df.sort_values(by="avg_salary", ascending=True)

    fig = px.bar(filtered_df, x="avg_salary", y=location_type, orientation="h",
                 color="avg_salary", color_continuous_scale="Viridis",
                 title=title, labels={"avg_salary": "Average Salary ($)", location_type: location_type})
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
