from typing import Dict, Any, List, Optional

class DiseaseProgressTracker:
    """
    Evaluates disease progression timelines across repeated monitoring scans for the same crop/plot.
    Classifies trend into:
    - Improving (सुधार)
    - Stable (स्थिर)
    - Increasing (बढ़ रहा है)
    - Rapidly Increasing (तेजी से बढ़ रहा है)
    - Uncertain (अनिश्चित)
    """

    @classmethod
    def evaluate_progression(
        cls,
        current_scan: Dict[str, Any],
        historical_scans: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        curr_score = current_scan.get("risk_score", 50)
        curr_conf = current_scan.get("confidence", 0.85)

        # If no prior scans exist, this is the baseline monitoring entry
        if not historical_scans or len(historical_scans) == 0:
            return {
                "trend": "Uncertain",
                "trend_hindi": "प्रारंभिक स्कैन (अनिश्चित)",
                "trend_description": "Initial baseline scan recorded. Repeat scan in 3-5 days to evaluate progression trend.",
                "trend_description_hindi": "पहला बेसलाइन स्कैन दर्ज किया गया। प्रगति जानने के लिए 3-5 दिनों बाद दोबारा स्कैन करें।",
                "previous_risk_score": None,
                "current_risk_score": curr_score,
                "risk_delta": 0,
                "recommend_expert_escalation": False,
                "total_historical_records": 1
            }

        # Compare with the most recent prior scan
        prev_scan = historical_scans[0]
        prev_score = prev_scan.get("risk_score", curr_score)
        prev_sev = (prev_scan.get("severity") or "Medium").lower()
        curr_sev = (current_scan.get("severity") or "Medium").lower()

        risk_delta = curr_score - prev_score

        # Classify trend
        if "healthy" in (current_scan.get("predicted_disease") or "").lower() or risk_delta <= -10:
            trend = "Improving"
            trend_hi = "सुधार हो रहा है"
            trend_desc_en = f"Foliar symptoms show noticeable recovery. Risk score decreased by {abs(risk_delta)} points."
            trend_desc_hi = f"फसल के स्वास्थ्य में सुधार दिख रहा है। जोखिम स्कोर {abs(risk_delta)} अंक कम हुआ है।"
            escalate = False
        elif abs(risk_delta) <= 5:
            trend = "Stable"
            trend_hi = "स्थिति स्थिर है"
            trend_desc_en = "Disease symptoms appear contained. No significant expansion detected."
            trend_desc_hi = "रोग के लक्षण नियंत्रित दिख रहे हैं। कोई नया फैलाव दर्ज नहीं हुआ है।"
            escalate = False
        elif 6 <= risk_delta <= 15:
            trend = "Increasing"
            trend_hi = "लक्षण बढ़ रहे हैं"
            trend_desc_en = f"Symptom intensity and risk score increased by +{risk_delta} points. Immediate intervention needed."
            trend_desc_hi = f"रोग की तीव्रता व जोखिम स्कोर +{risk_delta} अंक बढ़ा है। तुरंत ध्यान देने की आवश्यकता है।"
            escalate = True
        elif risk_delta > 15 or (prev_sev != "high" and curr_sev == "high"):
            trend = "Rapidly Increasing"
            trend_hi = "तेजी से बढ़ रहा है (चेतावनी)"
            trend_desc_en = f"Critical escalation alert: Risk score surged by +{risk_delta} points with rapid lesion spread."
            trend_desc_hi = f"गंभीर चेतावनी: जोखिम स्कोर तेजी से +{risk_delta} अंक बढ़ा है। तुरंत विशेषज्ञ परामर्श लें।"
            escalate = True
        else:
            trend = "Uncertain"
            trend_hi = "अनिश्चित"
            trend_desc_en = "Inconclusive comparison due to symptom variations or lighting."
            trend_desc_hi = "फोटो भिन्नता के कारण स्पष्ट तुलना नहीं हो सकी।"
            escalate = False

        return {
            "trend": trend,
            "trend_hindi": trend_hi,
            "trend_description": trend_desc_en,
            "trend_description_hindi": trend_desc_hi,
            "previous_risk_score": prev_score,
            "current_risk_score": curr_score,
            "risk_delta": risk_delta,
            "recommend_expert_escalation": escalate,
            "total_historical_records": len(historical_scans) + 1
        }
