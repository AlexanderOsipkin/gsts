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


# Данные категорий и подкатегорий
categories = {
    "Accessories": {
        "subcategories": [
            "Bags",
            "Designer Accessories",
            "Eyewear",
            "Luggage",
            "Watches"
        ],
        "stores": [
            "Coach",
            "Alex and Ani",
            "Kate Spade",
            "Shop at Future Memories"
        ]
    },
    "Art": {
        "subcategories": [
            "Art Supplies",
            "Portrait Studios",
            "Prints"
        ],
        "stores": [
            "Photography.com",
            "CanvasDiscount",
            "Blick Art Materials",
            "Shop at Art.com"
        ]
    },
    "Automotive": {
        "subcategories": [
            "Auto Accessories",
            "Auto Parts",
            "Auto Repair",
            "Motorcycle",
            "Motorsports",
            "Tires",
            "Truck"
        ],
        "stores": [
            "Safelite Auto Glass",
            "Tire Rack",
            "Advance Auto Parts",
            "eManualOnline.com"
        ]
    },
    "Baby": {
        "subcategories": [
            "Baby Care",
            "Baby Clothing",
            "Baby Furniture",
            "Diapers"
        ],
        "stores": [
            "Ergobaby",
            "The Honest Company",
            "WeeSprout",
            "Chicco"
        ]
    },
    "Beauty": {
        "subcategories": [
            "Bath And Body",
            "Fragrances",
            "Hair Care",
            "Makeup",
            "Nail Care",
            "Salon",
            "Skin Care",
            "Spa Services"
        ],
        "stores": [
            "Sephora",
            "Aveda",
            "MAC Cosmetics",
            "Honest Beauty"
        ]
    },
    "Books and News": {
        "subcategories": [
            "Books",
            "Magazines",
            "Newspapers"
        ],
        "stores": [
            "AbeBooks",
            "Better World Books",
            "Indigo Books & Music",
            "Bigger Books"
        ]
    },
    "Clothing": {
        "subcategories": [
            "Activewear",
            "Juniors' Clothing",
            "Kids' Clothing",
            "Men's Clothing",
            "Outerwear",
            "Novelty Shirts",
            "Socks",
            "Swimwear",
            "Underwear",
            "Women's Clothing",
            "Workwear"
        ],
        "stores": [
            "ASOS",
            "Old Navy",
            "Lands' End",
            "ABLE Clothing"
        ]
    },
    "Crafts": {
        "subcategories": [
            "Craft Supplies",
            "Hobby",
            "Scrapbooking",
            "Sewing"
        ],
        "stores": [
            "fabric.com",
            "JOANN Fabric & Craft",
            "Michaels",
            "Hobby Lobby"
        ]
    },
    "Electronics": {
        "subcategories": [
            "Audio",
            "Battery",
            "Cameras",
            "Cell Phones",
            "Computers",
            "Electronic Accessories",
            "GPS",
            "Headphones",
            "Phones",
            "Printers",
            "Television"
        ],
        "stores": [
            "Monoprice"
        ]
    }
}


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
