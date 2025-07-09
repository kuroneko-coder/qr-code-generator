import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

def generate_vcard(last_name, first_name, last_furigana, first_furigana,
                   personal_phone, personal_email,
                   company_name, company_zip, company_address, company_phone, company_fax,
                   company_position, company_department, company_website, instagram, youtube, pr_link):
    """iPhone / Android 両対応のVCARD形式を作成"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name};;;
FN:{first_name} {last_name}
SORT-STRING:{last_furigana}{first_furigana}
TITLE:{company_position}
ORG:{company_name};{company_department}
TEL;TYPE=CELL,VOICE:{personal_phone}
TEL;TYPE=WORK,VOICE:{company_phone}
TEL;TYPE=FAX,WORK:{company_fax}
EMAIL;TYPE=WORK:{personal_email}
ADR;TYPE=WORK:;;{company_address};;;{company_zip};
URL:{company_website}
URL:{instagram}
URL:{youtube}
URL:{pr_link}
END:VCARD"""
    return vcard.replace("\n", "\r\n")

def generate_qr_code(data):
    """QRコードを生成し、BytesIO形式で返す"""
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white").convert("RGB")
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes

def main():
    st.set_page_config(page_title="QR名刺メーカー", page_icon="📇", layout="centered")
    st.title("📇 QRコード名刺メーカー（iPhone / Android対応）")
    st.write("連絡先情報をQRコードに変換し、スマホの連絡帳にすぐ登録できる形式で出力します。")

    with st.form("business_card_form"):
        st.subheader("🧑‍💼 個人情報")
        last_name = st.text_input("姓（例：山田）")
        first_name = st.text_input("名（例：太郎）")
        last_furigana = st.text_input("姓のフリガナ（例：ヤマダ）")
        first_furigana = st.text_input("名のフリガナ（例：タロウ）")
        personal_phone = st.text_input("個人電話番号（例：090-1234-5678）")
        personal_email = st.text_input("個人メールアドレス")

        st.subheader("🏢 会社情報")
        company_name = st.text_input("会社名", "株式会社フェローズ")
        company_department = st.text_input("部署")
        company_position = st.text_input("役職")
        company_zip = st.text_input("郵便番号（例：150-0001）")
        company_address = st.text_input("会社住所（例：東京都渋谷区〇〇）")
        company_phone = st.text_input("会社電話番号")
        company_fax = st.text_input("会社FAX番号")
        company_website = st.text_input("会社Webサイト", "https://fellows2008.co.jp/")

        st.subheader("🌐 SNS・PR情報")
        instagram = st.text_input("Instagram URL", "https://www.instagram.com/fellows2008/")
        youtube = st.text_input("YouTube URL", "https://www.youtube.com/@fellows2008")
        pr_link = st.text_input("PRリンクURL", "https://fellows2008.co.jp/service/ai/")

        submit_button = st.form_submit_button("📤 QRコードを生成")

    if submit_button:
        vcard_data = generate_vcard(
            last_name, first_name, last_furigana, first_furigana,
            personal_phone, personal_email,
            company_name, company_zip, company_address, company_phone, company_fax,
            company_position, company_department, company_website,
            instagram, youtube, pr_link
        )

        qr_bytes = generate_qr_code(vcard_data)

        st.success("QRコードが生成されました。スマホでスキャンして連絡先に登録できます。")
        st.image(qr_bytes, caption="📷 スマホで読み取ってください", use_column_width=False)

        st.download_button(
            label="📥 QRコードをダウンロード",
            data=qr_bytes,
            file_name="vcard_qr.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
