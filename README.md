# Development of Credit Risk Model for ABC Finance

## Project Overview

ABC Finance, a Non-Banking Financial Company (NBFC) based in India, requires a sophisticated credit risk model to evaluate loan applications.

This project focuses on building a predictive credit risk model along with a credit scorecard system that categorizes loan applicants into:

* Poor

* Average

* Good

* Excellent

The scoring methodology is inspired by industry-standard frameworks such as the CIBIL scoring system, with strong emphasis on regulatory interpretability and business alignment.

## Scope of Work
### Phase 1: Development and Implementation
### 1️⃣ Model Development

Built predictive models using historical loan data.

Target variable: Default Indicator (0 = Non-Default, 1 = Default).

Dataset Size: 50000 observations

Non-Default: 45703

Default: 4297

Default Rate: ~8.6%

### 2️⃣ Scorecard Creation

Developed a scoring system:

Credit Score Range: 300 – 900

Score Formula:

* Credit Score = 300 + (1 - Probability of Default) × 600


#### Rating Classification:

300–499 → Poor

500–649 → Average

650–749 → Good

750–900 → Excellent

### 3️⃣ Streamlit UI Application

Developed a user-friendly Streamlit application where loan officers can input:

* Borrower demographics

* Loan details

* Bureau metrics (credit utilization, delinquency ratio, etc.)

The application outputs:

* Default Probability

* Credit Score

* Risk Rating

### 📂 Data Sources

The dataset was provided across three separate CSV files:

* customers.csv → 50,000 records × 12 columns

* loans.csv → 50,000 records × 15 columns

* bureau_data.csv → 50,000 records × 8 columns

Each dataset contains 50,000 observations and was merged using appropriate keys to create the final modeling dataset.
  
### Class Imbalance Analysis

Non-Default (Class 0): 45,703 observations (~91.4%)

Default (Class 1): 4,297 observations (~8.6%)

The dataset is highly imbalanced, with default cases representing only ~8.6% of total observations.

#### 🎯 Modeling Implication

Class imbalance presents challenges:

Models may bias toward predicting non-default.

Accuracy alone becomes misleading.

Recall for defaulters becomes critical.

This imbalance was addressed during model development using:

* Undersampling

* SMOTE

* SMOTE-Tomek

* Class weighting

* Hyperparameter tuning (Optuna)
  
### 🧹 Data Cleaning & Preprocessing

#### Missing Value Treatment

The column residence_type had 62 missing values.

Since this is a categorical variable, we examined its unique categories.

Missing values were imputed using the most frequent value (mode) to preserve distribution consistency.

#### Feature Segmentation

Features were divided into:

* Continuous variables

* Categorical variables

This separation ensured appropriate preprocessing techniques were applied to each type.

#### Preventing Data Leakage

After completing data cleaning:

performed the Train–Test Split before EDA and Feature Engineering (FE).

This ensures that no information from the test set leaks into the training process.

Maintains model integrity and realistic performance evaluation.

### 📊 Univariate Analysis

#### 📦 Outlier Detection – Boxplot Visualization

Initial boxplots indicated potential irregularities in:

* processing_fee

* gst

Further investigation was required.

#### 📈 Outlier Detection – Histogram Analysis

Observation

Maximum processing_fee observed:
₹5,293,543.52 (~52 Lakhs)

This appeared unrealistic.

On further inspection:

Corresponding loan_amount: ₹3,626,000

Processing fee exceeding loan amount → Clearly erroneous

#### 🧾 Processing Fee Validation

After consulting the business team:

✅ Processing fee cannot exceed 3% of loan_amount

We identified two irregular scenarios:

processing_fee > loan_amount

processing_fee > 3% of loan_amount

There are 7 exceptions where the processing_fee exceeds the loan_amount. In these cases, net_disbursement, processing_fee, and loan_amount are all zero.

All other invalid records were removed.

#### 💰 Net Disbursement Validation

Business Rule:

net_disbursement should not exceed loan_amount

Validation Results:

✅ No violations found in training dataset

✅ No violations found in test dataset

This confirms data consistency for disbursement logic.

#### 🧼 Cleaning Categorical Variables

loan_purpose Correction

Found a typo:

"Personal"

"Personaal"

Both represent the same category.

✔ Corrected "Personaal" → "Personal"

Ensured categorical consistency before model training.

## Exploratory Data Analysis & Key Insights

### 📈 Insights from Continuous Variable Analysis

#### Age-wise Credit Risk Analysis

##### 🔍 Key Observations

* Default risk decreases consistently with age.

##### Age 18–25:

* Highest default rate (~12%): Riskiest segment

##### Age 25–45:

* Gradual decline in default risk

##### Age 40–50:

* Moderate risk (~8%)

##### Age 50+:

* Safest segment (~4%)

##### Age 60–70:

* Smaller portfolio share and Stable and low default risk
  
#### Strong Predictors

The following variables show strong positive relationship with default probability:

* loan_tenure_months

* delinquent_months

* total_dpd

* credit_utilization_ratio

Higher values → Higher likelihood of default.

#### Weak / Neutral Predictors

Many continuous variables showed limited individual predictive power.

Surprisingly, loan amount and income did not show clear direct relationship with default.

💡 Feature Engineering Insights

🔹 Loan-to-Income (LTI) Ratio

 Combining loan amount and income may improve predictive power.

 Finding:

Default risk increases significantly when LTI ≥ ~2.5

Indicates repayment stress when loan size is large relative to income

🔹 Loan-to-Value (LTV) Ratio

Low LTV → Very low default risk

Borrowers with higher equity show stronger repayment behavior

#### 📊 Delinquency Ratio

Formula:

Delinquency Ratio = Delinquent Months / Total Loan Months

* KDE Plot Observations

Non-defaulters concentrated near 0

Defaulters show right-shifted distribution

Strong separation at higher values

Credit Interpretation

Low ratio → Low risk

High ratio → Strong default indicator

#### 📊 Avg DPD per Delinquency

Formula:

Avg DPD = Total Days Past Due / Delinquent Months

* Observations

Non-defaulters show low values

Defaulters show significantly higher values

Strong separation in distribution

Credit Interpretation

Higher Avg DPD → Severe delinquency behavior

Strong indicator of elevated credit risk

#### 🧹 Data Cleaning & Feature Selection

Removed Columns

cust_id and loan_id (unique identifiers)

Business-excluded variables (as per stakeholder guidance)

* Multicollinear variables (based on VIF analysis)

Loan amount and fee-derived features removed due to high VIF

Remaining features exhibit acceptable multicollinearity levels.

#### 📊 Categorical Feature Selection

Used:

Weight of Evidence (WOE)

Information Value (IV)

Selected features with:

IV > 0.02

#### 🤖 Model Training Strategy

* Strategy 1: Baseline Models (No Imbalance Handling)

Logistic Regression

Random Forest

XGBoost

* Strategy 2: Undersampling Approach
  
Logistic Regression with undersampling

XGBoost with undersampling

* Strategy 3: Oversampling Techniques
  
Logistic Regression with SMOTE

Logistic Regression with SMOTE-Tomek

Hyperparameter optimization using Optuna

* Strategy 4: Advanced Oversampling
  
XGBoost with oversampling

Hyperparameter optimization using Optuna

### 🏆 Final Model Selection

#### Business Objective

* Maximize Recall for Class 1 (Defaulters).

Why?

False Negative = High-risk customer approved

Leads to:

* Credit losses

* NPAs

* Higher provisioning

* Regulatory risk

#### Final Selected Model: Logistic Regression

Although XGBoost achieved slightly better accuracy, Logistic Regression demonstrated significantly higher recall for defaulters.

| Metric    | Class 0 (Non-Default) | Class 1 (Default) |
| --------- | --------------------- | ----------------- |
| Precision | 0.99                  | 0.55              |
| Recall    | 0.93                  | 0.94              |
| F1-Score  | 0.96                  | 0.70              |

Accuracy: 93%

Recall (Default): 94%

In this credit risk modeling project, the primary business objective is to maximize recall for the default class (Class 1).

In lending, a False Negative (FN) represents a high-risk customer incorrectly classified as low-risk.
This leads to:

* Credit losses
  
* Increased Non-Performing Assets (NPAs)
  
* Higher provisioning requirements
  
* Regulatory and capital risk
  
Therefore, minimizing missed defaulters is more important than maximizing overall accuracy.

Although XGBoost achieved higher overall accuracy and F1-score, Logistic Regression demonstrated significantly higher recall for the default class.

This means Logistic Regression misses fewer high-risk borrowers, directly reducing potential financial losses.

The trade-off:

Lower precision (more good customers may be rejected)

Slightly lower overall accuracy

However, given the stated business objective of prioritizing risk containment over portfolio growth, this trade-off is acceptable.

Note: Logistic Regression was selected as the final model because it:

* Meets regulatory expectations

* Provides strong recall for defaulters

* Is highly interpretable

* Integrates naturally with credit scorecards

* Offers excellent discriminatory power (ROC-AUC: 0.9838, Gini: 0.9675)

While XGBoost achieved strong predictive performance, Logistic Regression aligns better with real-world credit risk governance and business requirements.

##### Rationale:

Highest Recall (0.94): Captures 94% of actual defaulters

Business Alignment: Minimizes false negatives (missed high-risk customers)

Regulatory Compliance: High interpretability for regulatory requirements

Risk Management: Prioritizes risk containment over portfolio growth

Trade-off acceptable given risk-first business objective.

### Model Validation Metrics

#### Discriminatory Power

ROC-AUC: 0.9838 (Excellent discrimination)

Gini Coefficient: 0.9675 (Exceptional model performance)

#### Risk Segmentation (Decile Analysis)

KS Statistic: 86.09% (Very strong separation)

Decile 10: Captured ~84% of total defaults with 72% default rate

Deciles 9-10: Identified nearly 99% of all defaults

#### 🎯 Final Model Features

The final Logistic Regression model was built using the following selected features:

##### Continuous Features

* Age

* Loan Tenure (Months)

* Number of Open Accounts

* Credit Utilization Ratio

* Loan-to-Income Ratio

* Delinquency Ratio

* Average DPD per Delinquency

 ##### Categorical Features

* Residence Type (Owned/Rented/Mortgage)

* Loan Purpose (Education/Home/Personal/Auto)

* Loan Type(Unsecured/Secured)

### 💼 Business Impact

#### Risk Management Benefits

* 94% Recall: Identifies nearly all high-risk borrowers

* Financial Loss Prevention: Minimizes exposure to potential defaults
  
* Regulatory Compliance: Transparent, interpretable model structure
  
#### Trade-offs Accepted

* Lower Precision (55%): More good customers may be rejected

* Opportunity Cost: Balanced against risk reduction benefits
  
* Strategic Alignment: Supports conservative lending approach

## 🛠️ **Tools & Technologies Used**

Programming & Libraries

**Python** – Core programming language

**Pandas** – Data manipulation and preprocessing

**NumPy** – Numerical computations

**Scikit-learn** –

1. Model evaluation

2. Feature scaling

3. Hyperparameter tuning (RandomizedSearchCV)

**Optuna** - hyperparameter optimization software framework

**Logistic Regression** and  **XGBoost** – Regression models 

**Joblib** – Model and scaler persistence

**Data Visualization & Analysis**

**Matplotlib** – Basic plotting

**Seaborn**– Statistical visualizations and EDA

## **Web App & Deployment**

**Streamlit** – Interactive web application

**Streamlit Cloud** – Model deployment

**Version Control & Collaboration**

**Git** – Version control

**GitHub** – Code hosting and collaboration

**Development Environment**

**Jupyter Notebook** – Exploratory data analysis and model development

**PyCharm** - Development tool

**Git Bash** – Git operations


## 🖥️ **How to Use the App**

  Open the Streamlit app in your browser through this URL : https://abc-credit-risk-model-bklzssce28hywrhsqcuxqh.streamlit.app/
  
  Enter customer details such as:
  
  Age
  
  Income

  Loan Amount
  
  etc
  
  Click **Calculate Risk**
  
  View:
  
  Default Probability

  Credit Score

  Rating
