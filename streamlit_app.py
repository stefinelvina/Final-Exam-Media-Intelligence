import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import base64
from fpdf import FPDF

API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

st.set_page_config(page_title="Tropicode Dashboard", layout="wide")
st.title("📊 AI-Powered Media Intelligence Dashboard")
st.markdown("Visualisasi data media Tropicode: Sentimen, Engagement, dan Platform")

uploaded_file = st.file_uploader("Upload file CSV kamu di sini", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])

    st.subheader("📈 Visualisasi Data")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.pie(df, names='Sentiment', title='Distribusi Sentimen'), use_container_width=True)

    with col2:
        st.plotly_chart(px.bar(df, x='Platform', y='Engagements', color='Platform',
                               title='Engagement per Platform'), use_container_width=True)

    st.plotly_chart(px.line(df.sort_values("Date"), x='Date', y='Engagements',
                            title='Engagement dari Waktu ke Waktu'), use_container_width=True)

    st.plotly_chart(px.pie(df, names='Media_Type', title='Proporsi Tipe Media'), use_container_width=True)

    top_loc = df.groupby('Location')['Engagements'].sum().sort_values(ascending=False).head(5).reset_index()
    st.plotly_chart(px.bar(top_loc, x='Location', y='Engagements',
                           title='Top 5 Lokasi dengan Engagement Tertinggi'), use_container_width=True)

    st.subheader("📌 Ringkasan Statistik")
    col3, col4, col5 = st.columns(3)
    total_data = len(df)
    total_engagement = df['Engagements'].sum()
    total_positif = (df['Sentiment'] == "Positive").sum()
    col3.metric("Jumlah Data", total_data)
    col4.metric("Engagement Total", total_engagement)
    col5.metric("Sentimen Positif", total_positif)

    def generate_ai_insight(data):
        sample = data[['Platform', 'Sentiment', 'Engagements']].value_counts().head(5).to_string()
        prompt = f"Berdasarkan data berikut:\n{sample}\nBuatkan insight singkat terkait sentimen dan engagement pengguna."

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Tropicode Dashboard"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Kamu adalah analis media digital."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except requests.exceptions.HTTPError as err:
            return f"HTTP Error: {err}\n\nRAW: {response.text}"
        except Exception as e:
            return f"Terjadi error: {e}"
    def generate_pdf_report(insight_text, total_data, total_engagement, total_positif):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Tropicode Dashboard - Laporan Media Intelligence", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="Ringkasan Statistik", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 8, txt=f"Jumlah Data         : {total_data}", ln=True)
        pdf.cell(200, 8, txt=f"Engagement Total    : {total_engagement}", ln=True)
        pdf.cell(200, 8, txt=f"Sentimen Positif    : {total_positif}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="Insight Otomatis dari AI", ln=True)
        pdf.set_font("Arial", size=11)
        for line in insight_text.split('\n'):
            pdf.multi_cell(0, 8, line)

        pdf_path = "laporan_insight.pdf"
        pdf.output(pdf_path)
        return pdf_path

    st.subheader("💡 Insight Otomatis dari AI")
    if "insight_text" not in st.session_state:
        st.session_state.insight_text = ""

    if st.button("Generate Insight dari AI"):
        with st.spinner("Sedang menganalisis data dengan AI..."):
            insight = generate_ai_insight(df)
            st.session_state.insight_text = insight

    if st.session_state.insight_text:
        st.success(st.session_state.insight_text)

        b64 = base64.b64encode(st.session_state.insight_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="insight.txt">📥 Download Insight (TXT)</a>'
        st.markdown(href, unsafe_allow_html=True)

        if st.button("📄 Generate PDF Laporan"):
            pdf_file = generate_pdf_report(
                st.session_state.insight_text,
                total_data,
                total_engagement,
                total_positif
            )
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF Laporan", f, file_name="laporan_insight.pdf")

    st.subheader("🤖 Tanya Jawab dengan AI")
    user_input = st.text_input("Tanyakan sesuatu ke AI berdasarkan data yang diupload")
    if user_input:
        with st.spinner("Sedang diproses oleh AI..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Tropicode Dashboard"
            }

            prompt = f"Berdasarkan data media berikut:\n{df[['Platform', 'Sentiment', 'Engagements']].value_counts().head(10).to_string()}\n\nPertanyaan: {user_input}"

            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "Kamu adalah analis media digital."},
                    {"role": "user", "content": prompt}
                ]
            }

            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()
                answer = response.json()["choices"][0]["message"]["content"].strip()
                st.success(answer)
            except Exception as e:
                st.error(f"Terjadi error: {e}")
