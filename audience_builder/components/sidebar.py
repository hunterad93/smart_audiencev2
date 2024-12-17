import streamlit as st
from services.state_service import StateService
from services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

def render_sidebar(state_service: StateService, openai_service: OpenAIService):
    with st.sidebar:
        st.title("Group Management")
        
        if st.button("Create New Group", use_container_width=True):
            new_group_id = state_service.create_group(openai_service)
            st.session_state.active_group_id = new_group_id
            st.rerun()
        
        render_group_list()

def render_group_list():
    for group_id, group in st.session_state.audience["data_groups"].items():
        with st.container():
            if st.button(
                group["group_name"],
                key=f"select_{group_id}",
                use_container_width=True
            ):
                st.session_state.active_group_id = group_id
                st.rerun()
            
            render_group_controls(group_id, group)

def render_group_controls(group_id, group):
    col1, col2 = st.columns(2)
    with col1:
        current_status = group["status"]
        toggle_key = f"status_toggle_{group_id}"
        
        # Initialize session state only once when group is created
        if toggle_key not in st.session_state:
            st.session_state[toggle_key] = current_status == "include"
            logger.debug(f"Initializing toggle state for {group_id}: {st.session_state[toggle_key]}")
        
        # Don't pass a default value, rely only on session state
        status = st.toggle(
            "Include",
            key=toggle_key,
            on_change=lambda: handle_status_change(group_id, toggle_key)
        )
            
    with col2:
        if st.button(
            "Delete",
            key=f"delete_{group_id}",
            use_container_width=True
        ):
            handle_group_deletion(group_id)

def handle_group_deletion(group_id):
    del st.session_state.audience["data_groups"][group_id]
    del st.session_state.group_threads[group_id]
    if st.session_state.active_group_id == group_id:
        st.session_state.active_group_id = None
    st.rerun()

def handle_status_change(group_id: str, toggle_key: str):
    new_status = "include" if st.session_state[toggle_key] else "exclude"
    current_status = st.session_state.audience["data_groups"][group_id]["status"]
    
    logger.info(f"Status change triggered for {group_id}")
    logger.info(f"Toggle state: {st.session_state[toggle_key]}")
    logger.info(f"Current status: {current_status}, New status: {new_status}")
    
    if new_status != current_status:
        StateService.update_group_status(group_id, new_status)