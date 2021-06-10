import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
from dash.dependencies import Input, Output
from app import app

# conn=create_engine('mysql+pymysql://root:@localhost/amigodw')
# conn = create_engine('mysql+pymysql://admindw:admindw@10.10.14.5/amigodw')
# conn=create_engine('mysql+pymysql://admindw:admindw@192.168.1.1/amigodw')
conn = create_engine('mysql+pymysql://admindw:admindw@10.10.10.38/amigodw')

df_toko = pd.read_sql('select nama_toko from dim_TOKO', conn)
df_cust = pd.read_sql('select jns_customer from dim_CUSTOMER', conn)
df_strip = pd.read_sql('select kode_strip, kel_jns from dim_STRIP', conn)
kedprod = ['Kategori', 'Lini']
jenis_transaksi = ['TUNAI', 'BON']
toko_all = df_toko['nama_toko'].unique()
jns_cust = df_cust['jns_customer'].unique()
kategori_all = df_strip['kel_jns'].dropna().unique()
lini_all = df_strip['kode_strip'].dropna().unique()
frek = {'Harian':'tglnota',
        'Mingguan':'str_to_date(concat(yearweek(tglnota),"Sunday"), "%%X%%V %%W")',
        'Bulanan':'str_to_date(concat(date_format(tglnota,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
        'Kuartal':'dw.kuartal',
        'Semester':'dw.semester',
        'Tahunan':'dw.tahun',
        'Sekolah':'dw.sekolah',
        'Puasa':'dw.puasa',
        'Sisa Puasa':'dw.sisa_puasa',
        'Nyadran':'dw.nyadran',
        'Rasulan':'dw.rasulan',
        'Suro':'dw.suro',
        'Natal':'dw.natal'}

breadcrumb = html.Div(html.Ol([
    html.Li(
        html.A('Home',href='/'),
        className='breadcrumb-item'
    ),
    html.Li(
        html.P('Dashboard Penjualan'),
        className='breadcrumb-item'
    )
], className='breadcrumb'),
    id='bc-omset',
    style={'height':'50%','width':'101%','border-radius':'0px','margin-left':'-5px','margin-top':'-10px'}
)

fltrPT = dbc.Card([
    breadcrumb,
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Range Tanggal :"),
                    dcc.DatePickerRange(
                        id="tglPT",
                        start_date_id="startTglPT",
                        end_date_id="endTglTarget",
                        start_date=date(2013, 1, 1),
                        end_date=date(2015, 1, 1),
                        display_format='YYYY-MM-DD',
                        style={'fontSize': '50%', 'height': '120%', 'margin':'-5px'}
                    )
                ])
            ],className='card border-secondary mb-3',style={'height':'100px','width':'120%'})
        ], style={'height': '4rem'}),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Frekuensi Pengukuran :"),
                    dcc.Dropdown(
                        id='filterFrekPT',
                        options=[{'label': i, 'value': i} for i in frek],
                        placeholder='Frekuensi',
                        value=frek['Bulanan'],
                        clearable=False,
                        style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'}
                    )
                ])
            ],className='card border-secondary mb-3',style={'height':'100px','width':'90%','margin-left':'20%'})
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Toko :"),
                    dcc.Dropdown(
                        id='filterTokoPT',
                        options=[{'label': i, 'value': i} for i in toko_all],
                        placeholder='Toko',
                        value=[],
                        multi=True,
                        style={'fontSize': '110%', 'height': '120%','margin':'-5px'}
                    )
                ])
            ],className='card border-secondary mb-3',style={'height':'100px','width':'90%','margin-left':'10%'})
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Kedalaman Pengukuran :"),
                    dcc.RadioItems(
                        id='filterDepthPT',
                        options=[{'label': i, 'value': i} for i in kedprod],
                        labelStyle={'margin': 'auto', 'padding': '10px'},
                        style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'},
                        value='Kategori'
                    )
                ])
            ],className='card border-secondary mb-3',style={'height':'100px'})
        ]),
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Kategori :"),
                        dcc.Dropdown(
                            id='ddKategori',
                            options=[{'label': i, 'value': i} for i in kategori_all],
                            placeholder='Kategori',
                            value=[],
                            multi=True,
                            style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'}
                        )
                    ])
                ],className='card border-secondary mb-3',style={'height':'100px'})
            ], id='divKategori'),
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Lini :"),
                        dcc.Dropdown(
                            id='ddLini',
                            options=[{'label': i, 'value': i} for i in lini_all],
                            placeholder='Lini',
                            value=[],
                            multi=True,
                            style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'}
                        )
                    ])
                ],className='card border-secondary mb-3',style={'height':'100px'})
            ], id='divLini')
        ])
    ], no_gutters=True)
], style={'width':'100%','height':'100px'})

cardTunai = dbc.Card(
    dbc.Spinner([
        html.P('Jumlah Penjualan Tunai',
               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
        html.P(
            id='tunaiPT',
            style={'fontSize': '220%', 'text-align': 'center'}),
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.P('Jual',
                               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
                        html.P(
                            id='jualtunai',
                            style={'fontSize': '200%', 'text-align': 'center'})
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        html.P('Obral',
                               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
                        html.P(
                            id='obraltunai',
                            style={'fontSize': '200%', 'text-align': 'center'}),
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        html.P('Retur',
                               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
                        html.P(
                            id='returtunai',
                            style={'fontSize': '200%', 'text-align': 'center'}),
                    ])
                ])
            ], no_gutters=True)
        )
    ],color='danger')
)

cardBon = dbc.Card(
    dbc.Spinner([
        html.P('Jumlah Penjualan Bon',
               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
        html.P(
            id='bonPT',
            style={'fontSize': '220%', 'text-align': 'center'}),
        dbc.CardBody(
            dbc.Row(
                dbc.Col([
                    dbc.Card([
                        html.P('Retur',
                               style={'fontSize': '110%', 'text-align': 'center', 'margin-top': '1em'}),
                        html.P(
                            id='returbon',
                            style={'fontSize': '200%', 'text-align': 'center'}),
                    ])
                ])
            )
        )
    ],color='danger')
)

cardTarget = dbc.Card(
    dbc.Spinner([
        html.P('Pencapaian Target Omset',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='targetPT',
        )
    ],color='danger')
)

cardPertumbuhan = dbc.Card(
    dbc.Spinner([
        html.P('Pertumbuhan Omset',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='growthPT',
        )
    ],color='danger')
)

cardRasioTunai = dbc.Card(
    dbc.Spinner([
        html.P('Rasio Omset Tunai',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em','margin-bottom':'0px'}),
        html.Div(
            dcc.RadioItems(
                options=[
                    {'label': 'Kategori', 'value': 'kel_jns'},
                    {'label': 'Lini', 'value': 'kode_strip'},
                    {'label': 'Toko', 'value': 'nama_toko'}
                ],
                id='radioTunai',
                labelStyle={'margin':'10px','margin-top':'0px'},
                value='nama_toko',
            ),style={'textAlign':'center'}
        ),
        dcc.Graph(
            id='rasioTunaiPT',
        )
    ],color='danger')
)

cardRasioBon = dbc.Card(
    dbc.Spinner([
        html.P('Rasio Omset Bon',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em','margin-bottom':'0px'}),
        html.Div(
            dcc.RadioItems(
                options=[
                    {'label': 'Kategori', 'value': 'kel_jns'},
                    {'label': 'Lini', 'value': 'kode_strip'},
                    {'label': 'Toko', 'value': 'nama_toko'}
                ],
                id='radioBon',
                labelStyle={'margin':'10px','margin-top':'0px'},
                value='nama_toko',
            ),style={'textAlign':'center'}
        ),
        dcc.Graph(
            id='rasioBonPT',
        )
    ],color='danger')
)

cardKNK = dbc.Card(
    dbc.Spinner([
        html.P('Pencapaian Total Omset Supplier',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='growthSupPT',
        )
    ],color='danger')
)

cardOmsetK = dbc.Card(
    dbc.Spinner([
        html.P('Rasio Omset Konsinyasi',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='rasioKPT',
        )
    ],color='danger')
)

cardOmsetNK = dbc.Card(
    dbc.Spinner([
        html.P('Rasio Omset Non Konsinyasi',
               style={'fontSize': '110%', 'height': '120%', 'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='rasioNKPT',
        )
    ],color='danger')
)

dashPTunai = dbc.Container([
    dbc.Row([dbc.Col([cardTunai]),
             dbc.Col([cardBon])],
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
    dbc.Row(dbc.Col([cardPertumbuhan]),
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
    dbc.Row([dbc.Col([cardRasioTunai], width=6),
             dbc.Col([cardRasioBon], width=6)],
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
    dbc.Row(dbc.Col([cardKNK]),
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
    dbc.Row([dbc.Col([cardOmsetK], width=6),
             dbc.Col([cardOmsetNK], width=6)],
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
],fluid=True, style={'top':'10em'})

layout = html.Div([
    html.Div([fltrPT],
            style={'width':'100%',
                   'top':'0',
                   'margin-top':'50px',
                   'zIndex':'2',
                   'position':'fixed'}),
    html.Div([dashPTunai],
             style={'margin-top':'220px'})
])

@app.callback(
    Output('filterFrekPT', 'options'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'))
def changeFrekPT(start, end):
    range = (date.fromisoformat(end) - date.fromisoformat(start))
    if range.days < 14:
        return [{'label': i, 'value': frek[i]} for i in frek if i in ('Harian')]
    elif range.days < 60:
        return [{'label': i, 'value': frek[i]} for i in frek if i in ('Harian', 'Mingguan')]
    elif range.days < 180:
        return [{'label': i, 'value': frek[i]} for i in frek if i in ('Harian','Mingguan','Bulanan')]
    elif range.days < 365:
        return [{'label': i, 'value': frek[i]} for i in frek if i in ('Harian','Mingguan','Bulanan','Kuartal')]
    elif range.days < 720:
        return [{'label': i, 'value': frek[i]} for i in frek if i not in ('Tahunan','Puasa','Sisa Puasa','Nyadran','Rasulan','Suro','Natal')]
    else:
        return [{'label': i, 'value': frek[i]} for i in frek]


@app.callback(
    Output('divKategori', 'style'),
    Output('ddKategori', 'value'),
    Output('divLini', 'style'),
    Output('ddLini', 'value'),
    Input('filterDepthPT', 'value'))
def changeFltrDepth(pilDepth):
    if pilDepth == 'Kategori':
        return {'display': 'block'}, [], \
               {'display': 'none'}, []
    else:
        return {'display': 'none'}, [], \
               {'display': 'block'}, []


# jum transaksi tunai
@app.callback(
    Output('tunaiPT', 'children'),
    Output('jualtunai', 'children'),
    Output('obraltunai', 'children'),
    Output('returtunai', 'children'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def tunaiPT(start, end, frek, lini, kategori, toko):
    dft = pd.read_sql('''
                    select
                        status,
                        count(distinct no_nota) as jumltr
                    from fact_PENJUALAN fp
                    inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                    inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                    inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                    where (tglnota between %(start)s and %(end)s)
                        and jenis_transaksi='TUNAI'
                        and ds.kode_strip in %(lini)s
                        and ds.kel_jns in %(kategori)s
                        and dt.nama_toko in %(toko)s
                        and {season} != %(frek)s 
                    group by status'''.format(season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                    params={
                        'start': start, 'end': end,
                        'frek':'-' if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else '1',
                        'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                        'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                        'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)})
    if(len(dft['status'])!=0 or len(dft['jumltr'])!=0):
        jual = dft.loc[dft['status'] == 'JUAL', ('jumltr')].iloc[-1]
        obral = dft.loc[dft['status'] == 'OBRAL', ('jumltr')].iloc[-1]
        retur = dft.loc[dft['status'] == 'RETUR', ('jumltr')].iloc[-1]
        jumlah = jual + obral
        txtjumlahtunai = f"{jumlah:,.0f}"
        txtjualtunai = f"{jual:,.0f}"
        txtobraltunai = f"{obral:,.0f}"
        txtreturtunai = f"{retur:,.0f}"
        return txtjumlahtunai, txtjualtunai, txtobraltunai, txtreturtunai
    else:
        txtjumlahtunai = '0'
        txtjualtunai = '0'
        txtobraltunai = '0'
        txtreturtunai = '0'
        return txtjumlahtunai, txtjualtunai, txtobraltunai, txtreturtunai


# jum transaksi bon
@app.callback(
    Output('bonPT', 'children'),
    Output('returbon', 'children'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def bonPT(start, end, frek, lini, kategori, toko):
    dfb = pd.read_sql('''
                    select
                        status,
                        count(distinct no_nota) as jumltr
                    from fact_PENJUALAN fp
                    inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                    inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                    inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                    where (tglnota between %(start)s and %(end)s)
                        and jenis_transaksi='BON'
                        and ds.kode_strip in %(lini)s
                        and ds.kel_jns in %(kategori)s
                        and dt.nama_toko in %(toko)s
                        and {season} != %(frek)s 
                    group by status'''.format(season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                      params={
                          'start': start, 'end': end,
                          'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                          'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                          'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                          'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)})
    if (len(dfb['jumltr'])!=0):
        jual = dfb.loc[dfb['status'] == 'JUAL', ('jumltr')].iloc[-1]
        retur = dfb.loc[dfb['status'] == 'RETUR', ('jumltr')].iloc[-1]
        txtjumlahbon = f"{jual:,.0f}"
        txtreturbon = f"{retur:,.0f}"
        return txtjumlahbon, txtreturbon
    else :
        txtjumlahbon = '0'
        txtreturbon = '0'
        return txtjumlahbon, txtreturbon


# omset penjualan
@app.callback(
    Output('growthPT', 'figure'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def growthPT(start, end, frek, lini, kategori, toko):
    dft = pd.read_sql('''
                    select
                    {tgl} as Periode,
                    (sum(case when (fp.status='JUAL' or fp.status='OBRAL') then fp.total end)
                        -sum(case when (fp.status='RETUR') then fp.total end))/1000000000 as 'Rupiah Omset'
                    from fact_PENJUALAN fp
                    inner join dim_STRIP ds on fp.strip_id=ds.strip_key
                    inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                    inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                    where fp.tglnota between %(start)s and %(end)s
                        and dt.nama_toko in %(toko)s
                        and ds.kode_strip in %(lini)s
                        and ds.kel_jns in %(kategori)s
                        and {season} != %(frek)s 
                    group by {tgl}
                    order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                      params={
                          'start': start, 'end': end,
                          'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                          'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                          'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                          'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                      })
    dfg = pd.read_sql('''
                    select
                    {tgl} as Periode,
                    (sum(case when (fp.status='JUAL' or fp.status='OBRAL') then fp.total end)
                        -sum(case when (fp.status='RETUR') then fp.total end))/1000000000 as 'Rupiah Omset',
                    fp.jenis_transaksi as JENIS
                    from fact_PENJUALAN fp
                    inner join dim_STRIP ds on fp.strip_id=ds.strip_key
                    inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                    inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                    where fp.tglnota between %(start)s and %(end)s
                        and dt.nama_toko in %(toko)s
                        and ds.kode_strip in %(lini)s
                        and ds.kel_jns in %(kategori)s
                        and {season} != %(frek)s 
                    group by {tgl}, JENIS
                    order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                      params={
                          'start': start, 'end': end,
                          'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                          'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                          'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                          'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                      })
    if (len(dfg['Periode'])!=0 or len(dfg['Rupiah Omset'])!=0) :
        fig = px.line(dfg, x=dfg['Periode'], y=dfg['Rupiah Omset'], color=dfg['JENIS'])
        fig.update_layout(xaxis=dict(tickvals=dfg['Periode'].unique()))
        fig.add_bar(x=dft['Periode'], y=dft['Rupiah Omset'], name='TOTAL')
        return fig
    else :
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                          yshift=10)
        return fig

#rasio tunai
@app.callback(
    Output('rasioTunaiPT', 'figure'),
    Input('radioTunai','value'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def rasioTunai(radio, start, end, frek, lini, kategori, toko):
    dfrt = pd.read_sql('''
                        select  {tgl} as Periode,
                                ((sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') and fp.jenis_transaksi = 'TUNAI' then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') and fp.jenis_transaksi = 'TUNAI' then fp.total end)) /
                                (sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') then fp.total end)))*100 as 'Persen Omset',
                                {radio}
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                        inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where dt.nama_toko in %(toko)s
                            and fp.tglnota BETWEEN %(start)s AND %(end)s
                            and ds.kode_strip IN %(lini)s
                            and ds.kel_jns IN %(kategori)s
                            and {season} != %(frek)s 
                        group by {tgl},{radio}
                        order by {tgl};'''.format(radio=radio,tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                       params={
                           'start': start, 'end': end,
                           'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                           'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                           'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                           'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                       })
    if (len(dfrt['Periode']) != 0 or len(dfrt['Persen Omset']) != 0):
        fig = px.line(dfrt, x=dfrt['Periode'], y=dfrt['Persen Omset'], color=dfrt[radio])
        fig.update_layout(xaxis=dict(tickvals=dfrt['Periode'].unique()))
        fig.update_traces(mode='lines+markers')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

# rasio bon
@app.callback(
    Output('rasioBonPT', 'figure'),
    Input('radioBon','value'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def rasioBon(radio, start, end, frek, lini, kategori, toko):
    dfbt = pd.read_sql('''
                        select  {tgl} as Periode,
                                (sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') and fp.jenis_transaksi = 'BON' then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') and fp.jenis_transaksi = 'BON' then fp.total end)) /
                                (sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') then fp.total end))*100 as 'Persen Omset',
                                {radio}
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                        inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where dt.nama_toko in %(toko)s
                            and fp.tglnota BETWEEN %(start)s AND %(end)s
                            and ds.kode_strip IN %(lini)s
                            and ds.kel_jns IN %(kategori)s
                            and {season} != %(frek)s 
                        group by {tgl},{radio}
                        order by {tgl};'''.format(radio=radio,tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                       params={
                           'start': start, 'end': end,
                           'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                           'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                           'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                           'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                       })
    if(len(dfbt['Periode'])!=0 or len(dfbt['Persen Omset'])!=0):
        fig = px.line(dfbt, x=dfbt['Periode'], y=dfbt['Persen Omset'], color=dfbt[radio])
        fig.update_layout(xaxis=dict(tickvals=dfbt['Periode'].unique()))
        fig.update_traces(mode='lines+markers')
        return fig
    else :
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                          yshift=10)
        return fig

@app.callback(
    Output('growthSupPT', 'figure'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def rasioSupPT(start, end, frek, lini, kategori, toko):
    dft = pd.read_sql('''
                        select
                        {tgl} as Periode,
                        (sum(case when (fp.status='JUAL' or fp.status='OBRAL') then fp.total end)
                            -sum(case when (fp.status='RETUR') then fp.total end))/1000000 as 'Rupiah Omset'
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on fp.strip_id=ds.strip_key
                        inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where fp.tglnota between %(start)s and %(end)s
                            and dt.nama_toko in %(toko)s
                            and ds.kode_strip in %(lini)s
                            and ds.kel_jns in %(kategori)s
                            and {season} != %(frek)s 
                        group by {tgl}
                        order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                      params={
                          'start': start, 'end': end,
                          'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                          'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                          'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                          'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                      })
    dfg = pd.read_sql('''
                        select
                            {tgl} as Periode,
                            (sum(case when (fp.status='JUAL' or fp.status='OBRAL') then fp.total end)
                                -sum(case when (fp.status='RETUR') then fp.total end))/ 1000000 as 'Rupiah Omset',
                            dsp.status as JENIS
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on fp.strip_id=ds.strip_key
                        inner join dim_SUPPLIERR dsp on fp.supplier_id=dsp.supplier_key
                        inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where fp.tglnota between %(start)s and %(end)s
                            and dt.nama_toko in %(toko)s
                            and ds.kode_strip in %(lini)s
                            and ds.kel_jns in %(kategori)s
                            and {season} != %(frek)s
                        group by {tgl}, JENIS
                        order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                      params={
                          'start': start, 'end': end,
                          'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                          'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                          'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                          'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                      })
    if(len(dfg['Periode'])!=0 or len(dfg['Rupiah Omset'])!=0):
        fig = px.line(dfg, x=dfg['Periode'], y=dfg['Rupiah Omset'], color=dfg['JENIS'])
        fig.update_layout(xaxis=dict(tickvals=dfg['Periode'].unique()))
        fig.add_bar(x=dft['Periode'], y=dft['Rupiah Omset'], name='TOTAL')
        return fig
    else :
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                          yshift=10)
        return fig

#rasio k
@app.callback(
    Output('rasioKPT', 'figure'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def rasioKPT(start, end, frek, lini, kategori, toko):
    dfk = pd.read_sql('''
                        select  {tgl} as Periode,
                                ((sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') and dsr.status='KONSINYASI' then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') and dsr.status='KONSINYASI' then fp.total end)) /
                                (sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') then fp.total end)))*100 as 'Persen Omset',
                                dt.nama_toko as toko
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                        inner join dim_SUPPLIERR dsr on dsr.supplier_key=fp.supplier_id
                        inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where dt.nama_toko in %(toko)s
                            and fp.tglnota BETWEEN %(start)s AND %(end)s
                            and ds.kode_strip IN %(lini)s
                            and ds.kel_jns IN %(kategori)s
                            and {season}!=%(frek)s
                        group by {tgl},toko
                        order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                       params={
                           'start': start, 'end': end,
                           'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                           'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                           'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                           'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                       })
    if(len(dfk['Periode'])!=0 or len(dfk['Persen Omset'])!=0):
        fig = px.line(dfk, x=dfk['Periode'], y=dfk['Persen Omset'], color=dfk['toko'])
        fig.update_layout(xaxis=dict(tickvals=dfk['Periode'].unique()))
        fig.update_traces(mode='lines+markers')
        return fig
    else :
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                          yshift=10)
        return fig

#rasio nk
@app.callback(
    Output('rasioNKPT','figure'),
    Input('tglPT', 'start_date'),
    Input('tglPT', 'end_date'),
    Input('filterFrekPT', 'value'),
    Input('ddLini', 'value'),
    Input('ddKategori', 'value'),
    Input('filterTokoPT', 'value'))
def rasioNKPT(start, end, frek, lini, kategori, toko):
    dfnk = pd.read_sql('''
                        select  {tgl} as Periode,
                                ((sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') and dsr.status='NON KONSINYASI' then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') and dsr.status='NON KONSINYASI' then fp.total end)) /
                                (sum(case when (fp.status = 'JUAL' or fp.status = 'OBRAL') then fp.total end)
                                    - sum(case when (fp.status = 'RETUR') then fp.total end)))*100 as 'Persen Omset',
                                dt.nama_toko as toko
                        from fact_PENJUALAN fp
                        inner join dim_STRIP ds on ds.strip_key=fp.strip_id
                        inner join dim_SUPPLIERR dsr on dsr.supplier_key=fp.supplier_id
                        inner join dim_TOKO dt on dt.kode_toko=fp.kd_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where dt.nama_toko in %(toko)s
                            and fp.tglnota BETWEEN %(start)s AND %(end)s
                            and ds.kode_strip IN %(lini)s
                            and ds.kel_jns IN %(kategori)s
                            and {season} != %(frek)s
                        group by {tgl},toko
                        order by {tgl};'''.format(tgl=frek,season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                       params={
                           'start': start, 'end': end,
                           'frek': '-' if frek in ('dw.nyadran', 'dw.sisa_puasa', 'dw.puasa', 'dw.suro', 'dw.rasulan', 'dw.natal','dw.sekolah') else '1',
                           'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
                           'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
                           'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
                       })
    if(len(dfnk['Periode'])!=0 or len(dfnk['Persen Omset'])):
        fig = px.line(dfnk, x=dfnk['Periode'], y=dfnk['Persen Omset'], color=dfnk['toko'])
        fig.update_layout(xaxis=dict(tickvals=dfnk['Periode'].unique()))
        fig.update_traces(mode='lines+markers')
        return fig
    else :
        fig = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                          yshift=10)
        return fig