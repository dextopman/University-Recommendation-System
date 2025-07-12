import streamlit as st
import pandas as pd
import joblib
import warnings
from warnings import filterwarnings
filterwarnings("ignore")


def load_data(file_path):
    data = pd.read_csv(file_path + "/" + "university_data_for_app.csv")
    dataframe = pd.read_csv(file_path + "/" + "university_data_for_app_with_index.csv")
    return data, dataframe

def load_model(file_path):
    cosine_sim = joblib.load(file_path + "/" + "cosine_similarity.pkl")
    return cosine_sim

data, dataframe = load_data(r"F:\UNIVERSITY_RECOMMENDATION_SYSTEM\data")
cosine_sim = load_model(r"F:\UNIVERSITY_RECOMMENDATION_SYSTEM\data")

indices = pd.Series(data.index, index=data['Institution_Name']).drop_duplicates()

def universities_recom(institution_name, cosine_sim=cosine_sim, df=data, indices=indices):
  if institution_name not in indices:
    print("Univeristy not found in the list")
    return pd.DataFrame()

  idx = indices[institution_name]
  ##Getting similarity scores with that institution
  sim_scores = list(enumerate(cosine_sim[idx]))

  # Sort the universities based on similarity rank
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

  # Get the scores of the 19 most similar universities (excluding the input university itself)
  sim_scores = sim_scores[1:20]

  # get the univeristy indices
  university_indices = [i[0] for i in sim_scores]

  # Return the top 20 most similar universities
  return df.iloc[university_indices]




st.set_page_config(page_title="university search", layout="centered")

st.title("Universities Search App 💻📚🎓")

st.write("Find the best higher institutes for your studies! 🌍")

institutes = data['Institution_Name'].sort_values().tolist()

selected_institution = st.selectbox("Select a university", institutes)

if st.button("Get similar institutions"):
    if selected_institution:
        recommendations = universities_recom(selected_institution, cosine_sim, data, indices)

        st.subheader("Similar Institutions to: " + selected_institution)
        num_cols = 3  # Number of columns in the grid
        cols = st.columns(num_cols)
        for idx, (_, institute) in enumerate(recommendations.iterrows()):
            col = cols[idx % num_cols]
            with col:
                st.markdown(
                    f'''
                    <div style="background: rgba(255,255,255,0.85); border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); min-height: 100px;">
                        <b>{idx + 1}. {institute['Institution_Name']}</b><br>
                        {institute['Location']}<br>
                        {institute['Region']}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1590579491624-f98f36d4c763?q=80&w=1443&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-color: #f0f2f5;
        color: #333;
        }
     
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("This app is built with ❤️ using Streamlit.")