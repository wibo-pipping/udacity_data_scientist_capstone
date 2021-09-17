# Introduction - Stock Price Indicator
This repository contains all the code required to get a webapp running that uses facebook prophet to predict the stock price for a limited number of tickers. Current ticker supported are `AAPL`, `GOOG`, `MSFT`, `AMZN`, and `ASML`.

## Extending supported tickers
Supported tickers are read from [prophet_params.json](./params/prophet_params.json) at startup of the webapp. To extend supported trackers include them in the prophet_params.json and restart the webapp. Adding the tickers can be done by adding a valid JSON object with supported facebook prophet params, example:

```json
{"NEW_TICKER_NAME": {
   "changepoint_prior_scale": 0.45,
   "changepoint_range": 0.9,
   "seasonality_prior_scale": 10
   }
}
```

## How to run:
Requires python 3.8 or higher to run
To start the webapp on your local machine first make sure the requirements are installed by running: `pip install -r requirements.txt`

Then from the root folder of the directory run:
`python app/main.py`

The web app should now be running and available on [`http://192.168.0.182:5000/`](http://192.168.0.182:5000/).


## Project Definition
For this project, a stock price predictor using daily historic trading data to estimate the stock **adjusted close** value in the next 180 days was implemented. An interactive webapp serves as a user interface to pick a stock of interest and plot both the historic and future value on screen in a line chart.

This project can be divided in three major parts:
1. A ML model to predict the stock ticker prices
2. Collection and preprocessing of data for the model
3. A webapplication to collect user input and visualise the output of the ML model
   
For the ML part of the project [facebook prophet](https://pypi.org/project/fbprophet/) was used to create the forecasts. Stock ticker data is retrieved from [Yahoo! Finance](https://finance.yahoo.com/) to get the adjusted close values. The webapplication was implemented using a combination of [Flask](https://flask.palletsprojects.com/en/2.0.x/) for the framework and Plotly for the visualisation.


### Problem Statement
Estimate the Adjusted Close price of stock based on historical daily trading data over a certain date range. The stock ticker symbol and date range are input for the model to return estimated prices.

### Metrics
To evaluate the model performance the Mean Absolute Percentage Error (MAPE) score was used. The MAPE score was selected over Root Mean Squared Error (RMSE), Mean Squared Error (MSE) and Mean Abosolute Error (MAE) as it fit best for this particular project. The MAPE score is easy to understand, especially when placed in the context of stock prices. The percentage error here makes sense, as overall portfolio performance is also reported in percentage gained or lost.

As each stock was trained on its own model (see [Training the forecast model with prophet](#training-the-forecast-model-with-prophet) for more info) the MAPE score is very easy to compare between the different stocks. As the stocks prices can differ in the overall range they report in (`GOOG` for example is a lot more expensive than `GLPG`) making the MAE and MSE, not reporting in ratios but in actual number, blow the error on the high value stocks out of proportion.

The RMSE score suffers from the same issue, as it uses the value of the error directly it makes it hard to compare the error across different stock tickers. Again, as the models are fitted towards single stocks, it becomes hard to compare the comparison across the models based on quantified numbers over ratios or percentage errors.

Using the MAPE opens up adding additional information to the visualisation in the language the user expects, percentages. For this particular timeseries optimisation the MAPE score also doesn't suffer from some of its pitfalls, like not being able to handle division by 0.

MAPE formula:
![alt text](assets/mape_score_formula.png "MAPE score formula")
- *n* being the number of times the summation iteration happens
- *A<sub>t</sub>* the actual value
- *F<sub>t</sub>* the forecasted value

As the problem is a time series problem, simple cross validation is not an option as that does not take into account the temporal aspect of the data. In stead, the models are evaluated on the full data set minus the last forecast horizon of data. 


## Data Exploration & Visualisation

### Evaluating and selecting data API for historic data
For the data APIs both [Quandl](https://www.quandl.com/) and [Yahoo! Finance](https://finance.yahoo.com/) where evaluated, both through the python packages available online. Both of the APIs provide very similar data in a somewhat different structure. Yahoo!'s API was selected over Quandl with the main reason being it was easier to use and it does not require any login or API key.

### Historic data investigation
Downloading the data for one ticker symbol through the API for a period of a year returns a pandas DataFrame, making it very conventient to process it after. The data set includes the Date, the Open, High, Low, Close, Adj Close and Trading Volume. For this project we will only be using the Date and Adj Close columns.

The Date field is set as the index and inspection shows its loaded as a DatetimeIndex, conventient as this opens up out-of-the-box pandas time series functions like the `window()` and `resample()` functions

After downloading the shape of the DataFrame was checked, where the expected number of rows should be 365, 1 row for each day, this returned 252. There are some missing days of data. Closer inspectection on the data shows that its mostly weekends and some holidays that are missing, this makes sense as on theses days the stock market is closed. Using `resample()` the missing data was generated to ensure one data point per day, see [Data Preprocessing](#data-preprocessing) for more details.

There are no duplicate date values, and all columns are floats with the only exception being the Volume, which is an integer. There are no missing values for the ticker symbol (`GOOG`) inspected.

#### Exploring different stock tickers
For this step 2 years of data for a selection of ticker symbols was downloaded (see table for which ticker symbols). Using the `describe()` function on the adjusted close data shows different data point counts, different mean values and different min and max values, that differ quite greatly. This might be a potential issue in training a generic model if we don't rescale the data.

|       |   AAPL |   ADYEN.AS |   AGN.AS |   AKZA.AS |    AMZN |   ASML |   GLPG |    GOOG |   MSFT |
|:------|-------:|-----------:|---------:|----------:|--------:|-------:|-------:|--------:|-------:|
| count | 505    |     514    |   514    |    514    |  505    | 505    | 505    |  505    | 505    |
| mean  | 103.87 |    1451.04 |     3.11 |     85.64 | 2770.68 | 444.36 | 142.51 | 1761.51 | 207.09 |
| std   |  30.10 |     589.74 |     0.69 |     12.38 |  643.69 | 176.91 |  58.95 |  503.24 |  45.99 |
| min   |  53.54 |     570.00 |     1.46 |     46.50 | 1676.61 | 194.67 |  54.97 | 1056.62 | 131.92 |
| 25%   |  73.96 |     821.95 |     2.47 |     79.82 | 2009.29 | 292.10 |  82.19 | 1372.56 | 167.39 |
| 50%   | 114.24 |    1474.50 |     3.35 |     84.61 | 3104.00 | 374.67 | 138.50 | 1541.44 | 209.06 |
| 75%   | 128.20 |    1908.07 |     3.64 |     92.81 | 3272.71 | 585.87 | 199.84 | 2095.38 | 240.44 |
| max   | 156.69 |    2776.00 |     4.24 |    107.80 | 3731.41 | 889.33 | 274.03 | 2916.84 | 305.22 |

Creating a simple plot shows how big the differences actually are between the different tickers. Note that the data for the plot was transformed using:
```python
adj_close = (df['Adj Close']
             .fillna(method='ffill', axis=0) # Backfill initial missing days per row
             .resample('D') # Resample, fills in missing days
             # Fill na the newly generated row. This function is a resampler so does not support axis argument
             .fillna(method='ffill') 
            )

# Add the rolling 7 day window
adj_close.rolling(7).mean());
```

![7 day rolling window](./assets/eda_plot_7d_rolling_tickers.png)


### Initial price estimates & prophet output
For the forecasting/estimating of the prices the [facebook prophet](https://pypi.org/project/fbprophet/) package was used. The package expects as input a DataFrame with a `ds` column for the date and a `y` column for the value to be estimated. As mentioned [above](#historic-data-investigation) this fits perfectly with what we want to predict, namely the adjusted closing price for a stock.

As the missing data was backfilled ([see Data Preprocessing](#data-preprocessing)]) the input data now has two columns with the Date (ds) and Adj Close (y) that we require to create an initial prediction and investigate the output.

The estimator returns a pandas DataFrame with the following columns of interest:
- ds; the date of the estimation
- yhat; estimated value
- yhat_lower & yhat_upper; lower and upper bound of the uncertainty interval

### Line graph visualisation
As this is time series data with an interest in daily values, a line chart was selected to display both the historic and estimated data. See example below.

![alt text](assets/plotly_example_visualisation.png "MSFT ticker symbol example")

The graph uses the 7-day moving average as the historic line and plots the daily estimated price as individual markers.


## Methodology

### Data Preprocessing
Data preprocessing is only necessary on the historic data retrieved through the [Yahoo! Finance API](https://finance.yahoo.com/). As mentioned in [above](#historic-data-investigation), the data from the API suffers from missing days of data due to the stock markets being closed. To fill in the missing data  `resample('D')` was used to generate the missing days of data in the dataframe. This creates NULL values for the days with missing data. As the markets are closed on these days we assume the Adj close prices do not change during this days. Therefore we can use the last known value to fill the missing values, for this the `.ffill()` function is used to carry forward the last known closing prices.

### Implementation
The full project is implemented as a webapp and all steps, from data collection through forecasting all the way down to the visualisation is captured through the webapp. When initially launched the webapp displays a dropdown menu where a stock ticker symbol can be selected to retrieve the historic data and estimate the future values for said ticker. The main goal was to create a no code solution for users to get an idea of how their stock of interest could perform in the future. This means all complex logic is hidden from the frontend webapp.

In the development process a series of Jupyter notebooks where used to prototype and design the data retrieval from both [Yahoo finance](working_documents/Yahoo%20finance.ipynb) and [Quandl](working_documents/Quandle%20test.ipynb) (for Quandle a wrapper was made to ensure the API would not be pushed to a public github repository). The [Yahoo notebook](working_documents/Yahoo%20finance.ipynb) was used to include tests of Plotly, facebook prophet and implementing a gridsearch to tune the parameters for prophet.

The following sections discuss in more detail which decisions where made during the implementation.

#### Picking a framework for the webapp
Initally [FastAPI](https://fastapi.tiangolo.com/) was explored as the framework to use. FastAPI offers rapid development of webapps in python and as its based on Pydantic it comes with very strong documentation possibilities through OpenAPI documentation pages. For visualisation [bokeh](https://docs.bokeh.org/en/latest/index.html) had my interest for visualising the data. The bokeh python package is a wrapper around the very powerful D3 Javascript library, opening the possibilites for some fun visualisations like a OHLC or candlestick graph. This combination proved to be quite troublesome as bokeh has quite a steep learning curve and FastAPI as a webframework is relatively young so there aren't as many online resource available compared to the popular [Flask](https://flask.palletsprojects.com/en/2.0.x/).

This quickly led to a refactor from FastAPI to Flask, but still with bokeh as the go to for visualising the graph. I was pretty set on getting a Candle stick graph up and running in the webapp and found some nice resources. After giving this a try for a while I decided to swap out bokeh for Plotly. bokeh required more javascript knowledge to get working in the webapp. This combined with the availability of online resources for Flask+Plotly supported the decision to swap out bokeh before I got in too deep.

After giving the candle stick visualisation a go with Flask+Plotly it became clear that the webrendering template for Flask was lacking support for the candle stick graph. This required an approach to pre-render the full webpage or build a full backend server setup. This was outside of the scope of the current project, as the ML part also would requier some attention soon. This led to the decision of exposing the results as a line + scatter plot instead.

#### The webapp subparts
All of the python files needed to run the webapp are in the `.app/` folder, `main.py` has the Flask framework logic and ties together how the different subparts work together. The webapp has two different "states" which are determined by how the homepage is accessed. 
- A GET request will produce a webpage with the dropdown to select a ticker symbol of choice
- A POST request with the ticker symbol data will trigger the data download, forecast and eventually will display a table with the last 7 days of data plus a line graph with the full history 7-day rolling average and points for the 180 day forecast.

The idea behind the current setup is to make it modular and work with protocols/contracts between each section. This enables the app to be extended or models to be swapped out without affecting the flow of the overall program.

All the functions have a doc string to understand in detail what they achieve. For completeness here is a summary:
- **common.py**; contains common functions needed across the application
- **data.py**; Logic to download the data from yahoo finance and preprocess, `get_clean_ticker_data()` gets the ticker data cleaned and enriched with 7-day rolling mean.
  - `get_ticker_data()`; Download the ticker data from Yahoo finance
  - `preprocess_ticker_data()`; Preprocess by filling missing days with last known values
  - `enrich_ticker_data()`; Add 7-day rolling window, seperate function to allow easy extension
- **forecast.py**; Implementation of facebook prophet. Requires a JSON file with params in `./params` to provide optimized model params.
  - `forecast_data()`; Wrapper function to execute the forecast, renames forecast column to y and use index as date.
  - `get_prophet_params()`; Gets the model params from [./params/prophet_params.json](./params/prophet_params.json)
  - `forecast_with_prophet()`; Use the prophet params and input data to generate forecast
- **graph.py**; Graphing logic for the webapp, should return a JSON representation Plotly JS understands.
  - `generate_line_graph_json()`; Creates the line graph, adds a vertical line for today and adds the estimated values as points to the line graph. Sets the HoverTemplate for the objects to be plotted.


All of the templates are in the [./app/templates](./app/templates/) folder. The app has a `layout.html`, as the name implies, it tells the app the actual layout. The `home.html` template extends the layout with more details on the actual content blocks to be populated.


#### Notebook descriptions, working documents
**[Quandle test](working_documents/Quandle%20test.ipynb)**:
In this notebook the Quandl API was used to download a set of energy data and use the Bokeh python library to plot the information on a map of the United States. The Bokeh map was based on an public Dataset and demo on the World War II THOR data set. See [bokeh plot test - WWII THOR dataset](working_documents/Bokeh%20plot%20test%20-%20WWII%20THOR%20dataset.ipynb) for the notebook loading this data and making a simple Bokeh plot. To use the Quandle notebook a `.env` file is required in the root directory of the project with a value for `QUANDLE_API_KEY=<your_key_here>`, <u>this is not provided in the repo</u>. This prompted me to pick the Yahoo API over the Quandle API.

The data in the Quandle and Bokeh use energy production data per state as the initial idea for the project was to implement a forecast around energy consumption and production in the US. The webapp then would function as a interactive dashboard to enrich some of the data with type of energy produced (green, oil, gas, coal), population size per state and some interesting supporting graphs like population growth vs increase in energy production. This migrated to the stock ticker due to the idea being a bit ambitious and the green production data I was looking for not being freely available in an online data store.

**[Yahoo finance](./working_documents/Yahoo%20finance.ipynb)**:
This notebook is the basis for the full project and as the project was moving along parts where split out and moved to their own sections. [Forecasting parameter tuning](./working_documents/Forecasting%20parameter%20tuning.ipynb) describes how facebook prophet was used in combination with a gridsearch to optimize the parameters per ticker symbol. [Create graph on forecasted data](working_documents/Create%20graph%20on%20forecasted%20data.ipynb) uses a csv data dump from the facebook prophet forecast to create a Plotly graph object with a combination of graphical objects and plotly express plotting.

**Included datasets**:
- World War II THOR dataset; See [reference documentation](https://programminghistorian.org/en/lessons/visualizing-with-bokeh#the-basics-of-bokeh) for more information on the dataset
- Shapefiles; These are shapefiles for GeoPandas to create a map of the US with states to plot data. This is not being used in the actual application but it is still here as part of the brainstorming process.
- seds_tpopp_all_states.txt; Reference from the Quandle API to get energy consumption data per state. 





### Refinement
#### Training the forecast model with prophet
To get the estimates [facebook prophet](https://pypi.org/project/fbprophet/) was used to estimate the value of stock tickers up to 180 days ahead. The data for a select set of tickers was downloaded:
- `AAPL`; Apple
- `GOOG`; Google
- `MSFT`; Microsoft
- `ADYEN.AS`; Adyen
- `AMZN`; Amazon
- `AGN.AS`; Aegon
- `AKZA.AS`; AkzoNobel 
- `ASML`; ASML
- `GLPG`; Galapagos

The selection for this tickers was made to a selection of a few large tech companies, assuming they would behave more or less the same when it comes to seasonal patterns in the data. To validate a few non-tech companies where included like Aegon, a large insurance company, Adyen (payment provider), AkzoNobel (manufactures performance coatings and paints) and Galapagos (bio-tech in medicine development). After selecting the ticker symbols the following steps where taken for each:
- Download data for ticker symbol
- Pre-process data and fit to Prophet model
- Create estimates for the ticker
- Evaluate model using a period of data that was left out, in this case 180 days

The results for the default parameters ranged from very good (~10% MAPE) to very bad (~50% MAPE). After looking at the data this is where the decision was made to train the models per ticker symbol to get the best performing model per ticker. The different ticker symbols from different industries showed that they require a wildly different set of parameters to get some performance. See [Refinement](#refinement) for model improvements.

During this initial fitting phase one of the parameters that turned out to be a strong contributer to prediction was the yearly seasonality. Yearly seasonality only works if there is atleast 1.5 years of data available. **This is why the minimum start date by default is set to 2019-01-01** for the retrieve data function.

The next step was to use a grid search to identify a general range for param optimisation. For more on this please read [Forecasting parameter tuning](forecasting_parameter_tuning.md) The Mean Abosolute Percentage Error (`MAPE`) was used to evaluate model performance during the grid search. See [Metrics](#metrics) for the formula.


### Improving the visualisation
As this is stock data an candle plot or OHLC plot would be a nice fit as it not only shows the latest value of the stock, it also gives some information on the volatility of the stock over time. The intial attempts in Bokeh where quite straight forward as there is an out-of-the-box option for such a plot. Even after swapping plotting library to Plotly the OHLC plot in a local notebook worked like a charm. Unfortunately this hit a bit of a roadblock when it comes to passing the JSON object through Flask to render the same plot in the webapp.

This made me rethink the visualisation I wanted to do and I ended up with updating the visualisation, replacing the OHLC plot with a line chart displaying the 7-day moving average. This shows the trend of a stock much more clearly as it removes some potential high outliers. After the initial visualisation was up an running, and the forecasting data was added as points the visualisation was enchanced by picking complementary colors and adding a vertical line for the date of today, the date from where the forecast starts.

Example Open, High, Low, Close (OHLC) chart
![Example Open, High, Low, Close (OHLC) chart](./assets/ohlc_chart_example.svg "Example Open, High, Low, Close (OHLC) chart")


## Results

### Model Evaluation & Validation 
The facebook prophet models where trained using a gridsearch. After an initial inspection a set of three parameters where picked to optimize `changepoint_prior_scale`, `changepoint_range`, and `seasonality_prior_scale`. These values influence how heavy a change point in the trend should weigh, how much data to use to determine changepoints and how heavy the seasonality aspect should factor in the fine estimation.

For the parameter grid to investigate the below values where picked, based on the default values prophet sets. For each of the param ranges both lower and higher values where picked. 

```json
{
   "changepoint_prior_scale":[0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
   "yearly_seasonality":["auto"],
   "seasonality_prior_scale":[2, 5, 10, 20],
   "changepoint_range": [0.8, 0.9, 1.0]
}
```
<sub>*The yearly seasonality was set to auto, but due to the range of the input this was always true</sub>

All of the data was trained on the full set minus the last 180 day horizon. The evaluation below is visualised as heatmaps to make it easier to spot correlations. After the initial performace evaluation `AGN.AS`, `GLPG` and `AKZA.AS` where dropped from the supported ticker list. The current set of parameters did not work for these symbols and as the decision was made to train one model per ticker this doesn't influence the actual model, only the list of supported tickers.

![Average evaluation output](./assets/output_4_0.png)

As can be seen in the heatmap, the tickers have different preferences to what influences their performance. `AAPL` shows a better performance for a higher value of the changepoint range and a higher value than default for the changepoint prior scale whereas `MSFT` best performing param sets have the lowest possible values for changepoint prior scale. In the end the decision to make one model per ticker was made based on the heatmap, showing that the average value for all has a poor performance for half of the tickers included in the list.

### Justification

Why some models worked better than others might have something to do with the age of the companies & the industry they operate in. For example tech companies saw a huge spike in their results as a result of the Covid lockdowns and overall consumers relying more heavily on the products and services they provided while other industries suffered (like the air travel industry). For example, see the image below, prophet thinks the value of the stock is going to drop heavily (orange line) as that is what happend the year prior to it. This is actually an artifact from not enough historic data (2020-01-01 onward).

![Forecast yearly](./assets/forecast_wthout_yearly.png)

This prompted me to bump the amount of historic data to include in the final model to get it from 2019-01-01 onward and battle some of the pandamic issues we see on the stock market specifically.

## Conclusion

### Reflection
The webapp presented here successfully displays an estimated adjusted close price for a stock of interest for the next 180 days. It provides the user with an interface to provide input and get output, collects required data from open data sources and uses optimized parameters to adjust the model on the fly. To top it off the output is an easy to consume line graph, displaying trends and providing a powerful overview to make decisions.

I'm happy with the decoupling between the different parts of the application I built in. It is possible to swap out models without touching the actual visualisation code, as long as you adhere to the contracts. It currently is a soft coupling, so this could be improved in a next iterations by making the contracts/protocols more explicit, although that hinges more towards strong software engineering practices.

In the start up phase of the project I had some trouble scoping out the project. There is pressure on producing something you are proud off, and as I tend to put the bar really high that led to a somewhat slow start to implementation. Part of the decisions made at the start, like trying new libraries and frameworks Bokeh and FastAPI over material covered by the course, ended up eating up a lot of time. In the end I am quite proud on what the webapp can do now, eventhough I still think the functionality is limited and the models used to get the actual estimated values naive.

The other thing I found hard was the model optimisation. I have used prophet before and its a really great tool when it comes to forecasting, it is very hard to outdo it with custom home-made ARIMA, SARIMA or SARIMAX models. That said, the different stocks all behave very differently, indicating that a general model for this type of data tends to not work well. This combined with some of the somewhat complicated cross-validation for temporal data made implementing the grid search quite interesting.


### Improvement

#### Naïve models
The current forecasting approach is very naïve as it only looks at historic adjusted closing rates and ignores any forms of reports, quarterly updates from the companies or prospects shared by the company. Next to this it only forecasts the expected adjusted close value for the stocks, which does not take into account scheduled divident payouts or stock splits, which influcence the adjusted closing price. Additionally, the stock market reacts to what is going on in the world. Not only governments introducting laws, taxes or results from elections but also wars, natural disasters and the overall confidence in the economy by "we, the people" all have their influnce on the stock markets. None of these are currently included in the model.

This is a direct result of using facebook prophet as the ML model. One interesting thought experiment is if you could actually model all of this complex real world interactions and capture them in the prophet models as change points, or interesting season patterns that operate on their own cycle. Elections for example, in the US these happen every four years and they might have a four-year cycle instead of the yearly cycle prophet assumes.

#### Adding template to extend supported tickers & influence estimate
Currently the UI is very limited in that it only allows the user to select a ticker and get a visualisation + estimate. It doesn't have any way to set a date range of interest, no way to extend to horizon or length of the estimate you get returned as a user. Additonally you currently can only add tickers from the backend and it requires a webapp restart.

I would love to add a page where you can add other tickers for which there is no model yet. Doing this would need the gridsearch to be available as a function to the webapplication. As the gridsearch took a very long time to run on my local computer (~6 hours) this functionality should be supported with an asynchronous functionality and ideally some notification when it is done so the user can come back and have a look at their new ticker.

Influencing the date range of interest could be a more dynamic by providing a input field to pick how large the estimate should be. I don't think adding support for changing the historic date range will help the model improvement as we have seen above that the models require enough data to get seasonal trends down. As this is expert knowledge and I would like to keep the UI easy and friendly this won't be supported.

#### Portfolio overview & recommendation engine
Currently the app is a one time use, it doesn't remember the state and it doens't have any support to build a portfolio for a user. This would be a very nice feature to add. To achieve this it requires an additional module that takes care of creating user accounts. Furthermore, it requires a database that know when a stock was purchased and a what price. Next it requires the implementation of business logic to determine if it should recommend to sell or buy more of the stock. This by itself could be a project.


<details><summary>Project rubric</summary>

#### Project definition

| Criteria | Meets specifications |
| -------- | -------------------- |
| Project Overview | Student provides a high-level overview of the project. Background information such as the problem domain, the project origin, and related data sets or input data is provided |
| Problem Statement | The problem which needs to be solved is clearly defined. A strategy for solving the problem, including discussion of the expected solution, has been made |
| Metrics | Metrics used to measure performance of a model or result are clearly defined. Metrics are justified based on the characteristics of the problem |


#### Analysis

| Criteria | Meets specifications |
| -------- | -------------------- |
| Data Exploration | Features and calculated statistics relevant to the problem have been reported and discussed related to the dataset, and a thorough description of the input space or input data has been made. Abnormalities or characteristics about the data or input that need to be addressed have been identified |
| Data Visualization | Build data visualizations to further convey the information associated with your data exploration journey. Ensure that visualizations are appropriate for the data values you are plotting. |


#### Methodology

| Criteria | Meets specifications |
| -------- | -------------------- |
| Data Preprocessing | All preprocessing steps have been clearly documented. Abnormalities or characteristics about the data or input that needed to be addressed have been corrected. If no data preprocessing is necessary, it has been clearly justified |
| Implementation | The process for which metrics, algorithms, and techniques were implemented with the given datasets or input data has been thoroughly documented. Complications that occurred during the coding process are discussed. |
| Refinement | The process of improving upon the algorithms and techniques used is clearly documented. Both the initial and final solutions are reported, along with intermediate solutions, if necessary. |


#### Results

| Criteria | Meets specifications |
| -------- | -------------------- |
| Model Evaluation and Validation | If a model is used, the following should hold: The final model’s qualities — such as parameters — are evaluated in detail. Some type of analysis is used to validate the robustness of the model’s solution. <br><br>Alternatively a student may choose to answer questions with data visualizations or other means that don't involve machine learning if a different approach best helps them address their question(s) of interest. |
| Justification | The final results are discussed in detail. Exploration as to why some techniques worked better than others, or how improvements were made are documented. |

#### Conclusion

| Criteria | Meets specifications |
| -------- | -------------------- |
| Reflection | Student adequately summarizes the end-to-end problem solution and discusses one or two particular aspects of the project they found interesting or difficult. |
| Improvement | Discussion is made as to how at least one aspect of the implementation could be improved. Potential solutions resulting from these improvements are considered and compared/contrasted to the current solution. |

#### Deliverables

| Criteria | Meets specifications |
| -------- | -------------------- |
| Write-up or Application | If the student chooses to provide a blog post the following must hold: Project report follows a well-organized structure and would be readily understood by a technical audience. Each section is written in a clear, concise and specific manner. Few grammatical and spelling mistakes are present. All resources used to complete the project are cited and referenced.<br><br>If the student chooses to submit a web-application, the following holds: There is a web application that utilizes data to inform how the web application works. The application does not need to be hosted, but directions for how to run the application on a local machine should be documented.|
| Github Repository | Student must have a Github repository of their project. The repository must have a README.md file that communicates the libraries used, the motivation for the project, the files in the repository with a small description of each, a summary of the results of the analysis, and necessary acknowledgements. If the student submits a web app rather than a blog post, then the Project Definition, Analysis, and Conclusion should be included in the README file, or in their Jupyter Notebook. Students should not use another student's code to complete the project, but they may use other references on the web including StackOverflow and Kaggle to complete the project. |
| Best Practices | Code is formatted neatly with comments and uses DRY principles. A README file is provided that provides. PEP8 is used as a guideline for best coding practices.<br><br>Best practices from software engineering and communication lessons are used to create a phenomenal end product that students can be proud to showcase! |

</details>