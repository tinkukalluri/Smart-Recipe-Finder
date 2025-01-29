import streamlit as st
import google.generativeai as genai
import json
from PIL import Image
# Initialize Gemini API
genai.configure(api_key="AIzaSyB5r8XQy5pHg7GWBK3qhd6nuwV5epAqZ0k")
model = genai.GenerativeModel("gemini-1.5-flash")

# App Title
st.title("Smart Recipe Finder 🍳")
st.subheader("Find recipes based on your mood, preferences, and what's in your fridge!")

# Sidebar for User Inputs
st.sidebar.header("User Preferences")

# User Preferences
mood = st.sidebar.selectbox("What's your mood?", ["Happy", "Tired", "Adventurous", "Lazy", "Excited", "Stressed", "Relaxed"], index=0)
cuisine = st.sidebar.selectbox("Preferred Cuisine", ["No Preference", "Italian", "Indian", "Mexican", "Chinese", "Japanese", "Mediterranean", "Thai", "Middle Eastern", "American"], index=0)
time = st.sidebar.slider("Time Available (minutes)", 5, 120, 30)
skill = st.sidebar.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=0)


# Initialize session state for tracking selected values
if 'appliances' not in st.session_state:
    st.session_state.appliances = ["None"]
if 'dietary_restrictions' not in st.session_state:
    st.session_state.dietary_restrictions = ["None"]
if 'allergies' not in st.session_state:
    st.session_state.allergies = ["None"]
if 'health_goals' not in st.session_state:
    st.session_state.health_goals = ["None"]
if "vegetables" not in st.session_state:
    st.session_state.vegetables =  "eggs, tomatoes, cheese, onions"

# Available Appliances
appliances = st.sidebar.multiselect(
    "Available Appliances", 
    ["None", "Oven", "Air Fryer", "Blender", "Microwave", "Slow Cooker", "Pressure Cooker", "Rice Cooker", "Grill", "Induction Stove"],
    default=st.session_state.appliances
)

# Dietary Preferences/Restrictions
dietary_restrictions = st.sidebar.multiselect(
    "Dietary Restrictions", 
    ["None", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Carb", "Low-Sugar", "Halal", "Kosher", "Paleo", "Keto"],
    default=st.session_state.dietary_restrictions
)

# Allergies
allergies = st.sidebar.multiselect(
    "Food Allergies", 
    ["None", "Peanuts", "Shellfish", "Eggs", "Dairy", "Gluten", "Soy", "Tree Nuts", "Wheat", "Fish", "Sesame"],
    default=st.session_state.allergies
)

# Health Goals
health_goals = st.sidebar.multiselect(
    "Health Goals", 
    ["None", "Weight Loss", "Muscle Gain", "Heart Health", "Blood Sugar Control", "Boost Immunity", "Improve Digestion", "Increase Energy", "Healthy Skin"],
    default=st.session_state.health_goals
)

# Remove "None" if the user selects anything else
if "None" in appliances and len(appliances) > 1:
    appliances.remove("None")
if "None" in dietary_restrictions and len(dietary_restrictions) > 1:
    dietary_restrictions.remove("None")
if "None" in allergies and len(allergies) > 1:
    allergies.remove("None")
if "None" in health_goals and len(health_goals) > 1:
    health_goals.remove("None")

# Save the current selections to session state to persist them across reruns
st.session_state.appliances = appliances
st.session_state.dietary_restrictions = dietary_restrictions
st.session_state.allergies = allergies
st.session_state.health_goals = health_goals

# Recent Meals (to avoid repetition)
recent_meals = st.session_state.get("recent_meals", [])
new_meal = st.sidebar.text_area("Add or Edit Recent Meal", "")

if st.sidebar.button("Add to Recent Meals"):
    if new_meal.strip():  # Ensure the input is not empty
        if new_meal not in [meal['name'] for meal in recent_meals]:
            recent_meals.append({"name": new_meal})
            if len(recent_meals) > 5:  # Limit to 5 recent meals
                recent_meals.pop(0)
            st.session_state["recent_meals"] = recent_meals
            st.sidebar.success(f"Meal '{new_meal}' added to recent meals!")
        else:
            st.sidebar.warning(f"Meal '{new_meal}' is already in your recent meals.")
    else:
        st.sidebar.warning("Please enter a valid meal name.")

# Display Recent Meals
if recent_meals:
    st.write("### Recent Meals")
    for meal in recent_meals:
        st.write(f"- {meal['name']}")

# Main Input Section
st.write("### Ingredients Available in Your Fridge")
ingredients = st.text_area("List the ingredients (comma-separated)", st.session_state.vegetables)
st.session_state.vegetables = ingredients
st.subheader("           OR          ")
# Upload image
uploaded_file = st.file_uploader("Upload an image of fruits and vegetables", type=["jpg", "jpeg", "png"])



# Initialize session state for recipes and viewed recipe
if 'viewed_recipe' not in st.session_state:
    st.session_state.viewed_recipe = None  # Store the selected recipe index
if 'recipes' not in st.session_state:
    st.session_state.recipes = []  # Store fetched recipes


if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Use Gemini model to analyze the image
    response = model.generate_content(
        contents=[
            """
                Identify all the fruits and vegetables in this image. Return only the names of the fruits and vegetables, separated by commas.
                return the results with comma seperated values
            """,
            image
        ]
    )

    # Display the results
    st.subheader("Identified Fruits and Vegetables:")
    st.write(response.text)
    st.session_state.vegetables = response.text


# Button to fetch recipes
if st.button("Find Recipes"):
    # Call the Gemini API
    prompt = f""" 
        Suggest 3 recipes based on the following:
        - Mood: {mood}
        - Cuisine Preference: {cuisine}
        - Time Available: {time} minutes
        - Skill Level: {skill}
        - Available Ingredients: {st.session_state.vegetables}
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
    print("Prompt:", prompt)
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

# Display Recipes (only if they exist)
if "recipes" in st.session_state:
    st.write("### Recommended Recipes:")
    for i, recipe in enumerate(st.session_state.recipes, start=1):
        st.write(f"**{i}. {recipe['name']}**")
        st.write(f"Prep Time: {recipe['prep_time']} minutes")
        st.write(f"Missing Ingredients: {', '.join(recipe['missing_ingredients'])}")
        st.write(f"Nutritional Information: Calories: {recipe['nutritional_info']['calories']}, Protein: {recipe['nutritional_info']['protein']}g, Carbs: {recipe['nutritional_info']['carbs']}g, Fat: {recipe['nutritional_info']['fat']}g")
        
        # Display Shopping List
        if recipe["shopping_list"]:
            st.write("### Shopping List for Missing Ingredients:")
            for item in recipe["shopping_list"]:
                st.write(f"- {item}")

        # When the button is clicked, store the selected recipe index in session state
        if st.button(f"View Recipe", key = "View Recipe: "+str(i)):
            st.session_state.viewed_recipe = i

            # Create a collapsible section (Expander) to display recipe instructions
            selected_recipe = st.session_state.recipes[st.session_state.viewed_recipe - 1]
            with st.expander(f"Instructions for {selected_recipe['name']}", expanded=True):
                st.write(selected_recipe["instructions"])

        # Mark Recipe as Cooked button for each recipe
        if st.button(f"Mark Recipe as Cooked", key = "Mark Recipe as Cooked: "+str(i)):
            if st.session_state.viewed_recipe == i:  # Ensure the button is clicked after viewing the recipe
                recipe_name = recipe["name"]
                if recipe_name not in st.session_state.cooked_recipes:
                    st.session_state.cooked_recipes.append(recipe_name)
                    st.success(f"Recipe '{recipe_name}' marked as cooked!")
                else:
                    st.warning(f"You've already marked '{recipe_name}' as cooked.")

# Additional Features
# Gamification: Track recipes cooked
if 'cooked_recipes' not in st.session_state:
    st.session_state.cooked_recipes = []

if st.button("Mark Recipe as Cooked"):
    if st.session_state.viewed_recipe:
        recipe_name = st.session_state.recipes[st.session_state.viewed_recipe - 1]["name"]
        if recipe_name not in st.session_state.cooked_recipes:
            st.session_state.cooked_recipes.append(recipe_name)
            st.success(f"Recipe '{recipe_name}' marked as cooked!")
        else:
            st.warning(f"You've already marked '{recipe_name}' as cooked.")

# Display cooked recipes
if st.session_state.cooked_recipes:
    st.write("### Recipes You've Cooked:")
    for recipe in st.session_state.cooked_recipes:
        st.write(f"- {recipe}")
