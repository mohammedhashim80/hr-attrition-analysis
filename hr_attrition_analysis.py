"""
HR Employee Attrition Analysis
Tools: Python, Pandas, NumPy, Matplotlib
Author: Mohammed Hashim
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(10)
n = 1500

departments = ['Sales','IT','HR','Finance','Operations','Marketing']
job_roles = ['Manager','Analyst','Executive','Developer','Consultant']
education = ['High School','Bachelor','Master','PhD']

age = np.random.randint(22, 60, n)
tenure = np.random.exponential(5, n).clip(0.5, 30).round(1)
monthly_income = np.random.normal(8000, 3000, n).clip(3000, 25000).round(0)
satisfaction = np.random.randint(1, 5, n)
work_life = np.random.randint(1, 5, n)
overtime = np.random.choice(['Yes','No'], n, p=[0.3, 0.7])
dept = np.random.choice(departments, n)
role = np.random.choice(job_roles, n)
edu = np.random.choice(education, n, p=[0.1, 0.5, 0.3, 0.1])
distance = np.random.randint(1, 30, n)

attrition_prob = (
    0.3 * (satisfaction < 2).astype(float) +
    0.25 * (work_life < 2).astype(float) +
    0.2 * (overtime == 'Yes').astype(float) +
    0.15 * (tenure < 2).astype(float) +
    0.1 * (monthly_income < 5000).astype(float)
)
attrition_prob = (attrition_prob / attrition_prob.max() * 0.65).clip(0, 1)
attrition = np.where(np.random.random(n) < attrition_prob, 'Yes', 'No')

df = pd.DataFrame({
    'Employee_ID': [f'EMP{i:04d}' for i in range(1, n+1)],
    'Age': age, 'Department': dept, 'Job_Role': role,
    'Education': edu, 'Monthly_Income_AED': monthly_income,
    'Years_At_Company': tenure, 'Job_Satisfaction': satisfaction,
    'Work_Life_Balance': work_life, 'OverTime': overtime,
    'Distance_From_Home_km': distance, 'Attrition': attrition
})

df.to_csv('/home/claude/project4/hr_attrition_data.csv', index=False)

attr_rate = (df['Attrition'] == 'Yes').mean() * 100
print("=" * 50)
print("HR EMPLOYEE ATTRITION ANALYSIS REPORT")
print("=" * 50)
print(f"\nTotal Employees:  {len(df):,}")
print(f"Attrition Rate:   {attr_rate:.1f}%")
print(f"Active Employees: {(df['Attrition']=='No').sum():,}")
print(f"Left Company:     {(df['Attrition']=='Yes').sum():,}")

print("\nAttrition by Department:")
dept_attr = df.groupby('Department')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).round(1).sort_values(ascending=False)
for dept, rate in dept_attr.items():
    print(f"  {dept:<15} {rate:>5.1f}%")

print("\nAttrition by Satisfaction Level:")
sat_attr = df.groupby('Job_Satisfaction')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).round(1)
for sat, rate in sat_attr.items():
    print(f"  Level {sat}: {rate:.1f}%")

# Dashboard
fig = plt.figure(figsize=(16, 10), facecolor='#0f172a')
fig.text(0.5, 0.97, 'HR EMPLOYEE ATTRITION ANALYSIS', ha='center',
         fontsize=20, fontweight='bold', color='white')
fig.text(0.5, 0.935, f'1,500 Employees | Attrition Rate: {attr_rate:.1f}% | Python · Pandas · NumPy',
         ha='center', fontsize=11, color='#94a3b8')

colors = ['#f43f5e','#10b981','#3b82f6','#f59e0b','#8b5cf6','#06b6d4']

# KPI cards
kpis = [
    ('TOTAL EMPLOYEES', f'{len(df):,}', '#3b82f6'),
    ('ATTRITION RATE', f'{attr_rate:.1f}%', '#f43f5e'),
    ('ACTIVE STAFF', f'{(df["Attrition"]=="No").sum():,}', '#10b981'),
    ('AVG SALARY', f'AED {monthly_income.mean():,.0f}', '#f59e0b'),
]
for i, (lbl, val, col) in enumerate(kpis):
    ax = fig.add_axes([0.03+i*0.245, 0.78, 0.22, 0.12])
    ax.set_facecolor('#1e293b'); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor(col); sp.set_linewidth(2)
    ax.text(0.5, 0.70, val, ha='center', va='center', fontsize=18,
            fontweight='bold', color=col, transform=ax.transAxes)
    ax.text(0.5, 0.22, lbl, ha='center', va='center', fontsize=9,
            color='#94a3b8', transform=ax.transAxes)

# Chart 1 - Attrition by Department
ax1 = fig.add_axes([0.03, 0.43, 0.28, 0.30])
ax1.set_facecolor('#1e293b')
dept_attr = df.groupby('Department')['Attrition'].apply(lambda x: (x=='Yes').mean()*100)
bars = ax1.barh(dept_attr.index, dept_attr.values, color=colors, edgecolor='none', height=0.6)
ax1.set_title('Attrition Rate by Department (%)', color='white', fontsize=10, pad=8)
ax1.tick_params(colors='#94a3b8', labelsize=8)
for sp in ['top','right']: ax1.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax1.spines[sp].set_color('#334155')
for bar, val in zip(bars, dept_attr.values):
    ax1.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
             f'{val:.1f}%', va='center', color='white', fontsize=8)

# Chart 2 - Satisfaction vs Attrition
ax2 = fig.add_axes([0.37, 0.43, 0.28, 0.30])
ax2.set_facecolor('#1e293b')
sat_attr = df.groupby('Job_Satisfaction')['Attrition'].apply(lambda x: (x=='Yes').mean()*100)
ax2.bar(sat_attr.index, sat_attr.values, color=['#f43f5e','#f59e0b','#10b981','#3b82f6'],
        edgecolor='none', width=0.6)
ax2.set_title('Attrition by Job Satisfaction Level', color='white', fontsize=10, pad=8)
ax2.set_xlabel('Satisfaction (1=Low, 4=High)', color='#94a3b8', fontsize=8)
ax2.tick_params(colors='#94a3b8', labelsize=8)
for sp in ['top','right']: ax2.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax2.spines[sp].set_color('#334155')

# Chart 3 - Income distribution
ax3 = fig.add_axes([0.71, 0.43, 0.27, 0.30])
ax3.set_facecolor('#1e293b')
yes_inc = df[df['Attrition']=='Yes']['Monthly_Income_AED']
no_inc = df[df['Attrition']=='No']['Monthly_Income_AED']
ax3.hist(yes_inc, bins=20, alpha=0.7, color='#f43f5e', label='Left', density=True)
ax3.hist(no_inc, bins=20, alpha=0.7, color='#10b981', label='Stayed', density=True)
ax3.set_title('Income Distribution: Left vs Stayed', color='white', fontsize=10, pad=8)
ax3.tick_params(colors='#94a3b8', labelsize=8)
ax3.legend(facecolor='#0f172a', labelcolor='white', fontsize=9)
for sp in ['top','right']: ax3.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax3.spines[sp].set_color('#334155')

# Chart 4 - Overtime impact
ax4 = fig.add_axes([0.03, 0.05, 0.28, 0.30])
ax4.set_facecolor('#1e293b')
ot_attr = df.groupby('OverTime')['Attrition'].apply(lambda x: (x=='Yes').mean()*100)
ax4.bar(ot_attr.index, ot_attr.values, color=['#10b981','#f43f5e'], edgecolor='none', width=0.5)
ax4.set_title('Attrition Rate: Overtime vs No Overtime', color='white', fontsize=10, pad=8)
ax4.tick_params(colors='#94a3b8', labelsize=8)
ax4.set_ylabel('Attrition Rate (%)', color='#94a3b8', fontsize=9)
for sp in ['top','right']: ax4.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax4.spines[sp].set_color('#334155')
for i, (idx, val) in enumerate(ot_attr.items()):
    ax4.text(i, val+0.5, f'{val:.1f}%', ha='center', color='white', fontsize=10, fontweight='bold')

# Chart 5 - Age distribution
ax5 = fig.add_axes([0.37, 0.05, 0.28, 0.30])
ax5.set_facecolor('#1e293b')
yes_age = df[df['Attrition']=='Yes']['Age']
no_age = df[df['Attrition']=='No']['Age']
ax5.hist(yes_age, bins=15, alpha=0.7, color='#f43f5e', label='Left', density=True)
ax5.hist(no_age, bins=15, alpha=0.7, color='#3b82f6', label='Stayed', density=True)
ax5.set_title('Age Distribution: Left vs Stayed', color='white', fontsize=10, pad=8)
ax5.tick_params(colors='#94a3b8', labelsize=8)
ax5.legend(facecolor='#0f172a', labelcolor='white', fontsize=9)
for sp in ['top','right']: ax5.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax5.spines[sp].set_color('#334155')

# Chart 6 - Key metrics table
ax6 = fig.add_axes([0.71, 0.05, 0.27, 0.30])
ax6.set_facecolor('#1e293b'); ax6.axis('off')
stayed = df[df['Attrition']=='No']
left = df[df['Attrition']=='Yes']
rows = [
    ['Metric', 'Stayed', 'Left'],
    ['Avg Age', f"{stayed['Age'].mean():.1f}", f"{left['Age'].mean():.1f}"],
    ['Avg Tenure', f"{stayed['Years_At_Company'].mean():.1f}y", f"{left['Years_At_Company'].mean():.1f}y"],
    ['Avg Salary', f"AED {stayed['Monthly_Income_AED'].mean():,.0f}", f"AED {left['Monthly_Income_AED'].mean():,.0f}"],
    ['Avg Satisfaction', f"{stayed['Job_Satisfaction'].mean():.1f}", f"{left['Job_Satisfaction'].mean():.1f}"],
]
for r, row in enumerate(rows):
    for c, cell in enumerate(row):
        color = '#3b82f6' if r==0 else ('white' if c==0 else ('#10b981' if c==1 else '#f43f5e'))
        weight = 'bold' if r==0 else 'normal'
        ax6.text(c/3+0.02, 1-r*0.18-0.05, cell, transform=ax6.transAxes,
                color=color, fontsize=9, fontweight=weight, va='top')
ax6.set_title('Key Attrition Indicators', color='white', fontsize=10, pad=8)

plt.savefig('/home/claude/project4/hr_attrition_dashboard.png', dpi=150,
            bbox_inches='tight', facecolor='#0f172a')
print("\nDashboard saved.")
