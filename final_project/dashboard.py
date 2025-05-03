import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load CSV from GitHub
url = "https://raw.githubusercontent.com/RileyHan1518/weightlifting-dataset/refs/heads/main/weightlifting.csv"
df = pd.read_csv(url)

# Clean data
df = df.dropna(subset=["Athlete", "Bodyweight (kg)", "Snatch (kg)", "Clean & Jerk (kg)", "Total (kg)", "Gender"])
df = df[df["Gender"].isin(["Men", "Women"])]

# ------------------ CHART 1 ------------------
fig = px.scatter(
    df,
    x="Bodyweight (kg)", y="Total (kg)",
    color="Gender",
    title="Weight Lifted vs. Bodyweight by Gender",
    labels={"Bodyweight (kg)": "Bodyweight", "Total (kg)": "Total Lifted"},
    width=800, height=500
)
pio.write_html(fig, file="scatter_weight_vs_body.html", auto_open=False)

# ------------------ CHART 2 ------------------
top10 = df.sort_values("Total (kg)", ascending=False).groupby("Gender").head(10)
fig = px.bar(
    top10, x="Athlete", y="Total (kg)", color="Gender",
    title="Top 10 Lifters by Total (kg)",
    labels={"Total (kg)": "Total Weight"},
    width=800, height=500
)
pio.write_html(fig, file="bar_top10_total_lifters.html", auto_open=False)

# ------------------ CHART 3 ------------------
avg_by_gender = df.groupby("Gender")["Total (kg)"].mean().reset_index()
fig = px.line(avg_by_gender, x="Gender", y="Total (kg)", title="Average Total Lift by Gender")
pio.write_html(fig, file="line_avg_total_by_gender.html", auto_open=False)

# ------------------ CHART 4 ------------------
fig = px.histogram(df, x="Bodyweight (kg)", color="Gender", nbins=30,
                   title="Body Weight Distribution by Gender")
pio.write_html(fig, file="histogram_body_weight.html", auto_open=False)

# ------------------ CHART 5 ------------------
fig = px.box(df, x="Gender", y="Total (kg)", color="Gender", title="Lifted Weight Distribution by Gender")
pio.write_html(fig, file="boxplot_lift_distribution.html", auto_open=False)

# ------------------ TEXT 1 ------------------
top_heavy = df.sort_values("Bodyweight (kg)", ascending=False).groupby("Gender").head(5)
with open("top_heaviest_lifters.html", "w") as f:
    f.write("<h3>Top 5 Heaviest Lifters</h3><ul>")
    for _, row in top_heavy.iterrows():
        f.write(f"<li>{row['Athlete']} ({row['Gender']}) - {row['Bodyweight (kg)']} kg</li>")
    f.write("</ul>")

# ------------------ TEXT 2 ------------------
top_light = df.sort_values("Bodyweight (kg)").groupby("Gender").head(5)
with open("top_lightest_lifters.html", "w") as f:
    f.write("<h3>Top 5 Lightest Lifters</h3><ul>")
    for _, row in top_light.iterrows():
        f.write(f"<li>{row['Athlete']} ({row['Gender']}) - {row['Bodyweight (kg)']} kg</li>")
    f.write("</ul>")

# ------------------ TEXT 3 ------------------
top_total = df.sort_values("Total (kg)", ascending=False).groupby("Gender").head(5)
with open("top_total_lift.html", "w") as f:
    f.write("<h3>Top 5 by Total Weight Lifted</h3><ul>")
    for _, row in top_total.iterrows():
        f.write(f"<li>{row['Athlete']} ({row['Gender']}) - {row['Total (kg)']} kg</li>")
    f.write("</ul>")

# ------------------ TEXT 4 ------------------
df["Lift/Body Ratio"] = df["Total (kg)"] / df["Bodyweight (kg)"]
top_ratio = df.sort_values("Lift/Body Ratio", ascending=False).groupby("Gender").head(5)
with open("top_lift_to_body_ratio.html", "w") as f:
    f.write("<h3>Top 5 by Lift-to-Bodyweight Ratio</h3><ul>")
    for _, row in top_ratio.iterrows():
        f.write(f"<li>{row['Athlete']} ({row['Gender']}) - {row['Lift/Body Ratio']:.2f}</li>")
    f.write("</ul>")

# ------------------ TEXT 5 ------------------
strongest = df.loc[df.groupby(["Gender"])[["Snatch (kg)", "Clean & Jerk (kg)"]].idxmax().stack().values]
with open("strongest_by_lift_type.html", "w") as f:
    f.write("<h3>Strongest Lifters by Lift Type</h3><ul>")
    for _, row in strongest.iterrows():
        f.write(f"<li>{row['Athlete']} ({row['Gender']}) - Snatch: {row['Snatch (kg)']} kg, Clean & Jerk: {row['Clean & Jerk (kg)']} kg</li>")
    f.write("</ul>")
