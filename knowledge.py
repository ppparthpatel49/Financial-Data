"""
AuraCycle - Knowledge Base
A static, curated knowledge base for menstrual health information.
Source: Reputable health websites (e.g., Mayo Clinic, NHS, Healthline)
"""

class KnowledgeBase:
    """
    Static knowledge base with curated information on menstrual health
    """
    
    def __init__(self):
        self.wellness_data = {
            "Cramps": [
                "Apply a heating pad to your lower abdomen.",
                "Gentle yoga poses like Child's Pose or Cat-Cow can help.",
                "Light walking or stretching can increase blood flow and reduce pain.",
                "Drink chamomile or ginger tea to help relax uterine muscles.",
                "Over-the-counter pain relievers like ibuprofen can be effective."
            ],
            "Bloating": [
                "Drink plenty of water to help flush out excess sodium.",
                "Avoid salty foods, carbonated drinks, and caffeine.",
                "Gentle exercises like walking or cycling can improve digestion.",
                "Yoga poses like Wind-Relieving Pose (Pawanmuktasana) can help.",
                "Eat smaller, more frequent meals to avoid overwhelming your digestive system."
            ],
            "Headache": [
                "Rest in a quiet, dark room.",
                "Apply a cold compress to your forehead or the back of your neck.",
                "Stay hydrated by drinking plenty of water.",
                "Gentle neck stretches can relieve tension.",
                "Magnesium supplements may help, but consult a doctor first."
            ],
            "Fatigue": [
                "Prioritize 7-9 hours of quality sleep per night.",
                "Engage in light physical activity like a short walk to boost energy.",
                "Ensure your diet is rich in iron (e.g., spinach, lentils).",
                "Take short rest breaks or naps during the day if possible.",
                "Practice relaxation techniques like deep breathing or meditation."
            ],
            "Mood Swings": [
                "Practice mindfulness or meditation to stay grounded.",
                "Engage in activities you enjoy to boost your mood.",
                "Regular exercise can help stabilize mood by releasing endorphins.",
                "Talk to a friend, partner, or therapist about how you're feeling.",
                "Ensure a balanced diet with complex carbohydrates to stabilize blood sugar."
            ],
            "Anxiety": [
                "Practice deep breathing exercises: inhale for 4 seconds, hold for 4, exhale for 6.",
                "Limit caffeine and alcohol, which can worsen anxiety.",
                "Journaling can help you process and understand your anxious thoughts.",
                "Spend time in nature, which has a calming effect.",
                "Listen to calming music or a guided meditation."
            ],
            "Default": [
                "Listen to your body and rest when you need to.",
                "Stay hydrated by drinking at least 8 glasses of water a day.",
                "Gentle, regular exercise can improve overall well-being.",
                "A balanced diet is crucial for hormonal health.",
                "Track your symptoms to understand your body's unique patterns."
            ]
        }
        
        self.nutrition_data = {
            "Cramps": [
                "**Ginger**: Has anti-inflammatory properties that can reduce pain.",
                "**Turmeric**: Contains curcumin, a powerful anti-inflammatory compound.",
                "**Dark Chocolate**: Rich in magnesium, which helps relax muscles.",
                "**Leafy Greens**: Spinach and kale are high in iron and magnesium.",
                "**Avoid**: Salty foods, excessive sugar, and caffeine, which can worsen cramps."
            ],
            "Bloating": [
                "**Bananas**: High in potassium, which helps balance sodium levels.",
                "**Cucumber**: High water content helps with hydration and flushing toxins.",
                "**Yogurt**: Contains probiotics that support healthy digestion.",
                "**Peppermint Tea**: Can help relax digestive muscles and reduce bloating.",
                "**Avoid**: Carbonated drinks, beans, and cruciferous vegetables like broccoli if they trigger you."
            ],
            "Fatigue": [
                "**Lentils & Beans**: Excellent source of plant-based iron and protein for energy.",
                "**Oats**: Provide a slow release of energy through complex carbohydrates.",
                "**Nuts & Seeds**: Packed with healthy fats, protein, and magnesium.",
                "**Spinach**: High in iron, which is crucial for preventing anemia-related fatigue.",
                "**Avoid**: Sugary snacks that cause an energy crash."
            ],
            "Mood Swings": [
                "**Complex Carbs**: Whole grains like brown rice and quinoa help stabilize blood sugar and mood.",
                "**Avocado**: Rich in healthy fats and B vitamins that support brain health.",
                "**Berries**: High in antioxidants that can help reduce inflammation and support mood.",
                "**Tofu & Edamame**: Good source of tryptophan, a precursor to serotonin (the 'feel-good' hormone).",
                "**Avoid**: Alcohol and excessive caffeine, which can disrupt mood."
            ],
            "Acne": [
                "**Sweet Potatoes**: Rich in beta-carotene, which the body converts to Vitamin A, supporting skin health.",
                "**Pumpkin Seeds**: High in zinc, which can help regulate hormonal balance and reduce acne.",
                "**Berries**: Packed with antioxidants to fight inflammation.",
                "**Green Tea**: Contains compounds that can help reduce sebum production.",
                "**Avoid**: High-glycemic foods (sugary snacks, white bread) and excessive dairy."
            ],
            "Default": [
                "**Iron-Rich Foods**: Lentils, spinach, tofu, and fortified cereals are important, especially during your period.",
                "**Magnesium Sources**: Nuts, seeds, dark chocolate, and avocados can help with various PMS symptoms.",
                "**Omega-3 Fatty Acids**: Flaxseeds, chia seeds, and walnuts can help reduce inflammation.",
                "**Stay Hydrated**: Water is essential for overall health and can help with bloating and headaches.",
                "**Calcium**: Found in fortified plant milks, tofu, and leafy greens, it can help reduce PMS symptoms."
            ]
        }
        
        self.general_info = {
            "cycle length": "A normal menstrual cycle for adults is typically between 21 and 35 days. For teenagers, it can be wider, from 21 to 45 days. It's common for the length to vary slightly from month to month.",
            "pms": "Premenstrual Syndrome (PMS) is a combination of physical and emotional symptoms that many women get in the days leading up to their period. Common symptoms include mood swings, bloating, cramps, and fatigue. Lifestyle changes like diet and exercise can often help manage PMS.",
            "period": "A period is the part of the menstrual cycle where a woman bleeds from her vagina for a few days. It's a natural process. A typical period lasts between 3 to 7 days.",
            "ovulation": "Ovulation is when a mature egg is released from the ovary. It usually happens about 14 days before the start of the next period. This is the most fertile time in the menstrual cycle.",
            "irregular cycle": "An irregular cycle is one that varies by more than 7-9 days from month to month. Occasional irregularity is normal, but if your cycles are consistently irregular, it's a good idea to talk to a healthcare provider, as it can sometimes indicate an underlying health issue.",
            "hygiene": "During your period, it's important to change your pad, tampon, or menstrual cup regularly (usually every 4-8 hours) to prevent infections and odor. Gentle washing of the external genital area with water is sufficient."
        }

    def get_wellness_tips(self, symptoms: list) -> str:
        """
        Get relevant wellness tips for a list of symptoms
        
        Args:
            symptoms: List of symptom strings
            
        Returns:
            A formatted string of relevant wellness tips
        """
        tips = set()
        
        if not symptoms:
            symptoms = ["Default"]
            
        for symptom in symptoms:
            # Find the best matching key
            best_match = self._find_best_match(symptom, self.wellness_data.keys())
            if best_match:
                tips.update(self.wellness_data[best_match])
            else:
                tips.update(self.wellness_data["Default"])
        
        return "\n".join([f"- {tip}" for tip in tips])

    def get_nutrition_tips(self, symptoms: list) -> str:
        """
        Get relevant nutrition tips for a list of symptoms
        
        Args:
            symptoms: List of symptom strings
            
        Returns:
            A formatted string of relevant nutrition tips
        """
        tips = set()
        
        if not symptoms:
            symptoms = ["Default"]
            
        for symptom in symptoms:
            best_match = self._find_best_match(symptom, self.nutrition_data.keys())
            if best_match:
                tips.update(self.nutrition_data[best_match])
            else:
                tips.update(self.nutrition_data["Default"])
        
        return "\n".join([f"- {tip}" for tip in tips])

    def get_general_info(self, query: str) -> str:
        """
        Get general menstrual health information based on a query
        
        Args:
            query: User's query string
            
        Returns:
            Relevant information or a default message
        """
        query_lower = query.lower()
        
        for keyword, info in self.general_info.items():
            if keyword in query_lower:
                return info
        
        return "I can provide information on topics like cycle length, PMS, ovulation, and hygiene. For specific medical advice, please consult a healthcare provider."

    def _find_best_match(self, symptom: str, keys: list) -> str:
        """
        Find the best matching key for a given symptom
        """
        symptom_lower = symptom.lower()
        for key in keys:
            if key.lower() in symptom_lower:
                return key
        return None
