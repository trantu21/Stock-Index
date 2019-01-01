from flask import Flask, render_template, request
from pandas_datareader import data
import pandas
import datetime
import numpy
from bokeh.plotting import figure,show,output_file
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import column
from bokeh.models import BoxSelectTool, DatetimeTickFormatter, ColumnDataSource, HoverTool


def get_index_data(index_name,start_sp,end_sp,index_meaning):
    #Get stated
    #GET DATA FOR S&P INDEX
    df_sp = data.DataReader(name=index_name,data_source="yahoo",start=start_sp,end=end_sp)
    ###PLOT THE COMPANYS INDEX IN S&P 500
    p_cir = figure(x_axis_type="datetime",width = 600, height = 300,sizing_mode="scale_width",tools="")

    #create the source data frame for bohkeh
    source = ColumnDataSource(data={
    'date'      : numpy.array((df_sp.index.values),dtype=numpy.datetime64),
    'High'      : df_sp["High"],
    'Low'       : df_sp["Low"],
    'index'     : df_sp.index,
    'Adj Close' : df_sp["Adj Close"],
    })


    p_cir.title.text = index_meaning
    p_cir.grid.grid_line_alpha = 0.5


    p_cir.circle(x='index',y='High', size=5, color="blue", alpha=0.5,source=source)#plot the circle for high values
    p_cir.circle(x='index',y='Low', size=5, color="red", alpha=0.5, source=source)#plot the circle for lowest values

    high_line= p_cir.line(x ='date',y='High',color="blue",line_width = 0.5, legend = "High Price",source=source)#plot the line for highest values

    low_line = p_cir.line(x='date',y='Low',color="red",line_width = 0.5,legend="Low Price",source=source)#plot the line for lowest valuse

    #add the legend for plot area
    p_cir.legend.label_text_font_size = "0.5em"
    p_cir.legend.orientation = "horizontal"
    p_cir.legend.location = "bottom_right"
    #config the HoverTool for plot area
    p_cir.add_tools(HoverTool(renderers=[high_line],
    tooltips=[
    ( 'Date',   '@date{%F}'      ),
    ('High Price', '$@High{0.2f}'),
    ('Adj Close', '$@{Adj Close}{0.2f}'),

    ],
    formatters={
    'date' : 'datetime',
    'Hight Price' : 'printf',
    },
    mode = 'vline'

    ))

    p_cir.add_tools(HoverTool(renderers=[low_line],
    tooltips=[
    ( 'Date',   '@date{%F}'      ),
    ('Low Price', '$@Low{0.2f}'),
    ('Adj Close', '$@{Adj Close}{0.2f}'),

    ],
    formatters={
    'date' : 'datetime',
    'Low Price'   : 'printf',
    },
    mode = 'vline'

    ))

    #get script and components for S&P index
    script1, div1 = components(p_cir)
    #get the javascript link for embed html
    cdn_js=CDN.js_files[0]
    #get the css link for embed to html
    cdn_css=CDN.css_files[0]


    return (script1, div1, cdn_js, cdn_css)


# PROCESS THE COMPANYS(THE COMPANY IN S&P500) INDEX FROM YAHOO BEFOR PLOT
#function to make Status column(compare open value and close value)
def status_make(close,open):
    if close > open:
        value = "Increase"
    elif close < open:
        value = "Decrease"
    else:
        value = "Equal"
    return value

def companies_list_read_from_csv(companies_location):
    area_list_companies = {
    'america_companies':'static/csv/america_companies.csv',
    'euro_companies'   :'static/csv/euro_companies.csv',
    'asia_companies'   :'static/csv/asia_companies.csv',
    'japan_companies'   :'static/csv/japan_companies.csv',
    }
    df_company = pandas.read_csv(area_list_companies[companies_location])#read the list of 500 companys from csv file

    zip_company = zip(df_company["Symbol"],df_company["Name"])#zip the values of 2 column Symbol and Name become tuple
    list_company_name = list(zip_company)#add above tuple to
    return df_company,list_company_name


def get_companies_index(company_name_index, start_company, end_company,companies_location):

    df_america_company, list_company_name = companies_list_read_from_csv(companies_location)
    #get the data frame from yahoo
    df =data.DataReader(name=company_name_index,data_source="yahoo",start=start_company,end=end_company)

    #print(df)#this line for check the df frame
    #add Middle column to data frame
    df["Middle"] = (df.Open+df.Close)/2
    #add Status column to data frame
    df["Status"] = [status_make(close,open) for close,open in zip(df.Close,df.Open)]
    #add Height column to data frame
    df["Height"] = abs(df.Close-df.Open)
    #print(df)
    day_hours = 12*60*60*1000
    #Create source for bokeh
    #To avoid error difference lenght of source's column so need saparate source become 3 difference data_source
    source = ColumnDataSource(data={
    'date'      : numpy.array((df.index.values),dtype=numpy.datetime64),
    'High'      : df["High"],
    'Low'       : df["Low"],
    'index'     : df.index,
    'Adj Close' : df["Adj Close"],
    })

    increase_source = ColumnDataSource(data={
    'increase index': df.index[df.Status=="Increase"],
    'middle increase':df.Middle[df.Status=="Increase"],
    'height increase': df.Height[df.Status=="Increase"],
    'high price'     :df.High[df.Status=="Increase"],#high price of increasing day
    'low price'      :df.Low[df.Status=="Increase"],#low price of increasing day
    'close price'      :df.Close[df.Status=="Increase"],
    })

    decrease_source = ColumnDataSource(data={
    'decrease index' : df.index[df.Status=="Decrease"],
    'middle decrease':df.Middle[df.Status=="Decrease"],
    'height decrease':df.Height[df.Status=="Decrease"],
    'high price'     :df.High[df.Status=="Decrease"],#high price of increasing day
    'low price'      :df.Low[df.Status=="Decrease"],#low price of increasing day
    'close price'    :df.Close[df.Status=="Decrease"]
    })
    equal_source = ColumnDataSource(data={
    'keep index' : df.index[df.Status=="Equal"],
    'high price'     :df.High[df.Status=="Equal"],#high price of increasing day
    'low price'      :df.Low[df.Status=="Equal"],#low price of increasing day
    'close price'    :df.Close[df.Status=="Equal"],
    })

    if companies_location =="america_companies":
        ###PLOT FOR COMPANY IN S&P500
        p_rec = figure(x_axis_type='datetime', width = 600, height = 300,sizing_mode="scale_width",tools="")
        title_company_name = df_america_company.index[df_america_company.Symbol == company_name_index]
        #print(df_america_company.Name[title_company_name[0]])
        p_rec.title.text = df_america_company.Name[title_company_name[0]].upper() #get the company name for the company's code which was user choose
        p_rec.grid.grid_line_alpha = 0.5



        #add the segment to the graph(the black line behind the rectange)
        p_rec.segment(x0='index',y0='High', x1='index', y1='Low', color="Black",source=source)
        #rectange Plot
        #rectange for increasing day
        high_rec=p_rec.rect(x='increase index',y='middle increase',width=day_hours,height='height increase',fill_color="#CCFFFF",line_color="black",legend = "Increase",source = increase_source)
        #reactang for decreasing day
        low_rec=p_rec.rect(x='decrease index',y='middle decrease',width=day_hours,height='height decrease',fill_color="#FF3333",line_color="black", legend = "Decrease",source = decrease_source)

        p_rec.legend.label_text_font_size = "0.5em"
        p_rec.legend.orientation = "horizontal"
        p_rec.legend.location = "bottom_right"

        p_rec.add_tools(HoverTool(renderers=[high_rec],
        tooltips=[
        ( 'Date',   '@{increase index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'increase index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[low_rec],
        tooltips=[
        ( 'Date',   '@{decrease index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'decrease index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

    elif companies_location =="euro_companies":
        ##PLOT FOR COMPANY IN S&P500
        p_rec = figure(x_axis_type='datetime', width = 600, height = 300,sizing_mode="scale_width",tools="")
        title_company_name = df_america_company.index[df_america_company.Symbol == company_name_index]
        #print(df_america_company.Name[title_company_name[0]])
        p_rec.title.text = df_america_company.Name[title_company_name[0]].upper() #get the company name for the company's code which was user choose
        p_rec.grid.grid_line_alpha = 0.5



        #add the segment to the graph(the black line behind the rectange)
        keep_index=p_rec.scatter(x='keep index', y='close price',marker="square",size=10,line_color="navy",fill_color="orange",source=equal_source,legend='No change')
        high_index=p_rec.scatter(x='increase index', y='close price',marker="triangle",size=15,line_color="navy",fill_color="blue",source=increase_source, legend='Increase')
        low_index=p_rec.scatter(x='decrease index', y='close price',marker="inverted_triangle",size=15,line_color="navy",fill_color="red",source=decrease_source, legend='Decrease')

        p_rec.legend.label_text_font_size = "0.5em"
        p_rec.legend.orientation = "horizontal"
        p_rec.legend.location = "bottom_right"

        p_rec.add_tools(HoverTool(renderers=[high_index],
        tooltips=[
        ( 'Date',   '@{increase index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'increase index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[low_index],
        tooltips=[
        ( 'Date',   '@{decrease index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'decrease index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[keep_index],
        tooltips=[
        ( 'Date',   '@{keep index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'keep index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))
    elif companies_location =="asia_companies":
        ##PLOT FOR COMPANY IN S&P500
        p_rec = figure(x_axis_type='datetime', width = 600, height = 300,sizing_mode="scale_width",tools="")
        title_company_name = df_america_company.index[df_america_company.Symbol == company_name_index]
        #print(df_america_company.Name[title_company_name[0]])
        p_rec.title.text = df_america_company.Name[title_company_name[0]].upper() #get the company name for the company's code which was user choose
        p_rec.grid.grid_line_alpha = 0.5



        #add the segment to the graph(the black line behind the rectange)
        keep_index=p_rec.scatter(x='keep index', y='close price',marker="square",size=10,line_color="navy",fill_color="orange",source=equal_source,legend='No change')
        high_index=p_rec.scatter(x='increase index', y='close price',marker="triangle",size=15,line_color="navy",fill_color="blue",source=increase_source, legend='Increase')
        low_index=p_rec.scatter(x='decrease index', y='close price',marker="inverted_triangle",size=15,line_color="navy",fill_color="red",source=decrease_source, legend='Decrease')

        p_rec.legend.label_text_font_size = "0.5em"
        p_rec.legend.orientation = "horizontal"
        p_rec.legend.location = "bottom_right"

        p_rec.add_tools(HoverTool(renderers=[high_index],
        tooltips=[
        ( 'Date',   '@{increase index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'increase index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[low_index],
        tooltips=[
        ( 'Date',   '@{decrease index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'decrease index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))
    elif companies_location =="japan_companies":
        ##PLOT FOR COMPANY IN S&P500
        p_rec = figure(x_axis_type='datetime', width = 600, height = 300,sizing_mode="scale_width",tools="")
        title_company_name = df_america_company.index[df_america_company.Symbol == company_name_index]
        #print(df_america_company.Name[title_company_name[0]])
        p_rec.title.text = df_america_company.Name[title_company_name[0]].upper() #get the company name for the company's code which was user choose
        p_rec.grid.grid_line_alpha = 0.5



        #add the segment to the graph(the black line behind the rectange)
        keep_index=p_rec.scatter(x='keep index', y='close price',marker="square",size=10,line_color="navy",fill_color="orange",source=equal_source,legend='No change')
        high_index=p_rec.scatter(x='increase index', y='close price',marker="triangle",size=15,line_color="navy",fill_color="blue",source=increase_source, legend='Increase')
        low_index=p_rec.scatter(x='decrease index', y='close price',marker="inverted_triangle",size=15,line_color="navy",fill_color="red",source=decrease_source, legend='Decrease')

        p_rec.legend.label_text_font_size = "0.5em"
        p_rec.legend.orientation = "horizontal"
        p_rec.legend.location = "bottom_right"

        p_rec.add_tools(HoverTool(renderers=[high_index],
        tooltips=[
        ( 'Date',   '@{increase index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'increase index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[low_index],
        tooltips=[
        ( 'Date',   '@{decrease index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'decrease index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))

        p_rec.add_tools(HoverTool(renderers=[keep_index],
        tooltips=[
        ( 'Date',   '@{keep index}{%F}'      ),
        ('High Price', '$@{high price}{0.2f}'),
        ('Low Price', '$@{low price}{0.2f}'),

        ],
        formatters={
        'keep index' : 'datetime',
        'Hight Price' : 'printf',
        'Low Price'   : 'printf',
        },
        ))


    #get the script and dive of company in S&P 500 for embed to html
    #script1, div1 = components(column([p_cir,p_rec],sizing_mode='stretch_both'))
    script2, div2 = components(p_rec)
    #get the javascript link for embed html
    cdn_js=CDN.js_files[0]
    #get the css link for embed to html
    cdn_css=CDN.css_files[0]

    return (script2, div2, cdn_js, cdn_css)
