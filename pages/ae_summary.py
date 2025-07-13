import dash_mantine_components as dmc
import dash
from dash import html, dcc, callback, State, Input, Output
import pyreadr
import pandas as pd
import plotly.express as px
from dash_iconify import DashIconify
import dash_ag_grid as dag

dash.register_page(__name__)

# 数据整理
adae = pyreadr.read_r('./data/adae.rda')['adae']
adsl = pyreadr.read_r('./data/adsl.rda')['adsl']

adsl1 = adsl.loc[adsl['SAFFL'] == 'Y'].copy()
adae1 = adae.loc[adae['SAFFL'] == 'Y']

# 处理NA
adae1.loc[:, ['TRTEMFL']] = adae1[['TRTEMFL']].apply(lambda x: x.fillna('NULL'))
adae1.loc[:, adae1.select_dtypes(include='object').columns] = adae1.select_dtypes(include='object').apply(
    lambda x: x.fillna('NA'))

# 图标展示 不分组 + AEBODSYS汇总
adae1_copy = adae1.copy()
adae1_copy['AEDECOD'] = adae1_copy['AEBODSYS']
adae2 = pd.concat([adae1_copy, adae1])
adae2['UNGROUP'] = 'Total'
adsl1.loc[:, 'UNGROUP'] = 'Total'

layout = html.Div([
    dmc.Grid([
        dmc.GridCol([
            html.Div(
                id='summary-table',
                style={"height": "600px", "overflowY": "auto"}
                # fluid=True,
            )
        ], span=9.8),
        dmc.GridCol([
            dmc.Card(
                [
                    dmc.Stack(
                        [
                            dmc.Select(
                                label="Group variable",
                                value='SITEID',
                                id='group-variable',
                                data=[
                                    {"value": "SITEID", "label": "SITEID"},
                                    {"value": "TRT01A", "label": "TRT01A"},
                                    {"value": "SEX", "label": "SEX"},
                                    {"value": "AGEGR1", "label": "AGEGR1"},
                                    {"value": "UNGROUP", "label": "None"},
                                ],
                            ),
                            dmc.Text('Show Aedecod'),
                            dmc.SegmentedControl(
                                id='show-aedecod',
                                value='N',
                                data=[
                                    {"value": "Y", "label": "Yes"},
                                    {"value": "N", "label": "No"}
                                ]
                            ),
                            dmc.MultiSelect(
                                label="Select Subjid",
                                # placeholder="Select all you want",
                                id='subjid-selected',
                                # value=["ALL"],
                                data=[{"label": i, "value": i} for i in
                                      sorted(adae1["SUBJID"].unique())]
                            ),
                            dmc.MultiSelect(
                                label="Select SITEID",
                                # placeholder="Select all you want",
                                id='siteid-selected',
                                # value=["ALL"],
                                data=[{"label": i, "value": i} for i in
                                      adae1["SITEID"].unique()]
                            ),
                            dmc.MultiSelect(
                                label="Select AEREL",
                                # placeholder="Select all you want",
                                id='aerel-selected',
                                value=[v for v in adae1["AEREL"].unique()],
                                data=[{"label": i, "value": i} for i in adae1["AEREL"].unique()]
                            ),
                            dmc.MultiSelect(
                                label="Select AESDTH",
                                # placeholder="Select all you want",
                                id='aesdth-selected',
                                value=[v for v in adae1["AESDTH"].unique()],
                                data=[{"label": i, "value": i} for i in adae1["AESDTH"].unique()]
                            ),
                            dmc.MultiSelect(
                                label="Select TRTEMFL",
                                # placeholder="Select all you want",
                                id='trtemfl-selected',
                                value=[v for v in adae1["TRTEMFL"].unique()],
                                data=[{"label": i, "value": i} for i in adae1["TRTEMFL"].unique()]
                            ),
                            dmc.MultiSelect(
                                label="Select AEOUT",
                                # placeholder="Select all you want",
                                id='aeout-selected',
                                value=[v for v in adae1["AEOUT"].unique()],
                                data=[{"label": i, "value": i} for i in adae1["AEOUT"].unique()]
                            ),
                            dmc.MultiSelect(
                                label="Select AESEV",
                                # placeholder="Select all you want",
                                id='aesev-selected',
                                value=[v for v in adae1["AESEV"].unique()],
                                data=[{"label": i, "value": i} for i in adae1["AESEV"].unique()]
                            ),
                            dmc.NumberInput(
                                label='Filter by prevalence: >=',
                                placeholder='Enter numeric value',
                                value=0,
                                allowNegative=False,
                                suffix="%",
                                id='filter-prevalence'
                            )
                        ]
                    )
                ],
                withBorder=True,
                shadow="sm",
                radius="md"
            )
        ], span=2.2, style={"height": "600px", "overflowY": "auto"})
    ])
    # dmc.Container([
    #
    # ],fluid=True)
])

color_palette = px.colors.qualitative.Set2


def format_pct(x):
    return f"{int(x)}%" if x in (0, 100) else f"{x:.1f}%"

# def ae_summary_table(indata, group_var, filter_rate):

@callback(
    Output("summary-table", "children"),
    Input("group-variable", "value"),
    Input("show-aedecod", "value"),
    Input("subjid-selected", "value"),
    Input("siteid-selected", "value"),
    Input("aerel-selected", "value"),
    Input("aesdth-selected", "value"),
    Input("trtemfl-selected", "value"),
    Input("aeout-selected", "value"),
    Input("aesev-selected", "value"),
    Input("filter-prevalence", "value"),
)
def update_graphs(group_var, show_aedecod, subjid_selected, siteid_selected, aerel_selected, aesdth_selected,
                  trtemfl_selected, aeout_selected, aesev_selected, filter_prevalence):
    bign = adsl1.groupby([group_var]).agg(BIGN=('USUBJID', 'nunique')).reset_index()
    adae3 = adae2.copy()

    filter_prevalence = 0 if filter_prevalence == '' else filter_prevalence
    adae3 = adae3 if show_aedecod == 'Y' else adae3.loc[adae3['AEBODSYS'] == adae3['AEDECOD']]

    if subjid_selected:
        adae3 = adae3.loc[adae3['SUBJID'].isin(subjid_selected)]

    if siteid_selected:
        adae3 = adae3.loc[adae3['SITEID'].isin(siteid_selected)]

    adae3 = adae3[adae3['AEREL'].isin(aerel_selected)]
    adae3 = adae3[adae3['AESDTH'].isin(aesdth_selected)]
    adae3 = adae3[adae3['TRTEMFL'].isin(trtemfl_selected)]
    adae3 = adae3[adae3['AEOUT'].isin(aeout_selected)]
    adae3 = adae3[adae3['AESEV'].isin(aesev_selected)]

    # 分组计算频数
    soc_pt = adae3.groupby([group_var, 'AEBODSYS', 'AEDECOD'], dropna=False).agg(N=('USUBJID', 'nunique')).reset_index()
    soc_pt = pd.merge(soc_pt, bign, how="left", on=[group_var])
    soc_pt['PERCT'] = soc_pt['N'] / soc_pt['BIGN'] * 100

    # 不良事件发生率的筛选
    pts_rate = soc_pt.loc[soc_pt['PERCT'] >= filter_prevalence, "AEDECOD"].dropna().unique()
    soc_pt_rate = soc_pt.loc[soc_pt["AEDECOD"].isin(pts_rate)]
    soc_pt_rate['VALUE'] = soc_pt_rate['N'].astype(str) + ' (' + soc_pt_rate['PERCT'].apply(format_pct) + ')'

    t = soc_pt_rate.pivot(index=['AEBODSYS', 'AEDECOD'], columns=[group_var], values='VALUE').reset_index()
    format_col = list(filter(lambda x: x not in ['AEBODSYS', 'AEDECOD'], list(t.columns)))
    t.loc[:, format_col] = t.loc[:, format_col].apply(lambda x: x.fillna('0'))

    # 排序
    soc_sort = adae3.groupby(['AEBODSYS'], dropna=False).agg(SOCN=('USUBJID', 'nunique')).reset_index()
    pt_sort = adae3.groupby(['AEDECOD'], dropna=False).agg(PTN=('USUBJID', 'nunique')).reset_index()

    t = pd.merge(t, soc_sort, how="left", on='AEBODSYS') \
        .merge(pt_sort, how='left', on='AEDECOD')

    t.sort_values(by=['SOCN', 'AEBODSYS', 'PTN', 'AEDECOD'], ascending=[False, False, False, False], inplace=True,
                  ignore_index=True)

    df = t
    # 表格展示
    if show_aedecod == 'Y':
        columns = [x for x in df.columns if x not in ['SOCN', 'PTN']]
        columnDefs = []
        for i, col in enumerate(columns):
            color = 'black' if col in ('AEDECOD', 'AEBODSYS') else color_palette[i % len(color_palette)]
            header_n = bign.loc[bign[group_var] == col, 'BIGN'].values
            header_n = 0 if len(header_n) == 0 else header_n[0]
            col_def = {
                "field": col,
                "headerName": col if col in ['AEDECOD', 'AEBODSYS'] else f"{col} (N={header_n})",
                "valueFormatter": {
                    "function": "params.value != null ? params.value.toFixed(1) + '%' : ''"} if col not in ['AEBODSYS',
                                                                                                            'AEDECOD'] else None,
                # column spanning 列合并展示
                'colSpan': {
                    "function": "params.data.AEBODSYS === params.data.AEDECOD ? 2 : 1"} if col == 'AEBODSYS' else "",
                "cellStyle": {"color": color},
                'suppressSizeToFit': True if col in ['AEDECOD', 'AEBODSYS'] else False,
            }
            columnDefs.append(col_def)
    else:
        columns = [x for x in df.columns if x not in ['SOCN', 'PTN', 'AEDECOD']]
        columnDefs = []
        for i, col in enumerate(columns):
            color = 'black' if col in ('AEBODSYS') else color_palette[i % len(color_palette)]
            header_n = bign.loc[bign[group_var] == col, 'BIGN'].values
            header_n = 0 if len(header_n) == 0 else header_n[0]
            col_def = {
                "field": col,
                "headerName": col if col in ['AEBODSYS'] else f"{col} (N={header_n})",
                "valueFormatter": {
                    "function": "params.value != null ? params.value.toFixed(1) + '%' : ''"} if col not in [
                    'AEDECOD'] else None,
                "cellStyle": {"color": color},
                'suppressSizeToFit': True if col in ['AEBODSYS'] else False,
            }
            columnDefs.append(col_def)

    summary_table = dag.AgGrid(
        id="cell-selection",
        className="ag-theme-alpine",
        rowData=df.to_dict("records"),
        columnDefs=columnDefs,
        getRowId="params.data.AEBODSYS + '_' + params.data.AEDECOD",
        columnSize="responsiveSizeToFit",
        columnSizeOptions={'defaultMinWidth': 105},
        style={"height": "100%", "width": "100%"},
        # rowModelType="infinite",
        defaultColDef={'sortable': False, "filter": True},
        dashGridOptions={"pagination": True}  # 'domLayout':"autoHeight", "paginationAutoPageSize": True
    )
    return summary_table
