# import pandas as pd
# from bs4 import BeautifulSoup as bsp
# import requests
# # import csv file 
# link_mem = pd.read_csv(r"C:\Users\DELL\Documents\AeroLeadPrj\LinkedInProj\linkedIndata.csv")

# # iterate all link one by one

# print(requests.get("https://www.linkedin.com/in/pulkit-mittal-python-expert/"))
# for index,raw in link_mem.iterrows():
#     requests.get(raw["linkedIn Url"])

# -------------------------------

""" 
scrape_with_xpaths.py

Usage:
    python scrape_with_xpaths.py --input linkedIndata.csv --xpaths xpaths.json --output results.xlsx

Input CSV (example):
    url
    https://example.com/profile1
    C:\path\to\local\profile2.html

XPaths JSON (example):
{
  "name": "//h1[@class='profile-name']",
  "description": "//div[@class='about']//p",
  "email": "//a[contains(@href,'mailto:')]",
  "location": "//span[@class='location']"
}

The script will visit each URL (or local file) and attempt to extract values for each field using the provided XPath.
"""

import argparse
import json
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service

def prepare_driver(headless=True, user_agent=None):
    options = Options()
    print("part4-------")
    if headless:
        # For modern Chrome, headless=new is recommended; if your chrome version doesn't support it, remove '=new'
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    print("part5-------")
    # optional user agent
    if user_agent:
        options.add_argument(f'--user-agent={user_agent}')
        print("part6-------")

    # initialize driver via webdriver-manager (auto-download)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def normalize_url(raw):
    """
    If raw seems like a local path, convert to file:// URL.
    Otherwise return as-is (assumed to be http/https).
    """
    print("part8-------")
    raw = str(raw).strip()
    if raw.lower().startswith("http://") or raw.lower().startswith("https://") or raw.lower().startswith("file://"):
        print("part9-------")
        return raw
    # If it's an absolute Windows path like C:\... or Unix /home/..., convert
    if os.path.exists(raw):
        # on Windows, need to replace backslashes
        print("part10-------")
        path = os.path.abspath(raw)
        return "file:///" + path.replace("\\", "/")
    # fallback: return raw
    return raw

def extract_fields_from_page(driver, xpaths, wait_timeout=50):
    """
    Given a webdriver on a loaded page and a dict of xpaths, return a dict field->value or None.
    """
    results = {}
    for field, xpath in xpaths.items():
        try:
            print("part13-------",xpaths)
            # wait until element is present (but not too long)
            el = WebDriverWait(driver, wait_timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # get text. If it's an <a href="mailto:...">, keep text or href if text empty
            text = el.text.strip()
            print("text",text)
            if not text:
                # try attributes like href or alt or title
                print("part14-------")
                try:
                    
                    href = el.get_attribute("href")
                    if href:
                        print("part15-------",href)
                        text = href.strip()
                except Exception:
                    text = ""
            results[field] = text
            print("part16-------")
        except TimeoutException:
            # element not found in time
            print("part18-------")
            results[field] = None
        except Exception as e:
            # anything else (stale element, etc.)
            print("part9-------",e)
            results[field] = None
    return results

def main(args):
    # load input csv
    print("part1-------")
    df = pd.read_csv(args.input)
    if 'url' not in df.columns:
        raise SystemExit("Input CSV must have a column named 'url' with URLs or local file paths.")
        print("part2-------")

    # load xpaths mapping json
    with open(args.xpaths, 'r', encoding='utf-8') as f:
        xpaths = json.load(f)
    if not isinstance(xpaths, dict) or not xpaths:
        raise SystemExit("XPaths file should be a JSON object mapping field names to XPaths.")
        print("part3-------")

    # prepare selenium driver
    print("Starting Chrome driver...")
    driver = prepare_driver(headless=args.headless, user_agent=args.user_agent)

    results = []
    try:
        print("part7-------")
        count=0
        for idx, row in df.iterrows():
            if count==1:
                break
            count+=1
            raw_url = row['url']
            url = normalize_url(raw_url)
            print(f"[{idx+1}/{len(df)}] Visiting: {url}")

            try:
                print("part11-------")
                driver.get(url)
            except WebDriverException as e:
                print(f"  ERROR loading page: {e}")
                results.append({"source": raw_url, **{k: None for k in xpaths.keys()}})
                continue

            # optional wait for page to stabilize (increase 1-2s if heavy JS)
            time.sleep(args.post_load_sleep)

            # extract fields
            print("part12-------")
            data = extract_fields_from_page(driver, xpaths, wait_timeout=args.wait_timeout)
            results.append({"source": raw_url, **data})

            # polite delay between requests
            print("part17-------",results)
            time.sleep(args.delay_between_pages)

    finally:
        driver.quit()

    # save to excel
    out_df = pd.DataFrame(results)
    out_df.to_excel(args.output, index=False)
    print(f"Saved results to {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape pages using Selenium and XPaths, save results to Excel")
    parser.add_argument("--input", required=True, help="Input CSV path with a 'url' column")
    parser.add_argument("--xpaths", required=True, help="JSON file mapping field->xpath")
    parser.add_argument("--output", default="results.xlsx", help="Output Excel file")
    parser.add_argument("--headless", action="store_true", help="Run Chrome headless (no GUI)")
    parser.add_argument("--wait-timeout", dest="wait_timeout", type=int, default=8, help="Explicit wait timeout per element (seconds)")
    parser.add_argument("--delay-between-pages", dest="delay_between_pages", type=float, default=1.0, help="Delay between pages (seconds)")
    parser.add_argument("--post-load-sleep", dest="post_load_sleep", type=float, default=0.8, help="Sleep after page load before extraction (seconds)")
    parser.add_argument("--user-agent", dest="user_agent", default=None, help="Optional custom User-Agent string")
    args = parser.parse_args()

    main(args)

# -------------------------

# import streamlit as st
# import pandas as pd
# import time, random, io

# st.set_page_config(page_title='Autodialer — Streamlit Prototype', layout='wide')

# if 'numbers' not in st.session_state:
#     # number dict: {'raw':..., 'normalized':..., 'selected':True/False, 'status':''/'success'/'failed'}
#     example = [f'180012300{str(i).zfill(2)}' for i in range(1,11)]
#     st.session_state.numbers = [{'raw':n, 'normalized':n, 'selected':True, 'status':''} for n in example]
# if 'log' not in st.session_state:
#     st.session_state.log = []
# if 'calling' not in st.session_state:
#     st.session_state.calling = False

# def log(msg):
#     t = time.strftime('%H:%M:%S')
#     st.session_state.log.insert(0, f'[{t}] {msg}')
#     st.session_state.log = st.session_state.log[:500]

# def normalize_number(s):
#     return ''.join(ch for ch in s if ch.isdigit() or ch=='+')

# st.title('Autodialer — Streamlit Prototype')
# st.markdown('**Note:** This is a *frontend simulation*. Do not use real personal numbers while testing. Prefilled safe `1800...` numbers are included.')

# tab = st.tabs(["Call", "Blog"])
# with tab[0]:
#     col1, col2 = st.columns([3,1])
#     with col1:
#         st.subheader('Upload / Dialpad')
#         upload_mode = st.radio('Choose input method', ('Upload Numbers', 'Dialpad'), horizontal=True)
#         if upload_mode == 'Upload Numbers':
#             txt = st.text_area('Paste numbers (one per line)', height=200, placeholder='e.g.\n18001234567\n18007654321\n+911234567890')
#             uploaded = st.file_uploader('Or upload a .txt or .csv file', type=['txt','csv'])
#             if uploaded is not None:
#                 try:
#                     raw = uploaded.read().decode('utf-8')
#                 except:
#                     raw = uploaded.getvalue().decode('utf-8')
#                 txt = (txt + '\n' + raw).strip()
#             col_a, col_b = st.columns([1,1])
#             with col_a:
#                 if st.button('Parse & Add'):
#                     lines = [l.strip() for l in txt.splitlines() if l.strip()!='']
#                     added = 0
#                     for l in lines:
#                         nr = normalize_number(l)
#                         if nr == '': continue
#                         st.session_state.numbers.append({'raw':l, 'normalized':nr, 'selected':True, 'status':''})
#                         added += 1
#                     log(f'Parsed and added {added} numbers')
#             with col_b:
#                 if st.button('Clear List'):
#                     st.session_state.numbers = []
#                     log('Cleared number list')
#         else:
#             st.write('Use the dialpad to compose a number and add to the list')
#             if 'dial_display' not in st.session_state:
#                 st.session_state.dial_display = ''
#             dial_cols = st.columns([1,1,1])
#             keys = ['1','2','3','4','5','6','7','8','9','*','0','#']
#             for i,k in enumerate(keys):
#                 if st.button(k, key=f'k{i}'):
#                     st.session_state.dial_display += k
#             st.write('**Number:**', st.session_state.dial_display)
#             dcol1, dcol2 = st.columns([1,1])
#             with dcol1:
#                 if st.button('Add to list'):
#                     val = st.session_state.dial_display.strip()
#                     if val!='':
#                         nr = normalize_number(val)
#                         st.session_state.numbers.append({'raw':val, 'normalized':nr, 'selected':True, 'status':''})
#                         st.session_state.dial_display = ''
#                         log('Added number '+val)
#             with dcol2:
#                 if st.button('Clear'):
#                     st.session_state.dial_display = ''

#         st.markdown('---')
#         st.subheader('AI Prompt (front-end simulation)')
#         ai_prompt = st.text_area('Type an instruction for the AI assistant (e.g. "make a call to 18001230001")', height=120)
#         ai_col1, ai_col2 = st.columns([1,1])
#         with ai_col1:
#             if st.button('Run AI (simulate)'):
#                 p = ai_prompt.strip()
#                 if p == '':
#                     st.warning('Write an AI instruction first')
#                 else:
#                     log(f'AI prompt submitted: \"{p}\"')
#                     import re
#                     m = re.search(r'make a call to\\s+([0-9+\\-\\s]+)', p, re.I)
#                     if m:
#                         num = m.group(1).strip()
#                         nr = normalize_number(num)
#                         st.session_state.numbers.append({'raw':num, 'normalized':nr, 'selected':True, 'status':''})
#                         log('AI added number '+num)
#                     else:
#                         log('AI did not recognise a specific actionable instruction. (frontend demo)')
#         with ai_col2:
#             if st.button('Start Calls'):
#                 if st.session_state.calling:
#                     st.warning('Already calling')
#                 else:
#                     st.session_state.calling = True
#                     log('Starting call sequence...')
#                     queue = [n for n in st.session_state.numbers if n['selected'] and n['status']=='']
#                     placeholder = st.empty()
#                     for i, item in enumerate(queue):
#                         if not st.session_state.calling:
#                             log('Call sequence stopped by user')
#                             break
#                         placeholder.markdown(f'**Calling:** {item["raw"]} ({i+1}/{len(queue)})')
#                         log(f'Calling {item["raw"]} ...')
#                         time.sleep(0.9 + random.random()*0.6)
#                         ok = random.random() > 0.3
#                         item['status'] = 'success' if ok else 'failed'
#                         if ok:
#                             log(f'Result for {item["raw"]}: PICKED / SUCCESS')
#                         else:
#                             log(f'Result for {item["raw"]}: FAILED / NO ANSWER')
#                         time.sleep(0.05)
#                     st.session_state.calling = False
#                     placeholder.empty()
#                     log('All queued calls processed')
#             if st.button('Stop'):
#                 if st.session_state.calling:
#                     st.session_state.calling = False
#                     log('Stop requested')
#                 else:
#                     st.info('Not currently calling')

#         st.markdown('---')
#         st.subheader('Number List (click to select/deselect)')
#         nums = st.session_state.numbers
#         if len(nums)==0:
#             st.info('No numbers in list. Add via upload or dialpad.')
#         else:
#             for idx, n in enumerate(nums):
#                 cols = st.columns([0.06, 0.44, 0.3, 0.2])
#                 sel = cols[0].checkbox('', value=n.get('selected', False), key=f'sel_{idx}')
#                 if sel != n.get('selected', False):
#                     st.session_state.numbers[idx]['selected'] = sel
#                 cols[1].markdown(f'**{n["raw"]}**')
#                 cols[2].write(n['normalized'])
#                 status = n.get('status', '')
#                 if status=='success':
#                     cols[3].markdown(f':heavy_check_mark: **{status}**')
#                 elif status=='failed':
#                     cols[3].markdown(f':x: **{status}**')
#                 else:
#                     cols[3].markdown(status)

#     with col2:
#         st.subheader('Summary & Stats')
#         total = len(st.session_state.numbers)
#         selected = sum(1 for n in st.session_state.numbers if n.get('selected'))
#         success = sum(1 for n in st.session_state.numbers if n.get('status')=='success')
#         failed = sum(1 for n in st.session_state.numbers if n.get('status')=='failed')
#         remaining = total - success - failed
#         st.metric('Total uploaded', total)
#         st.metric('Selected / queued', selected)
#         st.metric('Success', success)
#         st.metric('Failed', failed)
#         st.metric('Remaining', remaining)

#         st.markdown('---')
#         st.subheader('Call Log')
#         for line in st.session_state.log[:200]:
#             st.write(line)

# with tab[1]:
#     st.subheader('Blog Section (UI placeholder)')
#     st.markdown('This area will hold blog creation tools and an AI prompt for drafting posts. Implement after call flow.')
#     blog_prompt = st.text_area('AI prompt for blog', height=200)
#     if st.button('Generate Blog'):
#         log('Blog AI prompt submitted (frontend demo).')
#         st.success('Generated draft (demo):\n\n' + (blog_prompt[:500] + '...' if len(blog_prompt)>500 else blog_prompt))

# st.markdown('---')
# st.caption('Frontend-only Streamlit prototype. Replace simulation code with real backend (Rails/Twilio/AI) to make production calls. Use only test numbers while developing.')
