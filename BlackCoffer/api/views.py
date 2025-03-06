from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dashboard.models import Data
from .serializers import DataSerializer
import plotly.colors as pc
import pycountry
from plotly.offline import plot
import pandas as pd
from django.db.models import Avg, Sum, Count, Max, Min
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
import json
from django.http import JsonResponse

class DataListView(generics.ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer



@api_view(['GET'])
def intensity_time_api(request):
    from_year = request.GET.get("from_year")
    to_year = request.GET.get("to_year")
    sector = request.GET.get("sector")
    country = request.GET.get("country")
    
    queryset = Data.objects.all()
    if from_year and to_year:
        queryset = queryset.filter(start_year__range=(from_year, to_year))
    elif from_year:
        queryset = queryset.filter(start_year__gte=from_year)
    elif to_year:
        queryset = queryset.filter(start_year__lt=to_year)

    if sector:
        queryset = queryset.filter(sector=sector)
    if country:
        queryset = queryset.filter(country=country)
    
    queryset = queryset.values('start_year','sector','country').annotate(avg_intensity=Avg("intensity"))
    df = pd.DataFrame(queryset)

    if df.empty:
        return Response({"graph": None})
    sectors = df['sector'].unique()
    colors = pc.qualitative.Dark24 
    if len(sectors) > len(colors):
        import random
        import matplotlib.colors as mcolors
        colors = [mcolors.to_hex([random.random(), random.random(), random.random()]) for _ in range(len(sectors))]
    color_map = {sector: colors[i % len(colors)] for i, sector in enumerate(sectors)}

    fig = go.Figure()
    for sector in df['sector'].unique():
        sector_data = df[df['sector'] == sector]

        x_values = sector_data['start_year'].tolist()  
        y_values = sector_data['avg_intensity'].tolist()


        fig.add_trace(go.Scatter(
            x=x_values,  
            y=y_values, 
            mode='lines+markers', 
            name=f"Intensity - {sector}",
            line=dict(color=color_map[sector])
            
        ))
    fig.update_layout(
        title="Intensity Over Time by Sector",
        xaxis_title="Year",
        yaxis_title="Intensity (Mean)",
        legend_title="Sector",
        template="plotly_white"
    )

    fig.update_layout(title="Intensity Over Time by Sector", xaxis_title="Year", yaxis_title="Intensity (Mean)")
    # graph_json = plot(fig, output_type='div')
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return JsonResponse({"Intensity_time_graph": graph_json}) 
#
    # return Response({"graph": graph_json})


def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None
    




















@api_view(['GET'])
# def sunburst_chart(request):
#     from_year = request.GET.get('from_year')
#     to_year = request.GET.get('to_year')
#     country = request.GET.get('country')
#     sector = request.GET.get('sector')
#     from_year = request.GET.get("from_year")
#     to_year = request.GET.get("to_year")
#     sector = request.GET.get("sector")
#     country = request.GET.get("country")
    
#     queryset = Data.objects.all()
#     if from_year and to_year:
#         queryset = queryset.filter(start_year__range=(from_year, to_year))
#     elif from_year:
#         queryset = queryset.filter(start_year__gte=from_year)
#     elif to_year:
#         queryset = queryset.filter(start_year__lt=to_year)

#     if sector:
#         queryset = queryset.filter(sector=sector)
#     if country:
#         queryset = queryset.filter(country=country)
    
#     queryset = queryset.values('start_year','sector', 'topic', 'country').annotate(avg_intensity=Avg("intensity"))
#     df = pd.DataFrame(queryset)
#     df_grouped = df.groupby(["sector", "topic", "country"]).size().reset_index(name="count")

#     # Create Sunburst Chart
#     fig = px.sunburst(
#         df_grouped,
#         path=["sector", "topic", "country"],  # Define hierarchy: Sector → Topic → Country
#         values="count",  # Size of slices
#         title="Sunburst Chart: Sector → Topic → Country",
#     )

#     # Convert figure to JSON
#     graph_json = json.loads(fig.to_json())

#     return Response(graph_json)
def sunburst_chart(request):
    # Get filter parameters from request
    from_year = request.GET.get('from_year')
    to_year = request.GET.get('to_year')
    country = request.GET.get('country')
    sector = request.GET.get('sector')

    # Filter queryset based on provided filters
    queryset = Data.objects.all()

    if from_year and to_year:
        queryset = queryset.filter(start_year__range=(from_year, to_year))
    elif from_year:
        queryset = queryset.filter(start_year__gte=from_year)
    elif to_year:
        queryset = queryset.filter(start_year__lt=to_year)

    if sector:
        queryset = queryset.filter(sector=sector)
    if country:
        queryset = queryset.filter(country=country)

    # Fetch necessary fields and compute average intensity
    queryset = queryset.values('start_year', 'sector', 'topic', 'country').annotate(avg_intensity=Avg("intensity"))

    # Convert queryset to DataFrame
    df = pd.DataFrame(queryset)

    # Ensure dataframe is not empty
    if df.empty:
        return Response({"error": "No data found for the given filters"}, status=400)

    # Group by sector, topic, and country
    df_grouped = df.groupby(["sector", "topic", "country"]).size().reset_index(name="count")

    # Create Sunburst Chart
    fig = px.sunburst(
        df_grouped,
        path=["sector", "topic", "country"],  # Define hierarchy: Sector → Topic → Country
        values="count",  # Size of slices
        title="Sunburst Chart: Sector → Topic → Country",
    )

    # Convert figure to JSON
    graph_json = json.loads(fig.to_json())

    return Response(graph_json)
















@api_view(['GET'])
def Intensity_Country_api(request):
    from_year = request.GET.get('from_year')
    to_year = request.GET.get('to_year')
    country = request.GET.get('country')
    sector = request.GET.get('sector')

    queryset = Data.objects.all()
    if from_year and to_year:
        queryset = queryset.filter(start_year__range=(from_year,to_year))
    elif from_year:
        queryset = queryset.filter(start_year__gt=from_year)
    elif to_year:
        queryset = queryset.filter(start_year__lt=to_year)

    if sector:
        queryset = queryset.filter(sector = sector)
    if country:
        queryset = queryset.filter(country = country)
    queryset = queryset.values('start_year','country', 'intensity')
    df = pd.DataFrame(queryset)
    # print(df)
    

    df['iso_code'] = df['country'].apply(get_iso3)
    # print("DEBUG: Unique ISO Codes:", df['iso_code'].unique())
    df_grouped = df.groupby(['iso_code', 'country'], as_index=False)['intensity'].mean()
    # print("DEBUG: df_grouped columns:", df_grouped.columns)
    # print("DEBUG: df_grouped shape:", df_grouped.shape)
    # print("DEBUG: df_grouped dtypes:\n", df_grouped.dtypes)
    print("DEBUG: df_grouped.empty:", df_grouped.empty)
    print("DEBUG: df_grouped at response stage:\n", df_grouped)

    df_filtered = df_grouped[df_grouped["intensity"] > 0]  # Example filter
    print("DEBUG: df_filtered shape:", df_filtered.shape)
    df_grouped = df_grouped.reset_index(drop=True)
    print("DEBUG: df_grouped after reset:\n", df_grouped)



    # print("DEBUG: Grouped DataFrame:\n", df_grouped) 
    fig = px.choropleth(
        df_grouped,
        locations='iso_code',  
        color='intensity', 
        hover_name='country',  
        color_continuous_scale="Viridis", 
        title="Global Intensity Analysis by Country",
        projection="natural earth"  
    )
    # print("DEBUG: Plotly Figure Data:", fig.to_dict()) 
    fig.update_layout(coloraxis_colorbar=dict(title="Intensity"))

    graph_json = json.loads(fig.to_json())
    return Response(graph_json)
    # graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    # return JsonResponse({"Intensity_Country_graph": graph_json}) 
    # Intensity_Country = plot(fig,output_type='div')
    # return Intensity_Country


