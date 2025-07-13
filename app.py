import streamlit as st
import json
import os

DATA_FILE = "snippets.json"


# Load snippets from file
def load_snippets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


# Save snippets to file
def save_snippet(snippets):
    with open(DATA_FILE, "w") as f:
        json.dump(snippets, f, indent=4)


# Main UI
st.set_page_config(page_title="CodeShelf", layout="wide")
st.title("📚 CodeShelf - Your Personal Code Cheatsheet")

# Load existing data
snippets = load_snippets()

# Sidebar to add new snippet
with st.sidebar:
    st.header("➕ Add New Snippet")
    title = st.text_input("Title")
    language = st.selectbox("Language", ["Python", "JavaScript", "SQL", "Markdown", "Other"])
    category = st.text_input("Category (e.g. Pandas, Regex, API)")
    code = st.text_area("Code Snippet", height=200)
    tags = st.text_input("Tags (comma-separated)")

    if st.button("Save Snippet"):
        if title and code:
            new_snippet = {
                "title": title,
                "language": language,
                "category": category,
                "code": code,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()]
            }
            snippets.append(new_snippet)
            save_snippet(snippets)
            st.success("✅ Snippet Saved!")
        else:
            st.warning("⚠️ Title and Code are required.")

# Search functionality
search_query = st.text_input("🔍 Search Snippets", "")

# Filter and show snippets
filtered_snippets = [
    s for s in snippets if
    search_query.lower() in s["title"].lower() or
    search_query.lower() in s["category"].lower() or
    any(search_query.lower() in tag.lower() for tag in s["tags"])
]

if filtered_snippets:
    for s in filtered_snippets:
        with st.expander(f"📌 {s['title']} ({s['language']})"):
            st.markdown(f"**Category:** `{s['category']}`")
            st.markdown(f"**Tags:** {', '.join(s['tags'])}")
            st.code(s['code'], language=s['language'].lower())
else:
    st.info("🙁 No snippets found. Try adding or changing your search.")
