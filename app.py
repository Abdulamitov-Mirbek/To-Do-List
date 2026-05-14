import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

# Page configuration
st.set_page_config(
    page_title="AURA - Магазин аксессуаров",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main theme colors */
    :root {{
        --primary: #1A1A2E;
        --secondary: #16213E;
        --accent: #E2C498;
        --light: #F8F6F0;
        --white: #FFFFFF;
        --dark: #0F0F1A;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Overall styling */
    .stApp {{
        background: linear-gradient(135deg, #F8F6F0 0%, #EBE5D9 100%);
    }}
    
    /* Title styling */
    .main-title {{
        font-family: 'Georgia', serif;
        font-size: 4.5rem;
        color: #1A1A2E;
        text-align: center;
        letter-spacing: 8px;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(26, 26, 46, 0.1);
    }}
    
    .subtitle {{
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        color: #8B7D6B;
        text-align: center;
        letter-spacing: 6px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }}
    
    /* Product card styling */
    .product-card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(26, 26, 46, 0.08);
        transition: all 0.4s ease;
        border: 1px solid #E8E0D5;
        height: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .product-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(26, 26, 46, 0.15);
        border-color: #E2C498;
    }}
    
    .product-title {{
        font-family: 'Georgia', serif;
        font-size: 1.3rem;
        color: #1A1A2E;
        font-weight: bold;
        margin-bottom: 8px;
        line-height: 1.3;
    }}
    
    .product-brand {{
        font-family: 'Georgia', serif;
        font-size: 0.9rem;
        color: #8B7D6B;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }}
    
    .product-price {{
        font-family: 'Georgia', serif;
        font-size: 1.6rem;
        color: #1A1A2E;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .old-price {{
        font-size: 1rem;
        color: #999;
        text-decoration: line-through;
        font-weight: normal;
    }}
    
    .product-material {{
        font-family: 'Helvetica', sans-serif;
        font-size: 0.85rem;
        color: #666;
        line-height: 1.6;
        margin-bottom: 15px;
        padding: 10px;
        background: #F8F6F0;
        border-radius: 8px;
    }}
    
    .category-badge {{
        display: inline-block;
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        color: #E2C498;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(90deg, #1A1A2E 0%, #16213E 100%);
        color: #E2C498;
        border: 2px solid #E2C498;
        padding: 12px 30px;
        border-radius: 30px;
        font-family: 'Georgia', serif;
        font-size: 0.9rem;
        font-weight: bold;
        transition: all 0.4s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(90deg, #E2C498 0%, #C9A96E 100%);
        color: #1A1A2E;
        border-color: #1A1A2E;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 26, 46, 0.3);
    }}
    
    /* Feature section */
    .feature-box {{
        background: white;
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(26, 26, 46, 0.08);
        border: 1px solid #E8E0D5;
        transition: all 0.3s ease;
    }}
    
    .feature-box:hover {{
        border-color: #E2C498;
        transform: translateY(-5px);
    }}
    
    .feature-title {{
        font-family: 'Georgia', serif;
        font-size: 1.3rem;
        color: #1A1A2E;
        margin: 15px 0;
        font-weight: bold;
    }}
    
    .feature-text {{
        font-family: 'Helvetica', sans-serif;
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    
    /* Hero section */
    .hero-box {{
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        padding: 60px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 40px rgba(26, 26, 46, 0.3);
    }}
    
    /* Divider */
    .custom-divider {{
        border: none;
        border-top: 2px solid #E8E0D5;
        margin: 50px 0;
    }}
    
    /* Newsletter section */
    .newsletter-box {{
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        padding: 50px;
        border-radius: 20px;
        color: white;
        margin-top: 50px;
        box-shadow: 0 15px 40px rgba(26, 26, 46, 0.3);
    }}
    
    /* Stats counter */
    .stat-number {{
        font-size: 3rem;
        font-weight: bold;
        color: #E2C498;
        font-family: 'Georgia', serif;
    }}
    
    /* Filter styling */
    .stSelectbox label {{
        color: #1A1A2E !important;
        font-family: 'Georgia', serif !important;
        font-weight: bold !important;
    }}
    
    /* Success message */
    .stSuccess {{
        background-color: #E2C498 !important;
        color: #1A1A2E !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Sample accessories data with enhanced information
products_data = [
    {
        "title": "Классические часы «Элеганс»",
        "brand": "AURA Collection",
        "price": "45 900 с",
        "old_price": "52 000 с",
        "material": "Сапфировое стекло • Швейцарский механизм • Кожаный ремешок",
        "category": "Часы",
        "image_code": "A01",
        "description": "Элегантные часы с классическим дизайном, отражающие вневременную красоту. Швейцарское качество в сочетании с итальянским кожаным ремешком.",
        "features": ["Водостойкость 50м", "Батарея 2 года", "Гарантия 2 года", "Премиум упаковка"]
    },
    {
        "title": "Кожаный портфель «Манхэттен»",
        "brand": "AURA Collection",
        "price": "28 500 с",
        "old_price": None,
        "material": "Натуральная кожа • Ручная работа • Отделение для ноутбука",
        "category": "Сумки",
        "image_code": "B02",
        "description": "Премиальный портфель ручной работы из натуральной итальянской кожи. Идеален для профессионалов, ценящих качество и функциональность.",
        "features": ["Отделение для ноутбука 15\"", "5 внутренних карманов", "Регулируемые ручки", "Прочные швы"]
    },
    {
        "title": "Серебряный браслет «Каскад»",
        "brand": "AURA Premium",
        "price": "18 900 с",
        "old_price": "22 000 с",
        "material": "Серебро 925 пробы • Родиевое покрытие • Замок-карабин",
        "category": "Украшения",
        "image_code": "J03",
        "description": "Изящный браслет из серебра высокой пробы с современным дизайном. Прекрасный подарок к любому случаю.",
        "features": ["Вес 12г", "Длина регулируется", "Сертификат подлинности", "Подарочная коробка"]
    },
    {
        "title": "Шелковый платок «Венеция»",
        "brand": "AURA Silk",
        "price": "12 500 с",
        "old_price": None,
        "material": "100% натуральный шелк • Ручная роспись • 90×90 см",
        "category": "Платки",
        "image_code": "S04",
        "description": "Роскошный шелковый платок, расписанный вручную итальянскими художниками. Каждый платок - уникальное произведение искусства.",
        "features": ["Ручная роспись", "100% шелк муслин", "Подходит для волос и шеи", "Легко комбинируется"]
    },
    {
        "title": "Кожаный ремень «Классик»",
        "brand": "AURA Collection",
        "price": "9 800 с",
        "old_price": "11 500 с",
        "material": "Итальянская кожа • Латунная пряжка • Ширина 3.5 см",
        "category": "Ремни",
        "image_code": "B05",
        "description": "Классический кожаный ремень с латунной пряжкой, символизирующий надежность и стиль. Идеальный выбор для повседневного использования.",
        "features": ["Регулируемая длина", "Латунная пряжка", "Долговечная кожа", "Компактная упаковка"]
    },
    {
        "title": "Брошь «Золотая ветвь»",
        "brand": "AURA Premium",
        "price": "22 000 с",
        "old_price": None,
        "material": "Позолота • Кристаллы Swarovski • Ручная работа",
        "category": "Украшения",
        "image_code": "J06",
        "description": "Элегантная брошь с кристаллами Swarovski, выполненная в форме ветви. Подчеркнет утонченный вкус владельца.",
        "features": ["Кристаллы Swarovski", "Позолота 24К", "Длина 5см", "Безопасный замок"]
    },
    {
        "title": "Портмоне «Бизнес»",
        "brand": "AURA Collection",
        "price": "15 600 с",
        "old_price": "18 000 с",
        "material": "Натуральная кожа • 12 отделений • RFID-защита",
        "category": "Кошельки",
        "image_code": "W07",
        "description": "Компактное портмоне с передовой RFID-защитой и множеством отделений. Функциональность встречается с элегантностью.",
        "features": ["RFID-защита", "12 отделений", "Защита от воды", "Тонкий дизайн"]
    },
    {
        "title": "Часы-хронограф «Маэстро»",
        "brand": "AURA Premium",
        "price": "68 000 с",
        "old_price": None,
        "material": "Титановый корпус • Водозащита 100м • Хронограф",
        "category": "Часы",
        "image_code": "A08",
        "description": "Премиальные часы со спортивным духом. Титановый корпус обеспечивает надежность и легкость. Идеальны для активного образа жизни.",
        "features": ["Титановый корпус", "Водозащита 100м", "Люминесцентные стрелки", "Сапфировое стекло"]
    },
    {
        "title": "Кашемировый шарф «Монблан»",
        "brand": "AURA Cashmere",
        "price": "16 900 с",
        "old_price": "19 500 с",
        "material": "100% кашемир • Двухсторонний • 180×30 см",
        "category": "Шарфы",
        "image_code": "S09",
        "description": "Роскошный кашемировый шарф, обеспечивающий максимальный комфорт и тепло. Подходит ко всему гардеробу благодаря классическому дизайну.",
        "features": ["100% кашемир", "Двухсторонний", "Легкий и теплый", "Универсальный размер"]
    },
    {
        "title": "Запонки «Граф»",
        "brand": "AURA Premium",
        "price": "11 200 с",
        "old_price": None,
        "material": "Серебро • Черный оникс • Подарочная коробка",
        "category": "Запонки",
        "image_code": "C10",
        "description": "Мужские запонки высокого класса с черным ониксом. Идеальный аксессуар для деловых встреч и торжественных событий.",
        "features": ["Серебро 925", "Черный оникс", "Подарочная упаковка", "Сертификат"]
    },
    {
        "title": "Сумка-клатч «Опера»",
        "brand": "AURA Collection",
        "price": "32 000 с",
        "old_price": "38 000 с",
        "material": "Кожа страуса • Атласная подкладка • Цепочка",
        "category": "Сумки",
        "image_code": "B11",
        "description": "Роскошная сумка-клатч из редкой кожи страуса с изящной цепочкой. Совершенный выбор для вечерних выходов.",
        "features": ["Кожа страуса", "Серебряная цепочка", "Атласная подкладка", "Регулируемый ремень"]
    },
    {
        "title": "Перчатки «Париж»",
        "brand": "AURA Leather",
        "price": "8 500 с",
        "old_price": None,
        "material": "Ягнячья кожа • Кашемировая подкладка • Сенсорные",
        "category": "Перчатки",
        "image_code": "G12",
        "description": "Элегантные кожаные перчатки с кашемировой подкладкой. Сенсорные, поэтому удобны для использования смартфонов.",
        "features": ["Сенсорные пальцы", "Кашемировая подкладка", "Размеры XS-XL", "Быстросохнущие"]
    },
]

# Create product image with PIL
def create_product_image(code, width=300, height=250):
    """Generate a product image with gradient background"""
    img = Image.new('RGB', (width, height), color=(250, 246, 240))
    draw = ImageDraw.Draw(img)
    
    # Create gradient-like effect with rectangles
    for i in range(width):
        # Gradient from #1A1A2E to #2D2D4A
        r = int(26 + (45 - 26) * i / width)
        g = int(26 + (45 - 26) * i / width)
        b = int(46 + (74 - 46) * i / width)
        draw.line([(i, 0), (i, height)], fill=(r, g, b))
    
    # Add border
    draw.rectangle([(2, 2), (width-2, height-2)], outline=(226, 196, 152), width=2)
    
    # Add text
    text_y = height // 2 - 30
    draw.text((width // 2, text_y - 20), "AURA", fill=(226, 196, 152), anchor="mm", font=None)
    draw.text((width // 2, text_y + 30), code, fill=(226, 196, 152), anchor="mm", font=None)
    
    return img

# Display product card using Streamlit components
def display_product_card(product, idx, key_prefix=""):
    """Display a product card without HTML"""
    # Display product image
    img = create_product_image(product["image_code"])
    st.image(img, use_column_width=True, caption=None)
    
    # Display product info
    st.markdown(f"**{product['category'].upper()}**")
    st.markdown(f"##### {product['title']}")
    st.caption(f"{product['brand']}")
    
    # Price
    if product["old_price"]:
        st.markdown(f"**{product['price']}** ~~{product['old_price']}~~")
    else:
        st.markdown(f"**{product['price']}**")
    
    # Material/Features
    st.caption(product['material'])
    
    # Features
    if 'features' in product:
        with st.expander("📋 Особенности"):
            for feature in product['features']:
                st.write(f"• {feature}")
    
    # Description
    with st.expander("ℹ️ Описание"):
        st.write(product['description'])
    
    # Buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Подробнее", key=f"{key_prefix}_detail_{idx}", use_container_width=True):
            st.session_state.selected_product = product
            st.session_state.page = "product_detail"
            st.rerun()
    with col_btn2:
        if st.button("🛒 Корзина", key=f"{key_prefix}_cart_{idx}", use_container_width=True):
            st.session_state.cart_count += 1
            st.success(f"✓ {product['title']} добавлен в корзину!")
            st.rerun()

# Main container
with st.container():
    # Header
    st.markdown('<div class="main-title">A U R A</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">✦ Премиальные аксессуары ✦</div>', unsafe_allow_html=True)
    
    # Navigation Bar
    cols = st.columns(7)
    nav_pages = [
        ("🏠 Главная", "home"),
        ("📦 Каталог", "shop"),
        ("⭐ Новинки", "new"),
        ("ℹ️ О бренде", "about"),
        ("📞 Контакты", "contact"),
        ("🔍 Поиск", "search"),
    ]
    
    for i, (label, page) in enumerate(nav_pages):
        with cols[i]:
            if st.button(label, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()
    
    st.divider()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'cart_count' not in st.session_state:
        st.session_state.cart_count = 0
    
    # Page routing
    if st.session_state.page == "home":
        st.markdown("## Искусство Детали")
        st.markdown("""
        Каждый аксессуар AURA — это воплощение безупречного стиля и высочайшего мастерства.
        Мы создаём не просто вещи, а произведения искусства, подчеркивающие вашу индивидуальность.
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Лет опыта", "10+")
        with col2:
            st.metric("Довольных клиентов", "5000+")
        with col3:
            st.metric("Ручная работа", "100%")
        
        if st.button("ПЕРЕЙТИ В КАТАЛОГ", key="hero_catalog"):
            st.session_state.page = "shop"
            st.rerun()
        
        st.markdown("---")
        
        # Features Section
        st.markdown("### НАШИ ПРЕИМУЩЕСТВА")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### ⭐ Премиальное качество")
            st.write("Используем только лучшие материалы: итальянскую кожу, швейцарские механизмы, серебро 925 пробы и натуральный шелк.")
        
        with col2:
            st.markdown("### ◆ Ручная работа")
            st.write("Каждое изделие создается вручную опытными мастерами с многолетним стажем и вниманием к каждой детали.")
        
        with col3:
            st.markdown("### ♦ Гарантия 2 года")
            st.write("Мы уверены в качестве нашей продукции и предоставляем расширенную гарантию на все аксессуары AURA.")
        
        st.markdown("---")
        
        # Popular Products
        st.markdown("## ПОПУЛЯРНЫЕ МОДЕЛИ")
        cols = st.columns(3)
        for idx, product in enumerate(products_data[:3]):
            with cols[idx % 3]:
                display_product_card(product, idx, "home")

    elif st.session_state.page == "shop":
        st.markdown("## КАТАЛОГ АКСЕССУАРОВ")
        
        # Filters
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
        with col_filter1:
            price_range = st.selectbox("Цена", 
                                        ["Все цены", "До 15 000 с", "15 000 - 30 000 с", "Свыше 30 000 с"])
        with col_filter2:
            category = st.selectbox("Категория", 
                                    ["Все категории"] + sorted(list(set(b["category"] for b in products_data))))
        with col_filter3:
            sort_by = st.selectbox("Сортировка", 
                                   ["По популярности", "По возрастанию цены", "По убыванию цены", "Новинки"])
        with col_filter4:
            st.metric("Товаров в корзине", st.session_state.cart_count)
        
        st.divider()
        
        # Product grid
        st.markdown("### Все товары")
        for idx in range(0, len(products_data), 3):
            cols = st.columns(3)
            for col_idx, product in enumerate(products_data[idx:idx+3]):
                with cols[col_idx]:
                    display_product_card(product, idx + col_idx, "shop")

    elif st.session_state.page == "new":
        st.markdown("## НОВИНКИ КОЛЛЕКЦИИ")
        
        # Show latest products
        new_products = products_data[-4:]  # Show last 4 as new arrivals
        
        for idx in range(0, len(new_products), 2):
            cols = st.columns(2)
            for col_idx, product in enumerate(new_products[idx:idx+2]):
                with cols[col_idx]:
                    st.markdown("🌟 **НОВИНКА** 🌟")
                    display_product_card(product, idx + col_idx, "new")

    elif st.session_state.page == "about":
        st.markdown("## О БРЕНДЕ AURA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Наша история")
            st.markdown("""
            AURA был основан в 2014 году с простой, но амбициозной целью — создавать 
            аксессуары, которые становятся неотъемлемой частью образа успешного человека.
            
            Наши мастера объединили вековые традиции ремесленного искусства с современным 
            дизайном, чтобы предложить изделия исключительного качества. Каждый аксессуар 
            AURA — это результат кропотливой работы, где важна каждая деталь.
            
            Сегодня AURA представлен в 15 странах мира, а наши коллекции выбирают 
            ценители стиля и качества, которые знают цену подлинному мастерству.
            """)
        
        with col2:
            st.markdown("### AURA")
            st.write("Аксессуары премиум-класса для тех, кто ценит совершенство")
            st.info("Создаём не просто вещи, а произведения искусства", icon="✨")
        
        # Values
        st.markdown("---")
        st.markdown("## НАШИ ЦЕННОСТИ")
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.markdown("### 01. Качество")
            st.write("Только премиальные материалы и безупречное исполнение")
        
        with col_b:
            st.markdown("### 02. Дизайн")
            st.write("Вневременная элегантность в каждой коллекции")
        
        with col_c:
            st.markdown("### 03. Традиции")
            st.write("Уважение к ремесленным техникам и ручному труду")
        
        with col_d:
            st.markdown("### 04. Сервис")
            st.write("Индивидуальный подход к каждому клиенту")

    elif st.session_state.page == "contact":
        st.markdown("## КОНТАКТЫ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Свяжитесь с нами")
            st.markdown("""
            **Адрес:**  
            Москва, Кутузовский проспект, 48  
            БЦ «Премьер», 5 этаж
            
            **Телефон:**  
            +7 (495) 123-45-67
            
            **Email:**  
            info@aura-accessories.ru
            
            **Режим работы:**  
            Пн-Пт: 10:00 - 21:00  
            Сб-Вс: 11:00 - 19:00
            """)
        
        with col2:
            st.markdown("### Напишите нам")
            name = st.text_input("Ваше имя", placeholder="Иван Петров")
            phone = st.text_input("Телефон", placeholder="+7 (999) 123-45-67")
            email = st.text_input("Email", placeholder="your@email.com")
            message = st.text_area("Сообщение", placeholder="Ваш вопрос или пожелание...", height=150)
            
            if st.button("ОТПРАВИТЬ", key="contact_send"):
                if name and email and message:
                    st.success("✓ Спасибо! Мы свяжемся с вами в ближайшее время.")
                else:
                    st.error("⚠️ Пожалуйста, заполните обязательные поля.")

    elif st.session_state.page == "search":
        st.markdown("## ПОИСК АКСЕССУАРОВ")
        
        search_query = st.text_input("", placeholder="Поиск по названию, бренду или категории...")
        
        if search_query:
            st.markdown(f"### Результаты поиска: **{search_query}**")
            filtered_products = [p for p in products_data 
                               if search_query.lower() in p["title"].lower() 
                               or search_query.lower() in p["brand"].lower()
                               or search_query.lower() in p["category"].lower()]
            
            if filtered_products:
                for idx in range(0, len(filtered_products), 3):
                    cols = st.columns(3)
                    for col_idx, product in enumerate(filtered_products[idx:idx+3]):
                        with cols[col_idx]:
                            display_product_card(product, idx + col_idx, "search")
            else:
                st.warning("❌ Ничего не найдено. Попробуйте изменить поисковый запрос или перейдите в каталог.")

# Product Detail Page
if 'selected_product' in st.session_state and st.session_state.page == "product_detail":
    product = st.session_state.selected_product
    
    st.markdown(f"### {product['category']}")
    st.markdown(f"## {product['title']}")
    st.markdown(f"*{product['brand']}*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img = create_product_image(product["image_code"])
        st.image(img, use_column_width=True)
    
    with col2:
        # Price
        if product["old_price"]:
            col_price1, col_price2 = st.columns(2)
            col_price1.metric("Цена", product['price'])
            col_price2.text(f"Была: {product['old_price']}")
        else:
            st.metric("Цена", product['price'])
        
        st.divider()
        
        st.markdown("### Материалы и характеристики")
        st.write(product['material'])
        
        st.divider()
        
        # Features
        if 'features' in product:
            st.markdown("### Особенности:")
            for feature in product['features']:
                st.write(f"✓ {feature}")
        
        st.divider()
        
        # Description
        st.markdown("### Описание")
        st.write(product['description'])
        
        st.divider()
        
        # Buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛒 ДОБАВИТЬ В КОРЗИНУ", key="detail_cart"):
                st.session_state.cart_count += 1
                st.success(f"✓ {product['title']} добавлен в корзину!")
                st.rerun()
        with col_btn2:
            if st.button("← ВЕРНУТЬСЯ", key="back_to_shop"):
                st.session_state.page = "shop"
                del st.session_state.selected_product
                st.rerun()

# Newsletter Section
st.divider()
st.markdown("## 📧 БУДЬТЕ В КУРСЕ НОВИНОК")
st.markdown("""
Подпишитесь на рассылку и получайте информацию о новых коллекциях, закрытых распродажах и особых предложениях
""")

col_news1, col_news2 = st.columns([3, 1])
with col_news1:
    email = st.text_input("Email", placeholder="Введите ваш email", label_visibility="collapsed", key="newsletter_email")
with col_news2:
    if st.button("ПОДПИСАТЬСЯ", key="newsletter_btn"):
        if email and "@" in email:
            st.success("✓ Спасибо за подписку! Добро пожаловать в мир AURA.")
        else:
            st.error("⚠️ Пожалуйста, укажите корректный email")

st.divider()

# Footer
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("### AURA")
    st.write("© 2024 AURA Accessories  \nВсе права защищены.")

with col_footer2:
    st.markdown("### Информация")
    st.write("[Политика конфиденциальности](#)  \n[Условия доставки](#)  \n[Возврат товара](#)")

with col_footer3:
    st.markdown("### Помощь")
    st.write("[Подарочные сертификаты](#)  \n[Служба поддержки](#)  \n[О компании](#)")

# Cart sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("## 🛒 КОРЗИНА")
    st.metric("Товаров", st.session_state.cart_count)
    
    if st.session_state.cart_count > 0:
        st.markdown("---")
        st.write("**Примерная сумма:** от 45 900 ₽")
        if st.button("ОФОРМИТЬ ЗАКАЗ", key="sidebar_order"):
            st.balloons()
            st.success("✓ Заказ оформлен! Менеджер свяжется с вами.")
    else:
        st.info("Ваша корзина пуста. Добавьте товары из каталога")