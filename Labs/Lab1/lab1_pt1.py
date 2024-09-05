import pandas as pd
# Pandas is a fast, powerful, flexible and easy to use open source data analysis and data manipulation library built on top of the Python programming language.
import matplotlib.pyplot as plt
# Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
import numpy as np
# NumPy is the mathematical library that allows us to work with arrays, matrices, and perform mathematical operations on the data.
from scipy import stats


url = "https://raw.githubusercontent.com/DAVE3625/DAVE3625-24H/main/Lab1/data/stud.csv"

# Df btw is a common name for a dataframe in pandas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 1 : Read csv file
df = pd.read_csv(url, sep=',') # read the csv file using pandas
print("First 5 rows in the dataframe:")
print(df.head()) # print first 5 rows of the df

print("\n Summary of the dataframe:")
print(df.info())


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 2 : Replacing any empty strings with NaN so that we can handle missing values

print("\n Missing values in the dataframe:")
print(df.isna().sum()) # check for missing values
df = df.replace(r'^\s*$', np.nan, regex=True) # replace empty strings with NaN values because empty strings are not considered as missing values in pandas
print("\n Missing values in the dataframe after replacing empty strings with NaN:")
print(df.isna().sum()) # check for missing values after replacing empty strings with NaN

# Since age is not that important for the analysis, I'll just replace the missing values with the median
df['Age'].replace(np.nan, 0, inplace=True) # replace missing values in the Age column with the median)
print("\n Missing values in the Age column after replacing with the median:")
print(df.isna().sum())

# I'll drop the row with missing value in the hrsStudy column since we believe it is important for the analysis
df.dropna(inplace=True)
print("\n Missing values in the dataframe after dropping remaining rows with missing values:")
print(df.isna().sum())

# Convert columns to correct data types:  
df['Age'] = df['Age'].astype(str).astype(int) 
df['hrsStudy'] = df['hrsStudy'].astype(str).astype(int)


print("\n Summary after cleaning up data and converting columns to correct data types:")
print(df.info()) # print a concise summary of the df


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 3 : Identify and remove outliers from the FinalGrade column

# One way to easily spot outliers is to use a boxplot
# df['FinalGrade'].plot.box()
# plt.show() # Uncomment to see the boxplot

# Scipy can help with identifying outliers using the z-score
## z-score is a measure of how many standard deviations an element is from the mean
z_scores = stats.zscore(df['FinalGrade']) # calculate the z-scores of the FinalGrade column
abs_z_scores = np.abs(z_scores) # calculate the absolute z-scores

# Then we can set a threshold (3) to identify outliers and remove them
df.drop(df[abs_z_scores > 3].index, inplace=True) 

# Checking boxplot again after removing outliers
# df['FinalGrade'].plot.box()
# # plt.show() # Uncomment to see the boxplot

# Reset the index after removing the outliers
df = df.reset_index(drop=True) 
print(df.tail(5))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 4 : Add a column 'Grade' and transform the FinalGrade column into a categorical column
def convert_grade(grade):
    if grade >= 91 and grade <= 100:
        return 'A'
    elif grade >= 81:
        return 'B'
    elif grade >= 71:
        return 'C'
    elif grade >= 61:
        return 'D'
    elif grade >= 51: 
        return 'E'
    else: 
        return 'F'
    
df['Grade'] = df['FinalGrade'].apply(convert_grade) # add column 'Grade' with data from the FinalGrade column after applying the convert_grade function
print("\n First 5 rows in the dataframe after adding the 'Grade' column:")
print(df.head())
        

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 5 : Create a bar plot of the Grade column
counts = df['Grade'].value_counts() # count the number of occurrences of each grade
grade_order = ['A', 'B', 'C', 'D', 'E', 'F'] # define the order of the grades
counts = counts.reindex(grade_order, fill_value=0) # reorder the counts to match the grade_order

plt.figure(figsize=(10, 6)) # set the size of the plot
counts.plot(kind='bar', color='red') # create a bar plot of the Grade column
plt.title('Distribution of Grades')
plt.xlabel('Grade')
plt.ylabel('Nr of Students')
# plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Task 4 (Alternative Solution):
df2 = df.copy() # create a copy of the original dataframe
conditions = [
    (df2['FinalGrade'] <= 50),
    (df2['FinalGrade'] > 50) & (df2['FinalGrade'] <= 60),
    (df2['FinalGrade'] > 60) & (df2['FinalGrade'] <= 70),
    (df2['FinalGrade'] > 70) & (df2['FinalGrade'] <= 80),
    (df2['FinalGrade'] > 80) & (df2['FinalGrade'] <= 90),
    (df2['FinalGrade'] > 90)
]

values = ['F', 'E', 'D', 'C', 'B', 'A']

# create new column 'Grade' and use np.select to assign values
df2['Grade'] = np.select(conditions, values)
print("\n\n\n Alternative solution output:")
print(df2.head())

df2_count = df2.groupby('Grade').count() # count the number of occurrences of each grade
print("\n Distribution of Grades using alternative solution:")
print(df2_count.FinalGrade)

df2_count["FinalGrade"].plot.bar()
plt.show() # Uncomment to see the bar plot


