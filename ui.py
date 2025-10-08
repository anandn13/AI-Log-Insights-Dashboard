import streamlit as st


def render_result(doc: dict):
    st.markdown(f"**Level**: {doc.get('level','')}  |  **Source**: {doc.get('source','')}")
    st.code(doc.get('message',''))
    meta = doc.get('meta')
    if meta:
        with st.expander('Meta'):
            st.json(meta)


