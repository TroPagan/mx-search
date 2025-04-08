
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Modulex Sign Family Search Tool", layout="wide")
st.title("📘 Modulex Sign Family Search Tool (SQL Edition)")
st.write("Search Modulex product codes by size, family, and location from a live database.")

@st.cache_data
def load_data():
    conn = sqlite3.connect("modulex.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df.to_dict(orient="records")

data = load_data()

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
