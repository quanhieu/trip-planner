# travel_ui.py
import streamlit as st
import requests
import datetime

st.title("Trip Planner Application")

# Input form
with st.form(key='trip_form'):
    destination = st.text_input("Where would you like to go?", "Da Nang")
    start_date = st.date_input("Departure date", datetime.date.today())
    end_date = st.date_input("Return date", datetime.date.today() + datetime.timedelta(days=3))
    num_people = st.number_input("Number of people", min_value=1, value=2)
    budget_per_person = st.number_input("Budget per person (VND)", min_value=100000, value=500000, step=100000)
    submit_button = st.form_submit_button(label='Plan Trip')

if submit_button:
    payload = {
        "destination": destination,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "num_people": num_people,
        "budget_per_person": budget_per_person
    }
    st.info("Creating your travel plan, please wait...")
    try:
        # Call Orchestrator Agent (port 8000)
        response = requests.post("http://localhost:8000/run", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        st.success("Your travel plan is ready!")
        
        st.subheader("Itinerary:")
        itinerary = result.get("itinerary", [])
        if itinerary:
            for day in itinerary:
                st.write(f"**Day {day.get('day', '')}:**")
                for activity in day.get("activities", []):
                    st.write(f"- *{activity.get('time', '')}*: {activity.get('activity', '')}")
        else:
            st.write("No detailed itinerary available.")
        
        st.subheader("Meal Plan:")
        meals = result.get("meals", [])
        if meals:
            for meal in meals:
                st.write(f"**Day {meal.get('day', '')}:** Lunch - {meal.get('lunch', '')} | Dinner - {meal.get('dinner', '')}")
        else:
            st.write("No detailed meal plan available.")
        
        st.subheader("Accommodation Suggestions:")
        stays = result.get("stays", {})
        if stays:
            st.write(f"- **Name**: {stays.get('name', '')}")
            st.write(f"- **Price/night**: {stays.get('price_per_night', '')} VND")
            st.write(f"- **Notes**: {stays.get('note', '')}")
        else:
            st.write("No accommodation suggestions available.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
