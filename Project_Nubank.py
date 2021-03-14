import dash
import dash_table

import plotly.express as px
import pandas as pd 
import dash_html_components as html
import dash_core_components as dcc 
from dash.dependencies import Output,Input

#Leitura das faturas de cada mês e adição da coluna 'Month' referente ao mês de pagamento
df_Jan_2020=pd.read_csv('nubank-2020-01.csv')
df_Jan_2020['Month']=['Jan']*df_Jan_2020.shape[0]
df_Fev_2020=pd.read_csv('nubank-2020-02.csv')
df_Fev_2020['Month']=['Fev']*df_Fev_2020.shape[0]
df_Mar_2020=pd.read_csv('nubank-2020-03.csv')
df_Mar_2020['Month']=['Mar']*df_Mar_2020.shape[0]
df_Abr_2020=pd.read_csv('nubank-2020-04.csv')
df_Abr_2020['Month']=['Abr']*df_Abr_2020.shape[0]
df_Mai_2020=pd.read_csv('nubank-2020-05.csv')
df_Mai_2020['Month']=['Mai']*df_Mai_2020.shape[0]
df_Jun_2020=pd.read_csv('nubank-2020-06.csv')
df_Jun_2020['Month']=['Jun']*df_Jun_2020.shape[0]
df_Jul_2020=pd.read_csv('nubank-2020-07.csv')
df_Jul_2020['Month']=['Jul']*df_Jul_2020.shape[0]
df_Ago_2020=pd.read_csv('nubank-2020-08.csv')
df_Ago_2020['Month']=['Ago']*df_Ago_2020.shape[0]
df_Set_2020=pd.read_csv('nubank-2020-09.csv')
df_Set_2020['Month']=['Set']*df_Set_2020.shape[0]
df_Out_2020=pd.read_csv('nubank-2020-10.csv')
df_Out_2020['Month']=['Out']*df_Out_2020.shape[0]
df_Nov_2020=pd.read_csv('nubank-2020-11.csv')
df_Nov_2020['Month']=['Nov']*df_Nov_2020.shape[0]
df_Dez_2020=pd.read_csv('nubank-2020-12.csv')
df_Dez_2020['Month']=['Dez']*df_Dez_2020.shape[0]
#União de todas as faturas
df_2020=pd.concat([df_Jan_2020,df_Fev_2020,df_Mar_2020,df_Abr_2020
                  ,df_Mai_2020,df_Jun_2020,df_Jul_2020,df_Ago_2020,
                  df_Set_2020,df_Out_2020,df_Nov_2020,df_Dez_2020])
#Definição como 'Aleatório' todas as categorias não identificadas pela empresa                  
df_2020['category'].fillna('Aleatório',inplace=True)
#Exclusão dos valores negativos que se tratam de pagamentos já realizados
df_2020.drop(df_2020[df_2020['amount']<0].index,inplace=True)
#DataFrame com a soma total de cada "title" para a formação da Tabela
df2020_Total_Title=df_2020.groupby(['title','category','Month']).amount.sum().to_frame().reset_index()







app=dash.Dash(__name__)




app.layout=html.Div([
    html.H1("Dahsboard Fatura Nubank 2020",style={'text-align':'center','color':'#354154'}),
    dcc.Dropdown(id='select_month',options=[{'label':i,'value':i} for i in df_2020['Month'].unique()]),
    html.Div(id='total_fatura',style={'position':'relative','top':'5px','color':'#354154','font-size':'30px','font-weight':'bold'}),
    html.Div([dcc.Graph(id="my-graph",figure=px.bar(df2020_Total_Title,x='amount',y='category'))],style={'backgroundColor':'#AF30D2','float':'left'}),
    html.Div([dash_table.DataTable(
    id='table',
    columns=[{"name":i,"id":i} for i in df2020_Total_Title.columns],
    data=df2020_Total_Title.to_dict('records'),
    style_cell={'padding':'3px'})],style={'float':'left','position':'relative','top':'60px','width':'45%'})
])

@app.callback(
    Output(component_id='my-graph',component_property='figure'),
    Output(component_id='table',component_property='data'),
    Output(component_id='total_fatura',component_property='children'),
    Input(component_id='select_month',component_property='value')
)

def interactive_graphing(month_select):
    dff=df2020_Total_Title[df2020_Total_Title['Month']==month_select]
    fig=px.bar(data_frame=dff,x='amount',y='category')
    Total=dff['amount'].sum()
    

    return fig,dff.to_dict('records'),'Total da Fatura do Mês:{}'.format(round(Total,2))





if __name__=="__main__":
    app.run_server()