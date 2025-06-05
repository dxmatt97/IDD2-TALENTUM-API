import pandas as pd
import ace_tools as tools

def mostrar_procesos_filtrados(df, estado):
    if not df.empty:
        tools.display_dataframe_to_user(name=f"Procesos en estado {estado}", dataframe=df)
