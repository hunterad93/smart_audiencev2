import streamlit as st
from services.state_service import StateService
from services.openai_service import OpenAIService
from components.chat import display_group_definition  # Import the display function
import logging

logger = logging.getLogger(__name__)

def render_sidebar(state_service: StateService, openai_service: OpenAIService):
    logger.debug(f"Session state at start: {st.session_state}")
    
    with st.sidebar:
        st.title("Audience Settings")
        
        # Initialize KPI if not already set
        if "selected_kpi" not in st.session_state:
            st.session_state.selected_kpi = None
        
        # Advertiser ID input - show this first
        advertiser_id = st.text_input(
            "Advertiser ID",
            key="advertiser_id",
            help="Enter the TradeDesk Advertiser ID",
            placeholder="e.g., 8vad7yi"
        )
        
        st.divider()
        
        # Debug log for KPI state
        logger.debug(f"Selected KPI: {st.session_state.get('selected_kpi')}")
        
        # Show KPI selector only if no KPI has been selected
        if st.session_state.selected_kpi is None:
            kpi_options = list(openai_service.conversion_kpis | 
                             openai_service.ctr_kpis | 
                             openai_service.viewability_kpis)
            kpi_options.sort()
            
            selected_kpi = st.selectbox(
                "First, choose your Optimization Goal",
                options=kpi_options,
                key="kpi_selector",  # Different key from session state
                index=None,
                help="Choose the KPI metric you want to optimize for this audience"
            )
            
            if selected_kpi:
                st.session_state.selected_kpi = selected_kpi  # Manually update session state
                provider_name = "Data Alliance" if selected_kpi in openai_service.conversion_kpis else "Audience Acuity"
                st.info(f"Using {provider_name} for {selected_kpi} optimization")
                st.rerun()
        else:
            # Show the selected KPI as info
            provider_name = "Data Alliance" if st.session_state.selected_kpi in openai_service.conversion_kpis else "Audience Acuity"
            st.info(f"Optimizing for: {st.session_state.selected_kpi} with {provider_name}")
            
            st.divider()
            
            # Rest of the sidebar UI (only shown after KPI selection)
            audience_description = st.text_area(
                "Audience Description",
                placeholder="Describe your target audience...",
                help="Describe who you want to target. For example: 'female millennials interested in sustainable fashion'",
                key="audience_description",
                on_change=None  # Prevent automatic rerun
            )
            
            # Separate button for submitting description
            if audience_description:
                if st.button("Structure Audience", use_container_width=True):
                    with st.spinner("Analyzing audience description..."):
                        try:
                            # Clear existing groups and threads
                            st.session_state.audience["data_groups"] = {}
                            st.session_state.group_threads = {}
                            st.session_state.active_group_id = None
                            
                            # Get new structure
                            structured_groups = openai_service.structure_audience(audience_description)
                            st.session_state.audience["audience_name"] = structured_groups.audience_name
                            st.rerun()
                        except Exception as e:
                            logger.error(f"Error structuring audience: {str(e)}")
                            st.error("Error creating audience structure. Please try again.")
            
            st.title("Group Management")
            
            # Only show create group button if we have a KPI selected
            if st.button("Create New Group", 
                        use_container_width=True, 
                        disabled=not st.session_state.selected_kpi):
                new_group_id = state_service.create_group(openai_service)
                st.session_state.active_group_id = new_group_id
                st.rerun()
            
            render_group_list(openai_service)
            
            # After all group management UI, add Push button
            st.divider()
            
            # Enable push button only if we have advertiser ID and at least one group
            can_push = (st.session_state.get('advertiser_id') and 
                       st.session_state.audience.get('data_groups'))
            
            if st.button("Push to TradeDesk", 
                        use_container_width=True,
                        disabled=not can_push):
                # TODO: Implement push functionality
                pass
            
            if not can_push:
                if not st.session_state.get('advertiser_id'):
                    st.caption("⚠️ Enter Advertiser ID to push")
                elif not st.session_state.audience.get('data_groups'):
                    st.caption("⚠️ Create at least one group to push")

def render_group_list(openai_service: OpenAIService):
    for group_id, group in st.session_state.audience["data_groups"].items():
        # Simple button with group name in sidebar
        if st.button(group["group_name"], key=f"group_button_{group_id}"):
            st.session_state.active_group_id = group_id
            
            # Get thread ID for this group
            thread_id = st.session_state.group_threads[group_id]
            
            try:
                # Fetch messages from OpenAI
                messages = openai_service.get_assistant_messages(thread_id)
                
                # Find the most recent assistant message
                assistant_messages = [m for m in messages if m["role"] == "assistant"]
                if assistant_messages:
                    last_message = assistant_messages[-1]["content"]
                    # Update the group with the segments from the last message
                    display_group_definition(last_message, group)
            except Exception as e:
                logger.error(f"Error fetching initial group state: {str(e)}")
            
            st.rerun()
        
        # Only show controls in sidebar if this is the active group
        if st.session_state.active_group_id == group_id:
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