# # import dash
# # from dash.dependencies import Input, Output
# # import dash_core_components as dcc
# # import dash_html_components as html
# # import dash_enterprise_auth as auth
# #
# #
# # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# #
# # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# #
# # server = app.server  # Expose the server variable for deployments
# #
# # # Standard Dash app code below
# # app.layout = html.Div(className='container', children=[
# #
# #     html.Div([
# #         html.H2('Sample App', id='header-title', className='ten columns'),
# #         html.Div(auth.create_logout_button(), className='two columns', style={'marginTop': 30})
# #     ]),
# #     html.Div(id='dummy-input', style={'display': 'none'}),
# #
# #     html.Div([
# #         html.Div(
# #             className='four columns',
# #             children=[
# #                 dcc.Dropdown(
# #                     id='dropdown',
# #                     options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
# #                     value='LA'
# #                 )
# #         ]),
# #         html.Div(
# #             className='eight columns',
# #             children=[
# #                 dcc.Graph(id='graph')
# #             ])
# #     ])
# # ])
# #
# #
# # @app.callback(Output('header-title','children'),
# #               Input('dummy-input', 'children'))
# # def update_title(_):
# #
# #     # print user data to the logs
# #     print(auth.get_user_data())
# #
# #     # update header with username
# #     return 'Hello {}'.format(auth.get_username())
# #
# #
# # @app.callback(Output('graph', 'figure'),
# #               Input('dropdown', 'value'))
# # def update_graph(value):
# #     return {
# #         'data': [{
# #             'x': [1, 2, 3, 4, 5, 6],
# #             'y': [3, 1, 2, 3, 5, 6]
# #         }],
# #         'layout': {
# #             'title': value,
# #             'margin': {
# #                 'l': 60,
# #                 'r': 10,
# #                 't': 40,
# #                 'b': 60
# #             }
# #         }
# #     }
# #
# # if __name__ == '__main__':
# #     app.run_server(debug=True)
# # # fltrPT = dbc.Container(
# # #     dbc.CardBody([
# # #         dbc.Row([
# # #             dbc.Col([
# # #                 dbc.CardBody([
# # #                     html.H6("Range Tanggal :"),
# # #                     dcc.DatePickerRange(
# # #                         id="tglPT",
# # #                         start_date_id="startTglPT",
# # #                         end_date_id="endTglTarget",
# # #                         start_date=date(2013, 1, 1),
# # #                         end_date=date(2015, 1, 1),
# # #                         display_format='YYYY-MM-DD',
# # #                         style={'fontSize': '50%', 'height': '120%'}
# # #                     )
# # #                 ])
# # #             ]),
# # #             dbc.Col([
# # #                 dbc.CardBody([
# # #                     html.H6("Frekuensi Pengukuran :"),
# # #                     dcc.Dropdown(
# # #                         id='filterFrekPT',
# # #                         options=[{'label': i, 'value': i} for i in frek],
# # #                         placeholder='Frekuensi',
# # #                         value=frek['Bulanan'],
# # #                         style={'fontSize': '110%', 'height': '120%'}
# # #                     )
# # #                 ])
# # #             ]),
# # #             dbc.Col([
# # #                 dbc.CardBody([
# # #                     html.H6("Kedalaman Pengukuran :"),
# # #                     dcc.RadioItems(
# # #                         id='filterDepthPT',
# # #                         options=[{'label': i, 'value': i} for i in kedprod],
# # #                         labelStyle={'margin': 'auto', 'padding': '10px'},
# # #                         style={'fontSize': '110%', 'height': '120%'},
# # #                         value='Kategori'
# # #                     )
# # #                 ])
# # #             ]),
# # #             dbc.Col([
# # #                 html.Div([
# # #                     dbc.CardBody([
# # #                         html.H6("Kategori :"),
# # #                         dcc.Dropdown(
# # #                             id='ddKategori',
# # #                             options=[{'label': i, 'value': i} for i in kategori_all],
# # #                             placeholder='Kategori',
# # #                             value=[],
# # #                             multi=True,
# # #                             style={'fontSize': '110%', 'height': '120%'}
# # #                         )
# # #                     ], id='divKategori')
# # #                 ]),
# # #                 html.Div([
# # #                     dbc.CardBody([
# # #                         html.H6("Lini :"),
# # #                         dcc.Dropdown(
# # #                             id='ddLini',
# # #                             options=[{'label': i, 'value': i} for i in lini_all],
# # #                             placeholder='Lini',
# # #                             value=[],
# # #                             multi=True,
# # #                             style={'fontSize': '110%', 'height': '120%'}
# # #                         )
# # #                     ], id='divLini')
# # #                 ])
# # #             ]),
# # #             dbc.Col([
# # #                 dbc.CardBody([
# # #                     html.H6("Toko :"),
# # #                     dcc.Dropdown(
# # #                         id='filterTokoPT',
# # #                         options=[{'label': i, 'value': i} for i in toko_all],
# # #                         placeholder='Toko',
# # #                         value=[],
# # #                         multi=True,
# # #                         style={'fontSize': '110%', 'height': '120%'}
# # #                     )
# # #                 ])
# # #             ])
# # #         ], no_gutters=True)
# # #     ], style={'width': '100%'}), fluid=True
# # # )
# #
# # # # rasio tunai
# # # @app.callback(
# # #     Output('rasioTunaiPT', 'figure'),
# # #     Input('tglPT', 'start_date'),
# # #     Input('tglPT', 'end_date'),
# # #     Input('filterFrekPT', 'value'),
# # #     Input('ddLini', 'value'),
# # #     Input('ddKategori', 'value'),
# # #     Input('filterTokoPT', 'value'))
# # # def rasioTunai(start, end, frek, lini, kategori, toko):
# # #     dfrt = pd.read_sql('''
# # #                         SELECT tunai.toko, tunai.tgl_nota, (tunai.jumlah-retur.jumlah)/total.jumlah*100 as jumlahh
# # #                             FROM
# # #                                  (SELECT {tgl} as tgl_nota, sum(fp.total) AS jumlah, kd_toko as toko
# # #                                             FROM fact_PENJUALAN fp
# # #                                             INNER JOIN dim_STRIP ds ON fp.strip_id = ds.strip_key
# # #                                             WHERE fp.status='RETUR'
# # #                                               AND fp.jenis_transaksi= 'TUNAI'
# # #                                               AND fp.kd_toko IN %(toko)s
# # #                                               AND tglnota BETWEEN %(start)s AND %(end)s
# # #                                               AND ds.kode_strip IN %(lini)s
# # #                                               AND ds.kel_jns IN %(kategori)s
# # #                                             GROUP BY tgl_nota,toko
# # #                                             ORDER BY tgl_nota) retur
# # #                                             JOIN
# # #                                  (SELECT {tgl} as tgl_nota, sum(fp.total) AS jumlah, kd_toko as toko
# # #                                             FROM fact_PENJUALAN fp
# # #                                             INNER JOIN dim_STRIP ds ON fp.strip_id = ds.strip_key
# # #                                             WHERE (fp.status='JUAL' or fp.status='OBRAL')
# # #                                               AND fp.kd_toko IN %(toko)s
# # #                                               AND fp.jenis_transaksi= 'TUNAI'
# # #                                               AND tglnota BETWEEN %(start)s AND %(end)s
# # #                                               AND ds.kode_strip IN %(lini)s
# # #                                               AND ds.kel_jns IN %(kategori)s
# # #                                             GROUP BY tgl_nota,toko
# # #                                             ORDER BY tgl_nota) tunai
# # #                                             JOIN
# # #                                  (SELECT {tgl} as tgl_nota, sum(fp.total) AS jumlah, kd_toko as toko
# # #                                             FROM fact_PENJUALAN fp
# # #                                             INNER JOIN dim_STRIP ds ON fp.strip_id = ds.strip_key
# # #                                             WHERE fp.status='JUAL'
# # #                                               AND fp.kd_toko IN %(toko)s
# # #                                               AND tglnota BETWEEN %(start)s AND %(end)s
# # #                                               AND ds.kode_strip IN %(lini)s
# # #                                               AND ds.kel_jns IN %(kategori)s
# # #                                             GROUP BY tgl_nota,toko
# # #                                             ORDER BY tgl_nota) total
# # #                         ON tunai.tgl_nota=retur.tgl_nota and tunai.toko=retur.toko
# # #                         and tunai.tgl_nota=total.tgl_nota and tunai.toko=total.toko'''.format(tgl=frek), conn,
# # #                        params={
# # #                            'start': start, 'end': end,
# # #                            'toko': tuple(toko) if len(toko) != 0 else tuple(toko_all),
# # #                            'lini': tuple(lini) if len(lini) != 0 else tuple(lini_all),
# # #                            'kategori': tuple(kategori) if len(kategori) != 0 else tuple(kategori_all)
# # #                        })
# # #     fig = px.line(dfrt, x=dfrt['tgl_nota'], y=dfrt['jumlahh'], color=dfrt['toko'])
# # #     fig.update_layout(xaxis=dict(tickvals=dfrt['tgl_nota'].unique()))
# # #     fig.update_traces(mode='lines+markers')
# # #     return fig
#
# frekwak = {
#     'Harian': ['tglnota', 'tgldaftar'],
#     'Mingguan': ['str_to_date(concat(yearweek(tglnota),"Sunday"), "%%X%%V %%W")',
#                  'str_to_date(concat(yearweek(tgl_daftar),"Sunday"), "%%X%%V %%W")'],
#     'Bulanan': ['str_to_date(concat(date_format(tglnota,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
#                 'str_to_date(concat(date_format(tgl_daftar,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'],
#     'Kuartal': ['str_to_date(concat(year(tglnota),"-", ((quarter(tglnota)*3)-2),"-01"),"%%Y-%%m-%%d")',
#                 'str_to_date(concat(year(tgl_daftar),"-", ((quarter(tgl_daftar)*3)-2),"-01"),"%%Y-%%m-%%d")'],
#     'Semester': ['concat(year(tglnota)," ",IF(MONTH(tglnota) < 7, "Ganjil", "Genap"))',
#                  'concat(year(tgl_daftar)," ",IF(MONTH(tgl_nota) < 7, "Ganjil", "Genap"))'],
#     'Tahunan': ['concat(" ",year(tglnota)," ")',
#                 'concat(" ",year(tgl_daftar)," ")'],
#     'Sekolah': ['dw.sekolah', 'dw.sekolah'],
#     'Puasa': ['dw.puasa', 'dw.puasa'],
#     'Sisa Puasa': ['dw.sisa_puasa', 'dw.sisa_puasa'],
#     'Nyadran': ['dw.nyadran', 'dw.nyadran'],
#     'Rasulan': ['dw.rasulan', 'dw.rasulan'],
#     'Suro': ['dw.suro', 'dw.suro'],
#     'Natal': ['dw.natal', 'dw.natal']}
#
# frek_all=['Harian','Mingguan','Bulanan','Kuartal','Semester','Tahunan']
# print(frekwak[0:3])

# frek = {'Harian': 'tglnota',
#         'Mingguan': 'str_to_date(concat(yearweek(tglnota),"Sunday"), "%%X%%V %%W")',
#         'Bulanan': 'str_to_date(concat(date_format(tglnota,"%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
#         'Kuartal': 'str_to_date(concat(year(tglnota),"-", ((quarter(tglnota)*3)-2),"-01"),"%%Y-%%m-%%d")',
#         'Semester': 'concat(year(tglnota)," ",IF(MONTH(tglnota) < 7, "Ganjil", "Genap"))',
#         'Tahunan': 'concat(" ",year(tglnota)," ")'}