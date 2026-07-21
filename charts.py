import plotly.graph_objects as go


def create_weather_chart(data):

    categories = [
        "Temperature",
        "Feels Like",
        "Humidity",
        "Pressure",
        "Wind Speed"
    ]

    values = [
        data["main"]["temp"],
        data["main"]["feels_like"],
        data["main"]["humidity"],
        data["main"]["pressure"],
        data["wind"]["speed"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=categories,
            y=values,
            text=values,
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Current Weather Statistics",
        xaxis_title="Weather Parameters",
        yaxis_title="Values",
        height=500
    )

    return fig