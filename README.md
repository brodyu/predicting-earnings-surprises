# Earnings Surprise Prediction

## Idea

In this project, we collected data from various external data providers with the goal of forecasting an earnings surprise prior to a company's earnings announcement. In our case, an earnings surprise is an actual EPS greater than a 15% change from the estimated EPS. Significant earnings surprises (positive and negative) usually correlate with respective price movements following the announcement. Our goal is to forecast the acutal EPS of a company and develop a trading strategy to long/short before the earnings announcement. 

## Data

The data used for this project was collected from three external data provider's API and stored in a MySQL database using AWS' Relational Database Service (RDS). The data is indexed further to provide training, validation, and testing data for our machine learning model. 

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/histogram_eps_diff.png)
