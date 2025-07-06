import dash_mantine_components as dmc
import dash
from dash import html, dcc
import pyreadr
import pandas as pd
from dash_iconify import DashIconify

from pages.ae import layout

dash.register_page(__name__)

# 数据整理
adae = pyreadr.read_r('./data/adae.rda')['adae']
adsl = pyreadr.read_r('./data/adsl.rda')['adsl']

# adae_copy = adae.copy()
# adae_copy['AEDECOD'] = adae_copy['AEBODSYS']
# adae_t = pd.concat([adae_copy, adae])
# adsl_saf = adsl.loc[adsl['SAFFL'] == 'Y'].copy()
# adsl_saf['UNGROUP'] = 'Total'
# adae_t['UNGROUP'] = 'Total'

layout = dmc.Grid([
    dmc.GridCol([
        dmc.Card(
            [
                dmc.Text("left"),
            ]
        )
    ], span=9),
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
                                {"value": "None", "label": "UNGROUP"},
                            ],
                        ),
                        dmc.MultiSelect(
                            label="Select AEREL",
                            placeholder="Select all you want",
                            id='aerel-selected',
                            value=[v for v in adae["AEREL"].dropna().unique()],
                            data=[{"label": i, "value": i} for i in adae["AEREL"].dropna().unique()]
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
            radius="md",
        )
    ], span=3)
])
