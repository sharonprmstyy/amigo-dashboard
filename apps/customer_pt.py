import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
from dash.dependencies import Input, Output
from app import app

# conn=create_engine('mysql+pymysql://root:@localhost/amigodw')
# conn=create_engine('mysql+pymysql://admindw:admindw@10.10.14.5/amigodw')
# conn=create_engine('mysql+pymysql://admindw:admindw@192.168.1.1/amigodw')
conn = create_engine('mysql+pymysql://admindw:admindw@10.10.10.38/amigodw')

df_toko=pd.read_sql('select nama_toko from dim_TOKO', conn)
df_cust=pd.read_sql('select jns_customer from dim_CUSTOMER', conn)
jns_cust=df_cust['jns_customer'].unique()
toko_all = df_toko['nama_toko'].unique()
frek_all=['Harian','Mingguan','Bulanan','Kuartal','Semester','Tahunan','Sekolah','Puasa','Sisa Puasa','Nyadran','Rasulan','Suro','Natal']
# frekwak={'Harian':['tglnota','tgldaftar'],
#      'Mingguan':['str_to_date(concat(yearweek(tglnota),"Sunday"), "%%X%%V %%W")',
#                  'str_to_date(concat(yearweek(tgl_daftar),"Sunday"), "%%X%%V %%W")'],
#      'Bulanan':['str_to_date(concat(date_format(tglnota,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
#                 'str_to_date(concat(date_format(tgl_daftar,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'],
#      'Kuartal':['str_to_date(concat(year(tglnota),"-", ((quarter(tglnota)*3)-2),"-01"),"%%Y-%%m-%%d")',
#                 'str_to_date(concat(year(tgl_daftar),"-", ((quarter(tgl_daftar)*3)-2),"-01"),"%%Y-%%m-%%d")'],
#      'Semester':['concat(year(tglnota)," ",IF(MONTH(tglnota) < 7, "Ganjil", "Genap"))',
#                  'concat(year(tgl_daftar)," ",IF(MONTH(tgl_nota) < 7, "Ganjil", "Genap"))'],
#      'Tahunan':['concat(" ",year(tglnota)," ")',
#                 'concat(" ",year(tgl_daftar)," ")']}

frekwak = {
    'Harian': ['tglnota', 'tgldaftar'],
    'Mingguan': ['str_to_date(concat(yearweek(tglnota),"Sunday"), "%%X%%V %%W")',
                 'str_to_date(concat(yearweek(tgl_daftar),"Sunday"), "%%X%%V %%W")'],
    'Bulanan': ['str_to_date(concat(date_format(tglnota,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
                'str_to_date(concat(date_format(tgl_daftar,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'],
    'Kuartal': ['dw.kuartal','dw.kuartal'],
    'Semester': ['dw.semester','dw.semester'],
    'Tahunan': ['dw.tahun','dw.tahun'],
    'Sekolah': ['dw.sekolah', 'dw.sekolah'],
    'Puasa': ['dw.puasa', 'dw.puasa'],
    'Sisa Puasa': ['dw.sisa_puasa', 'dw.sisa_puasa'],
    'Nyadran': ['dw.nyadran', 'dw.nyadran'],
    'Rasulan': ['dw.rasulan', 'dw.rasulan'],
    'Suro': ['dw.suro', 'dw.suro'],
    'Natal': ['dw.natal', 'dw.natal']}

breadcrumb = html.Div(html.Ol([
    html.Li(
        html.A('Home',href='/'),
        className='breadcrumb-item'
    ),
    html.Li(
        html.P('Dashboard Pelanggan'),
        className='breadcrumb-item'
    )
], className='breadcrumb'),
    id='bc-cust',
    style={'height':'50%','width':'101%','border-radius':'0px','margin-left':'-5px','margin-top':'-10px'}
)

fltrCustomer = html.Div([
    breadcrumb,
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Range Tanggal :"),
                    dcc.DatePickerRange(
                        id="tglCus",
                        start_date_id="startTglCus",
                        end_date_id="endTglCus",
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
                        id='filterFrekCus',
                        options=[{'label': i, 'value': i} for i in frek_all],
                        value='Bulanan',
                        placeholder='Frekuensi',
                        style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'},
                        clearable=False
                    )
                ])
            ],style={'height': '100px','width':'80%','margin-left':'20%'}, className='card border-secondary mb-3')
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Toko :"),
                    dcc.Dropdown(
                        id='filterTokoCus',
                        options=[{'label': i, 'value': i} for i in toko_all],
                        placeholder='Toko',
                        value=[],
                        multi=True,
                        style={'fontSize': '110%', 'height': '120%', 'margin':'-5px'}
                    )
                ])
            ], style={'height': '100px','width':'100%'}, className='card border-secondary mb-3')
        ])
    ], no_gutters=True)
],style={'width':'100%','height':'100px'})

cardOmsetMember = dbc.Card(
    dbc.Spinner([
        html.P('Omset Member', style={'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='omsetMember',
        )
    ],color='danger')
)

cardRataMember = dbc.Card(
    dbc.Spinner([
        html.P('Rata-rata Transaksi Member', style={'text-align': 'center', 'margin-top': '1em'}),
        dcc.Graph(
            id='rataTrMember',
        )
    ],color='danger')
)

cardGrowthMember = dbc.Card([
    html.P('Pertumbuhan Member Baru', style={'text-align': 'center', 'margin-top': '20px'}),
    dcc.Graph(
        id='growthMember',
    )
])

cardPrfProv = dbc.Card([
    html.P('Top 10 Provinsi Asal Member', style={'text-align': 'center', 'margin-top': '20px'}),
    dcc.Graph(
        id='provMember',
    )
])

cardPrfJob = dbc.Card([
    html.P('Profil Pekerjaan Member', style={'text-align': 'center', 'margin-top': '20px'}),
    html.H4(id='totalCusJob', style={'text-align': 'center', 'margin-top': '10px'}),
    dcc.Graph(
        id='jobMember',
    )
])

cardPrfUsia = dbc.Card([
    html.P('Profil Usia Member', style={'text-align': 'center', 'margin-top': '20px'}),
    html.H4(id='totalCusUsia', style={'text-align': 'center', 'margin-top': '10px'}),
    dcc.Graph(
        id='usiaMember',
    )
])

cardPrfGender = dbc.Card([
    html.P('Profil Gender Member', style={'text-align': 'center', 'margin-top': '20px'}),
    html.H4(id='totalCusGender', style={'text-align': 'center', 'margin-top': '10px'}),
    dcc.Graph(
        id='genderMember',
    )
])

dashCustTunai=dbc.Container([
    dbc.Row(dbc.Col([cardOmsetMember]),
            style={'margin-top':'5em', 'margin-bottom':'1em'}),
    dbc.Row([dbc.Col([cardRataMember],width=6),
            dbc.Col([cardGrowthMember],width=6)],
            style={'margin-top':'1em', 'margin-bottom':'1em'}),
    dbc.Row(dbc.Col([cardPrfProv]),
            style={'margin-top': '1em', 'margin-bottom': '1em'}),
    dbc.Row(dbc.Col([cardPrfJob]),
            style={'margin-top':'1em', 'margin-bottom':'1em'}),
    dbc.Row([dbc.Col([cardPrfGender],width=6),
            dbc.Col([cardPrfUsia],width=6)],
            style={'margin-top':'1em', 'margin-bottom':'1em'}),
], fluid=True)

layout = html.Div([
    html.Div([fltrCustomer],
            style={'width':'100%',
                   'top':'0',
                   'margin-top':'50px',
                   'zIndex':'2',
                   'position':'fixed'}),
    html.Div([dashCustTunai],
             style={'margin-top':'220px'})
])

@app.callback(
    Output('filterFrekCus', 'options'),
    Input('tglCus', 'start_date'),
    Input('tglCus', 'end_date'))
def changeFrekCus(start,end):
    range=(date.fromisoformat(end)-date.fromisoformat(start))
    if range.days<=2:
        return [{'label': k, 'value': k} for k in frek_all[0:1]]
    elif range.days<=14:
        return [{'label': k, 'value': k} for k in frek_all[0:2]]
    elif range.days<=60:
        return [{'label': k, 'value': k} for k in frek_all[0:2]]
    elif range.days<=180:
        return [{'label': k, 'value': k} for k in frek_all[0:2]]
    elif range.days<=365:
        return [{'label': k, 'value': k} for k in frek_all[0:4]]
    elif range.days<=720:
        return [{'label': k, 'value': k} for k in frek_all[0:13]]
    else:
        return [{'label': k, 'value': k} for k in frek_all[0:13]]

# OMSET MEMBER
@app.callback(
    Output('omsetMember','figure'),
    Input('tglCus','start_date'),
    Input('tglCus','end_date'),
    Input('filterFrekCus','value'),
    Input('filterTokoCus','value'))
def grafOmsetMember(start,end,frek,toko):
    dfo=pd.read_sql('''select
                            dt.nama_toko as toko,
                            {tgl} as Periode,
                            sum(fp.total)/1000000 as 'Total Rupiah'
                        from fact_PENJUALAN fp
                        inner join dim_CUSTOMER dc on fp.customer_id=dc.customer_id
                        inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                        inner join dim_WAKTU dw on fp.tglnota=dw.tanggal
                        where fp.tglnota between %(start)s and %(end)s
                            and dt.nama_toko in %(toko)s
                            and fp.customer_id<>1 and dc.kd_member<>'-'
                            and status!='RETUR'
                            and dc.jns_customer!='3'
                            and {season} != %(frek)s
                        group by Periode, toko
                        order by Periode, toko asc
                        '''.format(tgl=frekwak[frek][0],
                                   season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'), conn,
                        params={'start':start, 'end':end,
                                'frek':'-' if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else '1',
                                'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all)})
    fig=px.line(dfo,x=dfo['Periode'], y=dfo['Total Rupiah'], color=dfo['toko'])
    fig.update_layout(xaxis=dict(tickvals=dfo['Periode'].unique()))
    return fig

#RATA2 TRANSAKSI MEMBER
@app.callback(
    Output('rataTrMember','figure'),
    Input('tglCus','start_date'),
    Input('tglCus','end_date'),
    Input('filterFrekCus','value'),
    Input('filterTokoCus','value'))
def grafTrMember(start, end, frek, toko):
    dff=pd.read_sql('''SELECT
                            sq2.toko AS toko,
                            sq2.tglnota AS Periode, sq2.countt AS countt,
                            sq2.count_2 AS count_2, sq2.AVG_Member AS 'Jumlah Transaksi'
                        FROM
                        (SELECT
                            sq1.toko AS toko,
                            sq1.countt AS countt, sq1.count_2 AS count_2,
                            sq1.tglnota AS tglnota, sq1.countt AS count_22,
                            sq1.count_2 AS count_23,
                            (sq1.countt / CASE WHEN sq1.count_2 = 0 THEN NULL
                            ELSE sq1.count_2 END) AS AVG_Member
                        FROM
                        (SELECT
                            dt.nama_toko AS toko,
                            {tgl} AS tglnota,
                            count(*) AS countt, count(distinct dc.kd_member) AS count_2
                        FROM fact_PENJUALAN fp
                        INNER JOIN dim_CUSTOMER dc ON fp.customer_id = dc.customer_id
                        INNER JOIN dim_TOKO dt ON fp.kd_toko = dt.kode_toko
                        INNER JOIN dim_STRIP ds ON fp.strip_id = ds.strip_key
                        INNER JOIN dim_WAKTU dw on fp.tglnota=dw.tanggal
                        WHERE (dc.kd_member <> '-' OR dc.kd_member IS NULL)
                            AND dt.nama_toko in %(toko)s
                            AND fp.tglnota between %(start)s and %(end)s
                            AND dc.jns_customer!='3'
                            AND {season} != %(frek)s
                        GROUP BY tglnota, toko
                        ORDER BY tglnota, toko ASC) sq1) sq2
                        '''.format(tgl=frekwak[frek][0],
                                   season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'),conn,
                        params={'start':start, 'end':end,
                                'frek':'-' if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else '1',
                                'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all)})
    fig = px.line(dff, x=dff['Periode'], y=dff['Jumlah Transaksi'], color=dff['toko'])
    fig.update_layout(xaxis=dict(tickvals=dff['Periode'].unique()))
    return fig

#GROWTH MEMBER BARU
@app.callback(
    Output('growthMember','figure'),
    Input('tglCus', 'end_date'),
    Input('filterFrekCus','value'),
    Input('filterTokoCus', 'value'))
def grafGrwMember(end, frek, toko):
    dft=pd.read_sql('''
                    select
                        dt.nama_toko as toko,
                        {tgl} as Periode,
                    count(distinct dc.kd_member) as 'Jumlah Pelanggan'
                    from dim_CUSTOMER dc
                    inner join dim_TOKO dt on dt.kode_toko=dc.kd_toko
                    INNER JOIN dim_WAKTU dw on dc.tgl_daftar=dw.tanggal
                    where (kd_member<>"-" or kd_member is not null)
                        and dc.tgl_daftar <= %(end)s
                        and dt.nama_toko IN %(toko)s
                        and dc.jns_customer!='3'
                        and {season} != %(frek)s
                    group by Periode, toko
                    order by Periode, toko asc 
                    '''.format(tgl=frekwak[frek][1],
                               season=frek if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else 'dw.tanggal'),conn,
                    params={'frek':'-' if frek in ('dw.nyadran','dw.sisa_puasa','dw.puasa','dw.suro','dw.rasulan','dw.natal','dw.sekolah') else '1',
                            'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                            'end':end})
    fig = px.line(dft, x=dft['Periode'], y=dft['Jumlah Pelanggan'], color=dft['toko'])
    fig.update_layout(xaxis=dict(tickvals=dft['Periode'].unique()))
    return fig

#PROFIL TOP 10 PROVINSI
@app.callback(
    Output('provMember', 'figure'),
    Input('tglCus', 'start_date'),
    Input('tglCus', 'end_date'),
    Input('filterTokoCus', 'value'))
def grafProvMember(start, end, toko):
    dfp = pd.read_sql('''
                    select 
                        dK.provinsi as Provinsi,  
                        count(distinct dC.kd_member) as Jumlah 
                    from fact_PENJUALAN fp
                    inner join dim_CUSTOMER dC on fp.customer_id = dC.customer_id
                    inner join dim_KODEPOS dK on dC.kodepos_id = dK.kodepos_id
                    inner join dim_TOKO dT on dT.kode_toko=fp.kd_toko
                    where dC.customer_id=fp.customer_id
                      and (fp.customer_id<>1 or dC.kd_member<>'-')
                      and fp.tglnota between %(start)s and %(end)s
                      and dT.nama_toko IN %(toko)s
                      and dC.jns_customer!='3'
                    group by dK.provinsi
                    order by Jumlah desc
                    limit 5;
                    ''',conn,
                    params={'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                            'end':end, 'start':start})
    fig = px.bar(dfp, x=dfp['Jumlah'], y=dfp['Provinsi'])
    return fig

#PROFIL PEKERJAAN
@app.callback(
    Output('jobMember', 'figure'),
    Input('tglCus', 'end_date'),
    Input('filterTokoCus', 'value'))
def grafJobMember(end, toko):
    dfj = pd.read_sql('''select
                            dt.nama_toko as toko,
                            case
                                when dc.pekerjaan_customer='1' then 'IbuRumahTangga'
                                when dc.pekerjaan_customer='2' then 'Profesional'
                                when dc.pekerjaan_customer='3' then 'TNI/POLRI'
                                when dc.pekerjaan_customer='4' then 'Guru/Dosen'
                                when dc.pekerjaan_customer='5' then 'StaffBUMSwasta'
                                when dc.pekerjaan_customer='6' then 'Buruh'
                                when dc.pekerjaan_customer='7' then 'Pensiunan/Purnawirawan'
                                when dc.pekerjaan_customer='8' then 'PNS'
                                when dc.pekerjaan_customer='9' then 'Pelajar/Mahasiswa'
                                when dc.pekerjaan_customer='10' then 'Wiraswasta'
                                when dc.pekerjaan_customer='11' then 'Belum/TidakBekerja'
                                when dc.pekerjaan_customer='12' then 'StaffBUMN/BUMD'
                                when dc.pekerjaan_customer='13' then 'PejabatPemerintah'
                                when dc.pekerjaan_customer='14' then 'Rohaniawan'
                                when dc.pekerjaan_customer='15' then 'Seniman'
                                else 'Unknown'
                            end as Pekerjaan,
                            count(*) as Jumlah
                            from dim_CUSTOMER dc
                            inner join dim_TOKO dt on dt.kode_toko=dc.kd_toko
                            INNER JOIN dim_WAKTU dw on dc.tgl_daftar=dw.tanggal,
                                 (select fp.customer_id
                                 from fact_PENJUALAN fp
                                 group by fp.customer_id) sq1
                            where sq1.customer_id=dc.customer_id
                                and (sq1.customer_id<>1 or dc.kd_member<>'-')
                                and dt.nama_toko IN %(toko)s
                                and dc.tgl_daftar <= %(end)s
                                and dc.jns_customer!='3'
                            group by Pekerjaan, toko
                            order by toko;''',conn,
                            params={'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                                    'end':end})
    fig = px.bar(dfj, x=dfj['Jumlah'], y=dfj['Pekerjaan'], color=dfj['toko'])
    return fig

#PROFIL GENDER
@app.callback(
    Output('genderMember', 'figure'),
    Input('tglCus', 'end_date'),
    Input('filterTokoCus', 'value'))
def grafGenderMember(end, toko):
    dfg=pd.read_sql('''select dt.nama_toko as toko,
                        case
                            when dc.gender_customer='P' then 'Wanita'
                            when dc.gender_customer='L' then 'Pria'
                            else 'Other'
                            end as 'Jenis Kelamin',
                        count(*) as Jumlah
                        from dim_CUSTOMER dc
                        inner join dim_TOKO dt on dt.kode_toko=dc.kd_toko
                        INNER JOIN dim_WAKTU dw on dc.tgl_daftar=dw.tanggal,
                             (select fp.customer_id
                             from fact_PENJUALAN fp
                             group by customer_id) sq1
                        where sq1.customer_id=dc.customer_id
                            and (sq1.customer_id<>1 or dc.kd_member<>'-')
                            and dt.nama_toko in %(toko)s
                            and dc.tgl_daftar <= %(end)s
                            and dc.jns_customer!='3'
                        group by 'Jenis Kelamin', toko;''', conn,
                        params={'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                                'end':end})
    fig = px.pie(dfg, names=dfg['Jenis Kelamin'], values=dfg['Jumlah'])
    return fig

#PROFIIL USIA
@app.callback(
    Output('usiaMember','figure'),
    Input('tglCus', 'end_date'),
    Input('filterTokoCus', 'value'))
def grafUsiaMember(end, toko):
    dfu=pd.read_sql('''SELECT dt.nama_toko as toko,
                        CASE
                            WHEN dc.umur_customer < 26 THEN '15-25'
                            WHEN dc.umur_customer BETWEEN 26 and 35 THEN '26-35'
                            WHEN dc.umur_customer BETWEEN 36 and 45 THEN '36-45'
                            WHEN dc.umur_customer BETWEEN 46 and 55 THEN '46-55'
                            WHEN dc.umur_customer BETWEEN 56 and 65 THEN '56-65'
                            WHEN dc.umur_customer >65 THEN '>65'
                            ELSE 'Undefined'
                        END AS range_umur,
                        COUNT(*) AS jumlah
                        FROM dim_CUSTOMER dc
                        inner join dim_TOKO dt on dt.kode_toko=dc.kd_toko
                        INNER JOIN dim_WAKTU dw on dc.tgl_daftar=dw.tanggal,
                             (SELECT fp.customer_id
                             FROM fact_PENJUALAN fp
                             GROUP BY customer_id) sq1
                        WHERE sq1.customer_id=dc.customer_id
                            AND (sq1.customer_id<>1 or dc.kd_member<>'-')
                            and dt.nama_toko in %(toko)s
                            and dc.tgl_daftar <= %(end)s
                            and dc.jns_customer!='3'
                        GROUP BY range_umur, toko
                        ORDER BY range_umur ASC;''',conn,
                        params={'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                                'end':end})
    fig=px.pie(dfu, names=dfu['range_umur'], values=dfu['jumlah'])
    return fig

#TOTAL CUSTOMER UNTUK 3 PROFIL
@app.callback(
    Output('totalCusJob', 'children'),
    Output('totalCusUsia', 'children'),
    Output('totalCusGender', 'children'),
    Input('tglCus', 'end_date'),
    Input('filterTokoCus', 'value'))
def totalCustomer(end, toko):
    dftot = pd.read_sql('''
                        select count(dc.customer_id) as jumtot
                        from fact_PENJUALAN fp
                        inner join dim_CUSTOMER dc on fp.customer_id = dc.customer_id
                        inner join dim_TOKO dt on fp.kd_toko=dt.kode_toko
                        INNER JOIN dim_WAKTU dw on dc.tgl_daftar=dw.tanggal
                        where dc.customer_id=fp.customer_id
                          and (fp.customer_id<>1 or dc.kd_member<>'-')
                          and dc.tgl_daftar <= %(end)s
                          and dt.nama_toko in %(toko)s;''',conn,
                        params={'toko':tuple(toko) if len(toko)!=0 else tuple(toko_all),
                                'end':end})
    total = dftot.loc[:,('jumtot')].iloc[-1]
    txttotal = f"{total:,.0f}"
    return txttotal, txttotal, txttotal