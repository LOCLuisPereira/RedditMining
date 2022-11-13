'''
'random',
'grid',
'circle',
'concentric',
'breadthfirst',
'cose',
'cose-bilkent',
'dagre',
'cola',
'klay',
'spread',
'euler'
'''

def f( s ) :
    return s.decode()

from pymongo import MongoClient
from decouple import config
from dash import Dash, html
from bson import ObjectId


import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import redis
import dash




r = redis.Redis(db=config('REDIS_DB'))
client = MongoClient(config('MONGO_URL'))

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)




content = []








content.append(
    html.P('Medium Social Media Mining Project',
    style={
        'text-align' : 'center',
        'font-family' : 'georgia',
        'font-size' : '30px'
    })
)


num = client['test']['test'].count_documents({})
content.append(
    dbc.Alert([
        html.A('Information coming from '),
        html.A(f'{num}', style={'font-size':'30px'}),
        html.A(' reddit posts.')
    ], color='warning', style={'text-align':'center'} )
)








xs = []
for k, v in r.hgetall('count').items() :
    xs.append(( f(k), f(v) ))
xs.sort(key=lambda x : x[1], reverse=True)
xss = [
    html.Tr([html.Td(k), html.Td(v)]) for k, v in xs
]




dif_subs = len(xs)
print(dif_subs)





table_header = [
    html.Thead(html.Tr([html.Th("Subreddit"), html.Th("Count")]))
]

table_body = [html.Tbody(xss)]

table = dbc.Table(table_header + table_body, bordered=True)


cyto.load_extra_layouts()

network = cyto.Cytoscape(
    id='Example',
    layout={'name' : 'klay'},
    elements=[
        {'data':{'id':str(i),'label':k}} for i, (k,v) in enumerate(xs)
    ],
    style={'width':'100%', 'height':'100%'},
    stylesheet=[{
        'selector' : 'node',
        'style' : {
            'content' : 'data(label)',
            'font-size' : '5px',
            'text-halign' : 'center',
            'text-valign' : 'center',
            'background-color' : 'orange'
        }
    }]
)





import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dcc

df = pd.DataFrame.from_dict({
    'names' : [x for x,_ in xs],
    'count' : [y for _, y in xs]
})
fig = px.treemap(
    df,
    path=[px.Constant('all'),'count','names'],
    values='count',
    #hover_name='names',
    #hover_data=['names']
    width=700,
    height=700
)


content.append(
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                    html.A('In the mining process, '),
                    html.A(f'{dif_subs}', style={'font-size':'30px'}),
                    html.A(' different subreddits were found.')
                ],
                color='warning',
                style={'text-align':'center'}
            ),
            html.Div([table], style={'height':'60vh','overflow' : 'scroll'}, className='border')
        ]),
        #dbc.Col([dcc.Graph(figure=fig)], style={'height':'75vh'}, className='')
        dbc.Col([network], style={'height':'75vh'}, className='')
    ])
)





app.layout = html.Div(
    dbc.Container(content, className='pt-4')
)


if __name__ == "__main__":
    app.run_server(debug=True)