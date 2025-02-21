# Hungrig: Your AI-Powered Kitchen Assistant 📸🍳

Cooking can be a daunting task, especially when you're juggling a busy schedule, specific dietary needs, and the desire to eat something delicious and healthy. Enter the **Smart Recipe Finder**, an AI-powered app designed to simplify your cooking experience. Built with **Streamlit** and powered by **Google’s Gemini API**, this app is your personal kitchen assistant, helping you discover recipes tailored to your mood, preferences, and the ingredients you already have at home. 

With the latest addition of **Image-Based Ingredient Detection**, the Smart Recipe Finder is now more powerful than ever. Let’s dive into all the features that make this app a must-have for home cooks everywhere.

---

## 🎯 **What Does the Smart Recipe Finder Do?**

The Smart Recipe Finder is more than just a recipe generator. It’s a personalized cooking companion that takes into account your unique preferences and constraints. Here’s what it offers:

### **1. Mood-Based Recipes**
Whether you're feeling adventurous, lazy, or stressed, the app suggests recipes that match your mood. Craving comfort food after a long day? It’s got you covered.

### **2. Cuisine Preferences**
Love Italian food but tired of pasta? The app lets you choose your preferred cuisine, from Indian to Mediterranean, and everything in between.

### **3. Time-Saving Options**
Short on time? Use the slider to specify how much time you have, and the app will recommend recipes that fit your schedule.

### **4. Skill Level Adaptation**
Whether you're a beginner or an expert chef, the app tailors recipes to your skill level, ensuring you can cook with confidence.

### **5. Dietary Restrictions & Allergies**
The app respects your dietary needs, whether you're vegetarian, gluten-free, or have specific allergies like nuts or shellfish.

### **6. Health Goals**
Trying to lose weight, build muscle, or improve digestion? The app suggests recipes aligned with your health goals.

### **7. Ingredient-Based Suggestions**
Simply list the ingredients you have in your fridge, and the app will generate recipes that use them. It even tells you what’s missing and provides a shopping list!

### **8. Image-Based Ingredient Detection (New!)**
Snap a picture of the ingredients in your fridge, and the app will automatically detect them and suggest recipes tailored to what you have on hand. No more manually listing ingredients!

### **9. Gamification**
Track the recipes you’ve cooked and build a personal collection of your favorite dishes. It’s a fun way to stay motivated and explore new recipes.

---

## 🛠️ **How Does It Work?**

The app is built using **Streamlit**, a powerful framework for creating data-driven web apps, and leverages **Google’s Gemini API** for AI-powered recipe generation. Here’s a breakdown of its features:

### **User Inputs**
The app’s sidebar collects all your preferences:
- **Mood**: Choose from options like happy, tired, adventurous, or stressed.
- **Cuisine**: Select your preferred cuisine or opt for no preference.
- **Time Available**: Use a slider to specify how much time you have (5 to 120 minutes).
- **Skill Level**: Indicate whether you're a beginner, intermediate, advanced, or expert cook.
- **Appliances**: Select the kitchen tools you have, like an oven, air fryer, or blender.
- **Dietary Restrictions & Allergies**: Specify any dietary needs or allergies.
- **Health Goals**: Choose goals like weight loss, muscle gain, or heart health.

### **Recipe Generation**
Once you’ve entered your preferences, the app uses the Gemini API to generate three tailored recipes. Here’s how the recipe generation works:
```python
prompt = f""" 
        Suggest 3 recipes based on the following:
        - Mood: {mood}
        - Cuisine Preference: {cuisine}
        - Time Available: {time} minutes
        - Skill Level: {skill}
        - Available Ingredients: {ingredients}
        - Available Appliances: {', '.join(appliances) if appliances else 'None'}
        - Dietary Restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}
        - Allergies: {', '.join(allergies) if allergies else 'None'}
        - Health Goals: {', '.join(health_goals) if health_goals else 'None'}

        Ensure the recipes:
        - Match the mood and preferences.
        - Use the listed ingredients as much as possible.
        - Explicitly list missing ingredients.
        - Provide cooking instructions.
        - Provide Nutritional Information (Calories, Protein, Carbs, etc.).

        Return the result as a JSON array with the following structure:
        [
          {{
              "name": "Recipe Name",
              "prep_time": "Time in minutes",
              "missing_ingredients": ["list of missing ingredients"],
              "instructions": "Detailed cooking instructions",
              "nutritional_info": {{
                  "calories": "x",
                  "protein": "x",
                  "carbs": "x",
                  "fat": "x"
              }},
              "shopping_list": ["list of missing ingredients"]
          }} 
        ]

        Important Notes:
        1. Escape all newline characters in the instructions field with \\n to ensure valid JSON formatting.
        2. Do not include any additional text or comments outside the JSON array.
        3. Only return valid JSON in the response.
    """
    
    response = model.generate_content(prompt)
    print("LLM response:", response.text)

    if response:
        try:
            # Parse the response as JSON
            preprocess_response = response.text.replace("```json", "").replace('```', "")
            recipes = json.loads(preprocess_response)
            print("Recipes:", recipes)
            
            # Store recipes in session state to persist across reruns
            st.session_state.recipes = recipes

        except Exception as e:
            st.error("Error parsing the response. Please try again.")
            print(e)
            st.write(f"Error Details: {e}")
```
Once you’ve entered your preferences, the app uses the Gemini API to generate three tailored recipes. Each recipe includes:
- **Name**: The title of the dish.
- **Prep Time**: How long it takes to cook.
- **Missing Ingredients**: A list of ingredients you’ll need to buy.
- **Instructions**: Step-by-step cooking instructions.
- **Nutritional Information**: Calories, protein, carbs, and fat content.
- **Shopping List**: A handy list of missing ingredients to take to the store.

### **Image-Based Ingredient Detection**
The latest feature allows you to upload an image of your ingredients. Here’s how it works:
1. **Upload an Image**: Snap a picture of the ingredients in your fridge or pantry and upload it to the app.
2. **AI-Powered Detection**: The app uses advanced image recognition technology to identify the ingredients in your photo.
3. **Recipe Suggestions**: Based on the detected ingredients, the app generates personalized recipes that match your mood, dietary preferences, and health goals.
```python
# Image Upload for Ingredient Detection
uploaded_file = st.file_uploader("Upload an image of your ingredients", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    # Use a pre-trained model to detect ingredients
    detected_ingredients = detect_ingredients(uploaded_file)
    
    # Display detected ingredients
    st.write("Detected Ingredients:", detected_ingredients)
    
    # Use detected ingredients for recipe generation
    ingredients = ", ".join(detected_ingredients)
```
### **Recent Meals**
To avoid repetition, the app lets you log recent meals. You can add or edit these meals, ensuring you always have fresh ideas.

### **Gamification**
The app tracks the recipes you’ve cooked, creating a personal collection of your culinary achievements. It’s a fun way to stay motivated and explore new dishes.

---

## 🍽️ **Why You’ll Love It**

1. **Personalization**: The app tailors recipes to your unique preferences, making cooking a more enjoyable and stress-free experience.
2. **Efficiency**: No more scrolling through endless recipes. The app does the work for you, saving time and effort.
3. **Health-Conscious**: Whether you’re trying to eat healthier or manage dietary restrictions, the app ensures your meals align with your goals.
4. **Ingredient-Focused**: By using what you already have, the app reduces food waste and helps you get creative in the kitchen.
5. **Image-Based Detection**: The new feature makes it even easier to get started—just snap a photo and let the app do the rest.
6. **Gamification**: Tracking your cooked recipes adds a fun, gamified element to your cooking journey.


---

## 💡 **Behind the Scenes**

For the tech-savvy readers, here’s a quick look at how the app is built:
- **Frontend**: Streamlit for an intuitive and interactive user interface.
- **Backend**: Google’s Gemini API for AI-powered recipe generation.
- **Image Detection**: Gemini-1.5-flash Image to text capabilties.
- **Data Handling**: JSON for structuring recipe data and session state management for persisting user inputs.

---

## 📈 **What’s Next?**

The Smart Recipe Finder is just the beginning. Future updates could include:
- **Real-Time Ingredient Detection**: Use your phone’s camera to detect ingredients in real-time.
- **Meal Planning**: Generate weekly meal plans based on your preferences.
- **Grocery Delivery Integration**: Automatically order missing ingredients from your favorite grocery store.
- **Community Features**: Share your favorite recipes with other users and discover new dishes.
- **Retrieval Augmented Generation (RAG)**: Integrating RAG will allow us to fetch relevant recipes from a vast database, including online sources and even your favorite cookbooks. This will significantly expand the range of recipe suggestions.
- **Web Crawling**: We can implement web crawling to gather real-time information about trending recipes, seasonal ingredients, and local restaurants. 

---

## 🍴 **Cooking Made Smarter** [web App](https://tinkukalluri-smart-recipe-finder-main-widebb.streamlit.app/)


With features like mood-based recipes, dietary customization, and now image-based ingredient detection, the Smart Recipe Finder is your ultimate kitchen companion. Whether you’re looking to save time, reduce food waste, or simply enjoy delicious meals, this app has you covered.

So, what are you waiting for? Grab your phone, snap a pic of your fridge, and let the Smart Recipe Finder work its magic. Happy cooking! 🍳📸

---
## **Links**
- [streamlit app](https://tinkukalluri-smart-recipe-finder-main-widebb.streamlit.app/)
- [Github](https://github.com/tinkukalluri/Smart-Recipe-Finder)
- [linkedin](https://www.linkedin.com/in/abhinandan-kalluri/)

