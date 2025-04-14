from selene import browser, have, be
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver.common.action_chains import ActionChains


def test_logo_icon():
    browser.open('https://www.goodshop.com/coupons/baby-clothing')

    # Закрытие баннера куки
    banner = browser.element('#consentBanner')
    if banner.should(be.visible):
        banner.element('.bannerButton a.ok').click()

    browser.element('[data-track-click-type="goodshop logo"]').click()
    browser.element('div.block-title').should(have.text('Our Favorite Stores'))


def test_categories_in_header():
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
    dropdown_menu = browser.element('#categories-dropdown-menu')
    dropdown_menu.should(be.visible)

    # Наводим курсор на категорию "Accessories"
    accessories = browser.element('li.category-item a[title="Accessories"]')
    accessories.hover()

    # Ждем появления блока с подкатегориями
    subcategories_block = browser.element('.category-detail')
    subcategories_block.should(be.visible)

    # Проверяем наличие подкатегорий
    expected_subcategories = [
        "Bags",
        "Designer Accessories",
        "Eyewear",
        "Luggage",
        "Watches"
    ]

    subcategory_elements = subcategories_block.all('ul.sub-categories li.category-item a')

    # Проверка, что количество совпадает
    subcategory_elements.should(have.size(len(expected_subcategories)))

    # Проверка названий
    subcategory_elements.should(have.texts(*expected_subcategories))