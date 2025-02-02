import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Sample user profiles data
user_profiles = [
    {'id': 1, 'age': 25, 'location': 'New York', 'education': 'Masters', 'interests': 'Music, Travel'},
    {'id': 2, 'age': 30, 'location': 'Los Angeles', 'education': 'Bachelors', 'interests': 'Sports, Music'},
    {'id': 3, 'age': 28, 'location': 'Chicago', 'education': 'Masters', 'interests': 'Travel, Cooking'},
    {'id': 4, 'age': 35, 'location': 'New York', 'education': 'PhD', 'interests': 'Reading, Travel'},
]

# Convert user profiles to DataFrame
profiles_df = pd.DataFrame(user_profiles)

# Feature engineering: Convert categorical features into numerical values
profiles_df['location'] = profiles_df['location'].astype('category').cat.codes
profiles_df['education'] = profiles_df['education'].astype('category').cat.codes
profiles_df['interests'] = profiles_df['interests'].astype('category').cat.codes

# Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(profiles_df[['age', 'location', 'education', 'interests']])

# Calculate cosine similarity
similarity_matrix = cosine_similarity(scaled_features)

# Function to get matches for a user
def get_matches(user_id, similarity_matrix, profiles_df):
    user_index = profiles_df[profiles_df['id'] == user_id].index[0]
    similar_indices = similarity_matrix[user_index].argsort()[::-1][1:]
    matches = profiles_df.iloc[similar_indices]
    return matches

# Example usage
user_id_to_match = 1
matched_profiles = get_matches(user_id_to_match, similarity_matrix, profiles_df)
print(f'Matched profiles for user {user_id_to_match}:
', matched_profiles)
