# A script to pull the most popular stock market indicies and their performances over multiple timeframes
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Function to determine if string is in YYYY-MM-DD format
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

# Sector SPDR symbols info
sector_SPDRs_symbols = ['SPY', 'XLI', 'XLV', 'XLK', 'XLF', 'XLB', 'XLE', 'XLU', 'XLY', 'XLP', 'XLC', 'XLRE']
sector_SPDRs_symbols_str = ' '.join(sector_SPDRs_symbols)
sector_SPDRs_desc_dict = {
    'SPY': 'S&P 500 INDEX',
    'XLE': 'ENERGY',
    'XLF': 'FINANCIAL',
    'XLU': 'UTILITIES',
    'XLRE': 'REAL ESTATE',
    'XLI': 'INDUSTRIAL',
    'XLP': 'CONSUMER STAPLES',
    'XLC': 'COMMUNICATION SERVICES',
    'XLB': 'MATERIALS',
    'XLV': 'HEALTH CARE',
    'XLK': 'TECHNOLOGY',
    'XLY': 'CONSUMER DISCRETIONARY'}
sector_SPDRs_desc_df = pd.DataFrame.from_dict(sector_SPDRs_desc_dict, orient='index', columns=['Description'])

# Pull the performance for the user specified timeframe
charts = 0
range_options = ['dates', 'period']
valid_pds = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

# How many charts does the user want to generate?
while charts == 0:
    charts = int(input("Enter the number of charts you would like to generate. "))

for i in range(charts):
    # Does the user want to use specific dates or a pre-defined period
    range_choice = ''
    while range_choice not in range_options:
        print('Valid periods: ' + ', '.join(valid_pds))
        range_choice = input('Enter \'dates\' to use specific dates or \'period\' to use a pre-defined period. ')
    # Pull performance for a pre-defined period
    if range_choice == 'period':
        period = ''
        while period not in valid_pds:
            print('Valid periods: ' + ', '.join(valid_pds))
            period = input('Enter the period you would like to consider. ')
        performance = yf.download(tickers=sector_SPDRs_symbols_str, period=period, interval='1d', group_by='ticker')
    # Pull performance for specific date ranges
    else:
        start_date = ''
        end_date = ''
        while not validate(start_date):
            start_date = input('Enter the start date in YYYY-MM-DD format. ')
        while not validate(end_date):
            end_date = input('Enter the end date in YYYY-MM-DD format. ')
        performance = yf.download(tickers=sector_SPDRs_symbols_str, start=start_date, end=end_date, interval='1d', group_by='ticker')
    performance.to_csv('Sector SPDRs Performance')

    # Calculate the relative performance & a summary table
    relative_performance = pd.DataFrame(columns=sector_SPDRs_symbols, index=performance.index)
    performance_summary = pd.DataFrame(columns=['Percent Change'], index=sector_SPDRs_symbols)
    for symbol in sector_SPDRs_symbols:
        relative_performance[symbol] = (((performance[symbol]['Close'] - performance[symbol]['Close'][0]) / performance[symbol]['Close'][0])*100)
        performance_summary['Percent Change'][symbol] = relative_performance[symbol][-1]
    relative_performance.to_csv('Sector SPDRs Relative Performance')
    performance_summary = pd.concat([sector_SPDRs_desc_df, performance_summary], axis=1)
    performance_summary.sort_values(by=['Percent Change'], inplace=True, ascending=False)
    print(performance_summary)

    # Construct graph but don't show it yet to allow execution to continue
    relative_performance.plot()

# Show all constructed graphs
plt.show()