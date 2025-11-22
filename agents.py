"""
AuraCycle - Multi-Agent System
Contains all AI agents for health guidance
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
from database import Database
from knowledge import KnowledgeBase
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please set GEMINI_API_KEY in your .env file")


class WellnessAgent:
    """
    Specialized agent for physical wellness recommendations
    Provides yoga, exercise, and activity suggestions
    """
    
    def __init__(self):
        self.kb = KnowledgeBase()
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Error initializing Wellness Agent model: {e}")
            self.model = None
    
    def get_recommendations(self, symptoms: list, cycle_phase: str = "unknown", user_context: dict = None):
        """
        Get wellness recommendations based on symptoms and cycle phase
        
        Args:
            symptoms: List of symptom strings
            cycle_phase: Current phase of menstrual cycle
            user_context: Additional user information
            
        Returns:
            Formatted wellness recommendations
        """
        
        if not self.model:
            return "Wellness Agent unavailable. Please check API configuration."
        
        # Get relevant knowledge from knowledge base
        wellness_tips = self.kb.get_wellness_tips(symptoms)
        
        # Construct prompt for LLM
        prompt = f"""
You are a compassionate wellness expert specializing in women's menstrual health.

**User's Symptoms:** {', '.join(symptoms) if symptoms else 'General wellness inquiry'}
**Cycle Phase:** {cycle_phase}

**Relevant Health Information:**
{wellness_tips}

Based on the above, provide personalized recommendations in this format:

**🧘 Recommended Yoga Poses:**
(List 3 specific poses with brief 1-line instructions)

**🏃 Exercise Recommendations:**
(List 2 appropriate exercises or activities)

**💡 Lifestyle Tip:**
(One actionable lifestyle suggestion)

Keep your tone supportive and empathetic. Be specific and actionable.
Use emojis for better readability. Keep it concise.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating wellness recommendations: {str(e)}"


class NutritionAgent:
    """
    Specialized agent for nutritional guidance
    Provides vegetarian food and recipe recommendations
    """
    
    def __init__(self):
        self.kb = KnowledgeBase()
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Error initializing Nutrition Agent model: {e}")
            self.model = None
    
    def get_recommendations(self, symptoms: list, cycle_phase: str = "unknown", age: int = 25, user_context: dict = None):
        """
        Get nutrition recommendations
        
        Args:
            symptoms: List of symptom strings
            cycle_phase: Current phase of menstrual cycle
            age: User's age
            user_context: Additional user information
            
        Returns:
            Formatted nutrition recommendations
        """
        
        if not self.model:
            return "Nutrition Agent unavailable. Please check API configuration."
        
        # Get relevant nutrition knowledge
        nutrition_tips = self.kb.get_nutrition_tips(symptoms)
        
        # Construct prompt
        prompt = f"""
You are a nutrition expert specializing in vegetarian diets for menstrual health.

**User's Symptoms:** {', '.join(symptoms) if symptoms else 'General nutrition inquiry'}
**Cycle Phase:** {cycle_phase}
**Age:** {age}

**Relevant Nutritional Information:**
{nutrition_tips}

Based on the above, provide personalized vegetarian recommendations in this format:

**🥗 Foods to Eat:**
(List 3-4 specific vegetarian foods with brief benefits)

**🚫 Foods to Avoid:**
(List 2 foods/drinks to limit or avoid)

**🍽️ Quick Recipe Idea:**
(One simple vegetarian recipe or meal idea)

Be practical, specific, and supportive. Use emojis for readability. Keep it concise.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating nutrition recommendations: {str(e)}"


class PredictionAgent:
    """
    Agent for cycle prediction and irregularity detection
    Uses data analysis (no LLM needed)
    """
    
    def __init__(self):
        self.db = Database()
    
    def predict_next_cycle(self, user_id: str):
        """
        Predict next cycle start date based on history
        
        Args:
            user_id: User identifier
            
        Returns:
            Predicted date string (YYYY-MM-DD) or "Need more data"
        """
        
        dates = self.db.get_cycle_dates(user_id)
        
        if len(dates) < 2:
            return "Need more data"
        
        try:
            # Convert to datetime objects
            date_objects = [
                datetime.strptime(d['date'], "%Y-%m-%d") 
                for d in sorted(dates, key=lambda x: x['date'])
            ]
            
            # Calculate gaps between cycles
            gaps = [
                (date_objects[i+1] - date_objects[i]).days 
                for i in range(len(date_objects)-1)
            ]
            
            # Calculate average cycle length
            avg_cycle = sum(gaps) / len(gaps)
            
            # Predict next cycle
            last_date = date_objects[-1]
            next_date = last_date + timedelta(days=int(round(avg_cycle)))
            
            return next_date.strftime("%Y-%m-%d")
        
        except Exception as e:
            print(f"Error in prediction: {e}")
            return "Error calculating prediction"
    
    def detect_irregularity(self, user_id: str):
        """
        Detect irregular cycle patterns
        
        Args:
            user_id: User identifier
            
        Returns:
            Warning message if irregular, None if regular
        """
        
        dates = self.db.get_cycle_dates(user_id)
        
        if len(dates) < 3:
            return None  # Not enough data to determine
        
        try:
            # Convert to datetime
            date_objects = [
                datetime.strptime(d['date'], "%Y-%m-%d") 
                for d in sorted(dates, key=lambda x: x['date'])
            ]
            
            # Calculate cycle lengths
            gaps = [
                (date_objects[i+1] - date_objects[i]).days 
                for i in range(len(date_objects)-1)
            ]
            
            avg = sum(gaps) / len(gaps)
            
            # Check for various irregularities
            
            # Cycles too short (< 21 days)
            if avg < 21:
                return "⚠️ Your average cycle length is shorter than typical (21-35 days). Consider consulting a healthcare provider."
            
            # Cycles too long (> 35 days)
            if avg > 35:
                return "⚠️ Your average cycle length is longer than typical (21-35 days). Consider consulting a healthcare provider."
            
            # High variation in cycle length
            if len(gaps) > 1:
                variation = max(gaps) - min(gaps)
                if variation > 10:
                    return "⚠️ Your cycle length varies significantly (>10 days difference). This can be normal, but consider tracking for another 2-3 months. If it persists, consult a doctor."
            
            # Check if current cycle is significantly late
            if len(date_objects) >= 2:
                last_cycle = date_objects[-1]
                expected_next = last_cycle + timedelta(days=int(round(avg)))
                days_late = (datetime.now() - expected_next).days
                
                if days_late > 7:
                    return f"⚠️ Your current cycle appears to be {days_late} days late based on your average. If you're not pregnant and this is unusual for you, consider taking a pregnancy test or consulting a doctor."
            
            return None  # No irregularities detected
        
        except Exception as e:
            print(f"Error in irregularity detection: {e}")
            return None
    
    def get_cycle_statistics(self, user_id: str):
        """
        Get detailed cycle statistics
        
        Returns:
            Dictionary with cycle stats
        """
        dates = self.db.get_cycle_dates(user_id)
        
        if len(dates) < 2:
            return {
                "average_length": None,
                "min_length": None,
                "max_length": None,
                "total_cycles": len(dates)
            }
        
        date_objects = [
            datetime.strptime(d['date'], "%Y-%m-%d") 
            for d in sorted(dates, key=lambda x: x['date'])
        ]
        
        gaps = [
            (date_objects[i+1] - date_objects[i]).days 
            for i in range(len(date_objects)-1)
        ]
        
        return {
            "average_length": sum(gaps) / len(gaps) if gaps else None,
            "min_length": min(gaps) if gaps else None,
            "max_length": max(gaps) if gaps else None,
            "total_cycles": len(dates),
            "last_cycle_length": gaps[-1] if gaps else None
        }


class CoordinatorAgent:
    """
    Main coordinator agent that orchestrates all other agents
    Handles user interactions and synthesizes responses
    """
    
    def __init__(self):
        self.db = Database()
        self.wellness_agent = WellnessAgent()
        self.nutrition_agent = NutritionAgent()
        self.prediction_agent = PredictionAgent()
        
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Error initializing Coordinator Agent model: {e}")
            self.model = None
    
    def chat(self, user_id: str, message: str):
        """
        Handle user chat messages - main orchestration function
        
        Args:
            user_id: User identifier
            message: User's question/message
            
        Returns:
            Comprehensive response from coordinated agents
        """
        
        if not self.model:
            return "Chat system unavailable. Please check API configuration."
        
        # Get user context
        user_data = self.db.get_user_data(user_id)
        
        # Analyze message to determine which agents to call
        message_lower = message.lower()
        
        responses = []
        
        # Check if wellness-related
        wellness_keywords = ['yoga', 'exercise', 'workout', 'stretch', 'pain', 'cramp', 
                            'ache', 'physical', 'movement', 'activity']
        if any(keyword in message_lower for keyword in wellness_keywords):
            symptoms = self._extract_symptoms(message)
            wellness_response = self.wellness_agent.get_recommendations(symptoms)
            responses.append(f"## 🧘 Wellness Recommendations\n{wellness_response}")
        
        # Check if nutrition-related
        nutrition_keywords = ['food', 'eat', 'diet', 'nutrition', 'recipe', 'meal', 
                             'vegetarian', 'hungry', 'crave']
        if any(keyword in message_lower for keyword in nutrition_keywords):
            symptoms = self._extract_symptoms(message)
            nutrition_response = self.nutrition_agent.get_recommendations(symptoms)
            responses.append(f"## 🥗 Nutrition Advice\n{nutrition_response}")
        
        # Check if prediction-related
        prediction_keywords = ['predict', 'when', 'next', 'cycle', 'period', 'expect', 'due']
        if any(keyword in message_lower for keyword in prediction_keywords):
            prediction = self.prediction_agent.predict_next_cycle(user_id)
            
            if prediction != "Need more data":
                prediction_response = f"🔮 Based on your cycle history, your next period is expected around **{prediction}**."
                
                # Add days until
                try:
                    next_date = datetime.strptime(prediction, "%Y-%m-%d")
                    days_until = (next_date - datetime.now()).days
                    if days_until > 0:
                        prediction_response += f" That's approximately **{days_until} days** from today."
                    elif days_until == 0:
                        prediction_response += " That's **today**!"
                    else:
                        prediction_response += f" Your period is **{abs(days_until)} days late**. If this is unusual, consider consulting a healthcare provider."
                except:
                    pass
            else:
                prediction_response = "🔮 I need at least 2 logged cycles to make predictions. Please track your cycles for more personalized predictions!"
            
            responses.append(f"## 🔮 Prediction\n{prediction_response}")
        
        # If no specific agent triggered, use general AI response
        if not responses:
            kb = KnowledgeBase()
            general_info = kb.get_general_info(message)
            
            prompt = f"""
You are AuraCycle, a supportive and knowledgeable menstrual health assistant.

**User's Question:** {message}

**Relevant Health Information:**
{general_info}

**User's Recent Activity:** 
- Logged cycles: {len(user_data.get('cycles', []))}
- Logged symptoms: {len(user_data.get('symptoms', []))}

Provide a helpful, empathetic, and informative response. 
- Be conversational and supportive
- Give practical advice when possible
- Always remind users to consult a healthcare provider for serious concerns
- Use emojis to make it friendly
- Keep it concise but comprehensive

Remember: You are a supportive companion, not a doctor.
"""
            
            try:
                response = self.model.generate_content(prompt)
                responses.append(response.text)
            except Exception as e:
                responses.append(f"I'm having trouble generating a response right now. Error: {str(e)}")
        
        # Combine all responses
        final_response = "\n\n---\n\n".join(responses)
        
        # Add medical disclaimer
        final_response += "\n\n---\n\n*💡 **Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice. Always consult a qualified healthcare provider for medical concerns.*"
        
        # Save chat to database
        self.db.save_chat(user_id, message, final_response)
        
        return final_response
    
    def handle_symptoms(self, user_id: str, symptoms: list):
        """
        Handle symptom logging - get recommendations from relevant agents
        
        Args:
            user_id: User identifier
            symptoms: List of symptoms
            
        Returns:
            Combined recommendations from agents
        """
        
        # Call both wellness and nutrition agents
        wellness = self.wellness_agent.get_recommendations(symptoms)
        nutrition = self.nutrition_agent.get_recommendations(symptoms)
        
        response = f"""
## 🧘 Wellness Recommendations
{wellness}

---

## 🥗 Nutrition Advice
{nutrition}

---

*💡 These suggestions are based on your logged symptoms. Track daily for better personalized insights!*
"""
        return response
    
    def _extract_symptoms(self, message: str):
        """
        Extract symptoms mentioned in the message
        
        Args:
            message: User's message
            
        Returns:
            List of detected symptoms
        """
        common_symptoms = {
            'cramp': 'Cramps',
            'bloat': 'Bloating',
            'headache': 'Headache',
            'migraine': 'Headache',
            'pain': 'Pain',
            'fatigue': 'Fatigue',
            'tired': 'Fatigue',
            'mood': 'Mood Swings',
            'irritab': 'Irritability',
            'stress': 'Stress',
            'anxiety': 'Anxiety',
            'sad': 'Sadness',
            'nausea': 'Nausea',
            'breast': 'Breast Tenderness',
            'back': 'Back Pain',
            'acne': 'Acne'
        }
        
        found_symptoms = set()
        message_lower = message.lower()
        
        for keyword, symptom in common_symptoms.items():
            if keyword in message_lower:
                found_symptoms.add(symptom)
        
        return list(found_symptoms) if found_symptoms else ['general discomfort']
