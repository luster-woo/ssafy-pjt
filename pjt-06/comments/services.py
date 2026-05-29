import re
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent.parent
CHROME_DRIVER = BASE_DIR / 'chromedriver-win64' / 'chromedriver.exe'


@dataclass
class CrawlResult:
    matched_company_name: str
    stock_code: str
    comments: list[str]


@dataclass
class CleanResult:
    comments: list[str]
    lower: float | None
    upper: float | None


def fetch_toss_comments(company_name: str, limit: int = 20, max_scroll: int = 10) -> CrawlResult:
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--window-size=1440,1200')
    options.add_argument('--lang=ko-KR')
    user_data_dir = tempfile.mkdtemp(prefix='toss-selenium-')
    options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(service=Service(str(CHROME_DRIVER)), options=options)

    try:
        driver.get('https://www.tossinvest.com/')
        wait = WebDriverWait(driver, 15)

        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body.send_keys('/')
        search_input = _find_search_input(driver, wait)
        search_input.clear()
        search_input.send_keys(company_name)
        search_input.send_keys(Keys.ENTER)

        wait.until(lambda d: '/stocks/' in d.current_url or '/order' in d.current_url)
        stock_code = _extract_stock_code(driver.current_url)
        matched_company_name = _extract_company_name(driver, company_name) or company_name

        community_url = f'https://www.tossinvest.com/stocks/{stock_code}/community'
        driver.get(community_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(1.5)

        comments = _collect_comments(driver, limit=limit, max_scroll=max_scroll)
        return CrawlResult(matched_company_name, stock_code, comments)
    except (TimeoutException, WebDriverException, ValueError) as exc:
        raise RuntimeError(f'토스증권 크롤링 중 오류가 발생했습니다: {exc}') from exc
    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)


def clean_comments(comments: list[str]) -> CleanResult:
    df = pd.DataFrame(comments, columns=['comment'])
    df = df.dropna(subset=['comment'])
    df['comment'] = df['comment'].astype(str).str.strip()
    df = df[df['comment'] != '']

    df['clean'] = df['comment'].apply(lambda value: re.sub(r'[^가-힣a-zA-Z0-9\s]', '', value))
    df['clean'] = df['clean'].str.replace(r'\s+', ' ', regex=True).str.strip()

    pattern_filters = (
        df['clean'].str.match(r'^\d+$', na=False)
        | df['clean'].str.match(r'^[ㅋㅎㅠㅜ]+$', na=False)
        | df['clean'].str.match(r'^[A-Za-z\s]+$', na=False)
        | (df['clean'].str.lower() == 'none')
        | df['clean'].apply(_is_inappropriate)
    )
    df = df[~pattern_filters]
    df['length'] = df['clean'].str.len()

    lower = None
    upper = None
    if len(df) >= 5:
        q1 = df['length'].quantile(0.25)
        q3 = df['length'].quantile(0.75)
        iqr = q3 - q1
        lower = max(5, q1 - 1.5 * iqr)
        upper = q3 + 1.5 * iqr
        df = df[(df['length'] >= lower) & (df['length'] <= upper)]
    else:
        df = df[df['length'] >= 3]

    return CleanResult(df['clean'].tolist(), lower, upper)


def augment_comments(comments: list[str]) -> list[str]:
    augmented = []
    for comment in comments:
        text = comment.strip()
        if not text:
            continue
        if any(keyword in text for keyword in ['목표', '상승', '좋', '기대']):
            augmented.append(f'{text} 앞으로의 흐름도 긍정적으로 지켜볼 만하다')
        elif any(keyword in text for keyword in ['하락', '조정', '걱정', '매도']):
            augmented.append(f'{text} 단기 변동성은 있지만 차분히 확인할 필요가 있다')
        else:
            augmented.append(f'{text} 관련 의견을 조금 더 구체적으로 풀어쓴 댓글이다')
    return augmented


def _find_search_input(driver, wait):
    selectors = [
        "input[placeholder*='검색']",
        "input[placeholder*='회사']",
        "input[type='search']",
        "input[type='text']",
        'input',
    ]
    for selector in selectors:
        try:
            return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            continue
    raise TimeoutException('검색 입력창을 찾지 못했습니다.')


def _extract_stock_code(url: str) -> str:
    match = re.search(r'/stocks/([^/?#]+)', url)
    if match:
        return match.group(1)

    parts = [part for part in url.split('/') if part]
    if 'stocks' in parts:
        return parts[parts.index('stocks') + 1]
    raise ValueError('종목 코드를 찾지 못했습니다.')


def _extract_company_name(driver, query: str) -> str:
    visible_text = driver.execute_script('return document.body.innerText || ""')
    candidates = []

    for raw_text in visible_text.splitlines():
        text = raw_text.strip()
        if not _looks_like_company_name(text):
            continue
        if query in text or text in query:
            candidates.append(text)

    if candidates:
        return sorted(candidates, key=len)[0]

    title = driver.title.replace('토스증권', '').replace('|', '').strip()
    title_parts = [part.strip() for part in re.split(r'[-·|]', title)]
    for part in title_parts:
        if _looks_like_company_name(part):
            return part

    return ''


def _looks_like_company_name(text: str) -> bool:
    if not 2 <= len(text) <= 30:
        return False
    if re.search(r'\d', text) or any(mark in text for mark in ['원', '%', '+', '-']):
        return False
    if not re.search(r'[가-힣A-Za-z]', text):
        return False

    blocked_words = [
        '검색', '주문', '뉴스', '커뮤니티', '토론', '댓글', '인기', '최신',
        '관심', '차트', '현재가', '전일', '시가', '고가', '저가',
    ]
    return not any(word in text for word in blocked_words)


def _collect_comments(driver, limit: int, max_scroll: int) -> list[str]:
    selectors = [
        'div.tc3tm85 span span',
        '#stock-content article span',
        'article span',
        '[data-testid*="comment"] span',
    ]
    comments = []
    last_height = driver.execute_script('return document.body.scrollHeight')

    for _ in range(max_scroll):
        for selector in selectors:
            for element in driver.find_elements(By.CSS_SELECTOR, selector):
                text = element.text.strip()
                if _looks_like_comment(text) and text not in comments:
                    comments.append(text)
                    if len(comments) >= limit:
                        return comments[:limit]

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    return comments[:limit]


def _looks_like_comment(text: str) -> bool:
    blocked = {'댓글', '인기', '최신', '로그인', '좋아요', '답글', '공유'}
    return len(text) >= 2 and text not in blocked


def _is_inappropriate(text: str) -> bool:
    bad_words = ['씨발', '병신', '개새', '좆', '꺼져', '죽어', '미친']
    return any(word in text for word in bad_words)
