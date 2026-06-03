# Brent Volatility Forecasting with GARCH and LSTM

## Project overview

This project focuses on the forecasting of Brent Crude Oil futures volatility using daily historical price data.

The objective is to compare the predictive performance of three approaches:

1. a naive persistence baseline;
2. a classical econometric model: GARCH(1,1);
3. a deep learning sequential model: Long Short-Term Memory (LSTM).

The central research question is:

> Can an LSTM model forecast the 10-day future realized volatility of Brent Crude Oil more accurately than a GARCH(1,1) model and a naive baseline?

This project was developed as part of a Machine Learning assignment in a Master 2 program in Financial Markets.

---

## Data

The dataset consists of daily Brent Crude Oil futures prices collected from Investing.com.

The sample covers the period from January 2005 to December 2024.

The raw dataset includes the following columns:

- `Date`
- `Price`
- `Open`
- `High`
- `Low`
- `Vol.`
- `Change %`

Since the dataset does not contain a column explicitly named `Close` or `Adj Close`, the column `Price` is used as the daily closing price reference.

From this price series, daily log returns are computed and used to construct the volatility-related variables.

---

## Target variable

The target variable is the annualized 10-day future realized volatility.

For each date \(t\), the target is computed from the squared daily log returns observed from \(t+1\) to \(t+10\), and annualized using 252 trading days.

The forecasting task is therefore a supervised time-series regression problem.

---

## Input features

The LSTM model uses sequences of past observations. The input features are:

- daily log return;
- absolute return;
- squared return;
- past 10-day realized volatility;
- past 20-day realized volatility.

All input variables are constructed using only information available up to the prediction date, in order to avoid information leakage.

---

## Methodology

The project compares three forecasting approaches.

### Naive baseline

The naive baseline assumes that future volatility is equal to recently observed volatility. It is used as a minimum benchmark.

### GARCH(1,1)

The GARCH(1,1) model is used as a classical econometric benchmark for conditional volatility forecasting. The model is estimated on the training set only, and its variance forecasts are converted into annualized 10-day volatility forecasts.

### LSTM

The LSTM model is used as a deep learning approach designed to exploit temporal dependencies in past returns and volatility-related variables. The model receives 30-day sequences as input and predicts the 10-day future realized volatility.

The LSTM architecture is intentionally simple:

- one LSTM layer with 64 units;
- one dropout layer with a dropout rate of 0.2;
- one dense output layer;
- MSE loss function;
- Adam optimizer;
- early stopping based on validation loss.

---

## Experimental protocol

The final modeling dataset contains 5,128 daily observations after cleaning and feature construction.

The data are split chronologically as follows:

| Subset | Start date | End date | Number of observations |
|---|---:|---:|---:|
| Train | 2005-02-01 | 2019-01-02 | 3,589 |
| Validation | 2019-01-03 | 2021-12-23 | 769 |
| Test | 2021-12-24 | 2024-12-16 | 770 |

No random split is used.

Because the LSTM requires 30-day sequences, final model evaluation is performed on the aligned test period for which all models produce forecasts.

The models are evaluated using:

- RMSE;
- MAE;
- QLIKE.

---

## Final results

The final model performances on the aligned test set are:

| Model | RMSE | MAE | QLIKE | RMSE improvement vs naive (%) | MAE improvement vs naive (%) |
|---|---:|---:|---:|---:|---:|
| Naive baseline | 0.138458 | 0.099846 | -1.018300 | 0.00 | 0.00 |
| GARCH(1,1) | 0.125186 | 0.089989 | -1.130319 | 9.59 | 9.87 |
| LSTM | 0.131255 | 0.090167 | -1.057130 | 5.20 | 9.69 |

The results show that both GARCH(1,1) and LSTM improve upon the naive baseline.

However, the GARCH(1,1) model achieves the best overall performance according to RMSE, MAE and QLIKE. The LSTM improves the naive benchmark but does not outperform the GARCH(1,1) model in this experimental setting.

The main empirical conclusion is therefore nuanced: the LSTM learns useful information from past sequences, but its additional flexibility does not translate into superior forecasting performance compared with the GARCH(1,1) benchmark.

---

## Author

Baptiste Dehay

Master 2 — Financial Markets
Machine Learning Project

ResearchGate: https://www.researchgate.net/profile/Baptiste-Dehay
Research and development website: https://www.wavetropy.com/fr/journal/finance-quantitative/

---

## Repository structure

```text
brent-volatility-lstm-garch/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── notebooks/
│   └── 01_brent_volatility_forecasting.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
├── results/
│   ├── figures/
│   ├── metrics.csv
│   ├── predictions.csv
│   ├── baseline_predictions.csv
│   ├── garch_predictions.csv
│   ├── lstm_predictions.csv
│   ├── absolute_errors.csv
│   └── lstm_training_history.csv
│
└── report/
    └── rapport_projet_lstm_brent_vol_dehay.pdf

---