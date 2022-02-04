# Earnings Surprise Prediction

## Idea

In this project, we collected data from various external data providers with the goal of forecasting an earnings surprise prior to a company's earnings announcement. In our case, an earnings surprise is an actual EPS greater than a 15% change from the estimated EPS. Significant earnings surprises (positive and negative) usually correlate with respective price movements following the announcement. Our goal is to forecast the acutal EPS of a company and develop a trading strategy to long/short before the earnings announcement. 

## Data

The data used for this project was collected from three external data provider's API and stored in a MySQL database using AWS' Relational Database Service (RDS). The data is indexed further to provide training, validation, and testing data for our machine learning model. There are three types of data collected for this project: historical earnings data, pricing data, and technical price action data. 

#### Historical Earnings Data
Historical earnings data was collect from Financial Modeling Prep's Historical Earnings Calendar endpoint. This data provides insight into a company's previous earnings announcement, including earnings date, time, and analyst estimate data. Earnings data was collected for 2000+ companies that are traded on a U.S. exchange and greater than $1 billion market capitalization. All earnings data is collected from 2012 to 2022, which provides us with over 10 years to historical data. 

#### Pricing Data
For each historical earnings data point from FMP's API, we collect basic daily pricing data for the previous trading day prior to the earnings announcement. Pricing data includes the open, high, low, close, and volume. This collection of data gives us insight into the most recent information about a stock prior to their earnings announcement.

#### Technical Data
Technical or price action data was collected from various data providers and gives us insight into trends that are happening with price 5, 10, and 20 days out from a company's earnings announcement.

## Data Cleansing Process

Most data was filtered and cleansed of imperfections during the ETL process (see rds-mysql-pipeline repository for more information). However, we did find more 

## Feature Engineering

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/histogram_eps_diff.png)
