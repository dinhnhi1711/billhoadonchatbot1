import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Bill Trà Sữa",
    page_icon="🧋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

SIZE_LEVELS = ["M", "L"]
SUGAR_LEVELS = ["100%", "70%", "50%", "0%"]
ICE_LEVELS = ["100%", "70%", "50%", "0%"]
TEA_LEVELS = ["100%", "70%", "50%", "30%"]


# =========================================================
# HÀM
# =========================================================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


def calculate_item(drink, topping, quantity, size):
    drink_price = MENU[drink]
    topping_price = TOPPINGS[topping]

    # Size L cộng thêm 5.000
    size_price = 5000 if size == "L" else 0

    unit_price = drink_price + topping_price + size_price
    total_price = unit_price * quantity

    return drink_price, topping_price, size_price, unit_price, total_price


# =========================================================
# SESSION STATE
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "order_items" not in st.session_state:
    st.session_state.order_items = []


# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

    /* ================================
       TOÀN TRANG
    ================================= */
    .main {
        padding-top: 0.5rem;
        padding-bottom: 3rem;
    }

    .block-container {
        max-width: 850px;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* ================================
       HEADER
    ================================= */
    .header-box {
        background: linear-gradient(135deg, #8B4513, #D2691E);
        padding: 22px 20px;
        border-radius: 22px;
        color: white;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(139,69,19,0.20);
    }

    .header-title {
        font-size: 28px;
        font-weight: 800;
        margin: 0;
    }

    .header-sub {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 5px;
    }

    /* ================================
       SECTION
    ================================= */
    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #5D4037;
        margin: 8px 0 12px 0;
    }

    /* ================================
       PRODUCT CARD
    ================================= */
    .product-card {
        background: #FFFDF8;
        border: 1px solid #F0E2D0;
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .product-number {
        display: inline-block;
        background: #8B4513;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        text-align: center;
        line-height: 28px;
        font-size: 13px;
        font-weight: 700;
        margin-right: 7px;
    }

    .product-name {
        color: #5D4037;
        font-size: 16px;
        font-weight: 800;
    }

    .product-price {
        color: #D35400;
        font-size: 14px;
        font-weight: 700;
        float: right;
    }

    /* ================================
       CART CARD
    ================================= */
    .cart-card {
        background: white;
        border: 1px solid #EDEDED;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 10px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .cart-name {
        font-size: 16px;
        font-weight: 800;
        color: #4E342E;
    }

    .cart-detail {
        font-size: 13px;
        color: #777;
        line-height: 1.7;
        margin-top: 4px;
    }

    .cart-total {
        color: #D35400;
        font-weight: 800;
        font-size: 16px;
    }

    /* ================================
       TOTAL
    ================================= */
    .total-box {
        background: linear-gradient(135deg, #FFF8E7, #FFEFCB);
        border: 1px solid #FFD166;
        border-radius: 18px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-small {
        text-align: center;
        color: #856404;
        font-size: 13px;
        font-weight: 600;
    }

    .total-money {
        text-align: center;
        color: #D35400;
        font-size: 30px;
        font-weight: 900;
        margin-top: 5px;
    }

    /* ================================
       PRICE PREVIEW
    ================================= */
    .price-preview {
        background: #F8F9FA;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin: 8px 0 12px 0;
        border: 1px solid #EEEEEE;
    }

    .price-preview b {
        color: #D35400;
    }

    /* ================================
       BUTTON
    ================================= */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 42px !important;
    }

    /* ================================
       INPUT
    ================================= */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    .stTextInput input {
        border-radius: 10px;
    }

    /* ================================
       MOBILE
    ================================= */
    @media (max-width: 600px) {

        .header-title {
            font-size: 22px;
        }

        .block-container {
            padding-left: 0.7rem;
            padding-right: 0.7rem;
        }

        .total-money {
            font-size: 26px;
        }
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="header-box">
    <div class="header-title">🧋 BILL TRÀ SỮA</div>
    <div class="header-sub">
        Quản lý order nhanh • Gọn • Dễ sử dụng
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================
with st.expander("👤 Thông tin khách hàng", expanded=True):

    customer_name = st.text_input(
        "Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Ví dụ: Nguyễn Văn An",
        label_visibility="collapsed"
    )

    st.session_state.customer_name = customer_name


# =========================================================
# TABS
# =========================================================
tab_order, tab_cart = st.tabs([
    "🧋 CHỌN MÓN",
    f"🛒 ĐƠN HÀNG ({len(st.session_state.cart)})"
])


# =========================================================
# TAB CHỌN MÓN
# =========================================================
with tab_order:

    st.markdown(
        '<div class="section-title">🧋 Tạo món mới</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SỐ LƯỢNG MÓN MUỐN ORDER
    # -----------------------------------------------------
    number_of_items = st.number_input(
        "Bạn muốn thêm bao nhiêu loại món?",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )

    st.caption(
        "💡 Bạn có thể cấu hình từng món riêng rồi thêm tất cả vào đơn hàng cùng lúc."
    )

    # -----------------------------------------------------
    # FORM NHIỀU MÓN
    # -----------------------------------------------------
    current_items = []

    for i in range(int(number_of_items)):

        st.markdown(
            f"""
            <div class="product-card">
                <span class="product-number">{i + 1}</span>
                <span class="product-name">Món {i + 1}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            drink = st.selectbox(
                "Món",
                list(MENU.keys()),
                key=f"drink_{i}"
            )

        with col2:
            quantity = st.number_input(
                "SL",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key=f"quantity_{i}"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            size = st.selectbox(
                "📏 Size",
                SIZE_LEVELS,
                key=f"size_{i}"
            )

        with col2:
            topping = st.selectbox(
                "🍮 Topping",
                list(TOPPINGS.keys()),
                key=f"topping_{i}"
            )

        with col3:
            sugar = st.selectbox(
                "🍬 Đường",
                SUGAR_LEVELS,
                index=2,
                key=f"sugar_{i}"
            )

        col1, col2 = st.columns(2)

        with col1:
            ice = st.selectbox(
                "🧊 Đá",
                ICE_LEVELS,
                index=2,
                key=f"ice_{i}"
            )

        with col2:
            tea = st.selectbox(
                "🍵 Trà",
                TEA_LEVELS,
                index=0,
                key=f"tea_{i}"
            )

        (
            drink_price,
            topping_price,
            size_price,
            unit_price,
            total_price
        ) = calculate_item(
            drink,
            topping,
            quantity,
            size
        )

        st.markdown(
            f"""
            <div class="price-preview">
                Đơn giá: <b>{format_money(unit_price)}</b>
                &nbsp; × &nbsp;
                {quantity} ly
                &nbsp; = &nbsp;
                <b>{format_money(total_price)}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        current_items.append({
            "drink": drink,
            "quantity": int(quantity),
            "size": size,
            "topping": topping,
            "sugar": sugar,
            "ice": ice,
            "tea": tea,
            "drink_price": drink_price,
            "topping_price": topping_price,
            "size_price": size_price,
            "unit_price": unit_price,
            "total_price": total_price
        })

        if i < int(number_of_items) - 1:
            st.divider()

    # -----------------------------------------------------
    # TỔNG TIỀN CÁC MÓN ĐANG TẠO
    # -----------------------------------------------------
    current_total = sum(
        item["total_price"] for item in current_items
    )

    current_quantity = sum(
        item["quantity"] for item in current_items
    )

    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-small">
                🧾 ĐANG CHUẨN BỊ {current_quantity} LY
            </div>

            <div class="total-money">
                {format_money(current_total)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # THÊM TẤT CẢ VÀO GIỎ
    # -----------------------------------------------------
    if st.button(
        "➕ THÊM TẤT CẢ VÀO ĐƠN",
        type="primary",
        use_container_width=True
    ):

        st.session_state.cart.extend(current_items)

        st.success(
            f"✅ Đã thêm {len(current_items)} loại món "
            f"({current_quantity} ly) vào đơn hàng!"
        )

        st.rerun()


# =========================================================
# TAB GIỎ HÀNG
# =========================================================
with tab_cart:

    st.markdown(
        '<div class="section-title">🛒 Đơn hàng hiện tại</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.cart:

        st.info(
            "🛒 Đơn hàng đang trống.\n\n"
            "Hãy sang tab **🧋 CHỌN MÓN** để thêm món."
        )

    else:

        grand_total = 0
        total_quantity = 0

        # -------------------------------------------------
        # HIỂN THỊ GIỎ
        # -------------------------------------------------
        for index, item in enumerate(st.session_state.cart):

            grand_total += item["total_price"]
            total_quantity += item["quantity"]

            col_info, col_delete = st.columns([8, 1])

            with col_info:

                st.markdown(
                    f"""
                    <div class="cart-card">

                        <div class="cart-name">
                            🧋 {item["drink"]}
                            <span style="color:#D35400;">
                                × {item["quantity"]}
                            </span>
                        </div>

                        <div class="cart-detail">
                            📏 Size: {item["size"]}
                            &nbsp; • &nbsp;
                            🍮 {item["topping"]}
                            <br>

                            🍬 Đường: {item["sugar"]}
                            &nbsp; • &nbsp;
                            🧊 Đá: {item["ice"]}
                            &nbsp; • &nbsp;
                            🍵 Trà: {item["tea"]}
                        </div>

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            margin-top:8px;
                        ">

                            <span style="
                                color:#999;
                                font-size:12px;
                            ">
                                {format_money(item["unit_price"])} / ly
                            </span>

                            <span class="cart-total">
                                {format_money(item["total_price"])}
                            </span>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_delete:

                if st.button(
                    "🗑️",
                    key=f"delete_{index}",
                    help="Xóa món"
                ):

                    st.session_state.cart.pop(index)

                    st.rerun()

        # -------------------------------------------------
        # TỔNG ĐƠN
        # -------------------------------------------------
        st.markdown(
            f"""
            <div class="total-box">

                <div class="total-small">
                    🧾 TỔNG ĐƠN HÀNG
                </div>

                <div style="
                    text-align:center;
                    color:#777;
                    margin-top:4px;
                    font-size:13px;
                ">
                    {len(st.session_state.cart)} loại món
                    &nbsp; • &nbsp;
                    {total_quantity} ly
                </div>

                <div class="total-money">
                    {format_money(grand_total)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # THANH TOÁN
        # =================================================
        if st.button(
            "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
            type="primary",
            use_container_width=True
        ):

            customer = (
                st.session_state.customer_name.strip()
                if st.session_state.customer_name.strip()
                else "Khách lẻ"
            )

            now = datetime.now()

            invoice = ""

            invoice += """
========================================
           🧋 HÓA ĐƠN TRÀ SỮA
========================================
"""

            invoice += (
                f"\nNgày giờ   : "
                f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
            )

            invoice += f"Khách hàng : {customer}\n"

            invoice += """
========================================
              CHI TIẾT ĐƠN
========================================
"""

            for index, item in enumerate(st.session_state.cart):

                invoice += f"""
----------------------------------------
MÓN {index + 1}
----------------------------------------
Tên món       : {item["drink"]}
Số lượng      : {item["quantity"]}
Size          : {item["size"]}
Topping       : {item["topping"]}
Mức độ đường  : {item["sugar"]}
Mức độ đá     : {item["ice"]}
Mức độ trà    : {item["tea"]}

Giá trà sữa   : {format_money(item["drink_price"])}
Giá topping   : {format_money(item["topping_price"])}
Giá size      : {format_money(item["size_price"])}
Đơn giá       : {format_money(item["unit_price"])}
Thành tiền    : {format_money(item["total_price"])}
"""

            invoice += f"""
========================================
TỔNG SỐ LOẠI : {len(st.session_state.cart)}
TỔNG SỐ LY   : {total_quantity}
TỔNG THANH TOÁN: {format_money(grand_total)}
========================================

          CẢM ƠN QUÝ KHÁCH! ❤️
             HẸN GẶP LẠI!

========================================
"""

            st.success("✅ Thanh toán thành công!")

            st.subheader("📄 Hóa đơn")

            st.code(
                invoice,
                language="text"
            )

            file_name = (
                "hoa_don_"
                f"{now.strftime('%Y%m%d_%H%M%S')}.txt"
            )

            st.download_button(
                label="📥 TẢI HÓA ĐƠN",
                data=invoice.encode("utf-8"),
                file_name=file_name,
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        # =================================================
        # XÓA TOÀN BỘ
        # =================================================
        if st.button(
            "🗑️ XÓA TOÀN BỘ ĐƠN HÀNG",
            use_container_width=True
        ):

            st.session_state.cart = []

            st.rerun()
