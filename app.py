import streamlit as st
import pickle
import math

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Dictionaries for city names, crime types, and populations
city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', 
    '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', 
    '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata', 
    '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur', 
    '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', 
    '2': 'Crime against ST', '3': 'Crime against Senior Citizen', 
    '4': 'Crime against children', '5': 'Crime against women', 
    '6': 'Cyber Crimes', '7': 'Economic Offences', 
    '8': 'Kidnapping', '9': 'Murder'
}

population = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, 
    '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, 
    '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, 
    '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

# Streamlit UI
st.title("Crime Rate Prediction")

# Input fields for user input
city_code = st.selectbox("Select a City", options=list(city_names.keys()), format_func=lambda x: city_names[x])
crime_code = st.selectbox("Select a Crime Type", options=list(crimes_names.keys()), format_func=lambda x: crimes_names[x])
year = st.number_input("Enter the Year", min_value=2011, max_value=2050, step=1, value=2023)

# Predict button
if st.button("Predict Crime Rate"):
    # Calculate population growth
    pop = population[city_code]
    year_diff = int(year) - 2011
    pop = pop + 0.01 * year_diff * pop

    # Make predictions
    crime_rate = model.predict([[year, int(city_code), pop, int(crime_code)]])[0]

    # Determine crime status
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area"

    cases = math.ceil(crime_rate * pop)

    # Display results
    st.subheader("Prediction Results")
    st.write(f"**City:** {city_names[city_code]}")
    st.write(f"**Crime Type:** {crimes_names[crime_code]}")
    st.write(f"**Year:** {year}")
    st.write(f"**Crime Status:** {crime_status}")
    st.write(f"**Predicted Crime Rate:** {crime_rate:.2f}")
    st.write(f"**Estimated Number of Cases:** {cases}")
    st.write(f"**Population (Adjusted for Year):** {pop:.2f} million")
