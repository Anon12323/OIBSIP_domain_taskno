"""
Core BMI Calculator Logic
Handles calculations, data storage, and utilities
"""

import json
import os
from datetime import datetime

class BMICore:
    @staticmethod
    def calculate(weight, height):
        """Calculate BMI from weight(kg) and height(m)"""
        return weight / (height ** 2)
    
    @staticmethod
    def get_category(bmi):
        """Get BMI category and advice"""
        if bmi < 18.5:
            return "Underweight", "Consider consulting a nutritionist"
        elif bmi < 25:
            return "Normal", "Maintain your healthy lifestyle!"
        elif bmi < 30:
            return "Overweight", "Consider healthier eating habits"
        elif bmi < 35:
            return "Obese Class I", "Consult a healthcare professional"
        elif bmi < 40:
            return "Obese Class II", "Seek medical advice"
        else:
            return "Obese Class III", "Urgent medical consultation recommended"
    
    @staticmethod
    def validate_inputs(weight, height, age=None):
        """Validate user inputs"""
        if weight < 20 or weight > 500:
            raise ValueError("Weight must be between 20-500 kg")
        if height < 0.5 or height > 3.0:
            raise ValueError("Height must be between 0.5-3.0 meters")
        if age and (age < 1 or age > 120):
            raise ValueError("Age must be between 1-120 years")
        return True

class DataManager:
    def __init__(self, filename="bmi_data.json"):
        self.filename = filename
        self.data = self.load()
    
    def load(self):
        """Load data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save(self):
        """Save data to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save data: {str(e)}")
    
    def add_record(self, name, age, gender, weight, height, bmi, category):
        """Add a new BMI record"""
        record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': name,
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'bmi': round(bmi, 2),
            'category': category
        }
        self.data.append(record)
        self.save()
        return record
    
    def delete_record(self, index):
        """Delete a record by index"""
        if 0 <= index < len(self.data):
            del self.data[index]
            self.save()
            return True
        return False
    
    def clear_all(self):
        """Clear all records"""
        self.data = []
        self.save()
    
    def get_statistics(self):
        """Calculate statistics from data"""
        if not self.data:
            return None
        
        bmis = [r['bmi'] for r in self.data]
        categories = [r['category'] for r in self.data]
        
        stats = {
            'total': len(self.data),
            'avg_bmi': sum(bmis) / len(bmis),
            'max_bmi': max(bmis),
            'min_bmi': min(bmis),
            'category_counts': {}
        }
        
        for category in categories:
            stats['category_counts'][category] = stats['category_counts'].get(category, 0) + 1
        
        return stats