import dash_mantine_components as dmc
import dash
from dash import Dash, Input, Output, State, callback
from dash_iconify import DashIconify

app = Dash(use_pages=True, external_stylesheets=dmc.styles.ALL, suppress_callback_exceptions=True)

logo = "./assets/logo.png"

def get_icon(icon):
    return DashIconify(icon=icon, height=16)

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="mobile-burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Burger(
                        id="desktop-burger",
                        size="sm",
                        visibleFrom="sm",
                        opened=True,
                    ),
                    dmc.Image(src=logo, h=50, flex=0),
                    dmc.Title("NewO",  c="black", order=2),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                dmc.NavLink(
                    label="home",
                    href="/", active='exact',
                    leftSection=get_icon(icon="tabler:home"),
                    childrenOffset=28,
                ),
                dmc.NavLink(
                    label="Adverse Event",
                    href="/ae", active='exact',
                    leftSection=get_icon(icon="tabler:gauge"),
                    childrenOffset=28,
                    children=[
                        dmc.NavLink(label="AE Explorer", href='/ae-explorer', active='exact'),
                    ]
                ),
            ],
            p="md",
        ),
        dmc.AppShellMain(dash.page_container),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)

@callback(
    Output("appshell", "navbar"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, navbar):
    navbar["collapsed"] = {
        "mobile": not mobile_opened,
        "desktop": not desktop_opened,
    }
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
