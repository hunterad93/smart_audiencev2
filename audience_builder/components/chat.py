import streamlit as st
from services.openai_service import OpenAIService
from services.state_service import StateService
import json
import logging

logger = logging.getLogger(__name__)

def render_group_chat(openai_service: OpenAIService):
    if not st.session_state.active_group_id:
        st.info("Select a data group from the sidebar or create a new one")
        return
    
    group_id = st.session_state.active_group_id
    group = st.session_state.audience["data_groups"][group_id]
    thread_id = st.session_state.group_threads[group_id]
    
    # Display current state using the same display function
    if group.get('segments'):
        display_group_definition(f"```json\n{json.dumps(group, indent=2)}\n```", group)
    
    # Chat input and message handling
    if prompt := st.chat_input("Describe your data group..."):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your input..."):
                if not group["assistant_id"]:
                    # First message - classify and potentially create demographic thread
                    classification, segments = openai_service.classify_data_group(prompt)
                    
                    if segments:
                        # Create new thread with demographic segments
                        new_thread_id = openai_service.create_demographic_thread(prompt, segments)
                        st.session_state.group_threads[group_id] = new_thread_id
                        thread_id = new_thread_id
                        group.update(segments)
                        
                        # Set assistant but don't send message - thread already has initial messages
                        StateService.set_group_assistant(group_id, openai_service.demographic_assistant_id)
                        display_group_definition(f"```json\n{json.dumps(segments, indent=2)}\n```", group)
                        st.rerun()
                    else:
                        # Non-demographic flow - set assistant and send first message
                        assistant_id = openai_service.get_assistant_for_classification(classification)
                        StateService.set_group_assistant(group_id, assistant_id)
                        
                        response = openai_service.send_assistant_message(
                            thread_id=thread_id,
                            content=prompt,
                            assistant_id=assistant_id
                        )
                        if response:
                            display_group_definition(response, group)
                            st.rerun()
                else:
                    # Follow-up message - always use assistant
                    response = openai_service.send_assistant_message(
                        thread_id=thread_id,
                        content=prompt,
                        assistant_id=group["assistant_id"]
                    )
                    if response:
                        display_group_definition(response, group)
                        st.rerun()

def classify_and_select_assistant(prompt: str, openai_service: OpenAIService) -> str:
    try:
        classification, segments = openai_service.classify_data_group(prompt)
        logger.info(f"Classification: {classification.model_dump()}")
        
        if segments:
            # Create new thread with context
            thread_id = openai_service.create_demographic_thread(prompt, segments)
            # Update state with new thread
            st.session_state.group_threads[st.session_state.active_group_id] = thread_id
            # Update group with segments
            group = st.session_state.audience["data_groups"][st.session_state.active_group_id]
            group.update(segments)
            return openai_service.demographic_assistant_id
            
        return openai_service.get_assistant_for_classification(classification)
    except Exception as e:
        logger.error(f"Error in classification: {str(e)}")
        return openai_service.general_assistant_id

def display_group_definition(response_text: str, group: dict) -> None:
    try:
        if response_text.startswith('```json'):
            response_text = response_text.split('```json\n')[1].split('```')[0]
        
        group_data = json.loads(response_text)
        group.update(group_data)
        st.session_state.audience["data_groups"][st.session_state.active_group_id].update(group_data)
        
        # Compact display
        st.markdown(f"### {group_data['group_name']}")
        for i, segment in enumerate(group_data['segments']):
            st.markdown(
                f"**{segment['full_path']}**\n\n"
                f"{segment['description']}"
            )
            
    except Exception as e:
        logger.error(f"Error parsing response: {str(e)}")
        st.error(f"Error parsing response: {str(e)}")
        st.code(response_text)