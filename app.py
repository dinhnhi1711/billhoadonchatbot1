import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH
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
except:
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

    # Món không có size
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
# HÀM LẤY GIÁ
# =========================================================

def get_price(drink, size):

    return MENU[drink][size]


# =========================================================
# CHATBOT
# =========================================================

def chatbot_answer(question):

    q = question.lower().strip()

    # -----------------------------------------------------
    # CHÀO HỎI
    # -----------------------------------------------------

    if any(word in q for word in [
        "xin chào",
        "hello",
        "hi",
        "chào"
    ]):

        return (
            "Xin chào 👋 Mình là trợ lý của quán trà sữa. "
            "Mình có thể tư vấn món, topping, giá, "
            "best seller, giao hàng và chương trình khuyến mãi "
            "cho bạn."
        )


    # -----------------------------------------------------
    # TƯ VẤN
    # -----------------------------------------------------

    if (
        "tư vấn" in q
        or "tư vấn cho mình" in q
        or "tư vấn món" in q
    ):

        return (
            "Tất nhiên rồi 🧋😊\n\n"
            "Nếu bạn thích vị truyền thống, mình gợi ý "
            "**Trà sữa truyền thống**.\n\n"
            "Nếu bạn thích vị thơm, béo và nhẹ nhàng, "
            "có thể thử **Trà sữa matcha** hoặc "
            "**Trà sữa khoai môn**.\n\n"
            "Nếu thích vị trái cây, bạn có thể thử "
            "**Trà đào, Trà vải, Trà trái cây hoặc Trà mãng cầu**.\n\n"
            "Bạn cũng có thể thêm **trân châu, thạch hoặc pudding**."
        )


    # -----------------------------------------------------
    # BEST SELLER
    # -----------------------------------------------------

    if (
        "best seller" in q
        or "bán chạy" in q
        or "món bán chạy" in q
        or "món ngon nhất" in q
        or "món nào ngon" in q
    ):

        return (
            "⭐ Các món được quán giới thiệu nổi bật gồm:\n\n"
            "🥇 **Trà sữa truyền thống** – vị quen thuộc, "
            "dễ uống.\n\n"
            "🥈 **Trà sữa matcha** – thơm vị matcha, "
            "phù hợp với người thích vị thanh nhẹ.\n\n"
            "🥉 **Trà sữa khoai môn** – béo và thơm.\n\n"
            "Nếu bạn thích vị trái cây, mình gợi ý "
            "**Trà đào hoặc Trà mãng cầu**."
        )


    # -----------------------------------------------------
    # GIAO HÀNG
    # -----------------------------------------------------

    if (
        "giao hàng" in q
        or "giao hang" in q
        or "ship" in q
        or "giao ngay" in q
        or "giao liền" in q
    ):

        return (
            "🛵 Quán có hỗ trợ giao hàng.\n\n"
            "Bạn vui lòng cung cấp địa chỉ nhận hàng "
            "và số điện thoại để quán kiểm tra khả năng "
            "giao đến khu vực của bạn nhé.\n\n"
            "Thời gian giao hàng thực tế có thể phụ thuộc "
            "vào khoảng cách và tình trạng đơn hàng."
        )


    # -----------------------------------------------------
    # KHUYẾN MÃI
    # -----------------------------------------------------

    if (
        "khuyến mãi" in q
        or "khuyen mai" in q
        or "ưu đãi" in q
        or "giảm giá" in q
        or "giam gia" in q
        or "promotion" in q
    ):

        return (
            "🎁 Hiện quán đang có các chương trình ưu đãi "
            "dành cho khách hàng.\n\n"
            "Bạn có thể hỏi nhân viên tại quầy để biết "
            "chương trình áp dụng trong ngày.\n\n"
            "💡 Nếu bạn muốn, mình cũng có thể giúp bạn "
            "chọn món phù hợp với ngân sách."
        )


    # -----------------------------------------------------
    # GIÁ
    # -----------------------------------------------------

    if (
        "giá" in q
        or "bao nhiêu tiền" in q
        or "bao nhieu tien" in q
        or "giá bao nhiêu" in q
    ):

        return (
            "💰 Giá các món hiện tại:\n\n"
            "• Trà sữa truyền thống: 30.000đ - 35.000đ\n"
            "• Trà sữa matcha: 35.000đ - 40.000đ\n"
            "• Trà sữa socola: 35.000đ - 40.000đ\n"
            "• Trà sữa khoai môn: 35.000đ - 40.000đ\n"
            "• Trà thái xanh: 30.000đ - 35.000đ\n"
            "• Trà thái đỏ: 30.000đ - 35.000đ\n"
            "• Trà đào: 30.000đ - 35.000đ\n"
            "• Trà vải: 30.000đ - 35.000đ\n"
            "• Trà trái cây: 30.000đ - 35.000đ\n"
            "• Trà mãng cầu: 30.000đ - 35.000đ\n"
            "• Bánh tráng phơi sương trứng cút: 25.000đ"
        )


    # -----------------------------------------------------
    # TOPPING
    # -----------------------------------------------------

    if (
        "topping" in q
        or "thêm gì" in q
        or "có topping" in q
    ):

        topping_text = "🧋 Quán hiện có các topping:\n\n"

        for topping, price in TOPPINGS.items():

            if price == 0:

                topping_text += (
                    f"• {topping}\n"
                )

            else:

                topping_text += (
                    f"• {topping}: {money(price)}\n"
                )

        return topping_text


    # -----------------------------------------------------
    # SIZE
    # -----------------------------------------------------

    if (
        "size" in q
        or "cỡ" in q
        or "ly" in q
    ):

        return (
            "🥤 Quán có 2 size:\n\n"
            "• Size M\n"
            "• Size L\n\n"
            "Size L sẽ có giá cao hơn size M "
            "đối với các món trà sữa và trà."
        )


    # -----------------------------------------------------
    # ĐƯỜNG
    # -----------------------------------------------------

    if (
        "đường" in q
        or "ngọt" in q
        or "độ ngọt" in q
    ):

        return (
            "🍬 Quán có các mức đường:\n\n"
            "100% - 70% - 50% - 30% - 0%\n\n"
            "Nếu bạn không thích quá ngọt, mình gợi ý "
            "50% hoặc 30% đường."
        )


    # -----------------------------------------------------
    # ĐÁ
    # -----------------------------------------------------

    if (
        "đá" in q
        or "độ đá" in q
    ):

        return (
            "🧊 Quán có các mức đá:\n\n"
            "100% - 70% - 50% - 30% - 0%\n\n"
            "Bạn có thể chọn mức đá phù hợp với sở thích."
        )


    # -----------------------------------------------------
    # TRÀ
    # -----------------------------------------------------

    if (
        "mức trà" in q
        or "độ trà" in q
        or "trà bao nhiêu" in q
    ):

        return (
            "🍵 Mức trà hiện có:\n\n"
            "100% - 70% - 50% - 30%\n\n"
            "Nếu thích vị trà đậm, bạn có thể chọn 100%."
        )


    # -----------------------------------------------------
    # CẢM ƠN
    # -----------------------------------------------------

    if (
        "cảm ơn" in q
        or "cam on" in q
    ):

        return (
            "🥰 Rất vui được phục vụ bạn! "
            "Chúc bạn có một ly trà sữa thật ngon 🧋❤️"
        )


    # -----------------------------------------------------
    # KHÔNG HIỂU
    # -----------------------------------------------------

    return (
        "😊 Mình chưa hiểu rõ câu hỏi của bạn.\n\n"
        "Bạn có thể hỏi mình những câu như:\n\n"
        "• Bạn có thể tư vấn cho mình không?\n"
        "• Món best seller của quán là gì?\n"
        "• Bạn có giao hàng ngay không?\n"
        "• Chương trình khuyến mãi của bạn là gì?\n"
        "• Quán có những topping nào?\n"
        "• Giá trà sữa bao nhiêu?\n"
        "• Quán có những size nào?"
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

    text += f"Khách hàng: {customer_name}\n"

    text += (
        f"Thời gian: "
        f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
    )

    text += "-" * 55 + "\n"

    for i, item in enumerate(orders, 1):

        text += f"\n{i}. {item['drink']}\n"

        text += f"   Size: {item['size']}\n"

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

    # -----------------------------------------------------
    # CỘT 1
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # CỘT 2
    # -----------------------------------------------------

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
# CHATBOT TƯ VẤN KHÁCH HÀNG
# =========================================================

st.divider()

st.header("🤖 Trợ lý tư vấn khách hàng")

st.write(
    "Xin chào 👋 Bạn có thể hỏi mình về món uống, "
    "topping, giá, giao hàng hoặc chương trình khuyến mãi."
)


# ---------------------------------------------------------
# HIỂN THỊ CÂU HỎI GỢI Ý
# ---------------------------------------------------------

st.markdown("**💡 Câu hỏi gợi ý:**")

suggestion_cols = st.columns(4)

suggestions = [
    "Bạn có thể tư vấn cho mình không?",
    "Món best seller của quán là gì?",
    "Bạn có thể giao hàng ngay chứ?",
    "Chương trình khuyến mãi của bạn là gì?"
]

for i, suggestion in enumerate(suggestions):

    with suggestion_cols[i]:

        if st.button(
            suggestion,
            key=f"suggestion_{i}",
            use_container_width=True
        ):

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": suggestion
                }
            )

            answer = chatbot_answer(
                suggestion
            )

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


# ---------------------------------------------------------
# HIỂN THỊ LỊCH SỬ CHAT
# ---------------------------------------------------------

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# Ô NHẬP CHAT
# ---------------------------------------------------------

user_question = st.chat_input(
    "Nhập câu hỏi của bạn..."
)


if user_question:

    # Hiển thị câu hỏi của khách
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Chatbot trả lời
    answer = chatbot_answer(
        user_question
    )

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
        "🗑️ Xóa lịch sử trò chuyện"
    ):

        st.session_state.chat_messages = []

        st.rerun()
