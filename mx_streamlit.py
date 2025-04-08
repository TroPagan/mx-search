
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Modulex Sign Family Search Tool (SQL Edition)", layout="wide")

# Load data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("modulex.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df.to_dict(orient="records")

data = load_data()

# Tabs for Search and All Items
tab1, tab2 = st.tabs(["🔍 Search", "📋 All Products"])

with tab1:
    st.title("📘 Modulex Sign Family Search Tool (SQL Edition)")
    st.write("Search Modulex product codes by size, family, and location from a live database.")

    size_query = st.text_input("Search size (partial OK)", "")
    families = ["Any"] + sorted(set(d["family"] for d in data))
    locations = ["Any", "Interior", "Exterior"]

    family_filter = st.selectbox("Filter by Family", families)
    location_filter = st.selectbox("Filter by Location", locations)

    if st.button("Search"):
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

with tab2:
    st.title("📋 All Modulex Products")
    st.write("Below is the full list of available products in the database.")
    df_all = pd.DataFrame(data)
    st.dataframe(df_all, use_container_width=True)
