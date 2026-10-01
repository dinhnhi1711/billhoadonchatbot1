import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# Hiển thị logo nếu file tồn tại
try:
    st.image("logo.jpg", use_container_width=True)
except:
    pass


# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa trân châu đường đen": 40000,
    "Trà sữa ô long": 35000,
    "Trà sữa thái xanh": 35000,
    "Trà mãng cầu": 35000,
    "Trà trái cây nhiệt đới": 35000,
    "Bánh tráng phơi sương trứng cút": 25000,
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Trân châu đường đen": 8000,
}

SUGAR_LEVELS = ["100%", "70%", "50%", "0%"]
ICE_LEVELS = ["100%", "70%", "50%", "0%"]
TEA_LEVELS = ["100%", "70%", "30%", "0%"]


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================
# KHỞI TẠO SESSION STATE
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []


# =========================
# HÀM THÊM MÓN
# =========================
def add_to_cart(drink, quantity, topping, sugar, ice, tea):
    drink_price = MENU[drink]
    topping_price = TOPPINGS[topping]

    unit_price = drink_price + topping_price
    total_price = unit_price * quantity

    item = {
        "drink": drink,
        "quantity": quantity,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "tea": tea,
        "drink_price": drink_price,
        "topping_price": topping_price,
        "unit_price": unit_price,
        "total_price": total_price,
    }

    st.session_state.cart.append(item)


# =========================
# HÀM XÓA TOÀN BỘ GIỎ HÀNG
# =========================
def clear_cart():
    st.session_state.cart = []


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUẢN LÝ BILL QUÁN TRÀ SỮA")
st.caption(
    "Một khách hàng có thể gọi nhiều loại trà sữa trong cùng một hóa đơn."
)


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Ví dụ: Nguyễn Văn An"
)


# =========================
# THÊM MÓN
# =========================
st.divider()
st.subheader("🧋 Thêm món vào đơn hàng")


drink = st.selectbox(
    "Loại trà sữa / món",
    list(MENU.keys()),
    key="drink_select"
)

quantity = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
    key="quantity_select"
)

topping = st.selectbox(
    "Topping",
    list(TOPPINGS.keys()),
    key="topping_select"
)


col1, col2 = st.columns(2)

with col1:
    sugar = st.selectbox(
        "🍬 Mức độ đường",
        SUGAR_LEVELS,
        key="sugar_select"
    )

    tea = st.selectbox(
        "🍵 Mức độ trà",
        TEA_LEVELS,
        key="tea_select"
    )

with col2:
    ice = st.selectbox(
        "🧊 Mức độ đá",
        ICE_LEVELS,
        key="ice_select"
    )


# =========================
# GIÁ MÓN ĐANG CHỌN
# =========================
drink_price = MENU[drink]
topping_price = TOPPINGS[topping]
unit_price = drink_price + topping_price
current_total = unit_price * quantity

st.info(
    f"💰 Đơn giá: **{format_money(unit_price)}**  |  "
    f"Thành tiền: **{format_money(current_total)}**"
)


# =========================
# NÚT THÊM MÓN
# =========================
if st.button(
    "➕ THÊM MÓN VÀO ĐƠN",
    type="primary",
    use_container_width=True
):
    add_to_cart(
        drink,
        quantity,
        topping,
        sugar,
        ice,
        tea
    )

    st.success(
        f"✅ Đã thêm {quantity} × {drink} vào đơn hàng!"
    )


# =========================
# HIỂN THỊ GIỎ HÀNG
# =========================
st.divider()
st.subheader("🛒 Đơn hàng hiện tại")


if not st.session_state.cart:

    st.info(
        "Chưa có món nào trong đơn hàng. "
        "Hãy chọn món rồi bấm **THÊM MÓN VÀO ĐƠN**."
    )

else:

    grand_total = 0
    total_quantity = 0

    for index, item in enumerate(st.session_state.cart):

        st.markdown(f"### 🧋 Món {index + 1}")

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"**{item['drink']}** × {item['quantity']}"
            )

            st.write(
                f"🥤 Topping: {item['topping']}"
            )

            st.write(
                f"🍬 Đường: {item['sugar']}  |  "
                f"🧊 Đá: {item['ice']}  |  "
                f"🍵 Trà: {item['tea']}"
            )

            st.write(
                f"💵 Đơn giá: {format_money(item['unit_price'])}"
            )

            st.write(
                f"💰 Thành tiền: **{format_money(item['total_price'])}**"
            )

        with col2:

            if st.button(
                "🗑️ Xóa",
                key=f"delete_{index}",
                use_container_width=True
            ):
                st.session_state.cart.pop(index)
                st.rerun()

        grand_total += item["total_price"]
        total_quantity += item["quantity"]

        st.divider()


    # =========================
    # TỔNG ĐƠN HÀNG
    # =========================
    st.subheader("💰 Tổng đơn hàng")

    total_col1, total_col2 = st.columns(2)

    with total_col1:
        st.metric(
            "Tổng số món",
            total_quantity
        )

    with total_col2:
        st.metric(
            "Tổng tiền",
            format_money(grand_total)
        )


    st.markdown(
        f"""
        <div style="
            background-color:#FFF3CD;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #FFC107;
            margin-top:10px;
            margin-bottom:20px;
        ">
            <h3 style="margin:0;color:#856404;">
                💰 TỔNG TIỀN THANH TOÁN
            </h3>

            <h1 style="
                margin:10px 0;
                color:#D35400;
            ">
                {format_money(grand_total)}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # TẠO HÓA ĐƠN
    # =========================
    def create_invoice():

        now = datetime.now()

        customer = (
            customer_name.strip()
            if customer_name.strip()
            else "Khách lẻ"
        )

        invoice = f"""
========================================
          HÓA ĐƠN TRÀ SỮA
========================================

Ngày giờ: {now.strftime("%d/%m/%Y %H:%M:%S")}

Khách hàng: {customer}

========================================
              CHI TIẾT ĐƠN
========================================
"""

        for index, item in enumerate(st.session_state.cart):

            invoice += f"""
----------------------------------------
MÓN {index + 1}
----------------------------------------

Tên món       : {item['drink']}
Số lượng      : {item['quantity']}
Topping       : {item['topping']}

Mức độ đường  : {item['sugar']}
Mức độ đá     : {item['ice']}
Mức độ trà    : {item['tea']}

Giá trà sữa   : {format_money(item['drink_price'])}
Giá topping   : {format_money(item['topping_price'])}
Đơn giá       : {format_money(item['unit_price'])}

Thành tiền    : {format_money(item['total_price'])}
"""

        invoice += f"""
========================================
TỔNG SỐ MÓN    : {total_quantity}
TỔNG THANH TOÁN: {format_money(grand_total)}
========================================

          CẢM ƠN QUÝ KHÁCH!
         HẸN GẶP LẠI ❤️

========================================
"""

        return invoice


    # =========================
    # THANH TOÁN
    # =========================
    st.divider()

    if st.button(
        "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        invoice_content = create_invoice()

        st.success(
            "✅ Thanh toán thành công!"
        )

        st.subheader("📄 Hóa đơn")

        st.code(
            invoice_content,
            language="text"
        )

        file_name = (
            "hoa_don_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        st.download_button(
            label="📥 TẢI HÓA ĐƠN",
            data=invoice_content.encode("utf-8"),
            file_name=file_name,
            mime="text/plain",
            use_container_width=True
        )


    # =========================
    # XÓA ĐƠN HÀNG
    # =========================
    if st.button(
        "🗑️ XÓA TOÀN BỘ ĐƠN HÀNG",
        use_container_width=True
    ):
        clear_cart()
        st.rerun()
