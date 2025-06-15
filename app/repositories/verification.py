from typing import Optional, List
from bson import ObjectId
from app.core.database import get_database
from app.models.database import VerificationCreate, VerificationUpdate, VerificationInDB

class VerificationRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.verifications

    async def create(self, verification: VerificationCreate) -> VerificationInDB:
        verification_dict = verification.dict()
        result = await self.collection.insert_one(verification_dict)
        verification_dict["_id"] = result.inserted_id
        return VerificationInDB(**verification_dict)

    async def get_by_id(self, verification_id: str) -> Optional[VerificationInDB]:
        verification = await self.collection.find_one({"_id": ObjectId(verification_id)})
        if verification:
            return VerificationInDB(**verification)
        return None

    async def update(
        self,
        verification_id: str,
        verification: VerificationUpdate
    ) -> Optional[VerificationInDB]:
        update_data = verification.dict(exclude_unset=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(verification_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await self.get_by_id(verification_id)
        return None

    async def list(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[VerificationInDB]:
        cursor = self.collection.find().skip(skip).limit(limit)
        verifications = await cursor.to_list(length=limit)
        return [VerificationInDB(**verification) for verification in verifications]

    async def delete(self, verification_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(verification_id)})
        return result.deleted_count > 0 