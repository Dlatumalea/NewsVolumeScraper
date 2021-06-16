import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', '-t', type=str, required=True, help='Ticker to search for.')
    parser.add_argument('--start_date', '-start', type=str, required=True, help='Start date to start scraping from. Format must be m/d/y')
    parser.add_argument('--end_date', '-end', type=str, required=True, help='Last day to scrape. Format must be m/d/y')
    parser.add_argument('--output_dir', '-o', type=str, required=True, help='Output directory to save file to.')
    args = parser.parse_args()
    
    
    ticker = args.ticker
    start_date = args.start_date
    end_date = args.end_date
    out = args.output_dir
    
    scraper = NewsVolumeScraper(ticker=ticker)
    scraper.scrape(start_date=start_date, end_date=end_date)
    df = pd.DataFrame(data=scraper.get_data())
    df.to_csv('{}/{}_{}-{}.csv'.format(out, ticker, start_date.replace('/', ''), end_date.replace('/', '')), index=False)
