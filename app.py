import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# =========================================================
# LOGO
# =========================================================
try:
    st.image("logo.jpg", use_container_width=True)
except:
    pass


# =========================================================
# DỮ LIỆU MENU
# =========================================================
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


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================================================
# SESSION STATE
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown(
    """
    <style>

    /* Toàn trang */
    .main {
        padding-top: 1rem;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        color: #8B4513;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    /* Card sản phẩm trong giỏ */
    .cart-card {
        background: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .cart-name {
        font-size: 17px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 4px;
    }

    .cart-detail {
        font-size: 13px;
        color: #777777;
        line-height: 1.5;
    }

    .cart-price {
        font-size: 16px;
        font-weight: 700;
        color: #D35400;
        text-align: right;
    }

    /* Box tổng tiền */
    .total-box {
        background: linear-gradient(
            135deg,
            #FFF8E7,
            #FFF1C9
        );
        border: 1px solid #FFD166;
        border-radius: 16px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-label {
        color: #856404;
        font-size: 14px;
        font-weight: 600;
        text-align: center;
    }

    .total-money {
        color: #D35400;
        font-size: 30px;
        font-weight: 800;
        text-align: center;
        margin-top: 5px;
    }

    /* Giá món đang chọn */
    .current-price {
        background: #F8F9FA;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 10px 0;
        text-align: center;
        color: #555;
    }

    /* Divider */
    hr {
        margin-top: 15px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown(
    '<h1 class="main-title">🧋 QUẢN LÝ BILL QUÁN TRÀ SỮA</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Chọn món, tùy chỉnh và thêm vào đơn hàng'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================
st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Ví dụ: Nguyễn Văn An",
    key="customer_input"
)

st.session_state.customer_name = customer_name


# =========================================================
# THÊM MÓN
# =========================================================
st.divider()

st.subheader("🧋 Chọn món")


# ---------------------------------------------------------
# Tên món
# ---------------------------------------------------------
drink = st.selectbox(
    "Loại trà sữa / món",
    list(MENU.keys()),
    key="drink_select"
)


# ---------------------------------------------------------
# Số lượng
# ---------------------------------------------------------
quantity = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
    key="quantity_select"
)


# ---------------------------------------------------------
# Topping
# ---------------------------------------------------------
topping = st.selectbox(
    "Topping",
    list(TOPPINGS.keys()),
    key="topping_select"
)


# ---------------------------------------------------------
# Tùy chỉnh
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    sugar = st.selectbox(
        "🍬 Đường",
        SUGAR_LEVELS,
        key="sugar_select"
    )

    tea = st.selectbox(
        "🍵 Trà",
        TEA_LEVELS,
        key="tea_select"
    )


with col2:

    ice = st.selectbox(
        "🧊 Đá",
        ICE_LEVELS,
        key="ice_select"
    )


# =========================================================
# TÍNH GIÁ MÓN ĐANG CHỌN
# =========================================================
drink_price = MENU[drink]
topping_price = TOPPINGS[topping]

unit_price = drink_price + topping_price
item_total = unit_price * quantity


st.markdown(
    f"""
    <div class="current-price">
        Đơn giá:
        <b>{format_money(unit_price)}</b>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        Thành tiền:
        <b style="color:#D35400;">
            {format_money(item_total)}
        </b>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# THÊM VÀO GIỎ
# =========================================================
if st.button(
    "➕ THÊM VÀO ĐƠN HÀNG",
    type="primary",
    use_container_width=True
):

    new_item = {
        "drink": drink,
        "quantity": int(quantity),
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "tea": tea,
        "drink_price": drink_price,
        "topping_price": topping_price,
        "unit_price": unit_price,
        "total_price": item_total
    }

    st.session_state.cart.append(new_item)

    st.success(
        f"Đã thêm {quantity} × {drink} vào đơn hàng!"
    )


# =========================================================
# GIỎ HÀNG
# =========================================================
st.divider()

st.subheader("🛒 Đơn hàng")


if len(st.session_state.cart) == 0:

    st.info(
        "🛒 Đơn hàng đang trống. "
        "Hãy chọn món ở phía trên để bắt đầu."
    )

else:

    grand_total = 0
    total_quantity = 0


    # -----------------------------------------------------
    # HIỂN THỊ CÁC MÓN
    # -----------------------------------------------------
    for index, item in enumerate(st.session_state.cart):

        grand_total += item["total_price"]
        total_quantity += item["quantity"]

        # Card món
        col_info, col_delete = st.columns([6, 1])

        with col_info:

            st.markdown(
                f"""
                <div class="cart-card">

                    <div class="cart-name">
                        🧋 {item["drink"]}
                        &nbsp; × {item["quantity"]}
                    </div>

                    <div class="cart-detail">
                        Topping: {item["topping"]}
                        &nbsp; | &nbsp;
                        Đường: {item["sugar"]}
                        &nbsp; | &nbsp;
                        Đá: {item["ice"]}
                        &nbsp; | &nbsp;
                        Trà: {item["tea"]}
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        margin-top:8px;
                    ">

                        <span style="
                            font-size:12px;
                            color:#999;
                        ">
                            {format_money(item["unit_price"])}
                            / ly
                        </span>

                        <span class="cart-price">
                            {format_money(item["total_price"])}
                        </span>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col_delete:

            st.write("")

            if st.button(
                "🗑️",
                key=f"delete_{index}",
                help="Xóa món này"
            ):

                st.session_state.cart.pop(index)

                st.rerun()


    # =====================================================
    # TỔNG ĐƠN
    # =====================================================
    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-label">
                🧾 TỔNG ĐƠN HÀNG
            </div>

            <div style="
                text-align:center;
                color:#777;
                margin-top:5px;
                font-size:14px;
            ">
                {total_quantity} sản phẩm
            </div>

            <div class="total-money">
                {format_money(grand_total)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # THANH TOÁN
    # =====================================================
    if st.button(
        "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        # -------------------------------------------------
        # TÊN KHÁCH
        # -------------------------------------------------
        customer = (
            st.session_state.customer_name.strip()
            if st.session_state.customer_name.strip()
            else "Khách lẻ"
        )


        # -------------------------------------------------
        # THỜI GIAN
        # -------------------------------------------------
        now = datetime.now()


        # -------------------------------------------------
        # TẠO HÓA ĐƠN
        # -------------------------------------------------
        invoice = ""

        invoice += """
========================================
             HÓA ĐƠN TRÀ SỮA
========================================
"""

        invoice += (
            f"\nNgày giờ: "
            f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )

        invoice += f"\nKhách hàng: {customer}\n"


        invoice += """
========================================
              CHI TIẾT ĐƠN
========================================
"""


        # -------------------------------------------------
        # CHI TIẾT TỪNG MÓN
        # -------------------------------------------------
        for index, item in enumerate(st.session_state.cart):

            invoice += f"""
----------------------------------------
MÓN {index + 1}
----------------------------------------
Tên món       : {item["drink"]}
Số lượng      : {item["quantity"]}
Topping       : {item["topping"]}
Mức độ đường  : {item["sugar"]}
Mức độ đá     : {item["ice"]}
Mức độ trà    : {item["tea"]}

Giá trà sữa   : {format_money(item["drink_price"])}
Giá topping   : {format_money(item["topping_price"])}
Đơn giá       : {format_money(item["unit_price"])}
Thành tiền    : {format_money(item["total_price"])}
"""


        # -------------------------------------------------
        # TỔNG
        # -------------------------------------------------
        invoice += f"""
========================================
TỔNG SỐ LƯỢNG : {total_quantity}
TỔNG THANH TOÁN: {format_money(grand_total)}
========================================

          CẢM ƠN QUÝ KHÁCH!
         HẸN GẶP LẠI ❤️

========================================
"""


        # -------------------------------------------------
        # THÔNG BÁO
        # -------------------------------------------------
        st.success(
            "✅ Thanh toán thành công!"
        )


        # -------------------------------------------------
        # HIỂN THỊ HÓA ĐƠN
        # -------------------------------------------------
        st.subheader("📄 Hóa đơn")

        st.code(
            invoice,
            language="text"
        )


        # -------------------------------------------------
        # TÊN FILE
        # -------------------------------------------------
        file_name = (
            "hoa_don_"
            f"{now.strftime('%Y%m%d_%H%M%S')}.txt"
        )


        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------
        st.download_button(
            label="📥 TẢI HÓA ĐƠN",
            data=invoice.encode("utf-8"),
            file_name=file_name,
            mime="text/plain",
            use_container_width=True
        )


    # =====================================================
    # XÓA TOÀN BỘ ĐƠN
    # =====================================================
    if st.button(
        "🗑️ XÓA TOÀN BỘ ĐƠN HÀNG",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.rerun()
