import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database.models import ScanHistory, User
from app.schemas.schemas import OfflineScanPayload

class SyncService:
    """
    Ingests scans that were queued locally in the farmer's browser or mobile device
    while offline, reconciling them into the central database.
    """

    @staticmethod
    def sync_offline_scans(
        db: Session,
        user: User,
        scans: List[OfflineScanPayload]
    ) -> Dict[str, Any]:
        synced_ids = []
        
        for item in scans:
            new_scan = ScanHistory(
                user_id=user.id if user else None,
                farmer_name=item.farmer_name,
                farmer_phone=item.farmer_phone,
                crop=item.crop,
                predicted_disease=item.predicted_disease,
                confidence=item.confidence,
                severity=item.severity,
                follow_up_data=json.dumps(item.follow_up_data) if item.follow_up_data else None,
                generated_explanation=item.generated_explanation,
                is_synced=True
            )
            db.add(new_scan)
            db.flush()
            synced_ids.append(new_scan.id)

        if user:
            user.scan_count_month += len(scans)

        db.commit()

        return {
            "status": "success",
            "synced_count": len(synced_ids),
            "synced_scan_ids": synced_ids,
            "message": f"Successfully synced {len(synced_ids)} offline scan(s) to cloud backend."
        }
