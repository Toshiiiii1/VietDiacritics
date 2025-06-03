from bs4 import BeautifulSoup
from pandas import json_normalize
import requests
import feedparser
import os
from selenium import webdriver
import time
from tqdm import tqdm
import newspaper

# Tổng hợp các nguồn tin tức
"""
    {
        rss_urls: lưu các RSS của các trang báo
        main_page: lưu url của trang chính
        tag: tên của thẻ html chứa nội dung bài báo
        class_name: tên lớp của tag chứa nội dung bài báo
    }
"""

train_news = {
    "tuoi_tre": {
        "url": "https://tuoitre.vn",
        "rss_urls": ["https://tuoitre.vn/rss/the-thao.rss"],
        "main_page": ["https://tuoitre.vn/the-thao/bong-ro.htm", "https://tuoitre.vn/the-thao/cac-mon-khac.htm", "https://tuoitre.vn/the-thao/khoe-360.htm"],
        "tag": ["h3", "div"],
        "class": ["box-title-text", "detail-content"],
    },
    "thanh_nien": {
        "url": "https://thanhnien.vn",
        "rss_urls": ["https://thanhnien.vn/rss/the-thao.rss"],
        "main_page": ["https://thanhnien.vn/the-thao/the-thao-khac.htm", "https://thanhnien.vn/the-thao/bong-ro.htm", "https://thanhnien.vn/the-thao/the-thao-cong-dong.htm"],
        "tag": ["h3", "div"],
        "class": ["box-title-text", "detail-content"],
    },
    "nld": {
        "url": "https://nld.com.vn",
        "rss_urls": ["https://nld.com.vn/rss/the-thao.rss"],
        "main_page": ["https://nld.com.vn/the-thao/golf.htm", "https://nld.com.vn/the-thao/cac-mon-khac.htm", "https://nld.com.vn/the-thao/marathon.htm", "https://nld.com.vn/the-thao/tennis.htm"],
        "tag": ["h2", "div"],
        "class": ["box-category-title-text", "detail-content"],
    },
    "vnexpress": {
        "url": "",
        "rss_urls": ["https://vnexpress.net/rss/the-thao.rss"],
        "main_page": [f"https://vnexpress.net/the-thao/cac-mon-khac-p{i}" for i in range(1, 21)],
        "tag": ["h2", "article"],
        "class": ["title-news", "fck_detail"],
    },
    "thethao247": {
        "rss_urls": ["https://thethao247.vn/trang-chu.rss", "https://thethao247.vn/the-thao-24h.rss", "https://thethao247.vn/bong-da.rss", "https://thethao247.vn/world-cup.rss", "https://thethao247.vn/bong-da-viet-nam-c1.rss", "https://thethao247.vn/hang-nhi-2021-c292.rss", "https://thethao247.vn/u20-chau-a-c321.rss", "https://thethao247.vn/v-league-c15.rss", "https://thethao247.vn/giai-hang-nhat-c16.rss", "https://thethao247.vn/tuyen-quoc-gia-vn-c19.rss", "https://thethao247.vn/bong-da-nu-viet-nam-c20.rss", "https://thethao247.vn/noi-soi-bong-da-viet-c33.rss", "https://thethao247.vn/u17-quoc-gia-c161.rss", "https://thethao247.vn/futsal-c184.rss", "https://thethao247.vn/futsal-world-cup-c198.rss", "https://thethao247.vn/j-league-2-c195.rss", "https://thethao247.vn/u21-quoc-te-2020-c220.rss", "https://thethao247.vn/u19-quoc-gia-c225.rss", "https://thethao247.vn/afc-cup-champions-league-c226.rss", "https://thethao247.vn/thai-league-c227.rss", "https://thethao247.vn/u19-chau-a-2020-c239.rss", "https://thethao247.vn/kings-cup-2019-c272.rss", "https://thethao247.vn/giai-vdqg-bi-2019-20-c276.rss", "https://thethao247.vn/giai-vdqg-ha-lan-2019-20-c279.rss", "https://thethao247.vn/jleague-2021-c291.rss", "https://thethao247.vn/bong-da-quoc-te-c2.rss", "https://thethao247.vn/bong-da-anh-c8.rss", "https://thethao247.vn/cup-fa-c22.rss", "https://thethao247.vn/ngoai-hang-anh-c23.rss", "https://thethao247.vn/bong-da-anh-cac-giai-khac-c24.rss", "https://thethao247.vn/cup-lien-doan-c58.rss", "https://thethao247.vn/bong-da-tbn-c9.rss", "https://thethao247.vn/La-Liga-c59.rss", "https://thethao247.vn/cup-nha-vua-c60.rss", "https://thethao247.vn/bong-da-TBN-cac-giai-khac-c61.rss", "https://thethao247.vn/bong-da-y-c10.rss", "https://thethao247.vn/serie-a-c62.rss", "https://thethao247.vn/coppa-italia-c63.rss", "https://thethao247.vn/bong-da-italia-cac-giai-khac-c64.rss", "https://thethao247.vn/bong-da-phap-c12.rss", "https://thethao247.vn/ligue-one-c68.rss", "https://thethao247.vn/bong-da-Phap-cup-quoc-gia-c69.rss", "https://thethao247.vn/champions-league-c13.rss", "https://thethao247.vn/chung-ket-cup-c1-c91.rss", "https://thethao247.vn/cac-giai-bong-da-quoc-te-khac-c34.rss", "https://thethao247.vn/europa-league-c75.rss", "https://thethao247.vn/bong-da-duc-c11.rss", "https://thethao247.vn/bundes-liga-c65.rss", "https://thethao247.vn/cup-quoc-gia-duc-c66.rss", "https://thethao247.vn/bong-da-Duc-cac-giai-khac-c67.rss", "https://thethao247.vn/the-thao-tong-hop-c5.rss", "https://thethao247.vn/quan-vot-tennis-c4.rss", "https://thethao247.vn/ket-qua-tennis-c37.rss", "https://thethao247.vn/tin-tuc-tennis-c39.rss", "https://thethao247.vn/ban-tin-the-thao-c40.rss", "https://thethao247.vn/bong-ro-c43.rss", "https://thethao247.vn/cau-long-c44.rss", "https://thethao247.vn/bong-chuyen-c45.rss", "https://thethao247.vn/vtv-cup-2013-c118.rss"],
        "tag": "div",
        "class": "txt_content",
    },
    "vtc": {
        "rss_urls": ["https://vtc.vn/rss/the-thao.rss"],
        "tag": "div",
        "class": "edittor-content", # edittor-content box-cont mt15 clearfix 
    },
    "bongda24h": {
        "rss_urls": ["https://bongda24h.vn/RSS/172.rss", "https://bongda24h.vn/RSS/180.rss", "https://bongda24h.vn/RSS/180.rss", "https://bongda24h.vn/RSS/184.rss"],
        "tag": "div",
        "class": "the-article-content",
    },
    "webthethao": {
        "rss_urls": ["https://webthethao.vn/rss/rss.php"],
        "tag": "div",
        "class": "shortcode-content", # shortcode-content ck-content
    },
    "baogiaothong": {
        "rss_urls": ["https://www.baogiaothong.vn/rss/the-thao.rss"],
        "tag": "div",
        "class": "detail-content",
    },
    "nguoiduatin": {
        "rss_urls": ["https://www.nguoiduatin.vn/rss/the-thao.rss", "https://www.nguoiduatin.vn/rss/bong-da-anh.rss", "https://www.nguoiduatin.vn/rss/bong-da-viet-nam.rss", "https://www.nguoiduatin.vn/rss/bong-da-tay-ban-nha.rss", "https://www.nguoiduatin.vn/rss/bong-da-duc.rss", "https://www.nguoiduatin.vn/rss/bong-da-chau-au.rss"],
        "tag": "article",
        "class": "article-content",
    },
    "tinthethao": {
        "rss_urls": ["https://www.tinthethao.com.vn/feed.rss", "https://www.tinthethao.com.vn/feed.rss", "https://www.tinthethao.com.vn/v-league.rss", "https://www.tinthethao.com.vn/hang-nhat.rss", "https://www.tinthethao.com.vn/cac-dt-quoc-gia.rss", "https://www.tinthethao.com.vn/cup-quoc-gia.rss", "https://www.tinthethao.com.vn/giai-tre.rss", "https://www.tinthethao.com.vn/giai-khac.rss", "https://www.tinthethao.com.vn/bong-da-nu.rss", "https://www.tinthethao.com.vn/vff.rss", "https://www.tinthethao.com.vn/tin-khac.rss", "https://www.tinthethao.com.vn/quan-vot.rss", "https://www.tinthethao.com.vn/bong-ro.rss", "https://www.tinthethao.com.vn/nba.rss", "https://www.tinthethao.com.vn/vba.rss", "https://www.tinthethao.com.vn/cac-giai-khac.rss", "https://www.tinthethao.com.vn/cach-choi--luat-thi-dau.rss", "https://www.tinthethao.com.vn/oto--xe-may.rss", "https://www.tinthethao.com.vn/o-to.rss", "https://www.tinthethao.com.vn/xe-may.rss", "https://www.tinthethao.com.vn/tap-chi-xe-the-thao.rss", "https://www.tinthethao.com.vn/cau-long.rss", "https://www.tinthethao.com.vn/dien-kinh.rss", "https://www.tinthethao.com.vn/boi-loi.rss", "https://www.tinthethao.com.vn/golf.rss"],
        "tag": "div",
        "class": "exp_content",
    },
    "soha": {
        "rss_urls": ["https://soha.vn/rss/the-thao.rss", "https://soha.vn/rss/sea-games-32.rss"],
        "tag": "div",
        "class": "detail-content",
    },
    "laodong": {
        "rss_urls": ["https://laodong.vn/rss/the-thao.rss"],
        "tag": "div",
        "class": "art-body",
    },
}

test_news = {
    "danviet": {
        "url": "https://danviet.vn",
        "rss_urls": ["https://danviet.vn/rss/the-thao-1035.rss"],
        "main_page": ["https://danviet.vn/the-thao/bong-chuyen.htm", "https://danviet.vn/the-thao/cac-mon-khac.htm"],
        "tag": ["h2", "div"],
        "class": ["", "dt-content"],
    },
}

val_news  = {
    "dantri": {
        "url": "https://dantri.com.vn",
        "rss_urls": ["https://dantri.com.vn/rss/the-thao.rss"],
        "main_page": [f"https://dantri.com.vn/the-thao/cac-mon-the-thao-khac/trang-{i}.htm" for i in range(1, 16)],
        "tag": ["h3", "div"],
        "class": ["article-title", "singular-content"],
    },
}


# Lấy nội dung từ bài báo cụ thể
def get_news_content(url, tag, tag_class):
    result = ""
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    div = soup.find(tag, tag_class)
    if div is None:
        return ""
    texts = div.find_all("p")
    for text in texts:
        result += " " + text.get_text()
        
    return result


# Lấy nội dung các bài báo từ RSS
def crawl_text_from_rss(news, path):
    # tạo thư mục lưu dữ liệu tương ứng với train, val hoặc test
    if (not os.path.isdir(f"{path}")):
        os.mkdir(f"{path}")
        
    for name in news:
        # tạo thư mục theo tên trang báo để lưu các bài báo tương ứng
        if (not os.path.isdir(f"{path}{name}")):
            os.mkdir(f"{path}{name}")
            
        print(name)

        index = 0
        for rss_url in news[name]["rss_urls"]:
            # print(rss_url)

            # lấy thông tin các bài báo từ rss
            news_feed = feedparser.parse(rss_url)
            df_news_feed = json_normalize(news_feed.entries)
            
            if "summary" in df_news_feed.keys():
                for news_summary, news_url in zip(df_news_feed.summary, df_news_feed.link):
                    soup = BeautifulSoup(news_summary, "html.parser")
                    # print(news_url)
                    with open(os.path.join(f"{path}{name}", f'{index}.txt'), 'w', encoding='utf-8') as f:
                        try:
                            # lấy nội dung tóm tắt + nội dung đầy đủ của bài báo
                            f.write(soup.get_text() + " " + get_news_content(news_url, news[name]["tag"][1], news[name]["class"][1]))
                        except:
                            continue
                    index += 1

# Lấy nội dung các bài báo từ trang chính
def crawl_text_in_main_page(news, path):
    # tạo thư mục lưu dữ liệu tương ứng với train, val hoặc test
    if (not os.path.isdir(f"{path}")):
        os.mkdir(f"{path}")
        
    driver = webdriver.Chrome()
    
    for name in tqdm(news):
        print(name)
        if (not os.path.isdir(f"{path}{name}")):
            os.mkdir(f"{path}{name}")
        
        index = 100
        for mp_url in news[name]["main_page"]:
            # mở trang web
            driver.get(mp_url)
            
            # thời gian tạm ngưng giữa các lần scroll trang web
            scroll_pause_time = 4
            # lấy chiều cao của trang web
            last_height = driver.execute_script("return document.body.scrollHeight")
            i = 1
            # thực hiện thao tác scroll trang web để load các bài báo
            while True:
                driver.execute_script(f"window.scrollTo(0, {last_height * i});")
                i += 1
                time.sleep(scroll_pause_time)
                
                # tính lại chiều cao trang web sao khi scroll
                new_height = driver.execute_script("return document.body.scrollHeight")
                # so sánh chiều cao trang trước khi scroll và sao khi scroll
                if new_height == last_height:
                    break
                # cập nhật chiều cao của trang web sau khi scroll
                last_height = new_height

            # lấy dữ liệu từ HTML của trang web sao khi scroll
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # tìm những url đến mỗi bài báo, tên thẻ và tên lớp tùy biến
            news_urls = soup.find_all(news[name]["tag"][0], news[name]["class"][0])
            for news_url in news_urls:
                with open(os.path.join(f"{path}{name}", f'{index}.txt'), 'w', encoding='utf-8') as f:
                    try:
                        # lấy nội dung bài báo
                        f.write(get_news_content(f"{news[name]['url']}{news_url.find('a')['href']}", news[name]["tag"][1], news[name]["class"][1]))
                    except:
                        continue
                index += 1

    driver.quit()

if __name__ == "__main__":
    # crawl_text_from_rss(train_news, "./train_set/")
    # crawl_text_from_rss(test_news, "./test_set/")
    # crawl_text_from_rss(val_news, "./val_set/")
    
    # crawl_text_in_main_page(train_news, "./train_set/")
    # crawl_text_in_main_page(test_news, "./test_set/")
    # crawl_text_in_main_page(val_news, "./val_set/")

    article = newspaper.article("https://thethao247.vn/441-nhan-dinh-iraq-vs-han-quoc-co-hoi-den-tay-01h15-ngay-6-6-2025-d370282.html")
    print(article.text)