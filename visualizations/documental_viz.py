import pandas as pd
import ace_tools as tools

def mostrar_candidatos_con_skill(candidatos, skill):
    df = pd.DataFrame(candidatos)
    if not df.empty:
        tools.display_dataframe_to_user(name=f"Candidatos con skill {skill}", dataframe=df)
