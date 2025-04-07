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

    # Открыть страницу с нужным контентом
    browser.open('https://www.goodshop.com')

    # Проверить, что элемент categories присутствует в хедере
    browser.element('#categories-dropdown-menu').should(be.visible)

    # Навести курсор на элемент "Categories", чтобы раскрыть меню
    categories_header = browser.element('div#categories-dropdown-menu > div.categories-menu')
    categories_header.hover()

    # Перечень категорий и подкатегорий для проверки
    categories = [
        {
            'category_name': 'Accessories',
            'view_all_url': 'https://www.goodshop.com/coupons/clothing-accessories',
            'subcategories': ['Bags', 'Designer Accessories', 'Eyewear', 'Luggage', 'Watches']
        },
        # Добавьте сюда другие категории, если нужно расширить
    ]

    for category in categories:
        # Проверяем наличие самой категории
        category_element = browser.element(f'a[title="{category["category_name"]}"]')
        category_element.should(be.visible)

        # Навести на категорию, чтобы увидеть подкатегории
        category_element.hover()

        # Проверка, что все подкатегории видны
        for subcategory in category['subcategories']:
            subcategory_element = browser.element(f'a[title="{subcategory}"]')
            subcategory_element.should(be.visible)

        # Кликнуть по ссылке "View all" и проверка перехода
        view_all_link = browser.element(f'a[title="View all stores in this category"]')
        view_all_link.click()

        # Проверяем, что URL изменился на нужный
        browser.should(have.url(category['view_all_url']))

        # Возвращаемся на исходную страницу после проверки
        browser.back()