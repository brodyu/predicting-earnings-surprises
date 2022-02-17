# Earnings Surprise Prediction

## Idea

In this project, we collected data from various external data providers with the goal of forecasting an earnings surprise prior to a company's earnings announcement. In our case, an earnings surprise is an actual EPS greater than a 15% change from the estimated EPS. Significant earnings surprises (positive and negative) usually correlate with respective price movements following the announcement. Our goal is to forecast the acutal EPS of a company and develop a trading strategy to long/short before an earnings announcement. 

The metric we will forecast is earnings surprise which is defined as the difference between the actual EPS and the estimated EPS: 
```python
earnings_surprise = (actual_eps - estimated_eps) / |estimated_eps| * 100
```

An earnings surprise greater than 15% is considered to be 'Positive', while an earnings surprise less than -15% is considered to be 'Negative'. Therefore, any earnings surprise greater than -15% and less than 15% is considered to be 'Neutral'.

## Data

The data used for this project was collected from three external data provider's API and stored in a MySQL database using AWS' Relational Database Service (RDS). The data is indexed further to provide training, validation, and testing data for our machine learning model. There are three types of data collected for this project: historical earnings data, pricing data, and technical price action data. 

#### Historical Earnings Data
Historical earnings data was collect from Financial Modeling Prep's Historical Earnings Calendar endpoint. This data provides insight into a company's previous earnings announcement, including earnings date, time, and analyst estimate data. Earnings data was collected for 2000+ companies that are traded on a U.S. exchange and greater than $1 billion market capitalization. All earnings data is collected from 2012 to 2022, which provides us with over 10 years to historical data. 

#### Pricing Data
For each historical earnings data point from FMP's API, we collect basic daily pricing data for the previous trading day prior to the earnings announcement. Pricing data includes the open, high, low, close, and volume. This collection of data gives us insight into the most recent information about a stock prior to their earnings announcement.

#### Technical Data
Technical or price action data was collected from various data providers and gives us insight into trends that are happening with price 5, 10, and 20 days out from a company's earnings announcement.

## Feature Engineering / Data Wrangling

Most data was filtered and cleansed of imperfections during the ETL process (see rds-mysql-pipeline repository for more information). However, we did find more nuances that required further cleansing. After removing outliers, our earnings surprise results follow a normal distribution with majority of the values ranging -300% to 300%.

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/histogram_eps_diff.png)

Moreover, we investigated the potential differences between positive, neutral, and negative earnings surprises with earnings time and differences in the day of week in which an earnings report is announced. In order to do this, we created several new features including the day of week and day of year an earnings annoucement fell on. From the bar graph below, we can see the distribution between positive, neutral, and negative earnings surprises.

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/earn_bar.png)

While majority of earnings annoucements resulted in neutral earnings, there are signifiantly more positive earnings surprises than negative earnings surprises. Therefore when developing our trading strategy, it might be more lucrative to only go long positively predicted earnings surprises. 

When breaking down historical earnings surprises by earnings time, we can see that there is no significant difference between earnings surprise and when the earnings is announced. An earnings annoucement can occur before market open (bmo) or after market close (amc).

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/earn_bar_time.png)

In order to investigate the potential differences between earnings surprise and day of week, we created new features that extract the day of week of each earnings annoucement. 

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/earn_bar_dow.png)

In contrast to common belief, a company is not more likely to host a negative earnings surprise on a Friday. The original idea was that a company would purposefully report a negative surprise on a Friday to escape the attention of the market ahead of the weekend. However in reality, the distribution of earnings surprises over the past ten years are very similar amongst all earnings surprise brackets. There is no notable increase in negative earnings surprises on Fridays. In fact, most companies prefer to report on Thursdays rather than Fridays. 
