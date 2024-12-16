import streamlit as st
import pandas as pd
import requests
import pickle

st.set_page_config(page_title="Movie Recommendation System", layout="wide")


# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)


# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]


# Fetch movie posters from TMDB API
def fetch_poster(movie_id):
    api_key = '4a6368a3fe8672217c5b3f5ab4248f57' 
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path





# Title and Header
st.title("🎥 Movie Recommendation System")
st.subheader("Discover movies you'll love based on your preferences!")

# Sidebar for Movie Selection
st.sidebar.header("Search for a Movie")
selected_movie = st.sidebar.selectbox("Select a movie:", movies['title'].values)

# Recommendation Button
if st.sidebar.button('Recommend'):
    # Fetch Recommendations
    recommendations = get_recommendations(selected_movie)
    st.markdown(f"#### Recommended Movies for: **{selected_movie}**")
    
    if len(recommendations) == 0:
        st.error("Sorry, no recommendations found for the selected movie.")
    else:
        # Create a 2x5 grid layout
        for i in range(0, len(recommendations), 5):  # Loop over rows (2 rows, 5 movies each)
            cols = st.columns(5)  # Create 5 columns for each row
            for col, j in zip(cols, range(i, i + 5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    poster_url = fetch_poster(movie_id)
                    with col:
                        st.image(poster_url, width=120)
                        st.markdown(f"**{movie_title}**")
                        st.button("More Info", key=f"info_{movie_id}")

# Add a spacer to push the footer down
for _ in range(15): 
    st.sidebar.write("")


# Footer Section
st.sidebar.markdown("---")
st.sidebar.markdown("**Developed by Achini Sanjula**")
st.sidebar.markdown("📧 Contact: [achini.sna@gmail.com](mailto:achini.sna@gmail.com)")
st.sidebar.markdown("🌟 [GitHub](https://github.com/AchiniSNA) | [LinkedIn](https://linkedin.com/in/achini-sanjula-6811b0266)")
