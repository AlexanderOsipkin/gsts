from selene import browser, have, query, be, by
from datetime import datetime
import time


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
    # Ожидаем появления нового окна браузера
    browser.wait.until(lambda: len(browser.config.driver.window_handles) > len(initial_windows))

    # Находим новое окно браузера, которого не было раньше
    new_window = (set(browser.config.driver.window_handles) - initial_windows).pop()
    # Переключаемся в новое окно браузера
    browser.switch_to.window(new_window)

    # Проверяем, что URL нового окна браузера содержит "x.com" или "twitter.com"
    browser.should(have.url_containing('x.com' or 'twitter.com'))


def test_about_of_organization():
    # Открываем тестируемую страницу
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')

    # Проверяем, что заголовки и детали присутствуют
    elements = browser.all('.cause-about > *')

    # Извлекаем текст всех элементов на странице
    about_texts = [element.get(query.text) for element in elements]

    # Логируем найденные все значения
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} About Section: {', '.join(about_texts)}\n---------------------\n"

    # Записываем значения в файл
    with open("about_of_charity_organization.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)

    # Логируем в консоль
    print("Сохранены значения About Section:", log_entry)


def test_amount_raised():
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')

    browser.element('[href="#filter-amount"]').click()
    browser.element('div.together').should(have.text('TOGETHER, WE\'VE RAISED'))

    # Кликаем на селект, чтобы открыть список
    browser.element('select#year').click()

    # Выбираем нужный год по видимому тексту
    browser.element('select#year').element(by.text('2012')).click()

    # Ждём появления таблицы
    browser.element('div.breakdown').should(be.visible)

    # Ищем строку "2012 Total" и проверяем значение
    row = browser.all('div.breakdown tbody tr').element_by(have.text('2012 Total'))
    row.element('td:last-child').should(have.exact_text('$13.67'))


def test_how_it_works_section():
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')

    how_it_works = browser.element('div.how-it-works')

    # Проверяем заголовок
    how_it_works.element('.main-title').should(have.exact_text('How it works...'))

    steps = how_it_works.all('.step')

    # Проверяем, что все 3 элемента есть на странице
    steps.should(have.size(3))

    # You Shop.
    steps[0].element('.title').should(have.exact_text('You Shop.'))
    steps[0].element('.details').should(have.text('Shop at your favorite stores through Goodshop'))

    # You Save.
    steps[1].element('.title').should(have.exact_text('You Save.'))
    steps[1].element('.details').should(have.text('Save big on all your purchases'))

    # We Give.
    steps[2].element('.title').should(have.exact_text('We Give.'))
    steps[2].element('.details').should(have.text('we make a donation in your honor'))

    # Проверяем наличие кнопки "Get Started"
    how_it_works.element('a.get-started').should(have.exact_text('Get Started'))
    how_it_works.element('a.get-started').should(be.visible)


def test_cookie_settings_toggle_on_page():
    browser.open('https://www.goodshop.com/nonprofit/green-park-lutheran-school')

    # Шаг 1: Закрытие баннера куки, если он существует
    banner = browser.element('#consentBanner')
    if banner.should(be.visible):
        banner.element('.bannerButton a.ok').click()

    # Шаг 2: Ожидание исчезновения баннера и клик по кнопке для открытия настроек куки
    browser.element('#consentFloatingButton').click()  # Открываем настройки куки

    cookie_settings = browser.element('#consentSettings')
    cookie_settings.should(be.visible)

    # Заголовок
    cookie_settings.element('.settingsTitle').should(have.exact_text('Your cookie settings'))

    all_cookies = ['necessary', 'preferences', 'statistics', 'marketing']

    def assert_all_granted():
        for group in all_cookies:
            item = cookie_settings.element(f'.settingsItem.{group}')
            item.should(be.visible)
            item.should(have.text(group.capitalize()))
            item.element('span.granted').should(be.visible)
            item.element('span.denied').should(be.hidden)

    def assert_only_necessary_granted():
        for group in all_cookies:
            item = cookie_settings.element(f'.settingsItem.{group}')
            if group == 'necessary':
                item.element('span.granted').should(be.visible)
                item.element('span.denied').should(be.hidden)
            else:
                item.element('span.granted').should(be.hidden)
                item.element('span.denied').should(be.visible)

    # Step 1: всё включено
    assert_all_granted()

    # Step 2: отключаем — Withdraw consent
    cookie_settings.element('.settingsWithdrawButton').click()

    # Добавим небольшую задержку для обновления состояния
    time.sleep(1)  # Ждем 1 секунду, чтобы элементы обновились

    assert_only_necessary_granted()

    # Step 3: снова включаем — Approve consent
    cookie_settings.element('.settingsApproveButton').click()

    # Добавим задержку после клика на Approve
    time.sleep(1)  # Ждем 1 секунду, чтобы элементы обновились

    assert_all_granted()
