import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------

df = pd.read_csv("../Dataset/Student_Performance_Subject_Wise_Analysis.csv")

print("Original Dataset Shape:", df.shape)


# ---------------------------------------------------
# 2. CHECK DATA
# ---------------------------------------------------

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())


# ---------------------------------------------------
# 3. REMOVE DUPLICATES
# ---------------------------------------------------

df = df.drop_duplicates()

print("\nDataset Shape After Removing Duplicates:", df.shape)


# ---------------------------------------------------
# 4. HANDLE MISSING VALUES
# ---------------------------------------------------

numeric_columns = df.select_dtypes(include=np.number).columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

categorical_columns = df.select_dtypes(include="object").columns

for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])


# ---------------------------------------------------
# 5. DATA TYPE CONVERSION
# ---------------------------------------------------

df["Student_ID"] = df["Student_ID"].astype(int)

numeric_columns = [
    "Attendance_Percentage",
    "Study_Hours_Per_Week",
    "Sleep_Hours_Per_Day",
    "Internal_Marks",
    "Assignment_Score",
    "Final_Exam_Marks",
    "Total_Marks"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# ---------------------------------------------------
# 6. CHECK DATA RANGES
# ---------------------------------------------------

print("\nMinimum and Maximum Values:")

for column in numeric_columns:
    print(
        column,
        "Min =", df[column].min(),
        "Max =", df[column].max()
    )


# ---------------------------------------------------
# 7. SUBJECT-WISE PERFORMANCE
# ---------------------------------------------------

subject_performance = df.groupby("Subject")["Total_Marks"].mean()

print("\nSubject-Wise Average Marks:")
print(subject_performance)


# ---------------------------------------------------
# 8. CLASS-WISE PERFORMANCE
# ---------------------------------------------------

class_performance = df.groupby("Class")["Total_Marks"].mean()

print("\nClass-Wise Average Marks:")
print(class_performance)


# ---------------------------------------------------
# 9. OVERALL PERFORMANCE
# ---------------------------------------------------

overall_average = df["Total_Marks"].mean()

print("\nOverall Average Marks:", round(overall_average, 2))


# ---------------------------------------------------
# 10. SAVE CLEANED DATASET
# ---------------------------------------------------

df.to_csv(
    "../Dataset/Cleaned_Student_Performance_Analysis.csv",
    index=False
)

print("\nCleaned dataset saved successfully.")


print("\nFinal Dataset Shape:", df.shape)

# ---------------------------------------------------
# 11. SUBJECT-WISE PERFORMANCE ANALYSIS
# ---------------------------------------------------

print("\n========== SUBJECT-WISE PERFORMANCE ==========")

subject_analysis = df.groupby("Subject").agg(
    Average_Marks=("Total_Marks", "mean"),
    Maximum_Marks=("Total_Marks", "max"),
    Minimum_Marks=("Total_Marks", "min")
).round(2)

print(subject_analysis)


# ---------------------------------------------------
# 12. CLASS-WISE PERFORMANCE ANALYSIS
# ---------------------------------------------------

print("\n========== CLASS-WISE PERFORMANCE ==========")

class_analysis = df.groupby("Class").agg(
    Average_Marks=("Total_Marks", "mean"),
    Average_Attendance=("Attendance_Percentage", "mean"),
    Average_Study_Hours=("Study_Hours_Per_Week", "mean")
).round(2)

print(class_analysis)


# ---------------------------------------------------
# 13. GENDER-WISE PERFORMANCE
# ---------------------------------------------------

print("\n========== GENDER-WISE PERFORMANCE ==========")

gender_analysis = df.groupby("Gender")["Total_Marks"].mean().round(2)

print(gender_analysis)


# ---------------------------------------------------
# 14. PERFORMANCE CATEGORY DISTRIBUTION
# ---------------------------------------------------

print("\n========== PERFORMANCE CATEGORY ==========")

performance_distribution = df["Performance_Category"].value_counts()

print(performance_distribution)


# ---------------------------------------------------
# 15. RESULT ANALYSIS
# ---------------------------------------------------

print("\n========== RESULT ANALYSIS ==========")

result_distribution = df["Result"].value_counts()

print(result_distribution)


# ---------------------------------------------------
# 16. GRADE DISTRIBUTION
# ---------------------------------------------------

print("\n========== GRADE DISTRIBUTION ==========")

grade_distribution = df["Grade"].value_counts().sort_index()

print(grade_distribution)

# ---------------------------------------------------
# 17. VISUALIZATIONS
# ---------------------------------------------------

# Create Charts folder
import os

os.makedirs("../Report/Charts", exist_ok=True)


# ---------------------------------------------------
# CHART 1: SUBJECT-WISE AVERAGE MARKS
# ---------------------------------------------------

subject_avg = df.groupby("Subject")["Total_Marks"].mean()

plt.figure(figsize=(10, 6))
subject_avg.plot(kind="bar")

plt.title("Subject-Wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("../Report/Charts/subject_wise_average_marks.png")
plt.show()


# ---------------------------------------------------
# CHART 2: CLASS-WISE AVERAGE MARKS
# ---------------------------------------------------

class_avg = df.groupby("Class")["Total_Marks"].mean()

plt.figure(figsize=(8, 5))
class_avg.plot(kind="bar")

plt.title("Class-Wise Average Marks")
plt.xlabel("Class")
plt.ylabel("Average Marks")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../Report/Charts/class_wise_average_marks.png")
plt.show()


# ---------------------------------------------------
# CHART 3: STUDY HOURS VS AVERAGE MARKS
# ---------------------------------------------------

study_analysis = df.groupby(
    pd.cut(
        df["Study_Hours_Per_Week"],
        bins=[0, 5, 10, 15, 20, 25, 35],
        labels=["1-5", "6-10", "11-15", "16-20", "21-25", "26-35"]
    )
)["Total_Marks"].mean()

plt.figure(figsize=(10, 6))
study_analysis.plot(kind="line", marker="o")

plt.title("Study Hours vs Average Marks")
plt.xlabel("Study Hours Per Week")
plt.ylabel("Average Marks")
plt.grid(True)
plt.tight_layout()

plt.savefig("../Report/Charts/study_hours_vs_marks.png")
plt.show()


# ---------------------------------------------------
# CHART 4: ATTENDANCE VS AVERAGE MARKS
# ---------------------------------------------------

attendance_analysis = df.groupby(
    pd.cut(
        df["Attendance_Percentage"],
        bins=[39, 50, 60, 70, 80, 90, 100],
        labels=["40-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
    )
)["Total_Marks"].mean()

plt.figure(figsize=(10, 6))
attendance_analysis.plot(kind="line", marker="o")

plt.title("Attendance vs Average Marks")
plt.xlabel("Attendance Percentage")
plt.ylabel("Average Marks")
plt.grid(True)
plt.tight_layout()

plt.savefig("../Report/Charts/attendance_vs_marks.png")
plt.show()


# ---------------------------------------------------
# CHART 5: PERFORMANCE CATEGORY
# ---------------------------------------------------

performance_counts = df["Performance_Category"].value_counts()

plt.figure(figsize=(7, 7))
performance_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Performance Category Distribution")
plt.ylabel("")
plt.tight_layout()

plt.savefig("../Report/Charts/performance_category_distribution.png")
plt.show()


print("\nAll charts created successfully!")

# ---------------------------------------------------
# 18. FACTORS AFFECTING STUDENT PERFORMANCE
# ---------------------------------------------------

print("\n========== FACTORS AFFECTING PERFORMANCE ==========")


# ---------------------------------------------------
# STUDY HOURS ANALYSIS
# ---------------------------------------------------

df["Study_Hour_Group"] = pd.cut(
    df["Study_Hours_Per_Week"],
    bins=[0, 5, 10, 15, 20, 25, 35],
    labels=["1-5", "6-10", "11-15", "16-20", "21-25", "26-35"]
)

study_factor = df.groupby(
    "Study_Hour_Group",
    observed=True
).agg(
    Average_Marks=("Total_Marks", "mean"),
    Average_Attendance=("Attendance_Percentage", "mean"),
    Pass_Rate=("Result", lambda x: (x == "Pass").mean() * 100)
).round(2)

print("\nStudy Hours Analysis:")
print(study_factor)


# ---------------------------------------------------
# ATTENDANCE ANALYSIS
# ---------------------------------------------------

df["Attendance_Group"] = pd.cut(
    df["Attendance_Percentage"],
    bins=[39, 50, 60, 70, 80, 90, 100],
    labels=["40-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
)

attendance_factor = df.groupby(
    "Attendance_Group",
    observed=True
).agg(
    Average_Marks=("Total_Marks", "mean"),
    Average_Study_Hours=("Study_Hours_Per_Week", "mean"),
    Pass_Rate=("Result", lambda x: (x == "Pass").mean() * 100)
).round(2)

print("\nAttendance Analysis:")
print(attendance_factor)


# ---------------------------------------------------
# CORRELATION ANALYSIS
# ---------------------------------------------------

study_correlation = df["Study_Hours_Per_Week"].corr(
    df["Total_Marks"]
)

attendance_correlation = df["Attendance_Percentage"].corr(
    df["Total_Marks"]
)

print("\nCorrelation Results:")
print(
    "Study Hours vs Total Marks:",
    round(study_correlation, 3)
)

print(
    "Attendance vs Total Marks:",
    round(attendance_correlation, 3)
)


# ---------------------------------------------------
# OVERALL PASS RATE
# ---------------------------------------------------

pass_rate = (
    df["Result"].value_counts(normalize=True)
    .get("Pass", 0) * 100
)

print("\nOverall Pass Rate:", round(pass_rate, 2), "%")


# ---------------------------------------------------
# BEST PERFORMING SUBJECT
# ---------------------------------------------------

best_subject = (
    df.groupby("Subject")["Total_Marks"]
    .mean()
    .idxmax()
)

best_subject_score = (
    df.groupby("Subject")["Total_Marks"]
    .mean()
    .max()
)

print(
    "\nBest Performing Subject:",
    best_subject,
    "- Average Marks:",
    round(best_subject_score, 2)
)


# ---------------------------------------------------
# BEST PERFORMING CLASS
# ---------------------------------------------------

best_class = (
    df.groupby("Class")["Total_Marks"]
    .mean()
    .idxmax()
)

best_class_score = (
    df.groupby("Class")["Total_Marks"]
    .mean()
    .max()
)

print(
    "Best Performing Class:",
    best_class,
    "- Average Marks:",
    round(best_class_score, 2)
)


print("\nFactor analysis completed successfully!")