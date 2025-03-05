import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

def generate_vcard(last_name, first_name, last_furigana, first_furigana,
                   personal_phone, personal_email, 
                   company_name, company_zip, company_address, company_phone, company_fax):
    """iPhone対応のVCARD形式を作成"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name};;;
FN:{first_name} {last_name}
X-PHONETIC-LAST-NAME:{last_furigana}
X-PHONETIC-FIRST-NAME:{first_furigana}
ORG:{company_name}
TITLE:勤務先
TEL;TYPE=CELL,VOICE:{personal_phone}
TEL;TYPE=WORK,VOICE:{company_phone}
TEL;TYPE=FAX,WORK:{company_fax}
EMAIL;TYPE=WORK:{personal_email}
ADR;TYPE=WORK:;;{company_address};{company_zip};;;
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
    st.title("QRコード作成アプリ")
    st.write("名刺の情報をQRコード化し、スマートフォンの電話帳に登録できる形式で出力します。")

    with st.form("business_card_form"):
        st.subheader("個人情報")
        last_name = st.text_input("姓")
        first_name = st.text_input("名")
        last_furigana = st.text_input("姓（フリガナ）")
        first_furigana = st.text_input("名（フリガナ）")
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
        vcard_data = generate_vcard(last_name, first_name, last_furigana, first_furigana,
                                    personal_phone, personal_email, 
                                    company_name, company_zip, company_address, company_phone, company_fax)

        # QRコードを生成（BytesIOオブジェクト）
        qr_bytes = generate_qr_code(vcard_data)

        # QRコードを表示
        st.image(qr_bytes, caption="生成されたQRコード")

        # QRコードをダウンロード可能にする
        st.download_button(label="QRコードをダウンロード",
                           data=qr_bytes,
                           file_name="business_card_qr.png",
                           mime="image/png")

if __name__ == "__main__":
    main()
