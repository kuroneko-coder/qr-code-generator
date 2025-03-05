import streamlit as st
import qrcode
from io import BytesIO

def generate_vcard(name, furigana, personal_phone, personal_email, 
                   company_name, company_zip, company_address, company_phone, company_fax):
    """VCARD形式の文字列を作成"""
    vcard = f"""
BEGIN:VCARD
VERSION:3.0
N:{name}
FN:{furigana}
TEL;TYPE=CELL:{personal_phone}
EMAIL:{personal_email}
ORG:{company_name}
ADR;TYPE=WORK:;;{company_address};{company_zip}
TEL;TYPE=WORK:{company_phone}
TEL;TYPE=FAX:{company_fax}
END:VCARD
"""
    return vcard

def generate_qr_code(data):
    """QRコードを生成し、画像を返す"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    return img

def main():
    st.title("QRコード作成アプリ")
    st.write("名刺の情報をQRコード化し、スマートフォンの電話帳に登録できる形式で出力します。")

    with st.form("business_card_form"):
        st.subheader("個人情報")
        name = st.text_input("氏名")
        furigana = st.text_input("フリガナ")
        personal_phone = st.text_input("個人電話番号")
        personal_email = st.text_input("個人メールアドレス")

        st.subheader("会社情報")
        company_name = st.text_input("会社名")
        company_zip = st.text_input("会社郵便番号")
        company_address = st.text_input("会社住所")
        company_phone = st.text_input("会社代表電話番号")
        company_fax = st.text_input("会社代表FAX番号")

        submit_button = st.form_submit_button("QRコードを生成")

    if submit_button:
        # VCARDデータを作成
        vcard_data = generate_vcard(name, furigana, personal_phone, personal_email, 
                                    company_name, company_zip, company_address, company_phone, company_fax)

        # QRコード画像を生成
        qr_img = generate_qr_code(vcard_data)

        # QRコードを表示
        st.image(qr_img, caption="生成されたQRコード")

        # QRコードをダウンロード可能にする
        img_bytes = BytesIO()
        qr_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        st.download_button(label="QRコードをダウンロード",
                           data=img_bytes,
                           file_name="business_card_qr.png",
                           mime="image/png")

if __name__ == "__main__":
    main()
