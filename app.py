import streamlit as st
from utils.helpers import save_uploaded_file
from src.detector import detect_plagiarism

st.set_page_config(
    page_title="Plagiarism Detector",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
/* Global */
.block-container {
    max-width: 1180px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
}

/* Hero */
.hero-box {
    background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 100%);
    border: 1px solid #e5ecf6;
    border-radius: 28px;
    padding: 30px 34px;
    box-shadow: 0 12px 30px rgba(31, 41, 55, 0.07);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #111827;
    line-height: 1.1;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #4b5563;
    line-height: 1.7;
    max-width: 850px;
}

/* Cards */
.soft-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid #e8edf5;
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 10px 24px rgba(17, 24, 39, 0.06);
    margin-bottom: 18px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 750;
    color: #111827;
    margin-bottom: 14px;
}

/* Native Streamlit metric styling */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #e6edf8;
    border-radius: 22px;
    padding: 16px 18px;
    box-shadow: 0 8px 18px rgba(17, 24, 39, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 2.2rem;
    font-weight: 900;
}
            
div[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid #dbeafe !important;
    border-radius: 20px;
    padding: 18px !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08) !important;
}

/* Badge */
.result-badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 12px;
}

.badge-low {
    background: #e8fff2;
    color: #0f7a42;
    border: 1px solid #b7f0cd;
}

.badge-medium {
    background: #fff7e8;
    color: #a16207;
    border: 1px solid #fde0a3;
}

.badge-high {
    background: #ffecec;
    color: #b42318;
    border: 1px solid #fecaca;
}

/* Uploader */
div[data-testid="stFileUploader"] {
    background: #fbfdff;
    border: 1px dashed #cdd9ea;
    border-radius: 18px;
    padding: 10px 12px 4px 12px;
}

/* Slider spacing */
div[data-testid="stSlider"] {
    padding-top: 8px;
}

/* Button */
div[data-testid="stButton"] > button {
    width: 100%;
    height: 50px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    color: white;
    font-size: 1rem;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(59, 130, 246, 0.22);
    transition: 0.2s ease;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 28px rgba(59, 130, 246, 0.28);
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    overflow: hidden;
}

/* Minor text */
.helper-text {
    color: #6b7280;
    font-size: 0.92rem;
    margin-top: -4px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def get_result_badge(percent):
    if percent >= 70:
        return "High Similarity Detected", "badge-high"
    elif percent >= 35:
        return "Moderate Similarity Detected", "badge-medium"
    return "Low Similarity Detected", "badge-low"

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">AI-Powered Multiple Document Plagiarism Detection System</div>
    <div class="hero-subtitle">
        Compare two documents and detect copied or semantically similar content using a hybrid approach
        based on lexical similarity and sentence embeddings. Built for fast analysis, clear reporting,
        and an elegant presentation experience.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INPUT AREA
# -----------------------------
st.markdown('<div class="soft-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Upload and Compare Documents</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Supported formats: TXT, PDF, DOCX</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    file1 = st.file_uploader("Upload File 1", type=["txt", "pdf", "docx"], key="file1")

with col2:
    file2 = st.file_uploader("Upload File 2", type=["txt", "pdf", "docx"], key="file2")

threshold = st.slider("Detection Threshold", 0.30, 0.95, 0.78, 0.01)
compare_btn = st.button("Compare Files")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# ANALYSIS
# -----------------------------
if compare_btn:
    if not file1 or not file2:
        st.warning("Please upload both files before starting the comparison.")
    else:
        try:
            path1 = save_uploaded_file(file1)
            path2 = save_uploaded_file(file2)

            with st.spinner("Analyzing similarity between the uploaded documents..."):
                report, percent = detect_plagiarism(path1, path2, threshold=threshold)

            suspicious_count = int((report["Suspicious"] == "Yes").sum()) if "Suspicious" in report.columns else 0
            top_score = float(report["Final Score"].max()) if not report.empty else 0.0
            badge_text, badge_class = get_result_badge(percent)

            st.markdown('<div class="section-title">Analysis Summary</div>', unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3, gap="large")

            with m1:
                st.metric("Plagiarism Percentage", f"{percent}%")

            with m2:
                st.metric("Suspicious Segment Matches", suspicious_count)

            with m3:
                st.metric("Top Similarity Score", f"{top_score:.3f}")

            st.markdown(
                f'<div class="result-badge {badge_class}">{badge_text}</div>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Top Matching Segments</div>', unsafe_allow_html=True)

            top_matches = report.head(8)

            for idx, row in top_matches.iterrows():
                title = (
                    f"Match {idx + 1}  •  Score: {row['Final Score']}  •  "
                    f"File 1 Chunk {row['File1 Chunk No']} ↔ File 2 Chunk {row['File2 Chunk No']}"
                )
                with st.expander(title):
                    a, b = st.columns(2, gap="large")

                    with a:
                        st.markdown("**File 1 Segment**")
                        st.write(row["File1 Chunk"])

                    with b:
                        st.markdown("**File 2 Segment**")
                        st.write(row["File2 Chunk"])

                    s1, s2, s3 = st.columns(3, gap="large")
                    with s1:
                        st.metric("TF-IDF", row["TF-IDF Score"])
                    with s2:
                        st.metric("Jaccard", row["Jaccard Score"])
                    with s3:
                        st.metric("Embedding", row["Embedding Score"])

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Detailed Comparison Report</div>', unsafe_allow_html=True)
            st.dataframe(report, use_container_width=True)

            csv_data = report.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV Report",
                data=csv_data,
                file_name="plagiarism_report.csv",
                mime="text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")