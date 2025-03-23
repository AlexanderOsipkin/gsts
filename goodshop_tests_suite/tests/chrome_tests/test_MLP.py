from selene import browser, have, query
from urllib.parse import urlparse, parse_qs
from datetime import datetime


def test_merchants_logo():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # проверяем что перешли на нужную страницу
    browser.element('.merchant-header h1').should(have.text(
        'JOANN Fabric & Craft Coupons, Discounts and Promo Codes'))
    # Находим элемент, который открывает новую вкладку
    link = browser.element(
        '[id="sidebar"] [data-deal-redirect-type="logo-header-m"]')

    # Получаем список вкладок браузера до клика
    initial_windows = set(browser.driver.window_handles)
    link.click()

    # Определяем какие новые вкладки браузера открылись
    new_windows = set(browser.driver.window_handles) - initial_windows

    if not new_windows:
        raise Exception("Новая вкладка не была открыта")

    # Переключаемся на новую вкладку и проверяем что это нужная вкладка
    for new_window in new_windows:
        browser.driver.switch_to.window(new_window)
        if "joann.com" in browser.driver.current_url:
            browser.should(have.url("https://www.joann.com/"))
            break
    else:
        raise Exception("Не найдено окно с ожидаемым URL")


def test_add_rating_with_not_login():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # Выбираем рейтинг
    browser.element('span.star.icon-star-on[data-alt="4"]').click()
    # Проверка url
    browser.should(have.url_containing('https://www.goodshop.com/login'))


def test_store_info():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # проверяем что есть блок информации
    browser.element('[data-js="additional-store-info-media-box"]').should(
        have.text('JOANN Fabric & Craft Store Info'))


def test_faq_block():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # проверяем что блок FAQ есть
    browser.element('.blurb.how-to-use').should(
        have.text('More FAQs for JOANN Fabric & Craft'))


def test_coupon_id():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # Находим купон №1 и кликаем на него
    link = browser.element('[data-deal-position="1"]')

    # Получаем список вкладок до клика на кнопку
    initial_windows = set(browser.driver.window_handles)
    link.click()

    # Определяем новые вкладки браузера
    new_windows = set(browser.driver.window_handles) - initial_windows

    # если вкладка не открыта, пишем это
    if not new_windows:
        raise Exception("Новая вкладка не была открыта")

    # Переключаемся на новую вкладку
    for new_window in new_windows:
        browser.driver.switch_to.window(new_window)
        current_url = browser.driver.current_url

        if "joann.com" in current_url:
            parsed_url = urlparse(current_url)
            # Разбираем параметры URL
            query_params = parse_qs(parsed_url.query)
            # Извлекаем значение после ?open=
            string_coupon_id = query_params.get("open", [None])[0]

            # Проверяем, что значение является числом и получаем текущию дату и время
            if string_coupon_id and string_coupon_id.isdigit():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp} StringCouponID: {string_coupon_id}\n---------------------\n"

                # Добавляем запись в файл в лог
                with open("saved_data.txt", "a") as file:
                    file.write(log_entry)
                print("Сохранено значение StringCouponID:", log_entry)
            else:
                raise Exception("Некорректное или отсутствующее значение параметра 'StringCouponID' в URL")
            return
        raise Exception("Не найдено окно с ожидаемым URL")


def test_breadcrumbs():
    # Открываем тестируемую страницу
    browser.open("https://www.goodshop.com/coupons/joann.com")
    # Находим все элементы .crumb внутри .breadcrumbs
    breadcrumbs = browser.all(".breadcrumbs .crumb")

    # Проверяем, что в breadcrumbs есть хотя бы один элемент
    breadcrumbs.should(have.size_greater_than(0))

    # Получаем текст каждого элемента правильно
    breadcrumb_texts = [crumb.get(query.text) for crumb in breadcrumbs]

    # Логируем найденные элементы
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} Breadcrumbs: {', '.join(breadcrumb_texts)}\n---------------------\n"

    # Записываем в файл
    with open("breadcrumbs.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)

        # Логируем в консоль
    print("Сохранены значения Breadcrumbs:", log_entry)
