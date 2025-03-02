from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from app.core.config import settings
from app.db.supabase import get_supabase_client

T = TypeVar('T', bound=SQLModel)

class CRUDBase(Generic[T]):
    """
    Base class for CRUD operations using SQLModel with Supabase.
    """
    def __init__(self, model: Type[T]):
        self.model = model
        self.supabase = get_supabase_client()
        self.table_name = model.__tablename__

    async def get(self, id: Any) -> Optional[T]:
        """Get a single record by ID"""
        try:
            response = self.supabase.table(self.table_name).select("*").eq("id", id).execute()
            if response.data and len(response.data) > 0:
                return self.model(**response.data[0])
            return None
        except Exception as e:
            raise Exception(f"Error retrieving {self.table_name} with id {id}: {str(e)}")

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[T]:
        """Get multiple records with pagination"""
        try:
            response = self.supabase.table(self.table_name).select("*").range(skip, skip + limit - 1).execute()
            return [self.model(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error retrieving multiple {self.table_name}: {str(e)}")

    async def create(self, *, obj_in: Union[Dict[str, Any], T]) -> T:
        """Create a new record"""
        try:
            if isinstance(obj_in, dict):
                obj_data = obj_in
            else:
                obj_data = obj_in.dict(exclude_unset=True)
                
            response = self.supabase.table(self.table_name).insert(obj_data).execute()
            return self.model(**response.data[0])
        except Exception as e:
            raise Exception(f"Error creating {self.table_name}: {str(e)}")

    async def update(self, *, id: Any, obj_in: Union[Dict[str, Any], T]) -> Optional[T]:
        """Update an existing record"""
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
                
            response = self.supabase.table(self.table_name).update(update_data).eq("id", id).execute()
            if response.data and len(response.data) > 0:
                return self.model(**response.data[0])
            return None
        except Exception as e:
            raise Exception(f"Error updating {self.table_name} with id {id}: {str(e)}")

    async def delete(self, *, id: Any) -> bool:
        """Delete a record"""
        try:
            self.supabase.table(self.table_name).delete().eq("id", id).execute()
            return True
        except Exception as e:
            raise Exception(f"Error deleting {self.table_name} with id {id}: {str(e)}")

    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """Get a record by a specific field value"""
        try:
            response = self.supabase.table(self.table_name).select("*").eq(field, value).execute()
            if response.data and len(response.data) > 0:
                return self.model(**response.data[0])
            return None
        except Exception as e:
            raise Exception(f"Error retrieving {self.table_name} with {field}={value}: {str(e)}")