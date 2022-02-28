# Earnings Surprise Prediction

## Idea

In this project, we collected data from various external data providers with the goal of forecasting an earnings surprise prior to a company's earnings announcement. In our case, an earnings surprise is an actual EPS greater than a 15% change from the estimated EPS. Significant earnings surprises (positive and negative) usually correlate with respective price movements following the announcement. Our goal is to forecast the acutal EPS of a company and develop a trading strategy to long/short before an earnings announcement. 

One of the metric we will use to forecast EPS is earnings surprise which is defined as the percentage change between the actual EPS and the estimated EPS: 
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

### Lagging Earnings Features
While our pricing data contains lagging features with our technical price action dataset, we do not have lagged features for earnings related variables. Therefore, in our sql statement we will derive lagging indicators to feed our model with the LAG() function. In particular, we will create lagging features from the percentageChange, eps, and epsEstimated variables. The limitation of this approach is that it will decrease data size. Lagging each earnings feature is single time reduces the data size by 3.5% and two time reduces it by a total of 6.68%. For our approach we felt two lagging features were enough to capture historical trends. However, we would have prefered to increase our dataset size to account for data loss during feature lags. 

The SQL statement used to derive the lagging earnings features will be displayed below: 
```sql
SELECT *, 
LAG(perc_change) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS lastSurp, 
LAG(perc_change, 2) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS last2Surp,

LAG(eps) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS lastEps,
LAG(eps, 2) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS last2Eps,

LAG(epsEstimated) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS lastEst,
LAG(epsEstimated, 2) OVER(PARTITION BY symbol ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')) AS last2Est
FROM (
    SELECT *, COALESCE((eps - epsEstimated) / ABS(epsEstimated) * 100,0) AS perc_change
    FROM train_agg
    ORDER BY STR_TO_DATE(`date`, '%c/%e/%y')
)x
```
## Modeling
Due to this projects enphasis on machine learning infrastructure instead of modeling, we fitted a simple Random Forest Model from scikit-learn's ensemble library. The Random Forest algorithm is a supervised machine learning technique that uses multiple decision trees in parallel to predict our value. 

We can interpret the value of each feature using the feature_importances_ function from scikit-learn. As seen below, the feature with the most influence over our predicted EPS is the analysts' estimated EPS. This comes as no surprise as analysts' estimates are usually very close to the actual EPS.

![Untitled Workspace (1)](https://github.com/brodyu/predicting-earnings-surprises/blob/main/visuals/feature_import.png)
