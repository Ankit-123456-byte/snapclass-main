import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    st.markdown(f"""
<div style="
    background: white;
    border-radius: 16px;
    padding: 20px 22px 4px 22px;
    margin-bottom: 16px;
    border-left: 5px solid #5865F2;
    box-shadow: 0 2px 12px rgba(88,101,242,0.10);
">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
        <div>
            <div style="font-family:'Outfit',sans-serif; font-size:1.15rem; font-weight:700; color:#1a1a2e; margin-bottom:2px;">{name}</div>
            <div style="font-family:'Outfit',sans-serif; font-size:0.82rem; color:#6b7280;">Section: {section}</div>
        </div>
        <div style="background:#E0E3FF; color:#5865F2; padding:5px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; white-space:nowrap; margin-left:10px;">
            {code}
        </div>
    </div>
""", unsafe_allow_html=True)

    if stats:
        stat_cols = st.columns(len(stats))
        for i, (icon, label, value) in enumerate(stats):
            with stat_cols[i]:
                st.markdown(f"""
<div style="background:#F5F6FF; border-radius:10px; padding:10px 8px; text-align:center; margin-bottom:10px;">
    <div style="font-size:1.2rem;">{icon}</div>
    <div style="font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700; color:#1a1a2e;">{value}</div>
    <div style="font-family:'Outfit',sans-serif; font-size:0.75rem; color:#6b7280;">{label}</div>
</div>
""", unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

    st.markdown("</div>", unsafe_allow_html=True)
