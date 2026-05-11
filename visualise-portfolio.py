import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

df = pd.read_csv('money_invested.csv')
df_trades = pd.read_csv('portfoliobuys.csv', parse_dates=['Date'], dayfirst=True)

# Get cumulative value for money invested
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

df = df.sort_values('Date')

date = df['Date']
total = df['Total'].cumsum()

display_value = total.iloc[-1]

# Live data for portfolio from yfinance

tickers = df_trades['Ticker'].unique().tolist()
# Add exchange rate to the list to convert US stocks (like AAPL) to GBP or EU stocks to GBP
rates = ['GBPUSD=X', 'GBPEUR=X']
all_query = tickers + rates
start_date = df_trades['Date'].min()

print("Fetching live market data...")
data = yf.download(all_query, start=df_trades['Date'].min())['Close']

data = data.ffill().bfill()

data = data.fillna(0)

# Force the index to be a clean daily range to match loop
data.index = pd.to_datetime(data.index).normalize()

# Build the Timeline
all_days = pd.date_range(start=df_trades['Date'].min(), end=pd.Timestamp.today(), freq='D')
invested_history = []
value_history = []

# Stocks listed in pence are in the currency 'GBX'
gbx_tickers = ['RR.L']

for day in all_days:
    # Look at trades strictly on or before this day
    past_trades = df_trades[df_trades['Date'] <= day]
    
    total_invested = past_trades['Amount_spent'].sum()
    market_value_gbp = 0
    
    # Get rates with a fallback
    try:
        usd_per_gbp = data['GBPUSD=X'].asof(day)
    except:
        usd_per_gbp = 1.25 # Historical average fallback if rate is missing

    holdings = past_trades.groupby(['Ticker', 'Currency'])['Quantity'].sum().reset_index()
    
    for _, row in holdings.iterrows():
        ticker = row['Ticker']
        qty = row['Quantity']
        
        
        if ticker in data.columns:
            price_native = data[ticker].asof(day)
            
            # If price_native is 0 or NaN, use the previous day's value
            if pd.isna(price_native) or price_native == 0:
                continue 

            if row['Currency'] == 'USD':
                val = (qty * price_native) / usd_per_gbp
            elif ticker in gbx_tickers:
                val = (qty * price_native) / 100
            else:
                val = (qty * price_native)
                
            market_value_gbp += val

    invested_history.append(total_invested)
    value_history.append(market_value_gbp)

# Get the top ticker
latest_date = data.index[-1]
usd_per_gbp = data['GBPUSD=X'].iloc[-1]

# Group all trades to get current total quantities
current_holdings = df_trades.groupby(['Ticker', 'Currency'])['Quantity'].sum()

# Calculate the value for all stocks held and display the top one on the graph
holding_values = {}

for (ticker, currency), qty in current_holdings.items():
    if qty <= 0: continue 
    
    price_native = data[ticker].iloc[-1]
    
   
    if currency == 'USD':
        val_gbp = (qty * price_native) / usd_per_gbp
    elif ticker in ['RR.L']:
        val_gbp = (qty * price_native) / 100
    else:
        val_gbp = (qty * price_native)
        
    holding_values[ticker] = val_gbp

# Find the top holding
top_ticker = max(holding_values, key=holding_values.get)
top_value = holding_values[top_ticker]

# Get the top gainer in the portfolio
gainers = {}

for (ticker, currency), qty in current_holdings.items():
    if qty <= 0: continue
    
    ticker_trades = df_trades[df_trades['Ticker'] == ticker]
    buys = ticker_trades[ticker_trades['Quantity'] > 0]
    
    # Average Price = Total Paid / Total Qty Bought
    avg_cost_price = buys['Amount_spent'].sum() / buys['Quantity'].sum()
    total_cost_of_remaining = qty * avg_cost_price
    
    price_native = data[ticker].iloc[-1]
    if currency == 'USD':
        current_val = (qty * price_native) / usd_per_gbp
    elif ticker in gbx_tickers:
        current_val = (qty * price_native) / 100
    else:
        current_val = (qty * price_native)
        
    # Calculate % Gain
    percentage_gain = ((current_val - total_cost_of_remaining) / total_cost_of_remaining) * 100
    gainers[ticker] = percentage_gain

# Find the biggest gainer
top_gainer_ticker = max(gainers, key=gainers.get)
top_gainer_pct = gainers[top_gainer_ticker]

# Styling
plt.style.use('dark_background')

# Manual "Retro Terminal" Overrides
# plt.rcParams.update({
#     "font.family": "monospace",      # Classic terminal font
#     "text.color": "#00FF41",         # "Matrix" Green
#     "axes.labelcolor": "#00FF41",
#     "axes.edgecolor": "#00FF41",
#     "xtick.color": "#00FF41",
#     "ytick.color": "#00FF41",
#     "grid.color": "#00FF41",
#     "grid.alpha": 0.2,               # Subtle scanline-like grid
#     "axes.facecolor": "black",       # Pure black background
#     "figure.facecolor": "black"
# })

plt.figure(figsize=(10, 5))
plt.plot(date, total, color='#00FF41',linewidth=1.5, label="Invested")
plt.plot(all_days, value_history, color='#00FFFF', label='Portfolio Value (£)', linewidth=2)
#plt.plot(date, total, marker='o', linestyle='-')

# text box to display hghest holding and biggest gainer
info_text = (
    f'Total invested £{display_value}\n'
    f'Biggest holding: {top_ticker} at £{top_value:.2f}\n'
    f'Biggest gain: {top_gainer_ticker} at £{top_gainer_pct:.2f}')
plt.text(0.015, 0.8, info_text, 
         transform=plt.gca().transAxes, 
         fontsize=12, verticalalignment='top', 
         bbox=dict(boxstyle='round', facecolor='None', alpha=0.5))

plt.title(f'Total invested £{display_value}\n Current Portfolio Value: £{value_history[-1]:.2f}')
plt.xlabel('Date')
plt.ylabel('Total Invested(£)')
plt.legend()
plt.grid(False)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
