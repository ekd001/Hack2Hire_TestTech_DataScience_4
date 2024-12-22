import dash
from dash import dcc, html, Input, Output, State
import requests

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Scoring credit"),
    html.Div([
        dcc.Input(id="age", type="number", placeholder="Age", style={'marginBottom': '10px', "width":"300px", "height":"40px",
         "border-width":"2px"}),
        dcc.Input(id="credit_amount", type="number", placeholder="Montant du crédit", style={'marginBottom': '10px', "width":"300px",
         "height":"40px", "border-width":"2px"}),
        dcc.Input(id="duration", type="number", placeholder="Durée du crédit (en mois)", style={'marginBottom': '10px', "width":"300px",
         "height":"40px", "border-width":"2px"})
    ], style={"display":"flex", "flex-direction":"column"}),
    

    dcc.Dropdown(
        id="housing",
        options=[
            {'label': 'Libre', 'value': 'free'},
            {'label': 'Propre à vous', 'value': 'own'},
            {'label': 'Louer', 'value': 'rent'}
        ],
        placeholder="Type de logement",
        style={'marginBottom': '10px', "height":"50px", "width":"400px" ,"border-width":"2px"}
    ),
    
    dcc.Dropdown(
        id="saving_accounts",
        options=[
            {'label': 'Peu', 'value': 'little'},
            {'label': 'Moyen', 'value': 'moderate'},
            {'label': 'Elevé', 'value': 'rich'}
        ],
        placeholder="Compte d'épargne",
        style={'marginBottom': '10px', "height":"50px", "width":"400px", "border-width":"2px"}
    ),

    html.Button("Prédire", id="predict_button", n_clicks=0, style={'marginBottom': '10px', 'width':'200px', 'height':'50px',
                'cursor':'pointer'}),
     html.H4("Résultat"),

    html.Div(id="output")

])

@app.callback(
    dash.dependencies.Output("output", "children"),
    [Input("predict_button", "n_clicks")],
    [
        Input("age", "value"),
        Input("credit_amount", "value"),
        Input("duration", "value"),
        Input("housing", "value"),
        Input("saving_accounts", "value")
    ]
)

def update_prediction(n_clicks, age, credit_amount, duration, housing, saving_accounts):
    if n_clicks > 0 and all([age, credit_amount, duration, housing, saving_accounts]):
        data = {
            "age": age,
            "credit_amount": credit_amount,
            "duration": duration,
            "housing": housing,
            "saving_accounts": saving_accounts
        }

        response = requests.post(f"http://127.0.0.1:8000/predict", json=data)

        if response.status_code == 200:
            prediction = response.json()
            if(prediction["prediction"]):
                return html.P("Le risque est bon pour l'accord de crédit", style={})
            else:
                return html.P("Le risque est mauvais pour l'accord de crédit")
        else:
            return html.P("Le risque est mauvais pour l'accord de crédit")
        

if __name__ == "__main__":
    app.run_server(debug=True)