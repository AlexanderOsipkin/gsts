from selene import browser, have
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os


def test_merchants_logo():
    browser.open("https://www.goodshop.com/coupons/joann.com")  # Открываем тестируемую страницу
    browser.element('.merchant-header h1').should(have.text(
        'JOANN Fabric & Craft Coupons, Discounts and Promo Codes'))  # проверяем что перешли на нужную страницу
    link = browser.element(
        '[id="sidebar"] [data-deal-redirect-type="logo-header-m"]')  # Находим элемент, который открывает новую вкладку

    initial_windows = set(browser.driver.window_handles)  # Получаем список вкладок до клика
    link.click()  # Кликаем по ссылке

    new_windows = set(browser.driver.window_handles) - initial_windows  # Определяем новые вкладки

    if not new_windows:
        raise Exception("Новая вкладка не была открыта")

    for new_window in new_windows:
        browser.driver.switch_to.window(new_window)  # Переключаемся на новую вкладку
        if "joann.com" in browser.driver.current_url:
            browser.should(have.url("https://www.joann.com/"))  # Проверяем, что открылась нужная вкладка
            break
    else:
        raise Exception("Не найдено окно с ожидаемым URL")


def test_add_rating_with_not_login():
    browser.open("https://www.goodshop.com/coupons/joann.com")  # Открываем тестируемую страницу
    browser.element('span.star.icon-star-on[data-alt="4"]').click()  # Выбираем рейтинг
    browser.should(have.url_containing('https://www.goodshop.com/login'))  # Проверка url


def test_store_info():
    browser.open("https://www.goodshop.com/coupons/joann.com")  # Открываем тестируемую страницу
    browser.element('[data-js="additional-store-info-media-box"]').should(
        have.text('JOANN Fabric & Craft Store Info'))  # проверяем что есть блок информации


def test_FAQ_block():
    browser.open("https://www.goodshop.com/coupons/joann.com")  # Открываем тестируемую страницу
    browser.element('.blurb.how-to-use').should(
        have.text('More FAQs for JOANN Fabric & Craft'))  # проверяем что блок FAQ есть


def test_coupon_id():
    browser.open("https://www.goodshop.com/coupons/joann.com")  # Открываем тестируемую страницу
    link = browser.element('[data-deal-position="1"]')  # Находим купон №1 и кликаем на него

    initial_windows = set(browser.driver.window_handles)  # Получаем список вкладок до клика на кнопку
    link.click()  # Кликаем по кнопке

    new_windows = set(browser.driver.window_handles) - initial_windows  # Определяем новые вкладки браузера

    if not new_windows:
        raise Exception("Новая вкладка не была открыта")  # если вкладка не открыта, пишем это

    for new_window in new_windows:
        browser.driver.switch_to.window(new_window)  # Переключаемся на новую вкладку
        current_url = browser.driver.current_url

        if "joann.com" in current_url:
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)  # Разбираем параметры URL
            string_coupon_id = query_params.get("open", [None])[0]  # Извлекаем значение после ?open=

            if string_coupon_id and string_coupon_id.isdigit():  # Проверяем, что значение является числом
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущую дату и время
                log_entry = f"{timestamp} StringCouponID: {string_coupon_id}\n---------------------\n"

                with open("saved_data.txt", "a") as file:
                    file.write(log_entry)  # Добавляем запись в файл в виде столбика
                print("Сохранено значение StringCouponID:", log_entry)  # Логируем
            else:
                raise Exception("Некорректное или отсутствующее значение параметра 'StringCouponID' в URL")
            return
        raise Exception("Не найдено окно с ожидаемым URL")
