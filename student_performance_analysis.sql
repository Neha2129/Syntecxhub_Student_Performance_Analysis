Create database student_performance_analysis;
use student_performance_analysis;
USE student_performance_analysis;

CREATE TABLE student_performance (
    Student_ID VARCHAR(20),
    Student_Name VARCHAR(100),
    Gender VARCHAR(20),
    Class VARCHAR(10),
    Section VARCHAR(10),
    Subject VARCHAR(50),
    Attendance_Percentage DECIMAL(5,2),
    Study_Hours_Per_Week DECIMAL(5,2),
    Sleep_Hours_Per_Day DECIMAL(5,2),
    Parental_Support VARCHAR(30),
    Internet_Access VARCHAR(20),
    Extracurricular_Activities VARCHAR(20),
    Internal_Marks DECIMAL(5,2),
    Assignment_Score DECIMAL(5,2),
    Final_Exam_Marks DECIMAL(5,2),
    Total_Marks DECIMAL(5,2),
    Grade VARCHAR(5),
    Result VARCHAR(10),
    Performance_Category VARCHAR(30)
);

USE student_performance_analysis;

SELECT COUNT(*) AS Total_Records
FROM student_performance;

SELECT *
FROM student_performance
LIMIT 10;

SELECT 
    Subject,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    MAX(Total_Marks) AS Highest_Marks,
    MIN(Total_Marks) AS Lowest_Marks
FROM student_performance
GROUP BY Subject
ORDER BY Average_Marks DESC;

SELECT 
    Class,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    ROUND(AVG(Attendance_Percentage), 2) AS Average_Attendance,
    ROUND(AVG(Study_Hours_Per_Week), 2) AS Average_Study_Hours
FROM student_performance
GROUP BY Class
ORDER BY Average_Marks DESC;

SELECT 
    CASE
        WHEN Study_Hours_Per_Week < 10 THEN 'Less than 10 hours'
        WHEN Study_Hours_Per_Week < 15 THEN '10-14 hours'
        WHEN Study_Hours_Per_Week < 20 THEN '15-19 hours'
        ELSE '20+ hours'
    END AS Study_Hour_Group,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    ROUND(AVG(Attendance_Percentage), 2) AS Average_Attendance
FROM student_performance
GROUP BY Study_Hour_Group
ORDER BY Average_Marks DESC;

SELECT 
    CASE
        WHEN Attendance_Percentage < 60 THEN 'Below 60%'
        WHEN Attendance_Percentage < 75 THEN '60-74%'
        WHEN Attendance_Percentage < 90 THEN '75-89%'
        ELSE '90% and Above'
    END AS Attendance_Group,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    ROUND(AVG(Study_Hours_Per_Week), 2) AS Average_Study_Hours
FROM student_performance
GROUP BY Attendance_Group
ORDER BY Average_Marks DESC;

SELECT 
    Result,
    COUNT(*) AS Total_Records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_performance), 2) AS Percentage
FROM student_performance
GROUP BY Result;

SELECT 
    Grade,
    COUNT(*) AS Total_Records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_performance), 2) AS Percentage
FROM student_performance
GROUP BY Grade
ORDER BY Total_Records DESC;


SELECT 
    Performance_Category,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    ROUND(AVG(Attendance_Percentage), 2) AS Average_Attendance
FROM student_performance
GROUP BY Performance_Category
ORDER BY Average_Marks DESC;

SELECT 
    Subject,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks
FROM student_performance
GROUP BY Subject
ORDER BY Average_Marks DESC
LIMIT 1;

SELECT
    COUNT(DISTINCT Student_ID) AS Total_Students,
    COUNT(*) AS Total_Subject_Records,
    ROUND(AVG(Total_Marks), 2) AS Average_Marks,
    ROUND(AVG(Attendance_Percentage), 2) AS Average_Attendance,
    ROUND(AVG(Study_Hours_Per_Week), 2) AS Average_Study_Hours,
    ROUND(
        SUM(CASE WHEN Result = 'Pass' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS Pass_Percentage
FROM student_performance;
