# Introduction - Stock Price Indicator
This repository contains all the code required to get a webapp running that uses facebook prophet to predict the stock price for a limited number of tickers. Current ticker supported are `AAPL`, `GOOG`, `MSFT`, `AMZN`, and `ASML`.


## How to run:
Requires python 3.8 or higher to run
To start the webapp on your local machine first make sure the requirements are installed by running: `pip install -r requirements.txt`

Then from the root folder of the directory run:
`python app/main.py`

The web app should now be running and available on [`http://192.168.0.182:5000/`](http://192.168.0.182:5000/).

## Project definition
> Investment firms, hedge funds and even individuals have been using financial models to better understand market behavior and make profitable investments and trades. A wealth of information is available in the form of historical stock prices and company performance data, suitable for machine learning algorithms to process.

For this project, a webapp stock price predictor that takes daily trading data over a certain date range as input, and outputs projected estimates for 180 days into the future was made.

### Overview of required sections
In order for this project to be a success a few elements are needed:
1. A framework that can host a webapp to interact with
   - The webapp needs an interactive element, to pick the stock for example
   - The webapp needs to be able to visualise and display the historic and expected stock prices
2. The webapp needs to be able to download historic stock ticker data from a provided endpoint, in this case Yahoo! finance was used.
   - The stock market isn't trading on all days, see if the endpoint provides daily values.
3. A ML model to take the historic data and predict the future stockprices
   - The model needs to be evaluated with an error measure to make sure it doesn't overfit on a specific stock
   - As the data is timeseries, evaluating with cannot be done on just a random sample as the order of the data matters

### Picking a framework for the webapp
Initally [FastAPI](https://fastapi.tiangolo.com/) was explored as the framework to use. FastAPI offers rapid development of webapps in python and as its based on Pydantic it comes with very strong documentation possibilities through OpenAPI documentation pages. For visualisation [bokeh](https://docs.bokeh.org/en/latest/index.html) had my interest for visualising the data. The bokeh python package is a wrapper around the very powerful D3 Javascript library, opening the possibilites for some fun visualisations like a OHLC or candlestick graph. This combination proved to be quite troublesome as bokeh has quite a steep learning curve and FastAPI as a webframework is relatively young so there aren't as many online resource available compared to the popular [Flask](https://flask.palletsprojects.com/en/2.0.x/).

This quickly led to a refactor from FastAPI to Flask, but still with bokeh as the go to for visualising the graph. I was pretty set on getting a Candle stick graph up and running in the webapp and found some nice resources. After giving this a try for a while I decided to swap out bokeh for Plotly. bokeh required more javascript knowledge to get working in the webapp. This combined with the availability of online resources for Flask+Plotly supported the decision to swap out bokeh before I got in too deep.

After giving the candle stick visualisation a go with Flask+Plotly it became clear that the webrendering template for Flask was lacking support for the candle stick graph. This required an approach to pre-render the full webpage or build a full backend server setup. This was outside of the scope of the current project, as the ML part also would requier some attention soon. This led to the decision of exposing the results as a line + scatter plot instead.

### Getting the data through APIs
For the data APIs I explored both [Quandl](https://www.quandl.com/) and [Yahoo! Finance](https://finance.yahoo.com/), both through the python packages available online. The Yahoo had my preference as it didn't require a log in, reducing the need to come up with a way to hide these and it allowed my app to be open on the internet without the need for others that want to use it to register.

Right around the time I was ready to start implementing the API, Yahoo updated the response of their API, breaking all the API calls and resulting in error messages on download. Luckily the python package is well maintained and it was updated quickly.

### Forcasting analysis
- For the forecasting of the stock prices the [facebook prophet](https://pypi.org/project/fbprophet/) package was used.
- Grid search to identify a general range for param optimisation. For more on this please read [Forecasting parameter tuning](forecasting_parameter_tuning.md)

The Mean Abosolute Percentage Error (`MAPE`) was used to evaluate model performance. 

#### Short comings of the current approach
The current forecasting approach is very naïve as it only looks at historic adjusted closing rates and ignores any forms of reports, quarterly updates from the companies or prospects shared by the company. Next to this it only forecasts the expected adjusted close value for the stocks, which does not take into account scheduled divident payouts or stock splits, which influcence the adjusted closing price.

Additionally, the stock market reacts to what is going on in the world. Not only Governments introducting laws, taxes or results from elections but also wars, natural disasters and the overall confidence in the economy by "we, the people" all have their influnce on the stock markets. None of these are currently included in the model, assuming they don't operate on some interesting seasonal pattern.




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