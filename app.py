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
       for index, (_, institute) in enumerate(recommendations.iterrows()):
          st.write(str(index + 1) + "." + str(institute['Institution_Name']) + "-" + str(institute['Location']) + "-" + str(institute['Region']))
        
st.markdown(
    """
     <style>
     .stApp {
      background-image: url("university_campus.jpg");
      background-size: cover;
      background-repeat: no-repeat;
      background-attachment: fixed;
     }
     </style
    """,
    unsafe_allow_html=True
)
st.markdown("This app is built with ❤️ using Streamlit.")