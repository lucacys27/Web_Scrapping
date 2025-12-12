import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class CryptoNewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.headlines = []
        
        # Load BERT sentiment analysis model
        print("🤖 Loading BERT sentiment analysis model...")
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        print("✓ BERT model loaded successfully (FinBERT - optimized for financial text)\n")
        
        # Comprehensive list of cryptocurrencies with symbols and names
        self.crypto_list = {
            'BTC': ['Bitcoin', 'BTC'],
            'ETH': ['Ethereum', 'ETH', 'Ether'],
            'BNB': ['Binance Coin', 'BNB', 'Binance'],
            'SOL': ['Solana', 'SOL'],
            'XRP': ['Ripple', 'XRP'],
            'ADA': ['Cardano', 'ADA'],
            'DOGE': ['Dogecoin', 'DOGE'],
            'AVAX': ['Avalanche', 'AVAX'],
            'DOT': ['Polkadot', 'DOT'],
            'MATIC': ['Polygon', 'MATIC'],
            'LINK': ['Chainlink', 'LINK'],
            'UNI': ['Uniswap', 'UNI'],
            'SHIB': ['Shiba Inu', 'SHIB'],
            'LTC': ['Litecoin', 'LTC'],
            'TRX': ['Tron', 'TRX'],
            'ATOM': ['Cosmos', 'ATOM'],
            'XLM': ['Stellar', 'XLM'],
            'XMR': ['Monero', 'XMR'],
            'BCH': ['Bitcoin Cash', 'BCH'],
            'ALGO': ['Algorand', 'ALGO'],
            'VET': ['VeChain', 'VET'],
            'FIL': ['Filecoin', 'FIL'],
            'AAVE': ['Aave', 'AAVE'],
            'ETC': ['Ethereum Classic', 'ETC'],
            'NEAR': ['Near Protocol', 'NEAR'],
            'APT': ['Aptos', 'APT'],
            'ARB': ['Arbitrum', 'ARB'],
            'OP': ['Optimism', 'OP'],
            'STX': ['Stacks', 'STX'],
            'IMX': ['Immutable X', 'IMX'],
            'INJ': ['Injective', 'INJ'],
            'SUI': ['Sui', 'SUI'],
            'HBAR': ['Hedera', 'HBAR'],
            'GRT': ['The Graph', 'GRT'],
            'MKR': ['Maker', 'MKR'],
            'RUNE': ['THORChain', 'RUNE'],
            'FTM': ['Fantom', 'FTM'],
            'SAND': ['The Sandbox', 'SAND'],
            'MANA': ['Decentraland', 'MANA'],
            'AXS': ['Axie Infinity', 'AXS'],
            'XTZ': ['Tezos', 'XTZ']
        }
    
    def detect_coins(self, headline):
        """Detect which cryptocurrencies are mentioned in the headline"""
        detected = []
        headline_upper = headline.upper()
        
        for symbol, names in self.crypto_list.items():
            for name in names:
                # Use word boundaries to avoid false matches
                pattern = r'\b' + re.escape(name.upper()) + r'\b'
                if re.search(pattern, headline_upper):
                    if symbol not in detected:
                        detected.append(symbol)
                    break
        
        return detected if detected else ['GENERAL']
    
    def scrape_coindesk(self):
        """Scrape crypto headlines from CoinDesk"""
        try:
            url = "https://www.coindesk.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = soup.find_all(['h2', 'h3', 'h4', 'h6'], class_=lambda x: x and 'headline' in x.lower() if x else False)
            
            for headline in headlines[:40]:
                text = headline.get_text(strip=True)
                if text and len(text) > 15:
                    self.headlines.append({
                        'source': 'CoinDesk',
                        'headline': text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            print(f"✓ Scraped {len([h for h in self.headlines if h['source'] == 'CoinDesk'])} headlines from CoinDesk")
        except Exception as e:
            print(f"✗ Error scraping CoinDesk: {e}")
    
    def scrape_cointelegraph(self):
        """Scrape crypto headlines from Cointelegraph"""
        try:
            url = "https://cointelegraph.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = soup.find_all('a', class_=lambda x: x and 'post-card' in x if x else False)
            
            for headline in headlines[:40]:
                text = headline.get_text(strip=True)
                if text and len(text) > 15 and len(text) < 300:
                    self.headlines.append({
                        'source': 'Cointelegraph',
                        'headline': text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            print(f"✓ Scraped {len([h for h in self.headlines if h['source'] == 'Cointelegraph'])} headlines from Cointelegraph")
        except Exception as e:
            print(f"✗ Error scraping Cointelegraph: {e}")
    
    def scrape_decrypt(self):
        """Scrape crypto headlines from Decrypt"""
        try:
            url = "https://decrypt.co/news"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = soup.find_all(['h2', 'h3'], class_=lambda x: x and ('title' in x.lower() or 'headline' in x.lower()) if x else False)
            
            for headline in headlines[:40]:
                text = headline.get_text(strip=True)
                if text and len(text) > 15:
                    self.headlines.append({
                        'source': 'Decrypt',
                        'headline': text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            print(f"✓ Scraped {len([h for h in self.headlines if h['source'] == 'Decrypt'])} headlines from Decrypt")
        except Exception as e:
            print(f"✗ Error scraping Decrypt: {e}")
    
    def scrape_bitcoin_magazine(self):
        """Scrape crypto headlines from Bitcoin Magazine"""
        try:
            url = "https://bitcoinmagazine.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = soup.find_all(['h2', 'h3', 'h4'])
            
            for headline in headlines[:40]:
                text = headline.get_text(strip=True)
                if text and len(text) > 15 and len(text) < 300:
                    self.headlines.append({
                        'source': 'Bitcoin Magazine',
                        'headline': text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            print(f"✓ Scraped {len([h for h in self.headlines if h['source'] == 'Bitcoin Magazine'])} headlines from Bitcoin Magazine")
        except Exception as e:
            print(f"✗ Error scraping Bitcoin Magazine: {e}")
    
    def scrape_cryptonews(self):
        """Scrape crypto headlines from CryptoNews"""
        try:
            url = "https://cryptonews.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = soup.find_all(['h2', 'h3', 'h4'], class_=lambda x: x and 'title' in x.lower() if x else False)
            
            for headline in headlines[:40]:
                text = headline.get_text(strip=True)
                if text and len(text) > 15:
                    self.headlines.append({
                        'source': 'CryptoNews',
                        'headline': text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            print(f"✓ Scraped {len([h for h in self.headlines if h['source'] == 'CryptoNews'])} headlines from CryptoNews")
        except Exception as e:
            print(f"✗ Error scraping CryptoNews: {e}")
    
    def analyze_sentiment_bert(self, text):
        """Analyze sentiment using FinBERT model"""
        # Tokenize and prepare input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # FinBERT outputs: [positive, negative, neutral]
        scores = predictions[0].tolist()
        positive_score = scores[0]
        negative_score = scores[1]
        neutral_score = scores[2]
        
        # Determine sentiment based on highest confidence
        max_score = max(scores)
        if max_score == positive_score:
            sentiment = 'Positive'
            confidence = positive_score
        elif max_score == negative_score:
            sentiment = 'Negative'
            confidence = negative_score
        else:
            sentiment = 'Neutral'
            confidence = neutral_score
        
        # Calculate polarity score (-1 to 1)
        polarity = positive_score - negative_score
        
        return sentiment, polarity, confidence, positive_score, negative_score, neutral_score
    
    def scrape_all(self):
        """Scrape all crypto news sources"""
        print("\n" + "="*80)
        print("🔍 STARTING CRYPTO NEWS SCRAPER")
        print("="*80 + "\n")
        
        self.scrape_coindesk()
        time.sleep(1)
        
        self.scrape_cointelegraph()
        time.sleep(1)
        
        self.scrape_decrypt()
        time.sleep(1)
        
        self.scrape_bitcoin_magazine()
        time.sleep(1)
        
        self.scrape_cryptonews()
        
        print(f"\n✓ Total headlines scraped: {len(self.headlines)}\n")
    
    def analyze_all(self):
        """Perform sentiment analysis and coin detection on all headlines"""
        print("🧠 Analyzing sentiment with BERT and detecting coins...\n")
        
        for idx, item in enumerate(self.headlines, 1):
            if idx % 20 == 0:
                print(f"   Processed {idx}/{len(self.headlines)} headlines...")
            
            sentiment, polarity, confidence, pos_score, neg_score, neu_score = self.analyze_sentiment_bert(item['headline'])
            coins = self.detect_coins(item['headline'])
            
            item['sentiment'] = sentiment
            item['polarity_score'] = round(polarity, 3)
            item['confidence'] = round(confidence, 3)
            item['positive_score'] = round(pos_score, 3)
            item['negative_score'] = round(neg_score, 3)
            item['neutral_score'] = round(neu_score, 3)
            item['coins_mentioned'] = ', '.join(coins)
            item['coin_count'] = len([c for c in coins if c != 'GENERAL'])
        
        print(f"✓ Completed sentiment analysis on {len(self.headlines)} headlines\n")
        return self.headlines
    
    def get_coin_index(self):
        """Return a DataFrame with the coin index"""
        coin_data = []
        for idx, (symbol, names) in enumerate(self.crypto_list.items(), 1):
            coin_data.append({
                'Index': idx,
                'Symbol': symbol,
                'Name': names[0],
                'Aliases': ', '.join(names[1:])
            })
        
        return pd.DataFrame(coin_data)
    
    def display_results(self):
        """Display results in a formatted way"""
        if not self.headlines:
            print("No headlines found to analyze.")
            return None
        
        df = pd.DataFrame(self.headlines)
        
        print("="*80)
        print("📊 CRYPTO NEWS SENTIMENT ANALYSIS RESULTS (BERT)")
        print("="*80)
        print(f"\n⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 Model: FinBERT (Fine-tuned for Financial Sentiment)\n")
        
        # Overall sentiment summary
        print("📈 OVERALL SENTIMENT SUMMARY:")
        print("-"*80)
        sentiment_counts = df['sentiment'].value_counts()
        total = len(df)
        
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            count = sentiment_counts.get(sentiment, 0)
            percentage = (count / total) * 100
            bar = "█" * int(percentage / 2)
            emoji = {'Positive': '🟢', 'Neutral': '🟡', 'Negative': '🔴'}
            print(f"{emoji[sentiment]} {sentiment:8}: {count:3} ({percentage:5.1f}%) {bar}")
        
        print(f"\n📊 Average Polarity: {df['polarity_score'].mean():+.3f}")
        print(f"📊 Average Confidence: {df['confidence'].mean():.3f}")
        
        # Coin mention statistics
        print("\n" + "="*80)
        print("💰 MOST MENTIONED CRYPTOCURRENCIES:")
        print("-"*80)
        
        # Count mentions per coin
        all_coins = []
        for coins_str in df['coins_mentioned']:
            coins = [c.strip() for c in coins_str.split(',') if c.strip() != 'GENERAL']
            all_coins.extend(coins)
        
        if all_coins:
            coin_counts = pd.Series(all_coins).value_counts().head(10)
            for idx, (coin, count) in enumerate(coin_counts.items(), 1):
                coin_name = self.crypto_list.get(coin, [coin])[0]
                print(f"{idx:2}. {coin:6} ({coin_name:20}) - {count:3} mentions")
        else:
            print("No specific coins detected in headlines")
        
        # Sentiment by top coins
        print("\n" + "="*80)
        print("📊 SENTIMENT BY TOP COINS:")
        print("-"*80)
        
        if all_coins:
            top_coins = coin_counts.head(5).index.tolist()
            
            for coin in top_coins:
                coin_headlines = df[df['coins_mentioned'].str.contains(coin)]
                if len(coin_headlines) > 0:
                    pos = len(coin_headlines[coin_headlines['sentiment'] == 'Positive'])
                    neg = len(coin_headlines[coin_headlines['sentiment'] == 'Negative'])
                    neu = len(coin_headlines[coin_headlines['sentiment'] == 'Neutral'])
                    avg_pol = coin_headlines['polarity_score'].mean()
                    avg_conf = coin_headlines['confidence'].mean()
                    coin_name = self.crypto_list.get(coin, [coin])[0]
                    
                    print(f"\n{coin} ({coin_name}):")
                    print(f"  Total mentions: {len(coin_headlines)} | Pos: {pos} | Neu: {neu} | Neg: {neg}")
                    print(f"  Avg Sentiment: {avg_pol:+.3f} | Avg Confidence: {avg_conf:.3f}")
        
        # Show most positive and negative for specific coins
        coin_specific = df[df['coin_count'] > 0]
        
        if len(coin_specific) > 0:
            print("\n" + "="*80)
            print("🟢 MOST POSITIVE COIN-SPECIFIC HEADLINES:")
            print("-"*80)
            top_positive = coin_specific.nlargest(3, 'polarity_score')
            for idx, row in top_positive.iterrows():
                print(f"\n[{row['coins_mentioned']}] Polarity: {row['polarity_score']:+.3f} | Confidence: {row['confidence']:.3f}")
                print(f"{row['headline']}")
            
            print("\n" + "="*80)
            print("🔴 MOST NEGATIVE COIN-SPECIFIC HEADLINES:")
            print("-"*80)
            top_negative = coin_specific.nsmallest(3, 'polarity_score')
            for idx, row in top_negative.iterrows():
                print(f"\n[{row['coins_mentioned']}] Polarity: {row['polarity_score']:+.3f} | Confidence: {row['confidence']:.3f}")
                print(f"{row['headline']}")
        
        print("\n" + "="*80)
        
        return df
    
    def save_to_csv(self, filename=None):
        """Save results to CSV file"""
        if not self.headlines:
            print("No data to save.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save main results
        if filename is None:
            filename = f'crypto_sentiment_bert_{timestamp}.csv'
        
        df = pd.DataFrame(self.headlines)
        column_order = ['timestamp', 'source', 'headline', 'coins_mentioned', 'coin_count', 
                       'sentiment', 'polarity_score', 'confidence', 'positive_score', 
                       'negative_score', 'neutral_score']
        df = df[column_order]
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"\n✅ Headlines saved to: {filename}")
        print(f"📁 Total rows: {len(df)}")
        
        # Save coin index
        coin_index_file = f'coin_index_{timestamp}.csv'
        coin_df = self.get_coin_index()
        coin_df.to_csv(coin_index_file, index=False, encoding='utf-8')
        
        print(f"\n✅ Coin index saved to: {coin_index_file}")
        print(f"📁 Total coins: {len(coin_df)}")
        
        return filename, coin_index_file


def main():
    """Main execution function"""
    scraper = CryptoNewsScraper()
    
    # Display coin index
    print("\n" + "="*80)
    print("💎 TRACKED CRYPTOCURRENCIES")
    print("="*80)
    coin_index = scraper.get_coin_index()
    print(f"\nTracking {len(coin_index)} cryptocurrencies\n")
    print(coin_index.head(10).to_string(index=False))
    print(f"\n... and {len(coin_index) - 10} more\n")
    
    # Scrape headlines
    scraper.scrape_all()
    
    # Analyze sentiment and detect coins
    scraper.analyze_all()
    
    # Display results
    df = scraper.display_results()
    
    # Save to CSV
    scraper.save_to_csv()
    
    return df


if __name__ == "__main__":
    print("\n🚀 Crypto Coin News Sentiment Analyzer (BERT Edition)")
    print("="*80)
    print("Required packages:")
    print("  pip install requests beautifulsoup4 pandas transformers torch")
    print("\nNote: First run will download the FinBERT model (~500MB)")
    print("="*80 + "\n")
    
    main()