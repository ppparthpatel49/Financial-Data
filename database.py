"""
AuraCycle - Database Module
Simple JSON-based data storage for user data, cycles, symptoms, and chat history
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class Database:
    """
    Simple JSON file-based database for AuraCycle
    Stores user cycles, symptoms, and chat history
    """
    
    def __init__(self, filename: str = "auracycle_data.json"):
        """
        Initialize database
        
        Args:
            filename: Name of JSON file to store data
        """
        self.file = Path(filename)
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database file if it doesn't exist"""
        if not self.file.exists():
            self._save({})
            print(f"✅ Database initialized: {self.file}")
    
    def _load(self) -> Dict:
        """
        Load data from JSON file
        
        Returns:
            Dictionary containing all user data
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error reading database, initializing empty database")
            return {}
        except Exception as e:
            print(f"⚠️ Database error: {e}")
            return {}
    
    def _save(self, data: Dict):
        """
        Save data to JSON file
        
        Args:
            data: Dictionary to save
        """
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
    
    def get_user_data(self, user_id: str) -> Dict:
        """
        Get all data for a specific user
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user's cycles, symptoms, and chats
        """
        data = self._load()
        return data.get(user_id, {
            "cycles": [],
            "symptoms": [],
            "chats": [],
            "profile": {}
        })
    
    def save_cycle_date(self, user_id: str, date: str, flow: str = "Medium"):
        """
        Save a cycle start date
        
        Args:
            user_id: User identifier
            date: Cycle start date (YYYY-MM-DD format)
            flow: Flow intensity
        """
        data = self._load()
        
        # Initialize user if not exists
        if user_id not in data:
            data[user_id] = {
                "cycles": [],
                "symptoms": [],
                "chats": [],
                "profile": {}
            }
        
        # Add cycle data
        cycle_entry = {
            "date": date,
            "flow": flow,
            "logged_at": datetime.now().isoformat()
        }
        
        data[user_id]["cycles"].append(cycle_entry)
        self._save(data)
        print(f"✅ Cycle logged: {date}")
    
    def get_cycle_dates(self, user_id: str) -> List[Dict]:
        """
        Get all cycle dates for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of cycle dictionaries
        """
        user_data = self.get_user_data(user_id)
        return user_data.get("cycles", [])
    
    def save_symptom(self, user_id: str, symptom_data: Dict):
        """
        Save symptom log entry
        
        Args:
            user_id: User identifier
            symptom_data: Dictionary containing symptom information
        """
        data = self._load()
        
        # Initialize user if not exists
        if user_id not in data:
            data[user_id] = {
                "cycles": [],
                "symptoms": [],
                "chats": [],
                "profile": {}
            }
        
        # Add timestamp
        symptom_data["logged_at"] = datetime.now().isoformat()
        
        # Append symptom
        data[user_id]["symptoms"].append(symptom_data)
        self._save(data)
        print(f"✅ Symptoms logged for {symptom_data.get('date')}")
    
    def get_symptoms(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get symptom history for a user
        
        Args:
            user_id: User identifier
            limit: Optional limit on number of entries
            
        Returns:
            List of symptom dictionaries
        """
        user_data = self.get_user_data(user_id)
        symptoms = user_data.get("symptoms", [])
        
        if limit:
            return symptoms[-limit:]
        return symptoms
    
    def save_chat(self, user_id: str, question: str, answer: str):
        """
        Save chat conversation
        
        Args:
            user_id: User identifier
            question: User's question
            answer: AI's answer
        """
        data = self._load()
        
        # Initialize user if not exists
        if user_id not in data:
            data[user_id] = {
                "cycles": [],
                "symptoms": [],
                "chats": [],
                "profile": {}
            }
        
        # Create chat entry
        chat_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer
        }
        
        data[user_id]["chats"].append(chat_entry)
        self._save(data)
    
    def get_chat_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get chat history for a user
        
        Args:
            user_id: User identifier
            limit: Optional limit on number of conversations
            
        Returns:
            List of chat dictionaries
        """
        user_data = self.get_user_data(user_id)
        chats = user_data.get("chats", [])
        
        if limit:
            return chats[-limit:]
        return chats
    
    def clear_chat_history(self, user_id: str) -> bool:
        """
        Clear all chat history for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        data = self._load()
        
        if user_id in data:
            data[user_id]["chats"] = []
            self._save(data)
            print(f"✅ Chat history cleared for {user_id}")
            return True
        return False
    
    def update_profile(self, user_id: str, profile_data: Dict):
        """
        Update user profile information
        
        Args:
            user_id: User identifier
            profile_data: Dictionary with profile fields
        """
        data = self._load()
        
        if user_id not in data:
            data[user_id] = {
                "cycles": [],
                "symptoms": [],
                "chats": [],
                "profile": {}
            }
        
        data[user_id]["profile"].update(profile_data)
        self._save(data)
        print(f"✅ Profile updated for {user_id}")
    
    def get_profile(self, user_id: str) -> Dict:
        """
        Get user profile
        
        Args:
            user_id: User identifier
            
        Returns:
            Profile dictionary
        """
        user_data = self.get_user_data(user_id)
        return user_data.get("profile", {})
    
    def delete_user_data(self, user_id: str) -> bool:
        """
        Delete all data for a user (GDPR compliance)
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        data = self._load()
        
        if user_id in data:
            del data[user_id]
            self._save(data)
            print(f"✅ All data deleted for {user_id}")
            return True
        return False
    
    def get_all_users(self) -> List[str]:
        """
        Get list of all user IDs
        
        Returns:
            List of user IDs
        """
        data = self._load()
        return list(data.keys())
    
    def export_user_data(self, user_id: str, export_path: Optional[str] = None) -> str:
        """
        Export user data to JSON file
        
        Args:
            user_id: User identifier
            export_path: Optional custom export path
            
        Returns:
            Path to exported file
        """
        user_data = self.get_user_data(user_id)
        
        if not export_path:
            export_path = f"auracycle_export_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to {export_path}")
        return export_path


# Example usage and testing
if __name__ == "__main__":
    # Test the database
    db = Database("test_auracycle.json")
    
    # Test user
    test_user = "test_user_123"
    
    # Save cycle
    db.save_cycle_date(test_user, "2024-01-15", "Medium")
    db.save_cycle_date(test_user, "2024-02-12", "Heavy")
    
    # Save symptoms
    db.save_symptom(test_user, {
        "date": "2024-02-15",
        "physical": ["Cramps", "Fatigue"],
        "emotional": ["Mood Swings"],
        "energy_level": 4,
        "pain_level": 6
    })
    
    # Save chat
    db.save_chat(test_user, "What helps with cramps?", "Try yoga and heating pad")
    
    # Retrieve data
    print("\n--- User Data ---")
    print(f"Cycles: {db.get_cycle_dates(test_user)}")
    print(f"Symptoms: {db.get_symptoms(test_user)}")
    print(f"Chats: {db.get_chat_history(test_user)}")
    
    print("\n✅ Database tests completed!")
