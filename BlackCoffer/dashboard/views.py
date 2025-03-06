from django.shortcuts import render
import json
from datetime import datetime
from dashboard.models import Data
from django.db import connection
from django.http import JsonResponse
from django.db.models import Avg, Sum, Count, Max, Min
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import plotly.colors as pc
import plotly.graph_objects as go
import plotly.io as pio
import plotly.utils as pu 
import pycountry
import plotly.express as px 



def data(request):
    with open('jsondata.json','r',encoding='utf-8') as file:
        data = json.load(file)
    for i in data:
        Data.objects.create(
            end_year=int(i["end_year"]) if i["end_year"] else None,
            intensity=i["intensity"] if i["intensity"] else None,
            sector=i["sector"] if i["sector"] else None,
            topic=i["topic"] if i["topic"] else None,
            insight=i["insight"] if i["insight"] else None,
            url=i["url"] if i["url"] else None,
            region=i["region"] if i["region"] else None,
            start_year=int(i["start_year"]) if i["start_year"] else None,
            impact=i["impact"] if i["impact"] else None,
            added=datetime.strptime(i["added"], "%B, %d %Y %H:%M:%S") if i['added'] else None,
            published=datetime.strptime(i["published"], "%B, %d %Y %H:%M:%S") if i["published"] else None,
            country=i["country"] if i["country"] else None,
            relevance=i["relevance"] if i["relevance"] else None,
            pestle=i["pestle"] if i["pestle"] else None,
            source=i["source"] if i["source"] else None,
            title=i["title"] if i["title"] else None,
            likelihood=i["likelihood"] if i["likelihood"] else None,
        )

    print("Done")
    return render(request, "dashboard/success.html")



def intensaefsaity_time(request):
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
    # print(list(queryset))
    df = pd.DataFrame(queryset)
    # print(df)

    if df.empty:
        return render(request, 'dashboard/includes/intensity_time.html',{"graphJSON": None})
    
    sectors = df['sector'].unique()
    colors = pc.qualitative.Dark24 
    if len(sectors) > len(colors): 
        import random
        import matplotlib.colors as mcolors
        colors = [mcolors.to_hex([random.random(), random.random(), random.random()]) for _ in range(len(sectors))]
    color_map = {sector: colors[i % len(colors)] for i, sector in enumerate(sectors)}

    fig = go.Figure()
    for sector in sectors:
        sector_data = df[df['sector'] == sector]
        fig.add_trace(go.Scatter(
            x=sector_data['start_year'], 
            y=sector_data['avg_intensity'], 
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
    intensity_time_graph = plot(fig, output_type='div')
    return intensity_time_graph



def relevance_time(request):
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

    queryset = queryset.values('start_year','sector','country').annotate(avg_relevance = Avg("relevance"))        
    # print(list(queryset))
    df = pd.DataFrame(queryset)

    if df.empty:
        pass

    sectors = df['sector'].unique()
    colors = pc.qualitative.Dark24 
    if len(sectors) > len(colors): 
        import random
        import matplotlib.colors as mcolors
        colors = [mcolors.to_hex([random.random(), random.random(), random.random()]) for _ in range(len(sectors))]
    color_map = {sector: colors[i % len(colors)] for i, sector in enumerate(sectors)}

    fig = go.Figure()

    for sector in sectors:
        sector_data = df[df['sector']==sector]
        fig.add_trace(go.Scatter(
            x = sector_data['start_year'],
            y = sector_data['avg_relevance'],
            mode = 'lines+markers',
            name = f"Relevance-{sector}",   
            line = dict(color = color_map[sector])
        ))

    fig.update_layout(
        title = "Relevance Over Time by Sector",
        xaxis_title = "year",
        yaxis_title = "Relevance",
        legend_title = "Sector",
        template = "plotly_white"
    )

    relevance_time_graph = plot(fig,output_type='div')
    return relevance_time_graph



    
    
def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None
def Intensity_Country(request):
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

    df_grouped = df.groupby(['iso_code', 'country'], as_index=False)['intensity'].mean()

    fig = px.choropleth(
        df_grouped,
        locations='iso_code', 
        color='intensity',  
        hover_name='country',  
        color_continuous_scale="Viridis", 
        title="Global Intensity Analysis by Country",
        projection="natural earth"  
    )

    Intensity_Country = plot(fig,output_type='div')
    return Intensity_Country





    
def index(request):

    # intensity_time_graph = intensity_time(request)
    relevance_time_graph = relevance_time(request)
    Intensity_Country_graph = Intensity_Country(request)
    context= {
        # "intensity_time_graph":intensity_time_graph,
        "relevance_time_graph":relevance_time_graph,
        "Intensity_Country_graph":Intensity_Country_graph,
        "abcd":'hello '
    }
    return render(request, 'dashboard/index.html',context)


    
