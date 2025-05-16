import streamlit as st
import pandas as pd
import pickle

# --- Load Model Secara Efisien menggunakan cache_resource ---
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Panggil model
model = load_model()

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
        return prediction[0]  # ambil string hasil prediksi

    # Tombol Prediksi
    if st.button("Prediksi"):
        hasil = prediksi(user_input)
        
        # Format hasil prediksi yang lebih informatif dengan styling yang bekerja di dark mode
        if hasil.lower() == "other":
            st.markdown("""
            <style>
                .custom-result {
                    background-color: rgba(38, 39, 48, 0.8);
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin: 1rem 0;
                    border-left: 4px solid #9AD8E1;
                }
                .custom-result h3 {
                    color: #9AD8E1;
                    margin-top: 0;
                }
                .custom-result ul {
                    margin-bottom: 0.5rem;
                }
            </style>
            """, unsafe_allow_html=True)
            
            hasil_display = f"""
            <div class="custom-result">
                <h3>🟢 Hasil Screening</h3>
                <p>Berdasarkan jawaban Anda:</p>
                <p><b>Anda tidak terdeteksi mengalami gangguan kesehatan mental berikut:</b></p>
                <ul>
                    <li>Eating disorder</li>
                    <li>Marijuana abuse</li>
                    <li>Panic disorder</li>
                    <li>Postpartum depression</li>
                    <li>Substance-related mental disorder</li>
                </ul>
                <p><i>Catatan:</i> Aplikasi ini memiliki keterbatasan dalam mendeteksi berbagai jenis penyakit. 
                Jika Anda masih merasa tidak sehat, kami sarankan untuk berkonsultasi dengan tenaga kesehatan profesional.</p>
            </div>
            """
        else:
            st.markdown("""
            <style>
                .custom-result {
                    background-color: rgba(38, 39, 48, 0.8);
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin: 1rem 0;
                    border-left: 4px solid #FF4B4B;
                }
                .custom-result h3 {
                    color: #FF4B4B;
                    margin-top: 0;
                }
            </style>
            """, unsafe_allow_html=True)
            
            hasil_display = f"""
            <div class="custom-result">
                <h3>🔴 Hasil Screening</h3>
                <p>Berdasarkan jawaban Anda:</p>
                <p><b>Kemungkinan Anda mengalami: {hasil}</b></p>
                <p>Hasil ini merupakan prediksi awal. Untuk diagnosis yang akurat, silakan konsultasikan dengan tenaga kesehatan profesional.</p>
            </div>
            """
        
        st.markdown(hasil_display, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <hr>
        <footer style="text-align: center; color: grey; font-size: 14px;">
            <p>Developed with ❤️ by Team</p>
        </footer>
    """, unsafe_allow_html=True)
