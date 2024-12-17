from typing import List, Dict, Optional
from models.classification import AudienceType, Gender, GroupClassification
from itertools import combinations

class SegmentService:
    def __init__(self):
        # Gender segments
        self.gender_segments = {
            "male": {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Gender > Male",
                "description": "Individuals who identify as male. Deterministic, self-reported data verified by Truthset.",
                "id": "15493238|lds210audacu"
            },
            "female": {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Gender > Female",
                "description": "Individuals who identify as female. Deterministic, self-reported data verified by Truthset.",
                "id": "15493200|lds210audacu"
            }
        }
        
        # Age range segments
        self.age_range_segments = {
            (18, 20): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 18-20",
                "description": "People who are in the age range of 18-20. Deterministic, self-reported data verified by Truthset.",
                "id": "15493234|lds210audacu"
            },
            (21, 24): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 21-24",
                "description": "People who are in the age range of 21-24. Deterministic, self-reported data verified by Truthset.",
                "id": "15493174|lds210audacu"
            },
            (25, 29): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 25-29",
                "description": "People who are in the age range of 25-29. Deterministic, self-reported data verified by Truthset.",
                "id": "15493215|lds210audacu"
            },
            (30, 34): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 30-34",
                "description": "People who are in the age range of 30-34. Deterministic, self-reported data verified by Truthset.",
                "id": "15493219|lds210audacu"
            },
            (35, 39): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 35-39",
                "description": "People who are in the age range of 35-39. Deterministic, self-reported data verified by Truthset.",
                "id": "15493166|lds210audacu"
            },
            (40, 44): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 40-44",
                "description": "People who are in the age range of 40-44. Deterministic, self-reported data verified by Truthset.",
                "id": "15493192|lds210audacu"
            },
            (45, 49): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 45-49",
                "description": "People who are in the age range of 45-49. Deterministic, self-reported data verified by Truthset.",
                "id": "15493185|lds210audacu"
            },
            (50, 54): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 50-54",
                "description": "People who are in the age range of 50-54. Deterministic, self-reported data verified by Truthset.",
                "id": "15493052|lds210audacu"
            },
            (55, 59): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 55-59",
                "description": "People who are in the age range of 55-59. Deterministic, self-reported data verified by Truthset.",
                "id": "15493068|lds210audacu"
            },
            (60, 64): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 60-64",
                "description": "People who are in the age range of 60-64. Deterministic, self-reported data verified by Truthset.",
                "id": "15493009|lds210audacu"
            },
            (65, 69): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 65-69",
                "description": "People who are in the age range of 65-69. Deterministic, self-reported data verified by Truthset.",
                "id": "15493126|lds210audacu"
            },
            (70, 74): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 70-74",
                "description": "People who are in the age range of 70-74. Deterministic, self-reported data verified by Truthset.",
                "id": "15493111|lds210audacu"
            }
        }
        
        # Special range segments (open-ended)
        self.special_ranges = {
            (18, None): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 18+",
                "description": "People who are 18 years of age or older. Deterministic, self-reported data verified by Truthset.",
                "id": "15674755|lds210audacu"
            },
            (21, None): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 21+",
                "description": "People who are 21+ years old. Deterministic, self-reported data verified by Truthset.",
                "id": "15493128|lds210audacu"
            },
            (25, None): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 25+",
                "description": "People who are 25 years of age or older. Deterministic, self-reported data verified by Truthset.",
                "id": "15674754|lds210audacu"
            },
            (75, None): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 75+",
                "description": "People who are 75+ years old. Deterministic, self-reported data verified by Truthset.",
                "id": "15492988|lds210audacu"
            },
            (18, 54): {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age Range > 18-54",
                "description": "People who are 18-54 years old. Deterministic, self-reported data verified by Truthset.",
                "id": "15674753|lds210audacu"
            }
        }
        
        # Individual age segments (49-99)
        self.individual_age_segments = {
            49: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 49",
                "description": "Individuals who are 49 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493045|lds210audacu"
            },
            51: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 51",
                "description": "Individuals who are 51 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493067|lds210audacu"
            },
            52: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 52",
                "description": "Individuals who are 52 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492990|lds210audacu"
            },
            53: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 53",
                "description": "Individuals who are 53 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493144|lds210audacu"
            },
            54: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 54",
                "description": "Individuals who are 54 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493135|lds210audacu"
            },
            55: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 55",
                "description": "Individuals who are 55 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493018|lds210audacu"
            },
            56: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 56",
                "description": "Individuals who are 56 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493030|lds210audacu"
            },
            57: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 57",
                "description": "Individuals who are 57 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493031|lds210audacu"
            },
            58: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 58",
                "description": "Individuals who are 58 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492981|lds210audacu"
            },
            59: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 59",
                "description": "Individuals who are 59 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493153|lds210audacu"
            },
            60: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 60",
                "description": "Individuals who are 60 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493010|lds210audacu"
            },
            61: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 61",
                "description": "Individuals who are 61 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493077|lds210audacu"
            },
            62: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 62",
                "description": "Individuals who are 62 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493008|lds210audacu"
            },
            63: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 63",
                "description": "Individuals who are 63 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493139|lds210audacu"
            },
            64: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 64",
                "description": "Individuals who are 64 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493041|lds210audacu"
            },
            65: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 65",
                "description": "Individuals who are 65 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493124|lds210audacu"
            },
            66: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 66",
                "description": "Individuals who are 66 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493142|lds210audacu"
            },
            67: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 67",
                "description": "Individuals who are 67 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493049|lds210audacu"
            },
            68: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 68",
                "description": "Individuals who are 68 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493088|lds210audacu"
            },
            69: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 69",
                "description": "Individuals who are 69 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493021|lds210audacu"
            },
            70: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 70",
                "description": "Individuals who are 70 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493110|lds210audacu"
            },
            71: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 71",
                "description": "Individuals who are 71 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493042|lds210audacu"
            },
            72: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 72",
                "description": "Individuals who are 72 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493062|lds210audacu"
            },
            73: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 73",
                "description": "Individuals who are 73 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493059|lds210audacu"
            },
            74: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 74",
                "description": "Individuals who are 74 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493116|lds210audacu"
            },
            75: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 75",
                "description": "Individuals who are 75 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493091|lds210audacu"
            },
            76: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 76",
                "description": "Individuals who are 76 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493120|lds210audacu"
            },
            77: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 77",
                "description": "Individuals who are 77 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493028|lds210audacu"
            },
            78: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 78",
                "description": "Individuals who are 78 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493034|lds210audacu"
            },
            79: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 79",
                "description": "Individuals who are 79 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493050|lds210audacu"
            },
            80: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 80",
                "description": "Individuals who are 80 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493113|lds210audacu"
            },
            81: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 81",
                "description": "Individuals who are 81 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493016|lds210audacu"
            },
            82: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 82",
                "description": "Individuals who are 82 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493033|lds210audacu"
            },
            83: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 83",
                "description": "Individuals who are 83 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493123|lds210audacu"
            },
            84: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 84",
                "description": "Individuals who are 84 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493152|lds210audacu"
            },
            85: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 85",
                "description": "Individuals who are 85 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493006|lds210audacu"
            },
            86: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 86",
                "description": "Individuals who are 86 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492986|lds210audacu"
            },
            87: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 87",
                "description": "Individuals who are 87 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493026|lds210audacu"
            },
            88: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 88",
                "description": "Individuals who are 88 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493154|lds210audacu"
            },
            89: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 89",
                "description": "Individuals who are 89 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493095|lds210audacu"
            },
            90: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 90",
                "description": "Individuals who are 90 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493040|lds210audacu"
            },
            91: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 91",
                "description": "Individuals who are 91 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492992|lds210audacu"
            },
            92: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 92",
                "description": "Individuals who are 92 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493138|lds210audacu"
            },
            93: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 93",
                "description": "Individuals who are 93 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493140|lds210audacu"
            },
            94: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 94",
                "description": "Individuals who are 94 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492977|lds210audacu"
            },
            95: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 95",
                "description": "Individuals who are 95 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492978|lds210audacu"
            },
            96: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 96",
                "description": "Individuals who are 96 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493162|lds210audacu"
            },
            97: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 97",
                "description": "Individuals who are 97 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493066|lds210audacu"
            },
            98: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 98",
                "description": "Individuals who are 98 years old. This segment is deterministic and verified by Truthset.",
                "id": "15493089|lds210audacu"
            },
            99: {
                "full_path": "Custom Segment > Audience Acuity > Pathlabs > Demographics > Age > 99",
                "description": "Individuals who are 99 years old. This segment is deterministic and verified by Truthset.",
                "id": "15492985|lds210audacu"
            }
        }

    def get_segments_for_classification(self, classification: GroupClassification) -> Dict:
        if classification.audience_type == AudienceType.GENDER:
            return self.get_gender_group(classification.gender)
        elif classification.audience_type == AudienceType.AGE_RANGE:
            return self.get_optimal_age_coverage(classification.age_start, classification.age_end)
        return {}

    def get_gender_group(self, gender: Optional[Gender]) -> Dict:
        if not gender or gender not in self.gender_segments:
            return {}
            
        return {
            "group_name": f"{gender.title()} Audience",
            "segments": [self.gender_segments[gender]]
        }

    def get_optimal_age_coverage(self, start: Optional[int], end: Optional[int]) -> Dict:
        if not start:
            return {}
            
        # First check if we have an exact special range match
        special_key = (start, end)
        if special_key in self.special_ranges:
            return {
                "group_name": f"Age {start}{'-' + str(end) if end else '+'} Audience",
                "segments": [self.special_ranges[special_key]]
            }
            
        # For open-ended ranges (no end), check special ranges that cover it
        if end is None:
            for (range_start, range_end), segment in self.special_ranges.items():
                if start >= range_start and range_end is None:
                    return {
                        "group_name": f"Age {start}+ Audience",
                        "segments": [segment]
                    }
        
        # Build solution from standard ranges and individual ages
        needed_ages = set(range(start, (end or 99) + 1))
        solution = []
        remaining_ages = needed_ages.copy()
        
        # Add standard ranges that fit within our needed range
        for (range_start, range_end), segment in self.age_range_segments.items():
            range_coverage = set(range(range_start, range_end + 1))
            if range_coverage.issubset(needed_ages):
                solution.append(segment)
                remaining_ages -= range_coverage
        
        # Fill any gaps with individual ages
        for age in sorted(remaining_ages):
            if age in self.individual_age_segments:
                solution.append(self.individual_age_segments[age])
        
        if solution:
            return {
                "group_name": f"Age {start}{'-' + str(end) if end else '+'} Audience",
                "segments": solution
            }
                
        return {}
