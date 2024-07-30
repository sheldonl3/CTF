import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
import winsound
'''
通过palywright库模仿浏览器点击，自动刷新s6000“漏洞预警”内容，如果有新的预警则通过音乐提升值班人员
'''
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置部分
config = {
    "url": 'http://10.157.199.76/Portal/mainAdmin/main',
    "login_page_url": 'http://10.157.199.76/Portal/mainAdmin/main',
    "target_page_url": 'http://10.157.199.76/Portal/mainAdmin/main',
    "username_selector": '#username',
    "password_selector": '#password',
    "login_button_selector": '#submit_login',
    "navigate_button_selector": '#navigate-button',
    "element_selector": '#element-id',
    "username": 'XXXXXXX',
    "password": 'XXXXXXX',
    "iframe_src": '/s6000-earlyAlarm-pro/early-alarm-jump/home',
    "td_selector": 'td.el-table_1_column_9',
    "music": '4709.wav'
}


def fetch_element_value(page, selector):
    element = page.query_selector(selector)
    return element.text_content() if element else None


def fetch_element_value_td(td):
    span = td.locator("span data-v-15933b16")
    if span.is_hidden():
        logger.warning("Element is hidden")
    return span.text_content() if span else "空的span"


def play_music(total_time):
    start_time = time.time()
    try:
        while time.time() - start_time < total_time:
            winsound.PlaySound(config["music"], winsound.SND_LOOP)
    except Exception as e:
        logger.error(f"Error playing sound: {e}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome", args=["--window-size=1920,1080"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            # 打开登录页面
            logger.info("Navigating to login page")
            page.goto(config["login_page_url"])

            # 输入用户名和密码并登录
            logger.info("Filling in login credentials")
            page.fill(config["username_selector"], config["username"])
            page.fill(config["password_selector"], config["password"])
            page.click(config["login_button_selector"])
            page.goto(config["target_page_url"])

            while True:
                # 定位需要监控的元素
                spans = page.query_selector_all('span')
                for span in spans:
                    span_text = span.inner_text().strip()
                    logger.info(f"Found span with text: {span_text}")

                    if span_text == '应急响应' and span.is_visible():
                        span.click()
                        logger.info("Clicked on 应急响应 span")
                        page.wait_for_selector("span:has-text('网省预警')")

                    if span_text == '网省预警' and span.is_visible():
                        span.click()
                        logger.info("Clicked on 网省预警 span")
                        page.wait_for_selector("span:has-text('漏洞预警')")

                    if span_text == '漏洞预警' and span.is_visible():
                        span.click()
                        logger.info("Clicked on 漏洞预警 span")
                        break

                logger.info("Searching for 漏洞")
                page.wait_for_selector(f'iframe[src*="{config["iframe_src"]}"]')
                iframes = page.query_selector_all(f'iframe[src*="{config["iframe_src"]}"]')

                if not iframes:
                    logger.warning("No iframes found")
                    continue

                logger.info("Iframe found")
                iframe = iframes[0].content_frame()
                iframe.wait_for_selector(config["td_selector"])
                tds = iframe.query_selector_all(config["td_selector"])

                for td in tds:
                    span_text = fetch_element_value_td(td)
                    logger.info(f"Found span text: {span_text}")
                    if span_text == "待转发":
                        # 出声
                        logger.info("发现新的漏洞！！！！！！")
                        play_music(config["music"])
                        return
                logger.info("Done searching for 漏洞")
                time.sleep(20)
                page.reload()

        except TimeoutError as e:
            logger.error(f"Timeout error: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            browser.close()


if __name__ == '__main__':
    play_music(60)
