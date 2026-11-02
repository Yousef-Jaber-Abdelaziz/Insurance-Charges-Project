# Medical Cost Prediction

A complete regression project: explore and clean the data, train **Linear, Ridge and Lasso regression**, compare them with **MSE, RMSE, MAE and R2**, save the models, and use them in a **Streamlit app** that predicts a person's yearly medical insurance charges.

## Dataset

**Medical Cost Personal Datasets** (Kaggle, by Miri Choi): https://www.kaggle.com/datasets/mirichoi0218/insurance

1338 people, 6 input columns and 1 target.

| Column | Meaning |
| --- | --- |
| `age` | age of the person |
| `sex` | female / male |
| `bmi` | body mass index |
| `children` | number of children covered by the insurance |
| `smoker` | yes / no |
| `region` | northeast / northwest / southeast / southwest |
| `charges` | **target**: yearly medical costs billed by the insurance (USD) |

## Repository structure

```
project/
├── Data/
│   ├── Original/insurance.csv              original data, never edited
│   └── Cleaned/insurance_cleaned.csv       cleaned and encoded data (created by Notebook 01)
├── Notebooks/
│   ├── 01_EDA_and_Preprocessing.ipynb      EDA, cleaning, encoding, feature importance
│   └── 02_Modeling_and_Evaluation.ipynb    split, scaling, models, evaluation, saving
├── Models/                                 scaler.pkl, linear/ridge/lasso .pkl, model_results.csv
├── Helper/
│   ├── __init__.py
│   └── helper.py                           all the reusable functions
├── Presentation/                           the .pptx file goes here
├── Images/                                 plots saved by the notebooks
├── main.py                                 Streamlit app
├── requirements.txt
├── .gitignore
└── README.md
```

## Python version

Python **3.11 or newer** (developed and tested with Python 3.12).

## Setup

Open a terminal in the project folder, then:

**Windows (PowerShell)**
```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
(In Command Prompt, activate with `venv\Scripts\activate.bat`.)

**macOS / Linux**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run

**Notebooks** - run them in this order, each one top to bottom:

```
jupyter notebook
```
1. `Notebooks/01_EDA_and_Preprocessing.ipynb` creates `Data/Cleaned/insurance_cleaned.csv` and the plots in `Images/`.
2. `Notebooks/02_Modeling_and_Evaluation.ipynb` creates all the files in `Models/`.

(The notebooks use relative paths, so start Jupyter from the project folder or open the notebooks from the `Notebooks` folder.)

**Streamlit app**

```
streamlit run main.py
```
It opens in the browser at http://localhost:8501.

## Summary of the work

1. **EDA (Notebook 01).** Checked the shape, types, missing values (none) and duplicates (1). Explored the categorical and numerical variables, outliers (kept, they are real cases), the distribution of the target (right-skewed because smokers form a second, more expensive group) and the relationship between each feature and `charges`.
2. **Preprocessing (Notebook 01).** Removed the duplicate, encoded `sex` and `smoker` as 0/1, one-hot encoded `region` (northeast is the reference), and saved the result in `Data/Cleaned/`. Scaling is **not** done here, to avoid data leakage.
3. **Feature importance (Notebook 01).** Correlation with the target, and the coefficients of a linear regression model (in real units and standardized).
4. **Modeling (Notebook 02).** 80/20 split with `random_state=42`, `StandardScaler` fitted on the training set only, then Linear, Ridge and Lasso regression.
5. **Evaluation (Notebook 02).** MSE, RMSE, MAE and R2 on the training and test sets, 5-fold cross validation (scaler inside a pipeline), and `GridSearchCV` to tune `alpha` for Ridge and Lasso.
6. **Saving (Notebook 02).** The scaler and the three models are saved with `joblib` in `Models/`, then loaded again to check that they give the same predictions.
7. **App (`main.py`).** The user enters the person's data and chooses a model. The app encodes and scales the input with the saved scaler, and shows the prediction of the chosen model and a side-by-side comparison of the three models.

## Results

Test set results (268 people):

| Model | MSE | RMSE (USD) | MAE (USD) | R2 |
| --- | --- | --- | --- | --- |
| Linear Regression | 35,478,021 | 5,956 | 4,177 | 0.8069 |
| Ridge Regression (alpha = 1) | 35,512,475 | 5,959 | 4,180 | 0.8067 |
| Lasso Regression (alpha = 100) | 36,319,439 | 6,027 | 4,202 | 0.8023 |

- The three models perform almost the same. 5-fold cross validation on the training set gives a mean R2 of about 0.72, which is a more cautious estimate than the 0.81 of one test split.
- Feature importance: **smoker** is by far the most important feature, followed by **age** and **bmi**. `children`, `sex` and `region` have a small effect, and Lasso sets `sex` and `region_northwest` to exactly zero.
- Limitations: the models under-predict the most expensive smokers (the effect of bmi is stronger for smokers), and a linear model can predict a negative value for the cheapest cases (the app shows it as $0).

## Helper functions

All the functions are in `Helper/helper.py`: `load_data`, `encode_features`, `build_input_row`, `evaluate_model`, `save_object` and `load_object`. The encoding is written once, so the notebooks and the app prepare the data in exactly the same way.
