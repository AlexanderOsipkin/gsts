from selene import browser, have, be
from goodshop_tests_suite.tests.chrome_tests.categories_data import categories


def test_logo_icon():
    browser.open('https://www.goodshop.com/coupons/baby-clothing')

    # Закрытие баннера куки
    banner = browser.element('#consentBanner')
    if banner.should(be.visible):
        banner.element('.bannerButton a.ok').click()

    browser.element('[data-track-click-type="goodshop logo"]').click()
    browser.element('div.block-title').should(have.text('Our Favorite Stores'))


def verify_category(category_name, expected_subcategories, expected_stores):
    # Находим категорию и наводим курсор
    category_element = browser.element(f'li.category-item a[title="{category_name}"]')
    category_element.hover()

    # Получаем информацию о подкатегориях и магазинах
    category_detail = category_element.element('..').element('.category-detail')
    category_detail.should(be.visible)

    # Проверка подкатегорий
    category_detail.all('ul.sub-categories li.category-item a').should(have.texts(*expected_subcategories))

    # Проверка магазинов
    category_detail.all('.category-featured-stores .title').should(have.texts(*expected_stores))


def verify_all_stores_link():
    # Проверка ссылки "See all stores"
    all_stores_element = browser.element('.all-stores a[title="See all stores"]')
    all_stores_element.should(be.visible)
    all_stores_element.should(have.text("See all stores"))
    all_stores_element.should(have.attribute("href", "https://www.goodshop.com/coupons"))


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