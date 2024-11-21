import pandas as pd
from bs4 import BeautifulSoup
import requests
import holidays
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    Stocks={
        'Symbol':str,
        'Last Traded Price ($)': float,
        'Closing Price ($)':float,
        'PriceChange($)': float,
        'ClosingBid ($)':float,
        'ClosingAsk ($)':float,
        'Volume': pd.Int64Dtype(),
        "Today's Range ($) ":str,
        '52 Week  Range ($)':str,
        'Total PrevYr Div ($)':float,
        'Total  CurrentYr Div ($)':float

    }




    all_data = []
    start_date = '2019-01-02'
    end_date = '2019-01-04'
    all_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days only
    jamaica_holidays = holidays.Jamaica(years=range(2019, 2025))

    # Filter out Jamaican holidays from the business days
    workdays = [date for date in all_dates if date not in jamaica_holidays]
    workdays_list = [date.strftime('%Y-%m-%d') for date in workdays]  # Format dates as strings
    

    for workdays in workdays_list:
        try:
            #Dynamicly goes throuth all the dates in the Workday_List for the site and handles any errors that may come up
            url = f"https://www.jamstockex.com/trading/trade-quotes/?market=50&date={workdays}"
            headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
            response =requests.get(url,headers=headers)
            response.raise_for_status()# Raise an error if the request fails
            print("the page loaded")
        # handles the exception of the date not having data 
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {workdays}: {e}")
            continue
        #Uses Beautiful Soup to parse the url responce into a dataframe after which all tables are stored in a list
        soup = BeautifulSoup(response.content, 'html.parser')
        tables =soup.find_all('table')

        #ensures that the tables list has the required amount of tables
        if len(tables)<3:
            print(f"No data found for {workdays}")
            continue
        
        #Loads the second table from the site into the dataframe    
        table=tables[2]
        headers = [th.text.strip() for th in table.find_all('th')]
        # Add date as a column to the dataframe
        headers.append("StockDate")  

        #Extracts the rows from the site's table
        rows= table.find_all('tr')[1:] #Skips header row 
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            row_data.append(workdays)  # Append the date to each row
            all_data.append(row_data)
        

        #Stores each days data into a dataframe called Stocks    
        if all_data:
            Stocks=pd.DataFrame(all_data, columns=headers)  
            
        
        else:
            print(f"Could not find data for {workdays}")
           

    return Stocks


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'Output is not a DataFrame'
    assert not output.empty, 'The output DataFrame is empty'
