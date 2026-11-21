import pandas as pd
import matplotlib.pyplot as plt

# Step I : Load The dataset
data = pd.read_csv("sample_data_cleaning_project.csv")
print(data)

# Step II : Identify Missing values
print("\nMissing values count:")
print(data.isnull().sum())

# Step 3 : Handle Missing Values
data['Age'] = data['Age'].fillna(data['Age'].median())
data['Salary'] = data['Salary'].fillna(data['Salary'].mean())

data = data.dropna(subset=['Join_Date']) 
print("Data after handling missing values")
print(data)

# Step 4 : Check and remove duplicate rows
data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
data = data.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
print(data)

# Remove Duplicates
data = data.drop_duplicates(subset=['Name', 'Age'])
print("Data after removing duplicates")
print(data)

# To get number of duplicates
print("Number of Duplicates=", data.duplicated().sum())

# Step 5 : Handle Outliers
# Calculate IQR for salary
Q1 = data['Salary'].quantile(0.25)
Q3 = data['Salary'].quantile(0.75)
IQR = Q3 - Q1

# Filter the outliers
data = data[(data['Salary'] >= Q1 - 1.5 * IQR) & (data['Salary'] <= Q3 + 1.5 * IQR)]
print("Data after filtering Outliers")
print(data)

# Step 6 : Convert data types
data['Join_Date'] = pd.to_datetime(data['Join_Date'])
print("Data after changing Data Type of Join_Date")
print(data)

# Step 7 : Encode Categorical Variables
data = pd.get_dummies(data, columns=['Department'], drop_first=True)
binary_columns = [col for col in data.columns if col.startswith('Department_')]
data[binary_columns] = data[binary_columns].astype(int)

# Step 8 : Save the Dataset
data.to_csv("cleaned_data.csv", index=False)
data = pd.read_csv("cleaned_data.csv")

# Display first few rows of the dataset
print("First few rows of the dataset")
print(data.head())

# Bar chart from Departments
department_counts = data[['Department_HR', 'Department_IT']].sum()

# Plotting Department distribution
department_counts.plot(kind='bar', color=['blue', 'green'], figsize=(8, 6))
plt.title("Department Distribution")
plt.xlabel("Department")
plt.ylabel("Numbers of Employees")
plt.xticks(ticks=[0, 1], labels=["HR", "IT"], rotation=0)
plt.show()

# Histogram for Salary
plt.figure(figsize=(8, 6))
plt.hist(data['Salary'], bins=10, color='orange', edgecolor='black')
plt.title("Salary Distribution")
plt.xlabel('Salary')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# To plot a line graph for Age and Salary
plt.figure(figsize=(8, 6))
plt.plot(data['Age'], data['Salary'], marker='*', linestyle='-', color='purple')
plt.title("Salary vs Age")
plt.xlabel("Age")
plt.ylabel("Salary")
plt.grid(True)
plt.show()

# Scatter plot for Salary and Department
plt.figure(figsize=(8, 6))
colours = ['blue' if dept == 1 else 'green' for dept in data['Department_HR']]
plt.scatter(data['Salary'], data['Age'], c=colours, alpha=0.7, edgecolor='black')
plt.title("Salary vs Age by Department (HR in Blue and IT in Green)")
plt.xlabel('Salary')
plt.ylabel("Age")
plt.grid(True)
plt.show()
