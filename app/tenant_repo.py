import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

class TenantRepo:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client["mlport"]
        self.collection = self.db["tenants"]

    def get_tenant(self, tenant_id: str):
        doc = self.collection.find_one({"tenant_id": tenant_id})
        if not doc:
            return None
        return {
            "tenant_id": doc["tenant_id"],
            "plan": doc.get("plan"),
            "limits": doc.get("limits", {}),
            "roles": doc.get("roles", []),
        }
