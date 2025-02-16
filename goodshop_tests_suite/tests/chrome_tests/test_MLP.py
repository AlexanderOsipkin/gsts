from selene import browser, have


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
    browser.element('span.star.icon-star-on[data-alt="4"]').click() # Выбираем рейтинг
    browser.should(have.url_containing('https://www.goodshop.com/login')) # Проверка url
