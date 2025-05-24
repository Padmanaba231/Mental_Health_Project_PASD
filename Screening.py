import streamlit as st
import pandas as pd
import pickle
from fpdf import FPDF
import base64
from datetime import datetime

# --- Load Model Secara Efisien menggunakan cache_resource ---
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Panggil model
model = load_model()

# Fungsi untuk membuat PDF
def create_pdf(hasil, answers, questions):
    pdf = FPDF()
    pdf.add_page()
    
    # Gunakan font yang konsisten (helvetica)
    pdf.set_font("helvetica", size=12)  # Font regular
    
    # Header
    pdf.set_font("helvetica", 'B', 16)  # Bold
    pdf.cell(0, 10, "Hasil Screening Kesehatan Mental", 0, 1, 'C')
    pdf.ln(5)
    
    # Hasil Screening
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "Hasil Screening", 0, 1)
    pdf.set_font("helvetica", size=12)
    
    if hasil.lower() == "other":
        pdf.multi_cell(0, 10, "Hasil: Tidak terdeteksi gangguan kesehatan mental spesifik")
        pdf.ln(5)
        pdf.multi_cell(0, 10, "Anda tidak terdeteksi mengalami gangguan kesehatan mental berikut:")
        pdf.ln(3)
        pdf.cell(10)  # indent
        pdf.cell(0, 10, "- Eating disorder")
        pdf.ln()
        pdf.cell(10)
        pdf.cell(0, 10, "- Marijuana abuse")
        pdf.ln()
        pdf.cell(10)
        pdf.cell(0, 10, "- Panic disorder")
        pdf.ln()
        pdf.cell(10)
        pdf.cell(0, 10, "- Postpartum depression")
        pdf.ln()
        pdf.cell(10)
        pdf.cell(0, 10, "- Substance-related mental disorder")
    else:
        pdf.multi_cell(0, 10, f"Hasil: Kemungkinan {hasil}")
    
    pdf.ln(10)
    
    # Detail Jawaban
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "Detail Jawaban", 0, 1)
    pdf.set_font("helvetica", size=10)
    
    for i, (question, _) in enumerate(questions):
        answer = "Ya" if answers[i] == 1 else "Tidak"
        # Split long questions to prevent overflow
        if len(question) > 80:
            parts = [question[j:j+80] for j in range(0, len(question), 80)]
            pdf.cell(10, 8, f"{i+1}. {parts[0]}", 0, 1)
            for part in parts[1:]:
                pdf.cell(20, 8, part, 0, 1)
            pdf.cell(20, 8, f"Jawaban: {answer}", 0, 1)
        else:
            pdf.multi_cell(0, 8, f"{i+1}. {question} : {answer}")
        pdf.ln(2)
    
    # Footer PDF
    pdf.ln(10)
    pdf.set_font("helvetica", 'I', 10)
    pdf.multi_cell(0, 8, "Catatan: Hasil ini merupakan prediksi awal dan tidak menggantikan diagnosis profesional. Jika Anda memiliki kekhawatiran tentang kesehatan mental Anda, silakan berkonsultasi dengan tenaga kesehatan profesional.")
    
    pdf.set_font("helvetica", size=8)
    pdf.cell(0, 10, f"Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'C')
    
    return pdf

# Fungsi untuk generate link download PDF
def get_pdf_download_link(pdf, filename):
    # Generate PDF output
    import io
    buffer = io.BytesIO()
    pdf.output(buffer)
    pdf_output = buffer.getvalue()

def screening():
    # Antarmuka pengguna Streamlit
    st.title("Screening Penyakit Mental")

    st.write("""
    Silakan jawab pertanyaan-pertanyaan di bawah ini:
    """)

    # Input pertanyaan ke user
    questions = [
        ("Apakah Anda merasa cemas atau gugup?", "anxiety and nervousness"),
        ("Apakah Anda merasa tertekan?", "depression"),
        ("Apakah Anda merasa sesak nafas?", "shortness of breath"),
        ("Apakah Anda memiliki gejala depresif atau psikosis?", "depressive or psychotic symptoms"),
        ("Apakah Anda merasa pusing?", "dizziness"),
        ("Apakah Anda mengalami insomnia?", "insomnia"),
        ("Apakah Anda memiliki gerakan involunter abnormal?", "abnormal involuntary movements"),
        ("Apakah Anda merasakan ketegangan di dada?", "chest tightness"),
        ("Apakah Anda merasakan detak jantung yang cepat atau tidak teratur?", "palpitations"),
        ("Apakah detak jantung Anda tidak teratur?", "irregular heartbeat"),
        ("Apakah Anda bernapas dengan cepat?", "breathing fast"),
        ("Apakah Anda mengalami kesulitan berbicara?", "difficulty speaking"),
        ("Apakah Anda menyalahgunakan alkohol?", "abusing alcohol"),
        ("Apakah Anda merasa perilaku Anda menjadi lebih agresif?", "hostile behavior"),
        ("Apakah Anda menyalahgunakan obat-obatan?", "drug abuse"),
        ("Apakah Anda merasa sakit?", "feeling ill"),
        ("Apakah Anda mengalami pendarahan antar periode menstruasi?", "intermenstrual bleeding"),
        ("Apakah Anda mengalami jerawat atau bopeng?", "acne or pimples"),
        ("Apakah Anda merasa nyeri saat hamil?", "pain during pregnancy"),
        ("Apakah Anda mengalami penambahan berat badan?", "weight gain"),
        ("Apakah Anda mengalami kesulitan makan?", "difficulty eating"),
        ("Apakah Anda mengalami penurunan nafsu makan?", "decreased appetite"),
        ("Apakah Anda merasa mudah marah?", "excessive anger"),
        ("Apakah Anda mengalami masalah selama kehamilan?", "problems during pregnancy"),
        ("Apakah Anda mengalami delusi atau halusinasi?", "delusions or hallucinations"),
        ("Apakah Anda mengalami masalah temperamen?", "temper problems"),
        ("Apakah Anda memiliki ketakutan atau fobia?", "fears and phobias"),
        ("Apakah Anda merasa memiliki harga diri rendah?", "low self-esteem")
    ]

    # Tampung jawaban user
    user_input = []

    for question, feature_name in questions:
        answer = st.radio(question, ["Tidak", "Ya"], key=feature_name)
        user_input.append(1 if answer == "Ya" else 0)

    # Nama kolom sesuai training
    column_name = [feature_name for _, feature_name in questions]

    # Fungsi prediksi
    def prediksi(input_data):
        input_df = pd.DataFrame([input_data], columns=column_name)
        prediction = model.predict(input_df)
        return prediction[0]

    # Tombol Prediksi
    if st.button("Prediksi"):
        hasil = prediksi(user_input)
        
        # Format hasil prediksi
        if hasil.lower() == "other":
            hasil_display = f"""
            <div style="background-color:rgba(38, 39, 48, 0.8); border-radius:0.5rem; padding:1rem; margin:1rem 0; border-left:4px solid #9AD8E1;">
                <h3 style="color:#9AD8E1; margin-top:0;">🟢 Hasil Screening</h3>
                <p>Berdasarkan jawaban Anda:</p>
                <p><b>Anda tidak terdeteksi mengalami gangguan kesehatan mental berikut:</b></p>
                <ul>
                    <li>Eating disorder</li>
                    <li>Marijuana abuse</li>
                    <li>Panic disorder</li>
                    <li>Postpartum depression</li>
                    <li>Substance-related mental disorder</li>
                </ul>
                <p><i>Catatan:</i> Aplikasi ini memiliki keterbatasan dalam mendeteksi berbagai jenis penyakit.</p>
            </div>
            """
        else:
            hasil_display = f"""
            <div style="background-color:rgba(38, 39, 48, 0.8); border-radius:0.5rem; padding:1rem; margin:1rem 0; border-left:4px solid #FF4B4B;">
                <h3 style="color:#FF4B4B; margin-top:0;">🔴 Hasil Screening</h3>
                <p>Berdasarkan jawaban Anda:</p>
                <p><b>Kemungkinan Anda mengalami: {hasil}</b></p>
                <p>Hasil ini merupakan prediksi awal.</p>
            </div>
            """
        
        st.markdown(hasil_display, unsafe_allow_html=True)
        
        # Buat PDF
        pdf = create_pdf(hasil, user_input, questions)
        
        # Tampilkan tombol download
        st.markdown("### Download Hasil Screening")
        st.markdown(get_pdf_download_link(pdf, "Hasil_Screening.pdf"), 
                    unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <hr>
        <footer style="text-align: center; color: grey; font-size: 14px;">
            <p>Developed with ❤️ by Team</p>
        </footer>
    """, unsafe_allow_html=True)

# Untuk menjalankan
if __name__ == "__main__":
    screening()
