
import os
import io
import json
import base64
from PIL import Image
import google.generativeai as genai
from django.conf import settings

class GeminiImageProcessor:
    """Process images using Google's Gemini Flash 2.0 model"""
    
    def __init__(self):
        # Set up the API key from Django settings
        api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def process_image(self, image_path):
        """Process an image to extract tube data with colors"""
        
        # Load and prepare the image
        with Image.open(image_path) as img:
            # Convert to bytes for Gemini API
            buffer = io.BytesIO()
            img.save(buffer, format=img.format)
            image_bytes = buffer.getvalue()
            image_parts = [{"mime_type": f"image/{img.format.lower()}", "data": image_bytes}]
        
        # Create the prompt for Gemini
        prompt = """
        Analyze this laboratory image that contains rows of microcentrifuge tubes with colored liquid.
        For each visible row and tube:
        1. Identify the number of rows in the image
        2. Count the number of tubes in each row
        3. Extract the RGB color values for the liquid inside each tube
        
        Return the data in this JSON format:
        {
          "Row1": [
            {
              "Tube1": {
                "Color": "yellow",
                "RGB": {
                  "R": 255,
                  "G": 255, 
                  "B": 0
                }
              }
            },
            // More tubes in Row1
          ],
          // More rows
        }
        
        Only provide the JSON output, no additional text.
        """
        
        # Generate content with Gemini
        response = self.model.generate_content([prompt] + image_parts)
        
        # Extract and format the JSON response
        try:
            # Parse the response text for JSON content
            response_text = response.text
            # Look for JSON content between triple backticks if present
            if "```json" in response_text and "```" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "{" in response_text and "}" in response_text:
                # Extract everything between first { and last }
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text.strip()
                
            # Parse the JSON
            result_json = json.loads(json_str)
            
            # Format to match your desired structure
            formatted_json = self._format_json(result_json)
            return json.dumps(formatted_json, indent=2)
            
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini response: {str(e)}")
    
    def _format_json(self, raw_json):
        """Ensure the JSON follows the correct format with RGB values as numbers"""
        formatted = {}
        
        for row_key, row_data in raw_json.items():
            formatted_row = []
            
            for tube_item in row_data:
                for tube_key, tube_data in tube_item.items():
                    # Ensure RGB values are numeric
                    if isinstance(tube_data.get("RGB"), dict):
                        rgb = tube_data["RGB"]
                        formatted_tube = {
                            tube_key: {
                                "Color": tube_data.get("Color", ""),
                                "RGB": {
                                    "R": float(rgb.get("R", 0)),
                                    "G": float(rgb.get("G", 0)),
                                    "B": float(rgb.get("B", 0))
                                }
                            }
                        }
                    else:
                        # Handle case where RGB might be in a different format
                        formatted_tube = {
                            tube_key: {
                                "Color": tube_data.get("Color", ""),
                                "RGB": {
                                    "R": 0,
                                    "G": 0,
                                    "B": 0
                                }
                            }
                        }
                    formatted_row.append(formatted_tube)
            
            formatted[row_key] = formatted_row
            print(formatted)
        return formatted