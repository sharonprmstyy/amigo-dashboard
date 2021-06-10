import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from apps import omset_pt, customer_pt

AMIGO_LOGO='https://amigogroup.co.id/wp-content/uploads/2021/04/Pin-1.png'

navbar = dbc.Navbar([
    dbc.Col(
        html.A(
            html.Img(src=AMIGO_LOGO, height='30px'), href='/'
        ),width=1, style={'margin-left':'10px'}
    ),
    dbc.Col(
        dbc.NavbarBrand(id='navbrand'),width=2),
    dbc.Col(
    #     dbc.Input(type='search', placeholder='Search here ...'),
             width=8),
    dbc.Col(
        dbc.DropdownMenu(
            label='Menu',
            children=[
                dbc.DropdownMenuItem("Dashboard", header=True),
                dbc.DropdownMenuItem("Penjualan Tunai", href="/dashboard/penjualan"),
                dbc.DropdownMenuItem("Pelanggan Tunai", href="/dashboard/pelanggan")
            ],
            right=True,
            color='primary'
        ),width=1
    )
],  color='primary',
    dark=True,
    style={'width': '100%','position':'fixed', 'zIndex':'3', 'top':'0'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', children=[])
],
    style={"width": "100%"})

menu = html.Div([
    html.Div(id='breadcrumbs'),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.CardLink(
                    dbc.Card([
                        html.Div(
                            dbc.CardImg(src=app.get_asset_url('penjualan.png')
                                        , top=True
                                        , style={'width': '150px', 'height': '150px',
                                                 'align-item': 'center', 'justify-content': 'center'}),
                            style={'textAlign':'center','margin-top':'30px'}),
                        dbc.CardBody([
                            html.H4('Dashboard Penjualan', className='card-Title', style={'textAlign':'center'}),
                            html.P('Dashboard berisi visualisasi penjualan yang terjadi', style={'color': 'black', 'textAlign':'center'})
                        ])
                    ]),
                    href='/dashboard/penjualan'
                ),className='btn btn-outline-secondary'
            ),
            dbc.Col(
                dbc.CardLink(
                    dbc.Card([
                        html.Div(
                        dbc.CardImg(src=app.get_asset_url('pelanggan.png')
                                    , top=True
                                    , style={'width': '150px', 'height': '150px',
                                             'align-item':'center', 'justify-content':'center'}),
                            style={'textAlign':'center','margin-top':'30px'}),
                        dbc.CardBody([
                            html.H4('Dashboard Pelanggan', className='card-Title', style={'textAlign':'center'}),
                            html.P('Dashboard berisi visualisasi pelanggan yang berbelanja', style={'color': 'black', 'textAlign':'center'})
                        ])
                    ]),
                    href='/dashboard/pelanggan'
                ),className='btn btn-outline-secondary'
            )
        ])
    ], style={'margin-top': '200px','align-item':'center', 'justify-content':'center'})
])

@app.callback(
    Output('page-content', 'children'),
    # Output('bc-omset','children'),
    # Output('bc-cust','children'),
    Output('navbrand','children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    home = html.Div([
        dcc.Location(id='url', refresh=True),
        menu
    ])
    if pathname == '/dashboard/penjualan':
        return omset_pt.layout, 'Dashboard Penjualan Tunai'
    if pathname == '/dashboard/pelanggan':
        return customer_pt.layout, 'Dashboard Pelanggan Tunai'
    else:
        return home, 'ABC Group'

if __name__ == '__main__': app.run_server(debug=False)
