from selene import browser, have, be


def test_facebook_button():
    # Открываем тестируемую страницу
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')
    # Сохраняем идентификатор текущего окна
    main_window = browser.config.driver.current_window_handle
    # Запоминаем все открытые окна до клика
    initial_windows = set(browser.config.driver.window_handles)

    # Кликаем по кнопке "share"
    browser.element('[title="share"]').click()
    # Ожидаем появления нового окна
    browser.wait.until(lambda: len(browser.config.driver.window_handles) > len(initial_windows))

    # Находим новое окно, которого не было раньше
    new_window = (set(browser.config.driver.window_handles) - initial_windows).pop()
    # Переключаемся в новое окно
    browser.switch_to.window(new_window)

    # Проверяем, что URL нового окна содержит "facebook.com"
    browser.should(have.url_containing('facebook.com'))


def test_twitter_button():
    # Открываем тестируемую страницу
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')
    # Сохраняем идентификатор текущего окна
    main_window = browser.config.driver.current_window_handle
    # Запоминаем все открытые окна до клика
    initial_windows = set(browser.config.driver.window_handles)

    # Кликаем по кнопке "share"
    browser.element('[data-js="twitter-share"]').click()
    # Ожидаем появления нового окна
    browser.wait.until(lambda: len(browser.config.driver.window_handles) > len(initial_windows))

    # Находим новое окно, которого не было раньше
    new_window = (set(browser.config.driver.window_handles) - initial_windows).pop()
    # Переключаемся в новое окно
    browser.switch_to.window(new_window)

    # Проверяем, что URL нового окна содержит "x.com" или "twitter.com"
    browser.should(have.url_containing('x.com' or 'twitter.com'))
