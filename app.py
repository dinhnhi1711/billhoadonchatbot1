import streamlit as st
from datetime import datetime
from openai import OpenAI


# =========================================================
# CẤU HÌNH STREAMLIT
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
    "Kem cheese": 10000,
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
# Bạn có thể sửa phần này theo quán thật
# =========================================================

SHOP_INFO = {
    "best_seller": [
        "Trà sữa truyền thống",
        "Trà sữa matcha",
        "Trà sữa khoai môn"
    ],

    "delivery": (
        "Quán có hỗ trợ giao hàng. "
        "Khách vui lòng cung cấp địa chỉ và số điện thoại "
        "để quán kiểm tra khả năng giao hàng."
    ),

    "promotion": (
        "Hiện quán chưa cấu hình chương trình khuyến mãi "
        "cụ thể trong hệ thống. Khách vui lòng hỏi nhân viên "
        "để biết chương trình đang áp dụng trong ngày."
    ),

    "address": "Bạn hãy cập nhật địa chỉ quán tại đây.",

    "phone": "Bạn hãy cập nhật số điện thoại quán tại đây.",

    "opening_hours": "Bạn hãy cập nhật giờ mở cửa tại đây."
}


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
# TẠO THÔNG TIN MENU CHO AI
# =========================================================

def build_menu_text():

    text = "DANH SÁCH MENU:\n"

    for drink, sizes in MENU.items():

        text += f"- {drink}: "

        if sizes["M"] == sizes["L"]:
            text += f"{money(sizes['M'])}\n"
        else:
            text += (
                f"Size M {money(sizes['M'])}, "
                f"Size L {money(sizes['L'])}\n"
            )

    text += "\nTOPPING:\n"

    for topping, price in TOPPINGS.items():

        if price == 0:
            text += f"- {topping}: miễn phí\n"
        else:
            text += f"- {topping}: {money(price)}\n"

    text += "\nMỨC ĐƯỜNG:\n"
    text += ", ".join(SUGAR_LEVELS)

    text += "\n\nMỨC ĐÁ:\n"
    text += ", ".join(ICE_LEVELS)

    text += "\n\nMỨC TRÀ:\n"
    text += ", ".join(TEA_LEVELS)

    return text


# =========================================================
# TẠO SYSTEM PROMPT CHO CHATBOT
# =========================================================

def build_system_prompt():

    menu_text = build_menu_text()

    best_seller = ", ".join(
        SHOP_INFO["best_seller"]
    )

    return f"""
Bạn là trợ lý AI chăm sóc khách hàng cho một quán trà sữa.

NHIỆM VỤ:
- Tư vấn đồ uống cho khách.
- Giải thích menu.
- Giải thích giá.
- Tư vấn topping.
- Tư vấn mức đường, đá, trà.
- Trả lời câu hỏi về giao hàng.
- Trả lời câu hỏi về chương trình khuyến mãi.
- Tư vấn món phù hợp với sở thích và ngân sách của khách.
- Nói chuyện thân thiện, tự nhiên bằng tiếng Việt.

PHONG CÁCH:
- Thân thiện.
- Ngắn gọn.
- Dễ hiểu.
- Có thể dùng emoji vừa phải.
- Không trả lời quá dài nếu khách chỉ hỏi một câu đơn giản.

QUY TẮC QUAN TRỌNG:
1. Chỉ sử dụng thông tin menu và giá được cung cấp bên dưới.
2. Không tự bịa ra món hoặc giá không có trong menu.
3. Không tự bịa chương trình khuyến mãi.
4. Nếu không có thông tin, hãy nói rõ là quán chưa cập nhật thông tin đó.
5. Khi khách hỏi "best seller", hãy giới thiệu các món:
   {best_seller}
6. Khi khách hỏi giao hàng, sử dụng thông tin giao hàng được cung cấp.
7. Nếu khách muốn được tư vấn món, hãy hỏi thêm sở thích nếu cần:
   - thích béo hay thanh
   - thích trà sữa hay trà trái cây
   - thích ngọt nhiều hay ít
   - thích nhiều đá hay ít đá
   - ngân sách khoảng bao nhiêu
8. Không tự xác nhận đơn hàng hoặc thanh toán thay cho hệ thống bill.
9. Nếu khách muốn đặt món, hãy hướng dẫn khách sử dụng phần "Thêm món" của ứng dụng.

THÔNG TIN QUÁN:

Best seller:
{best_seller}

Giao hàng:
{SHOP_INFO["delivery"]}

Khuyến mãi:
{SHOP_INFO["promotion"]}

Địa chỉ:
{SHOP_INFO["address"]}

Số điện thoại:
{SHOP_INFO["phone"]}

Giờ mở cửa:
{SHOP_INFO["opening_hours"]}

{menu_text}
"""


# =========================================================
# LẤY OPENROUTER API KEY
# =========================================================

def get_api_key():

    # Ưu tiên Streamlit Secrets
    try:
        key = st.secrets["OPENROUTER_API_KEY"]

        if key:
            return key

    except Exception:
        pass

    # Nếu chạy local có biến môi trường
    import os

    key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    return key


# =========================================================
# KHỞI TẠO OPENROUTER CLIENT
# =========================================================

def get_ai_client():

    api_key = get_api_key()

    if not api_key:
        return None

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )


# =========================================================
# GỌI CHATBOT AI
# =========================================================

def chatbot_answer(question):

    client = get_ai_client()

    if client is None:

        return (
            "⚠️ Chatbot AI chưa được cấu hình API key.\n\n"
            "Bạn hãy tạo file `.streamlit/secrets.toml` "
            "và thêm:\n\n"
            "`OPENROUTER_API_KEY = \"your-key\"`"
        )

    try:

        messages = [
            {
                "role": "system",
                "content": build_system_prompt()
            }
        ]

        # Giới hạn lịch sử để tránh request quá dài
        history = st.session_state.chat_messages[-12:]

        for message in history:

            messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=messages,
            temperature=0.7,
            max_tokens=700
        )

        answer = response.choices[0].message.content

        if not answer:
            return (
                "Xin lỗi, mình chưa nhận được câu trả lời. "
                "Bạn thử hỏi lại giúp mình nhé."
            )

        return answer

    except Exception as e:

        return (
            "❌ Không thể kết nối chatbot AI.\n\n"
            f"Chi tiết lỗi: `{str(e)}`"
        )


# =========================================================
# HÀM TẠO HÓA ĐƠN
# =========================================================

def create_invoice(customer_name, orders):

    now = datetime.now()

    total = sum(
        item["total"]
        for item in orders
    )

    text = ""

    text += "=" * 55 + "\n"
    text += "             HÓA ĐƠN TRÀ SỮA\n"
    text += "=" * 55 + "\n"

    text += (
        f"Khách hàng: {customer_name}\n"
    )

    text += (
        f"Thời gian: "
        f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
    )

    text += "-" * 55 + "\n"

    for i, item in enumerate(orders, 1):

        text += (
            f"\n{i}. {item['drink']}\n"
        )

        text += (
            f"   Size: {item['size']}\n"
        )

        text += (
            f"   Số lượng: "
            f"{item['quantity']}\n"
        )

        text += (
            f"   Topping: "
            f"{item['topping']}\n"
        )

        text += (
            f"   Đường: "
            f"{item['sugar']}\n"
        )

        text += (
            f"   Đá: "
            f"{item['ice']}\n"
        )

        text += (
            f"   Trà: "
            f"{item['tea']}\n"
        )

        text += (
            f"   Đơn giá: "
            f"{money(item['unit_price'])}\n"
        )

        text += (
            f"   Thành tiền: "
            f"{money(item['total'])}\n"
        )

        text += "-" * 55 + "\n"

    text += "\n"

    text += (
        f"TỔNG THANH TOÁN: "
        f"{money(total)}\n"
    )

    text += "=" * 55 + "\n"

    text += (
        "              CẢM ƠN QUÝ KHÁCH!\n"
    )

    text += "=" * 55 + "\n"

    return text


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🧋 QUẢN LÝ BILL TRÀ SỮA")

st.write(
    "Nhập thông tin khách hàng và thêm từng món "
    "vào hóa đơn."
)


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name


# =========================================================
# THÊM MÓN
# =========================================================

st.header("🧋 Thêm món")

with st.form("order_form"):

    col1, col2 = st.columns(2)

    with col1:

        drink = st.selectbox(
            "Loại món",
            list(MENU.keys())
        )

        size = st.selectbox(
            "Size",
            ["M", "L"]
        )

        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        topping = st.selectbox(
            "Topping",
            list(TOPPINGS.keys())
        )

    with col2:

        sugar = st.selectbox(
            "Mức độ đường",
            SUGAR_LEVELS
        )

        ice = st.selectbox(
            "Mức độ đá",
            ICE_LEVELS
        )

        tea = st.selectbox(
            "Mức độ trà",
            TEA_LEVELS
        )

    # -----------------------------------------------------
    # TÍNH GIÁ
    # -----------------------------------------------------

    unit_price = (
        MENU[drink][size]
        + TOPPINGS[topping]
    )

    total_price = (
        unit_price * quantity
    )

    st.info(
        "Đơn giá: "
        + money(unit_price)
        + " | Thành tiền: "
        + money(total_price)
    )

    submitted = st.form_submit_button(
        "➕ THÊM VÀO HÓA ĐƠN"
    )


# =========================================================
# XỬ LÝ THÊM MÓN
# =========================================================

if submitted:

    if customer_name.strip() == "":

        st.error(
            "⚠️ Vui lòng nhập tên khách hàng."
        )

    else:

        order = {
            "drink": drink,
            "size": size,
            "quantity": quantity,
            "topping": topping,
            "sugar": sugar,
            "ice": ice,
            "tea": tea,
            "unit_price": unit_price,
            "total": total_price
        }

        st.session_state.orders.append(
            order
        )

        st.success(
            "✅ Đã thêm món vào hóa đơn."
        )

        st.rerun()


# =========================================================
# HIỂN THỊ HÓA ĐƠN
# =========================================================

st.divider()

st.header("🧾 HÓA ĐƠN HIỆN TẠI")


if len(st.session_state.orders) == 0:

    st.info(
        "Chưa có món nào trong hóa đơn."
    )

else:

    total_bill = 0

    for index, item in enumerate(
        st.session_state.orders
    ):

        st.subheader(
            f"Món {index + 1}: "
            f"{item['drink']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**Size:** "
                f"{item['size']}"
            )

            st.write(
                f"**Số lượng:** "
                f"{item['quantity']}"
            )

            st.write(
                f"**Topping:** "
                f"{item['topping']}"
            )

        with col2:

            st.write(
                f"**Đường:** "
                f"{item['sugar']}"
            )

            st.write(
                f"**Đá:** "
                f"{item['ice']}"
            )

            st.write(
                f"**Trà:** "
                f"{item['tea']}"
            )

        with col3:

            st.write(
                f"**Đơn giá:** "
                f"{money(item['unit_price'])}"
            )

            st.write(
                f"**Thành tiền:** "
                f"{money(item['total'])}"
            )

            if st.button(
                "🗑️ Xóa món",
                key=f"delete_{index}"
            ):

                st.session_state.orders.pop(
                    index
                )

                st.rerun()

        st.divider()

        total_bill += item["total"]


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    st.header("💰 TỔNG THANH TOÁN")

    total_quantity = sum(
        item["quantity"]
        for item in st.session_state.orders
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Số loại món",
            len(st.session_state.orders)
        )

    with col2:

        st.metric(
            "Tổng số ly / món",
            total_quantity
        )

    with col3:

        st.metric(
            "Tổng tiền",
            money(total_bill)
        )


    # =====================================================
    # THANH TOÁN
    # =====================================================

    st.divider()

    st.header("💳 Thanh toán")

    if st.button(
        "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        invoice_text = create_invoice(
            customer_name,
            st.session_state.orders
        )

        current_time = datetime.now()

        filename = (
            "hoa_don_"
            + current_time.strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".txt"
        )

        st.success(
            "✅ Thanh toán thành công!"
        )

        st.download_button(
            label="📥 TẢI HÓA ĐƠN",
            data=invoice_text.encode(
                "utf-8"
            ),
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

        st.text_area(
            "Xem trước hóa đơn",
            invoice_text,
            height=450
        )


# =========================================================
# XÓA TOÀN BỘ HÓA ĐƠN
# =========================================================

if len(st.session_state.orders) > 0:

    st.divider()

    if st.button(
        "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
        use_container_width=True
    ):

        st.session_state.orders = []

        st.rerun()


# =========================================================
# CHATBOT AI
# =========================================================

st.divider()

st.header("🤖 Trợ lý AI của quán")

st.write(
    "Bạn có thể hỏi mình về menu, giá, món bán chạy, "
    "topping, giao hàng, khuyến mãi hoặc nhờ tư vấn món."
)


# =========================================================
# CÂU HỎI GỢI Ý
# =========================================================

st.markdown("### 💡 Bạn có thể hỏi")

suggestions = [
    "Bạn có thể tư vấn cho mình không?",
    "Món best seller của quán là gì?",
    "Bạn có thể giao hàng ngay chứ?",
    "Chương trình khuyến mãi của bạn là gì?"
]

suggestion_cols = st.columns(4)

for i, suggestion in enumerate(suggestions):

    with suggestion_cols[i]:

        if st.button(
            suggestion,
            key=f"ai_suggestion_{i}",
            use_container_width=True
        ):

            # Lưu câu hỏi vào lịch sử
            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": suggestion
                }
            )

            # Gọi AI
            with st.spinner("🤖 Đang suy nghĩ..."):

                answer = chatbot_answer(
                    suggestion
                )

            # Lưu câu trả lời
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


# =========================================================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================================================

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# Ô CHAT
# =========================================================

user_question = st.chat_input(
    "🧋 Nhập câu hỏi của bạn..."
)


if user_question:

    # -----------------------------------------------------
    # LƯU CÂU HỎI
    # -----------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # -----------------------------------------------------
    # GỌI AI
    # -----------------------------------------------------

    with st.spinner(
        "🤖 Trợ lý đang trả lời..."
    ):

        answer = chatbot_answer(
            user_question
        )

    # -----------------------------------------------------
    # LƯU CÂU TRẢ LỜI
    # -----------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# =========================================================
# XÓA LỊCH SỬ CHAT
# =========================================================

if len(st.session_state.chat_messages) > 0:

    if st.button(
        "🗑️ Xóa lịch sử trò chuyện",
        key="clear_chat"
    ):

        st.session_state.chat_messages = []

        st.rerun()
