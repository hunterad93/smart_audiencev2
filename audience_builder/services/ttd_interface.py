import logging
from typing import Dict, Any, List, Tuple, Optional
from ttd_sdk import TTDClient
from ttd_sdk.models.base import ApiObject
import streamlit as st

logger = logging.getLogger(__name__)

class TTDInterfaceService:
    # Set a fixed advertiser ID for safety
    FIXED_ADVERTISER_ID = "8vad7yi"
    
    def __init__(self, sandbox: bool = True):
        self.advertiser_id = self.FIXED_ADVERTISER_ID
        self.client = TTDClient(
            sandbox=sandbox,
            log_level="DEBUG"
        )

    def create_data_group(self, group_data: Dict[str, Any]) -> str:
        """Create a data group and return its ID"""
        try:
            third_party_data_ids = [
                segment["id"] 
                for segment in group_data["segments"]
                if "id" in segment
            ]
            
            if not third_party_data_ids:
                raise ValueError("No valid third party data IDs found in segments")
            
            data_group = ApiObject(
                AdvertiserId=self.advertiser_id,
                DataGroupName=group_data["group_name"],
                ThirdPartyDataIds=third_party_data_ids,
                IsSharable=False,
                SkipUnauthorizedThirdPartyData=True
            )
            
            logger.debug(f"Creating data group with IDs: {third_party_data_ids}")
            response = self.client.data_groups.create(data_group)
            return response.DataGroupId
            
        except Exception as e:
            logger.error(f"Failed to create data group: {str(e)}")
            raise

    def push_audience(self, audience_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Push the audience structure to TradeDesk
        Returns: (success: bool, audience_id: Optional[str])
        """
        try:
            # First create data groups for all included and excluded groups
            included_group_ids = []
            excluded_group_ids = []
            
            for group_id, group in audience_data["data_groups"].items():
                if not group.get("segments"):
                    logger.warning(f"Skipping group {group_id} - no segments defined")
                    continue
                    
                group_id = self.create_data_group(group)
                
                if group["status"] == "include":
                    included_group_ids.append(group_id)
                else:
                    excluded_group_ids.append(group_id)
            
            if not included_group_ids:
                raise ValueError("No valid included groups found")
            
            # Then create the audience that references these groups
            audience = ApiObject(
                AdvertiserId=self.advertiser_id,
                AudienceName=audience_data["audience_name"],
                IncludedDataGroupIds=included_group_ids,
                ExcludedDataGroupIds=excluded_group_ids
            )
            
            response = self.client.audiences.create(audience)
            audience_id = response.AudienceId
            return True, audience_id
            
        except Exception as e:
            logger.error(f"Failed to push audience: {str(e)}")
            return False, None


# Test execution section
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from dotenv import load_dotenv
    load_dotenv('ttd_test.env')
    # Test data
    test_audience = {
        "audience_name": "zTest AI Audience",
        "data_groups": {
            "group1": {
                "group_name": "zTest Group 1",
                "status": "include",
                "segments": [
                    {
                        "full_path": "Demographics > Age > 25-34",
                        "description": "Adults aged 25-34",
                        "id": "15493238|lds210audacu"  # Example TTD segment ID
                    }
                ]
            }
        }
    }
    
    try:
        # Initialize service in sandbox mode
        ttd_service = TTDInterfaceService(
            sandbox=True
        )
        
        # Test push with a default description instead of using Streamlit
        def push_test_audience(audience_data):
            audience = ApiObject(
                AdvertiserId=ttd_service.advertiser_id,
                AudienceName=audience_data["audience_name"],
                IncludedDataGroupIds=[],
                ExcludedDataGroupIds=[]
            )
            
            # Create data groups first
            for group_id, group in audience_data["data_groups"].items():
                if not group.get("segments"):
                    continue
                    
                group_id = ttd_service.create_data_group(group)
                
                if group["status"] == "include":
                    audience.IncludedDataGroupIds.append(group_id)
                else:
                    audience.ExcludedDataGroupIds.append(group_id)
            
            if not audience.IncludedDataGroupIds:
                raise ValueError("No valid included groups found")
                
            ttd_service.client.audiences.create(audience)
            return True
            
        success = push_test_audience(test_audience)
        
        if success:
            print("✅ Test audience successfully pushed to TTD sandbox!")
        else:
            print("❌ Failed to push test audience")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")