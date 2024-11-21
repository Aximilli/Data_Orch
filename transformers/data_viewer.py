import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    # Select relevant columns
    df = data[['Symbol', 'Last Traded Price ($)', 'Closing Price ($)', 'PriceChange($)', 'ClosingBid ($)', 
               'ClosingAsk ($)', 'Volume', "Today's Range ($)", '52 Week  Range ($)', 
               'Total PrevYr Div ($)', 'Total  CurrentYr Div ($)', 'StockDate']]
    
    # Rename columns
    df = df.rename(columns={
        'Last Traded Price ($)': 'LastTradedPrice',
        'Closing Price ($)': 'ClosingPrice',
        'PriceChange($)': 'PriceChange',
        'ClosingBid ($)': 'ClosingBid',
        'ClosingAsk ($)': 'ClosingAsk',
        'Volume': 'TradeVolume',
        "Today's Range ($)": 'TodaysRange',
        '52 Week  Range ($)': 'Week52Range',
        'Total PrevYr Div ($)': 'TotalPrevYrDiv',
        'Total  CurrentYr Div ($)': 'TotalCurrentYrDiv'
    })
    df['TradeVolume']=df['TradeVolume'].str.replace(",", "").astype(int)
    df['LastTradedPrice']=df['LastTradedPrice'].str.replace(",","").astype(float)
    df['ClosingPrice']=df['ClosingPrice'].str.replace(",","").astype(float)
    df['ClosingAsk']=df['ClosingAsk'].str.replace(",","").astype(float)
    #df['ClosingPrice']=df['ClosingPrice'].astype(float)
    print(df)   
  
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
