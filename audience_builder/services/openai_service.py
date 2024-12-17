from typing import List, Dict, Type, Optional
from pydantic import BaseModel
import logging
from openai import OpenAI
import streamlit as st
import json
from models.classification import GroupClassification, AudienceType
from services.segment_service import SegmentService
from settings.prompts import CLASSIFICATION_PROMPT

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        self.temperature = 1
        self.timeout = 30
        self.classification_model = "gpt-4o"
        
        # Assistant IDs
        self.demographic_assistant_id = "asst_bvWOWqZ7myFeBsmuEQMdRcLs"
        self.general_assistant_id = "asst_KFSoUugvWdugdeLCrpNYlStD"
        logger.info("OpenAIService initialized with models and assistants configured")
    
    def get_structured_completion(
        self, 
        model: str,
        messages: List[Dict[str, str]],
        response_format: Type[BaseModel],
        temperature: Optional[float] = None,
    ) -> BaseModel:
        logger.debug(f"Requesting structured completion from {model}")
        logger.debug(f"Messages: {messages}")
        logger.debug(f"Response format: {response_format}")
        logger.debug(f"Temperature: {temperature or self.temperature}")
        
        try:
            parsed_response = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format,
                temperature=temperature or self.temperature,
                timeout=self.timeout,
                seed=42
            )
            logger.info(f"Structured completion successful")
            logger.debug(f"Raw response: {parsed_response}")
            return parsed_response.choices[0].message.parsed
        except Exception as e:
            logger.error(f"Error in API call to {model}: {str(e)}", exc_info=True)
            raise

    def create_thread(self) -> str:
        logger.debug("Creating new thread")
        try:
            thread_id = self.client.beta.threads.create().id
            logger.info(f"Created thread: {thread_id}")
            return thread_id
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}", exc_info=True)
            raise

    def get_assistant_messages(self, thread_id: str):
        logger.debug(f"Fetching messages for thread: {thread_id}")
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            formatted_messages = [{"role": m.role, "content": m.content[0].text.value} for m in messages.data]
            logger.debug(f"Retrieved {len(formatted_messages)} messages")
            logger.debug(f"Messages: {formatted_messages}")
            return formatted_messages
        except Exception as e:
            logger.error(f"Error fetching messages for thread {thread_id}: {str(e)}", exc_info=True)
            raise

    def send_assistant_message(
        self, 
        thread_id: str, 
        content: str,
        assistant_id: str
    ) -> Optional[str]:
        logger.info(f"Sending message to assistant {assistant_id} in thread {thread_id}")
        logger.debug(f"Message content: {content}")
        
        try:
            # Send the message
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
            logger.debug(f"Message created: {message}")
            
            # Run the assistant
            logger.debug(f"Starting assistant run")
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            
            # Wait for completion
            logger.debug(f"Waiting for run {run.id} to complete")
            while run.status in ["queued", "in_progress"]:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                logger.debug(f"Run status: {run.status}")
            
            if run.status == "completed":
                logger.info(f"Run completed successfully")
                messages = self.get_assistant_messages(thread_id)
                latest_message = messages[0]["content"]
                logger.debug(f"Latest message: {latest_message}")
                return latest_message
            else:
                logger.error(f"Assistant run failed with status: {run.status}")
                logger.error(f"Run details: {run}")
                return None
                
        except Exception as e:
            logger.error(f"Error in assistant communication: {str(e)}", exc_info=True)
            raise 

    def classify_data_group(self, description: str) -> GroupClassification:
        logger.info("Starting data group classification")
        logger.debug(f"Input description: {description}")
        
        messages = [
            {"role": "system", "content": CLASSIFICATION_PROMPT},
            {"role": "user", "content": description}
        ]
        
        try:
            classification = self.get_structured_completion(
                model=self.classification_model,
                messages=messages,
                response_format=GroupClassification,
                temperature=0.3
            )
            
            # If it's a demographic classification, get segments immediately
            if classification.audience_type in [AudienceType.AGE_RANGE, AudienceType.GENDER]:
                segment_service = SegmentService()
                segments = segment_service.get_segments_for_classification(classification)
                if segments:
                    logger.info(f"Found matching segments: {segments}")
                    return classification, segments
                
            logger.info(f"Classification complete: {classification}")
            return classification, None
            
        except Exception as e:
            logger.error(f"Error in classification: {str(e)}", exc_info=True)
            return GroupClassification(
                audience_type=AudienceType.OTHER,
                split_recommended=False
            ), None
    
    def get_assistant_for_classification(self, classification: GroupClassification) -> str:
        logger.debug(f"Selecting assistant for classification: {classification}")
        assistant_id = (
            self.demographic_assistant_id 
            if classification.audience_type in [AudienceType.AGE_RANGE, AudienceType.GENDER]
            else self.general_assistant_id
        )
        logger.info(f"Selected assistant: {assistant_id}")
        return assistant_id
    
    def create_demographic_thread(self, user_prompt: str, segments: dict) -> str:
        try:
            # Format response as JSON matching assistant style
            assistant_response = {
                "group_name": segments["group_name"],
                "segments": segments["segments"]
            }
            
            # Create thread with initial conversation
            thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                    {
                        "role": "assistant",
                        "content": f"```json\n{json.dumps(assistant_response, indent=2)}\n```"
                    }
                ]
            )
            logger.info(f"Created demographic thread with initial messages: {thread.id}")
            return thread.id
        except Exception as e:
            logger.error(f"Error creating demographic thread: {str(e)}")
            raise