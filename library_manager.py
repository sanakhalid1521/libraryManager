import streamlit as st
import json

# Apply Custom Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: Arial, sans-serif;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        padding: 8px 16px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stTextInput, .stNumberInput {
        border-radius: 10px;
        padding: 10px;
    }
    .stSelectbox > div {
        border-radius: 10px;
    }
    .scrollable-container {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 10px;
        background-color: pink;
    }

    .view-library-container h2, 
    .view-library-container p {
        color: black;
        background-color: pink;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class PersonalLibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status
        }
        self.library.append(book)
        self.save_library()

    def remove_book(self, title):
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        self.save_library()

    def search_books(self, keyword):
        return [book for book in self.library if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]

    def display_statistics(self):
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, percentage_read

manager = PersonalLibraryManager()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox(
    "Menu", 
    ["➕ Add Book", "❌ Remove Book", "🔍 Search Books", "📚 View Library", "📊 Statistics"],
    format_func=lambda x: f"{x}"
)

# ➕ Add Book Section
if menu == "➕ Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("📘 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=2011, max_value=2025, step=1)
    genre = st.text_input("📂 Genre")
    read_status = st.checkbox("✅ Have you read this book?")
    if st.button("➕ Add Book"):
        manager.add_book(title, author, year, genre, read_status)
        st.success("✅ Book added successfully!")

# ❌ Remove Book Section
elif menu == "❌ Remove Book":
    st.subheader("🗑 Remove a Book")
    title = st.text_input("📕 Enter the title of the book to remove")
    if st.button("🗑 Remove Book"):
        manager.remove_book(title)
        st.success("✅ Book removed successfully!")

# 🔍 Search Books Section
elif menu == "🔍 Search Books":
    st.subheader("🔎 Search for a Book")
    keyword = st.text_input("Enter title or author")
    if st.button("🔎 Search"):
        results = manager.search_books(keyword)
        if results:
            st.markdown("**Matching Books:**")
            for book in results:
                st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📖 Unread'}")
        else:
            st.warning("⚠ No books found.")

# 📚 View Library Section (Updated Layout)
elif menu == "📚 View Library":
    st.subheader("📚 Your Library")
    st.markdown('<div class="view-library-container">', unsafe_allow_html=True)

    if manager.library:
        for book in manager.library:
            st.markdown("---")  # Line separator
            st.markdown(f"<h2>📘 {book['title']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p><b>✍️ Author:</b> {book['author']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>📅 Publication Year:</b> {book['year']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>📂 Genre:</b> {book['genre']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>📚 Status:</b> {'✅ Read' if book['read'] else '📖 Unread'}</p>", unsafe_allow_html=True)
            st.markdown("---")  # Line separator
    else:
        st.warning("⚠ Your library is empty.")

    st.markdown('</div>', unsafe_allow_html=True)

# 📊 Statistics Section
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = manager.display_statistics()
    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"📖 **Percentage Read:** {percentage_read:.2f}%")
