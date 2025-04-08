import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Modulex Search", layout="wide")

st.title("📘 Modulex Sign Family Search Tool")
st.write("Upload your PDF, parse it, and search signs by size, family, or location.")

def parse_pdf(file):
    families = ["Compass", "Pacific", "Messenger", "Macer", "Basic", "Via", "Infinity", "Breeze", "Sirius", "Safety Signs", "Paperflex"]
    section_location_map = {"Exterior": "Exterior", "Interior": "Interior"}

    entries = []
    current_family = None
    current_location = None

    doc = fitz.open(stream=file.read(), filetype="pdf")

    for page in doc:
        text = page.get_text()
        lines = text.split("\\n")

        for line in lines:
            for fam in families:
                if fam in line:
                    current_family = fam
                    for key in section_location_map:
                        if key in line:
                            current_location = section_location_map[key]

            matches = re.findall(r'([a-z]{1,3}: \\d{6}--)[^\\d]*(\\d{2,4} x \\d{2,4} mm)', line)
            for code, size in matches:
                entries.append({
                    'code': code.strip(),
                    'size': size.strip(),
                    'family': current_family or 'Unknown',
                    'location': current_location or 'Unknown'
                })
    return entries


uploaded_file = st.file_uploader("Upload Modulex PDF", type="pdf")

if uploaded_file:
    st.info("Parsing PDF... please wait ⏳")
    data = parse_pdf(uploaded_file)
    st.success(f"Parsed {len(data)} entries 🎉")

    size_query = st.text_input("Search size (partial OK)", "")
    families = ["Any"] + sorted(set(d["family"] for d in data))
    locations = ["Any", "Interior", "Exterior"]

    family_filter = st.selectbox("Filter by Family", families)
    location_filter = st.selectbox("Filter by Location", locations)

    filtered = []
    for item in data:
        if size_query.lower() not in item["size"].lower():
            continue
        if family_filter != "Any" and item["family"] != family_filter:
            continue
        if location_filter != "Any" and item["location"] != location_filter:
            continue
        filtered.append(item)

    st.markdown(f"### 🔍 Results: {len(filtered)} match{'es' if len(filtered)!=1 else ''}")
    for item in filtered:
        st.write(f"**{item['code']}** — {item['size']} — {item['family']} — {item['location']}")
