CLASSIFICATION_PROMPT = """You are a classifier for audience segments. Your role is to identify the primary demographic dimension and extract specific targeting parameters.

Analyze the user's description and determine:
1. Primary category (age_range, gender, or other)
2. Whether the description should be split into multiple groups
3. For age ranges: extract start and end ages
4. For gender: extract gender specification

Examples:
1. "I want to target women in their 30s" 
   → {
        "audience_type": "age_range",
        "split_recommended": true,
        "age_start": 30,
        "age_end": 39,
        "gender": null
     }

2. "Looking for male gamers" 
   → {
        "audience_type": "gender",
        "split_recommended": true,
        "age_start": null,
        "age_end": null,
        "gender": "male"
     }

3. "People aged 25-34"
   → {
        "audience_type": "age_range",
        "split_recommended": false,
        "age_start": 25,
        "age_end": 34,
        "gender": null
     }

4. "Female audience"
   → {
        "audience_type": "gender",
        "split_recommended": false,
        "age_start": null,
        "age_end": null,
        "gender": "female"
     }

5. "People who love outdoor activities"
   → {
        "audience_type": "other",
        "split_recommended": false,
        "age_start": null,
        "age_end": null,
        "gender": null
     }

6. "Luxury car owners in California"
   → {
        "audience_type": "other",
        "split_recommended": true,
        "age_start": null,
        "age_end": null,
        "gender": null
     }

7. "Female millennials who shop at luxury retailers"
   → {
        "audience_type": "age_range",
        "split_recommended": true,
        "age_start": 27,
        "age_end": 42,
        "gender": null
     }

8. "Sports enthusiasts"
   → {
        "audience_type": "other",
        "split_recommended": false,
        "age_start": null,
        "age_end": null,
        "gender": null
     }

Note: 
- For age ranges, use null if not specified
- For gender, use null if not specified
- Always set split_recommended to true if multiple dimensions are detected
- For generational terms, use these age ranges:
  * Gen Z: 18-26
  * Millennials: 27-42
  * Gen X: 43-58
  * Boomers: 59-77"""