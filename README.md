# portfolio-tracker
### This is an on going project and overtime I would like to add to the project, such as the data is dispalys for your portfolio. 
* `TODO` Get highest holding in portfolio and display it in the text box
* `TODO` add a YTD in a text box and an all time figure.
* `TODO` nest parts of the script in functions

Keep track of the amount you have invested into the stock market compared to the value of your investments based off live data from `yfinance`.

The data from your portfolio is dispayed using `matplotlib.pyplot` to plot two lines, one shows a cumulative amount of money you have put into the market, and the second line shows the data from `yfinance` to help provide accurate, up-to date data. 

`pandas` is used to put the csv files that are required for the lines into dataframes. The strucutre of the csvs can be seen below, the first csv is for the amount invested and the second is for your portfolio data (dates, amount of stock purchased, currency etc...)

### Invested csv

| Time  | Total |
|----------|-------|
| 26/11/2024 | 100  |
| 26/12/2024 | 100  |
| 26/01/2024 | 100  |

`Date` is the date that you deposited the money from your bank account into the brokerage account.
`Total` is the amount of money that you deposited into the brokerage account and then invested. 

### Portfolio data csv

| Date |	Ticker |	Quantity |	Amount_spent |	Currency |
|:------:|:---------:|:-----------:|:---------------:|:-----------:|
| 02/12/2024 |	VUAG.L |	0.110471 |	10	| GBP |
| 09/12/2024 |	GOOG |	0.0523560 |	9.99 |	USD |
| 30/12/2024 |	AAPL |	0.0198115	| 4 |	USD |
| 31/12/2024 |	VUAG.L |	0.11178 |	10 |	GBP |

`Date` is the day you bought the stock.  

`Ticker` is the tickey symbol of the stock (e.g. AAPL for Apple or GOOG for Google). Stocks listed on non-us markets are followed by a small identifier to ensure you are looking for the correct stock, for example VUAG.L is a ETF listed on the London Stock Exchange or AIR.PA is for Airbus which is listed on the Paris exchange.  

`Quantity` is the amount of shares that were bought in the order (e.g. 5  shares of Apple or 0.75 shares of the VUAG ETF).  

`Amount_spent` is the amount of money you spent on the stock (e.g. you bought £20 worth of shares in VUAG).  

`Currency` is the currency the stock was bought in/is listed in. 


