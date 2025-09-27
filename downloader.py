import requests
import os
import time
from urllib.parse import unquote

def smart_download(url, save_path=None):
    """
    স্মার্ট ডাউনলোডার যেটা Microsoft এর মতো সাইট থেকে ডাউনলোড করতে পারবে
    """
    if save_path is None:
        # অটো ফাইলনাম ডিটেকশন
        filename = extract_filename(url)
        save_path = filename
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
        'Referer': 'https://www.microsoft.com/'
    }
    
    try:
        print("🔍 ফাইল তথ্য চেক করা হচ্ছে...")
        
        # প্রথমে HEAD request দিয়ে ফাইল সাইজ চেক
        with requests.Session() as session:
            session.headers.update(headers)
            
            # HEAD request
            head_response = session.head(url, allow_redirects=True, timeout=30)
            head_response.raise_for_status()
            
            file_size = int(head_response.headers.get('content-length', 0))
            final_url = head_response.url
            
            print(f"📁 ফাইল সাইজ: {file_size/(1024*1024):.2f} MB")
            print(f"🔗 ফাইনাল URL: {final_url}")
            
            # GET request with progress
            print("⬇️ ডাউনলোড শুরু হচ্ছে...")
            response = session.get(final_url, stream=True, timeout=60)
            response.raise_for_status()
            
            # ডাউনলোড 진행
            downloaded = 0
            start_time = time.time()
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        # প্রোগ্রেস শো করুন
                        if file_size > 0:
                            progress = (downloaded / file_size) * 100
                            speed = downloaded / (time.time() - start_time) / 1024
                            print(f"\r📊 Progress: {progress:.1f}% | Speed: {speed:.1f} KB/s", end='', flush=True)
            
            print(f"\n✅ ডাউনলোড সম্পূর্ণ! ফাইল সেভ হয়েছে: {save_path}")
            return True
            
    except Exception as e:
        print(f"❌ ডাউনলোড ব্যর্থ: {str(e)}")
        return False

def extract_filename(url):
    """URL থেকে ফাইলনাম এক্সট্রাক্ট করুন"""
    try:
        # URL decode করুন
        decoded_url = unquote(url)
        
        # path থেকে ফাইলনাম নিন
        filename = decoded_url.split('/')[-1]
        
        # query parameters remove করুন
        if '?' in filename:
            filename = filename.split('?')[0]
        
        # যদি ফাইলনাম না থাকে
        if not filename or '.' not in filename:
            filename = "download.iso"
        
        return filename
    except:
        return "download.iso"

# আপনার URL সহ ব্যবহার করুন
url = "https://software.download.prss.microsoft.com/dbazure/Win10_22H2_English_x64v1.iso?t=0fb16a8c-2ac6-4fe5-8ab7-745b963f951b&P1=1759047369&P2=601&P3=2&P4=JWmL6s7rq141QdL6G36snXg79dBLk2eF2qK%2f2BIMMoqCBpjphWBb5%2fSoYrzN6euz2%2fwOWWSJSDro6XA3laMpMxwJm0Hts1KcuBSAXsFKmH%2fgYqQ%2bs4Iu7uv6HEPwmh2bs5JnMtH6LVGQ4nnP3E3iEL9WF1BmxJrxVYybAhAlVpv93E3O%2btcGJGbIbwFJIiKAnGS6MWngCSmvPb5WCDJrx%2fQjCqda644UCFkcQQocpvL4dOFifk74cQcn7jP3myd5DLwkC%2flf1Vmn9FAFbdlpiPk1Kb8ZF82WUleVrLlbCw01ZkMjjOwvpTrRvOVSTtTorTHhJt5id54B8NmCz0w9Og%3d%3d"

print("🚀 ইউনিভার্সাল ডাউনলোডার শুরু হচ্ছে...")
smart_download(url)