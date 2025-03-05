import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# 🎨 背景画像の設定（アップロードされた画像を使用）
BACKGROUND_IMAGE = "modern-3d-lighting-lamp-design.jpg"

st.markdown(
    f"""
    <style>
    body {{
        background-image: url('data:image/jpg;base64,{BACKGROUND_IMAGE}');
        background-size: cover;
        background-position: center;
        color: #FFD700; /* 文字色（ゴールド） */
    }}

    /* フォームの背景色 */
    .stTextInput, .stNumberInput, .stTextArea {{
        background-color: rgba(255, 215, 0, 0.1); /* 半透明ゴールド */
        color: #FFD700;
    }}

    /* ボタンのカスタマイズ */
    .stButton>button {{
        background: linear-gradient(145deg, #b8860b, #ffd700);
        color: black;
        border: 2px solid #ffd700;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }}

    /* ボタンのホバーエフェクト */
    .stButton>button:hover {{
        background: #ffd700;
        color: black;
        box-shadow: 0px 0px 10px #ffd700;
    }}

    /* QRコードの枠 */
    .stImage img {{
        border: 5px solid #ffd700;
        padding: 10px;
        border-radius: 10px;
        background: black;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def generate_vcard(name, furigana, personal_phone, personal_email, 
                   company_name, company_zip, company_address, company_phone, company_fax):
    """iPhone対応のVCARD形式を作成"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;;
FN:{name}
SORT-STRING:{furigana}
TEL;TYPE=CELL:{personal_phone}
EMAIL;TYPE=WORK:{personal_email}
ORG:{company_name}
TITLE:勤務先
ADR;TYPE=WORK:;;{company_address};{company_zip};;;
TEL;TYPE=WORK:{company_phone}
TEL;TYPE=FAX:{company_fax}
END:VCARD"""

    # iPhone対応のため、改行コードを "\r\n" に統一
    return vcard.replace("\n", "\r\n")

def generate_qr_code(data):
    """QRコードを生成し、画像をバイナリデータに変換"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高エラー修正レベル
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # PILのImageオブジェクトとしてQRコードを生成
    img = qr.make_image(fill="black", back_color="white").convert("RGB")

    # 画像をBytesIOに保存（st.image() で表示するため）
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes  # BytesIOオブジェクトを返す

def main():
    st.title("✨ ゴージャスな QRコード作成アプリ ✨")

    with st.form("business_card_form"):
        st.subheader("📜 個人情報")
        name = st.text_input("📝 氏名")
        furigana = st.text_input("📝 フリガナ")
        personal_phone = st.text_input("📱 個人電話番号")
        personal_email = st.text_input("📧 個人メールアドレス")

        st.subheader("🏢 会社情報")
        company_name = st.text_input("🏢 会社名")
        company_zip = st.text_input("📮 会社郵便番号")
        company_address = st.text_input("🏙️ 会社住所")
        company_phone = st.text_input("☎️ 会社代表電話番号")
        company_fax = st.text_input("📠 会社代表FAX番号")

        submit_button = st.form_submit_button("✨ QRコードを生成 ✨")

    if submit_button:
        vcard_data = generate_vcard(name, furigana, personal_phone, personal_email, 
                                    company_name, company_zip, company_address, company_phone, company_fax)

        # QRコードを生成（BytesIOオブジェクト）
        qr_bytes = generate_qr_code(vcard_data)

        # QRコードを表示
        st.image(qr_bytes, caption="📸 生成されたQRコード")

        # QRコードをダウンロード可能にする
        st.download_button(label="📥 QRコードをダウンロード",
                           data=qr_bytes,
                           file_name="business_card_qr.png",
                           mime="image/png")

if __name__ == "__main__":
    main()
