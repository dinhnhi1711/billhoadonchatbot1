import streamlit as st
import requests
from datetime import datetime


# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Quản lý Bill Trà Sữa",
    page_icon="🧋",
    layout="wide"
)


# =========================================================
# LOGO
# =========================================================

try:
    st.image("logo.jpg", width=250)
except Exception:
    pass


# =========================================================
# MENU
# =========================================================

MENU = {
    "Trà sữa truyền thống": {
        "M": 30000,
        "L": 35000
    },

    "Trà sữa matcha": {
        "M": 35000,
        "L": 40000
    },

    "Trà sữa socola": {
        "M": 35000,
        "L": 40000
    },

    "Trà sữa khoai môn": {
        "M": 35000,
        "L": 40000
    },

    "Trà sữa thái xanh": {
        "M": 30000,
        "L": 35000
    },

    "Trà sữa thái đỏ": {
        "M": 30000,
        "L": 35000
    },

    "Trà đào": {
        "M": 30000,
        "L": 35000
    },

    "Trà vải": {
        "M": 30000,
        "L": 35000
    },

    "Trà trái cây": {
        "M": 30000,
        "L": 35000
    },

    "Trà mãng cầu": {
        "M": 30000,
        "L": 35000
    },

    "Bánh tráng phơi sương trứng cút": {
        "M": 25000,
        "L": 25000
    }
}


# =========================================================
# TOPPING
# =========================================================

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000
}


# =========================================================
# MỨC ĐỘ
# =========================================================

SUGAR_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

ICE_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

TEA_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%"
]


# =========================================================
# THÔNG TIN QUÁN
# =========================================================
# BẠN CÓ THỂ SỬA PHẦN NÀY THEO THÔNG TIN THẬT CỦA QUÁN
# =========================================================

SHOP_NAME = "QUÁN TRÀ SỮA"

BEST_SELLERS = [
    "Trà sữa truyền thống",
    "Trà sữa matcha",
    "Trà sữa khoai môn"
]

DELIVERY_INFO = """
Quán có hỗ trợ giao hàng.
Khách vui lòng cung cấp địa chỉ nhận hàng và số điện thoại
để quán kiểm tra khả năng giao hàng.
"""

PROMOTION_INFO = """
Hiện chưa cấu hình chương trình khuyến mãi cụ thể.
Khách vui lòng hỏi nhân viên để biết chương trình đang
áp dụng trong ngày.
"""

SHOP_ADDRESS = "Chưa cập nhật địa chỉ quán"

SHOP_PHONE = "Chưa cập nhật số điện thoại"

SHOP_HOURS = "Chưa cập nhật giờ mở cửa"


# =========================================================
# SESSION STATE
# =========================================================

if "orders" not in st.session_state:
    st.session_state.orders = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def money(value):
    return f"{value:,.0f}".replace(",", ".") + " đ"


# =========================================================
# HÀM LẤY API KEY
# =========================================================

def get_api_key():

    # -----------------------------------------
    # Ưu tiên Streamlit Secrets
    # -----------------------------------------

    try:

        api_key = st.secrets.get(
            "OPENROUTER_API_KEY",
            ""
        )

        if api_key:
            return api_key

    except Exception:
        pass

    # -----------------------------------------
    # Nếu không có secrets thì kiểm tra
    # biến môi trường
    # -----------------------------------------

    try:

        import os

        api_key = os.environ.get(
            "OPENROUTER_API_KEY",
            ""
        )

        return api_key

    except Exception:

        return ""


# =========================================================
# TẠO THÔNG TIN MENU CHO CHATBOT
# =========================================================

def get_menu_for_ai():

    menu_text = ""

    for drink, sizes in MENU.items():

        menu_text += f"- {drink}: "

        if sizes["M"] == sizes["L"]:

            menu_text += (
                f"{money(sizes['M'])}\n"
            )

        else:

            menu_text += (
                f"Size M {money(sizes['M'])}, "
                f"Size L {money(sizes['L'])}\n"
            )

    return menu_text


# =========================================================
# TẠO THÔNG TIN TOPPING CHO CHATBOT
# =========================================================

def get_topping_for_ai():

    topping_text = ""

    for topping, price in TOPPINGS.items():

        if price == 0:

            topping_text += (
                f"- {topping}: miễn phí\n"
            )

        else:

            topping_text += (
                f"- {topping}: {money(price)}\n"
            )

    return topping_text


# =========================================================
# TẠO THÔNG TIN BILL HIỆN TẠI CHO CHATBOT
# =========================================================

def get_current_bill_for_ai():

    orders = st.session_state.orders

    if not orders:

        return "Hiện tại khách chưa có món nào trong bill."

    total = 0
    total_quantity = 0

    text = ""

    for index, item in enumerate(
        orders,
        start=1
    ):

        text += (
            f"{index}. {item['drink']} - "
            f"Size {item['size']} - "
            f"Số lượng {item['quantity']} - "
            f"Topping {item['topping']} - "
            f"Đường {item['sugar']} - "
            f"Đá {item['ice']} - "
            f"Trà {item['tea']} - "
            f"Thành tiền {money(item['total'])}\n"
        )

        total += item["total"]

        total_quantity += item["quantity"]

    text += (
        f"\nTổng số lượng: {total_quantity}"
    )

    text += (
        f"\nTổng tiền: {money(total)}"
    )

    return text


# =========================================================
# SYSTEM PROMPT CHO CHATBOT
# =========================================================

def build_system_prompt():

    menu_text = get_menu_for_ai()

    topping_text = get_topping_for_ai()

    bill_text = get_current_bill_for_ai()

    best_seller_text = ", ".join(
        BEST_SELLERS
    )

    return f"""
Bạn là chatbot AI chăm sóc khách hàng của {SHOP_NAME}.

Bạn đang hỗ trợ khách hàng trong một ứng dụng quản lý
bill trà sữa.

=============================
NHIỆM VỤ
=============================

Bạn có thể:

- Tư vấn đồ uống.
- Tư vấn món phù hợp sở thích.
- Tư vấn theo ngân sách.
- Giới thiệu best seller.
- Giải thích giá.
- Giới thiệu topping.
- Tư vấn mức đường.
- Tư vấn mức đá.
- Tư vấn mức trà.
- Trả lời câu hỏi về giao hàng.
- Trả lời câu hỏi về khuyến mãi.
- Xem thông tin bill hiện tại.
- Tính toán đơn giản dựa trên bill hiện tại.
- Giải thích các món trong bill.

=============================
QUY TẮC
=============================

1. Luôn trả lời bằng tiếng Việt.

2. Nói chuyện thân thiện, tự nhiên.

3. Có thể sử dụng emoji nhưng không lạm dụng.

4. Không được tự bịa món không có trong menu.

5. Không được tự bịa giá.

6. Không được tự bịa chương trình khuyến mãi.

7. Nếu thông tin chưa được cung cấp,
hãy nói rõ rằng thông tin chưa được cập nhật.

8. Khi khách hỏi best seller,
hãy giới thiệu các món:
{best_seller_text}

9. Khi khách hỏi giao hàng,
hãy sử dụng thông tin giao hàng bên dưới.

10. Khi khách hỏi về bill,
hãy sử dụng BILL HIỆN TẠI được cung cấp.

11. Nếu khách muốn đặt món,
hãy hướng dẫn khách sử dụng phần
"Thêm món" trong ứng dụng.

12. Chatbot không được tự ý sửa bill.

13. Chatbot không được tự ý xác nhận thanh toán.

14. Không nói rằng đơn hàng đã được đặt
nếu khách chưa bấm nút thêm món.

=============================
MENU
=============================

{menu_text}

=============================
TOPPING
=============================

{topping_text}

=============================
MỨC ĐƯỜNG
=============================

{", ".join(SUGAR_LEVELS)}

=============================
MỨC ĐÁ
=============================

{", ".join(ICE_LEVELS)}

=============================
MỨC TRÀ
=============================

{", ".join(TEA_LEVELS)}

=============================
BEST SELLER
=============================

{best_seller_text}

=============================
GIAO HÀNG
=============================

{DELIVERY_INFO}

=============================
KHUYẾN MÃI
=============================

{PROMOTION_INFO}

=============================
THÔNG TIN QUÁN
=============================

Địa chỉ:
{SHOP_ADDRESS}

Số điện thoại:
{SHOP_PHONE}

Giờ mở cửa:
{SHOP_HOURS}

=============================
BILL HIỆN TẠI
=============================

{bill_text}

=============================
CÁCH TRẢ LỜI
=============================

Nếu khách hỏi:
"Bạn có thể tư vấn cho mình không?"

Hãy hỏi khách thích:
- vị béo hay thanh
- trà sữa hay trà trái cây
- ngọt nhiều hay ít
- nhiều đá hay ít đá
- ngân sách khoảng bao nhiêu

Nếu khách hỏi:
"Món best seller của quán là gì?"

Hãy giới thiệu các món best seller.

Nếu khách hỏi:
"Bạn có thể giao hàng ngay chứ?"

Hãy giải thích thông tin giao hàng hiện có
và nói rằng thời gian thực tế phụ thuộc
địa chỉ và tình trạng đơn hàng.

Nếu khách hỏi:
"Chương trình khuyến mãi của bạn là gì?"

Hãy sử dụng thông tin khuyến mãi được cung cấp.
Không được tự tạo chương trình giảm giá.

Nếu khách hỏi:
"Bill của tôi bao nhiêu tiền?"

Hãy lấy tổng tiền từ BILL HIỆN TẠI.

Nếu bill đang trống,
hãy nói rằng hiện chưa có món nào trong bill.
"""


# =========================================================
# GỌI OPENROUTER API
# =========================================================

def chatbot_answer(question):

    api_key = get_api_key()

    # -----------------------------------------------------
    # KIỂM TRA API KEY
    # -----------------------------------------------------

    if not api_key:

        return """
⚠️ **Chatbot AI chưa được cấu hình API key.**

Bạn hãy tạo file:

`.streamlit/secrets.toml`

và thêm:

```toml
OPENROUTER_API_KEY = "API_KEY_CUA_BAN"
