import logging
from datetime import datetime
from selene import browser, have, be
from goodshop_tests_suite.tests.chrome_tests.categories_data import categories

# Настройка логирования для категорий
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Создаем файл обработчик для записи логов в файл
file_handler = logging.FileHandler('header_categories_log.txt', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Формат вывода
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем файл обработчик в логгер
logger.addHandler(file_handler)


def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} {message}\n---------------------\n"

    with open("header_categories_log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)


def test_logo_icon():
    browser.open('https://www.goodshop.com/coupons/baby-clothing')

    # Закрытие баннера куки
    banner = browser.element('#consentBanner')
    if banner.should(be.visible):
        banner.element('.bannerButton a.ok').click()

    browser.element('[data-track-click-type="goodshop logo"]').click()
    browser.element('div.block-title').should(have.text('Our Favorite Stores'))


def verify_category(category_name, expected_subcategories, expected_stores):
    try:
        # Логируем начало проверки категории
        logger.info(f"Проверка категории: {category_name}")

        # Находим категорию и наводим курсор
        category_element = browser.element(f'li.category-item a[title="{category_name}"]')
        category_element.hover()

        # Получаем информацию о подкатегориях и магазинах
        category_detail = category_element.element('..').element('.category-detail')
        category_detail.should(be.visible)

        # Проверка подкатегорий
        logger.info(f"Ожидаемые подкатегории: {expected_subcategories}")
        category_detail.all('ul.sub-categories li.category-item a').should(have.texts(*expected_subcategories))

        # Проверка магазинов
        logger.info(f"Ожидаемые магазины: {expected_stores}")
        category_detail.all('.category-featured-stores .title').should(have.texts(*expected_stores))

    except Exception as e:
        logger.error(f"Ошибка при проверке категории '{category_name}': {e}")
        raise


def verify_all_stores_link():
    try:
        # Проверка ссылки "See all stores"
        logger.info("Проверка ссылки 'See all stores'")
        all_stores_element = browser.element('.all-stores a[title="See all stores"]')
        all_stores_element.should(be.visible)
        all_stores_element.should(have.text("See all stores"))
        all_stores_element.should(have.attribute("href", "https://www.goodshop.com/coupons"))

    except Exception as e:
        logger.error(f"Ошибка при проверке ссылки 'See all stores': {e}")
        raise


def test_category_dropdowns_and_subcategories():
    browser.open('https://www.goodshop.com')

    # Закрытие баннера куки
    banner = browser.element('#consentBanner')
    if banner.should(be.visible):
        banner.element('.bannerButton a.ok').click()

    # Убедитесь, что элемент с id="categories" существует на странице
    categories_button = browser.element('.navbar .categories')
    categories_button.should(be.visible)

    # Навести курсор на элемент с id="categories" для раскрытия выпадающего меню
    categories_button.hover()

    # Проверить, что выпадающее меню с id="categories-dropdown-menu" появилось
    dropdown_menu = browser.element('.navbar .categories')
    dropdown_menu.should(be.visible)

    # Проверка всех категорий
    for category_name, data in categories.items():
        verify_category(category_name, data["subcategories"], data["stores"])

    # Проверка ссылки "See all stores"
    verify_all_stores_link()


def test_goodsearch_button():
    browser.open('https://www.goodshop.com')
    # нажимаем на нужный нам элемент
    browser.element('[data-track-click-type="goodsearch link"]').click()
    # убеждаемся что нас перешли на нужную страницу
    browser.should(have.url_containing('https://www.goodsearch.com'))
    browser.element('[id="keywords"]').should(be.visible)
    browser.element('.Search_odometerLabel__t7vyl').should(have.text('In Donations Earned'))


def test_holiday_page():
    browser.open('https://www.goodshop.com')
    # нажимаем на нужную кнопку
    browser.element('.navbar li.holiday-item').click()
    # проверяем что перешли на нужную страницу
    browser.element('.block-title').should(have.text('Coupon Codes & Deals'))
    browser.element('.alphabet').should(have.text('Browse by Store'))
