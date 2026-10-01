import streamlit as st
from datetime import datetime
from io import BytesIO

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

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
# TIÊU ĐỀ
# =========================
st.title("🧋 QUẢN LÝ BILL QUÁN TRÀ SỮA")
st.caption("Nhập thông tin đơn hàng và xuất hóa đơn sau khi thanh toán.")

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Ví dụ: Nguyễn Văn An"
)

# =========================
# NHẬP ĐƠN HÀNG
# =========================
st.subheader("🧋 Thông tin đồ uống")

drink = st.selectbox(
    "Loại trà sữa",
    list(MENU.keys())
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

col1, col2 = st.columns(2)

with col1:
    sugar = st.selectbox(
        "🍬 Mức độ đường",
        SUGAR_LEVELS
    )

    tea = st.selectbox(
        "🍵 Mức độ trà",
        TEA_LEVELS
    )

with col2:
    ice = st.selectbox(
        "🧊 Mức độ đá",
        ICE_LEVELS
    )

# =========================
# TÍNH TIỀN
# =========================
drink_price = MENU[drink]
topping_price = TOPPINGS[topping]

unit_price = drink_price + topping_price
total_price = unit_price * quantity

# =========================
# HIỂN THỊ KẾT QUẢ
# =========================
st.divider()
st.subheader("🧾 Thông tin đơn hàng")

result_col1, result_col2 = st.columns(2)

with result_col1:
    st.write(f"**Khách hàng:** {customer_name if customer_name else 'Chưa nhập tên'}")
    st.write(f"**Trà sữa:** {drink}")
    st.write(f"**Số lượng:** {quantity}")
    st.write(f"**Topping:** {topping}")

with result_col2:
    st.write(f"**Đường:** {sugar}")
    st.write(f"**Đá:** {ice}")
    st.write(f"**Trà:** {tea}")
    st.write(f"**Đơn giá:** {format_money(unit_price)}")

st.divider()

st.markdown(
    f"""
    <div style="
        background-color:#FFF3CD;
        padding:20px;
        border-radius:12px;
        text-align:center;
        border:1px solid #FFC107;
    ">
        <h3 style="margin:0;color:#856404;">
            💰 TỔNG TIỀN THANH TOÁN
        </h3>
        <h1 style="margin:10px 0;color:#D35400;">
            {format_money(total_price)}
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# TẠO NỘI DUNG HÓA ĐƠN
# =========================
def create_invoice():
    now = datetime.now()

    invoice = f"""
========================================
        HÓA ĐƠN TRÀ SỮA
========================================

Ngày giờ: {now.strftime("%d/%m/%Y %H:%M:%S")}

Khách hàng: {customer_name if customer_name else "Khách lẻ"}

----------------------------------------
THÔNG TIN ĐỒ UỐNG
----------------------------------------

Trà sữa       : {drink}
Số lượng      : {quantity}
Topping       : {topping}

Mức độ đường  : {sugar}
Mức độ đá     : {ice}
Mức độ trà    : {tea}

----------------------------------------
CHI TIẾT THANH TOÁN
----------------------------------------

Giá trà sữa   : {format_money(drink_price)}
Giá topping   : {format_money(topping_price)}
Đơn giá       : {format_money(unit_price)}

Số lượng      : {quantity}

----------------------------------------
TỔNG THANH TOÁN: {format_money(total_price)}
----------------------------------------

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
    if not customer_name.strip():
        customer_name = "Khách lẻ"

    invoice_content = create_invoice()

    st.success("✅ Thanh toán thành công!")

    st.subheader("📄 Hóa đơn")

    st.code(invoice_content, language="text")

    file_name = (
        f"hoa_don_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    st.download_button(
        label="📥 TẢI HÓA ĐƠN",
        data=invoice_content.encode("utf-8"),
        file_name=file_name,
        mime="text/plain",
        use_container_width=True
    )
