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

Dataset Size: 12,497 observations

Non-Default: 11,423

Default: 1,074

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

* bBureau metrics (credit utilization, delinquency ratio, etc.)

The application outputs:

* Default Probability

* Credit Score

* Risk Rating

## Exploratory Data Analysis & Key Insights

### 📈 Insights from Continuous Variable Analysis
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

#### 🏆 Final Model Selection

##### Business Objective

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

The selected model incorporates the following key features:

['age', 'loan_tenure_months', 'number_of_open_accounts',
 'credit_utilization_ratio', 'loan_to_income', 'delinquency_ratio',
 'avg_dpd_per_delinquency', 'residence_type_Owned',
 'residence_type_Rented', 'loan_purpose_Education', 'loan_purpose_Home',
 'loan_purpose_Personal', 'loan_type_Unsecured']
 
### 💼 Business Impact

#### Risk Management Benefits

* 94% Recall: Identifies nearly all high-risk borrowers

* Financial Loss Prevention: Minimizes exposure to potential defaults
  
* Regulatory Compliance: Transparent, interpretable model structure
  
#### Trade-offs Accepted

* Lower Precision (55%): More good customers may be rejected

* Opportunity Cost: Balanced against risk reduction benefits
  
* Strategic Alignment: Supports conservative lending approach
