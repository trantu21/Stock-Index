from flask import Flask, render_template, request, session
from pandas_datareader import data
import pandas
import datetime
from plot_function import *
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)


app.config['SECRET_KEY'] = b'@\xc0\x8c\x06\xed\xaf\x18e\x9b>kz\xa9\xec`\xdf\xb7\xed\x8f\xda\xc4\x9d\x1a\x1b'#set the secret key for SESSION


@app.route('/', methods=['GET', 'POST'])
def index():

    america_index_name_meaning = {"^GSPC":"S&P500", "^IXIC":"NASDAQ COMPOSITE", "^DJI":"DOWN JONES INDUSTRIAL AVERAGE", "^XMI":"NYSE ARCA MAJOR MARKET INDEX","CBOE":"CBOE GLOBAL MARKETS", "^NDX":"NASDAQ 100", "IWV" :"RUSSELL 3000","OEF":"S&P 100"}


    if request.method == 'GET':
        #get the company's name from csv file
        df_company, america_list_company_name = companies_list_read_from_csv('america_companies')

        #get the company's name from csv file
        #defaul company and code index for company in S&P 500
        company_name_index="AAPL"
        index_name="^GSPC"
        #default time for the first time get data from yahoo
        start_sp = start_company = datetime.datetime(2016,1,2)
        end_sp = end_company = datetime.datetime(2016,3,10)

        #Get the request from user
        script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, america_index_name_meaning[index_name])

        script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'america_companies')

        key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
        values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]
        for i in range(0,len(key_list)):
            session[key_list[i]] = values_list[i]

        return render_template("america_stock_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,america_list_company_name=america_list_company_name)



    elif request.method =='POST':

        #get the name of the index, start date and end date for america index from  html form
        if (request.values.get('action')=="submit_sp")&(request.values.get('start_date_sp')!="")&(request.values.get("end_date_sp")!="")&(request.values.get("index_name")!=""):
            #get the company's name from csv file
            df_company, america_list_company_name = companies_list_read_from_csv('america_companies')
            index_name = request.form.get("america_index_name")#get the name of the america index from font

            start_time_string = request.form.get("start_date_sp")#get time string from form
            end_time_string = request.values.get("end_date_sp")#get end time string from form
            start_sp=datetime.datetime.strptime(start_time_string,"%Y-%m-%d")#convert start time string type to datime type
            end_sp=datetime.datetime.strptime(end_time_string,"%Y-%m-%d")#convert end time string type to datime type

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, america_index_name_meaning[index_name])

            #get the variable for america's company plot from session dict
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'america_companies')

            #CREATE THE SESSION DICTIONARY TO SAVE VARIABLE
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]#create the key_list
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]#create the value list
            #pair keys and values to session dict
            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("america_stock_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,america_list_company_name=america_list_company_name)

      #get the name of the company, start date and end date from html form
        elif (request.form.get("action")=="submit_company")&(request.form.get('start_date_company')!="")&(request.form.get("end_date_company")!="")&(request.form.get("company_name_index")!=""):
            #get the company's name from csv file
            df_company, america_list_company_name = companies_list_read_from_csv('america_companies')
            company_name_index = request.form.get("america_company_name_index")

            start_time_string_1 = request.form.get("start_date_company")
            end_time_string_1 = request.form.get("end_date_company")
            start_company=datetime.datetime.strptime(start_time_string_1,"%Y-%m-%d")
            end_company=datetime.datetime.strptime(end_time_string_1,"%Y-%m-%d")
            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'america_companies')

            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,america_index_name_meaning[index_name])

            #send variables to save in SESSION
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]

            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("america_stock_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,america_list_company_name=america_list_company_name)

        else:
            #get the company's name from csv file
            df_company, america_list_company_name = companies_list_read_from_csv('america_companies')
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)
            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,america_index_name_meaning[index_name])

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'america_companies')

            return render_template("america_stock_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,america_list_company_name=america_list_company_name)


@app.route('/euro_index',methods=['GET','POST'])
def euro_index():
    euro_index_name_meaning = {"FEZ":"SPDR EURO STOXX 50 ETF","EXSA.DE":"STOCXX EUROPE 600(DE)","E1X.FGI":"FTSE EUROTOP 100","MOX.FGI":"FTSE EUROMID","EB1X.FGI":"FTSE EURO 100","IEUR.L":"FTSEUROFIRST 80 ETF EUR DIST","EFC1.AS":"FTSEUROFIRST 100","E3X8570.FGI":"FTSEUROFIRST300","^SPE350-10":"S&P EUROPE 350"}


    if request.method == 'GET':
        #get the company's name from csv file
        df_company, euro_list_company_name = companies_list_read_from_csv('euro_companies')
        #defaul company and code index for company in S&P 500
        company_name_index="MSFT.BA"
        index_name="FEZ"
        #default time for the first time get data from yahoo
        start_sp = start_company = datetime.datetime(2016,1,2)
        end_sp = end_company = datetime.datetime(2016,3,10)


        #Get the request from user
        script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, euro_index_name_meaning[index_name])

        script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'euro_companies')

        key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
        values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]
        for i in range(0,len(key_list)):
            session[key_list[i]] = values_list[i]

        return render_template("euro_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,euro_list_company_name=euro_list_company_name)

    elif request.method =='POST':

        #get the name of the index, start date and end date for america index from  html form
        if (request.values.get('action')=="submit_sp")&(request.values.get('start_date_sp')!="")&(request.values.get("end_date_sp")!="")&(request.values.get("index_name")!=""):
            #get the company's name from csv file
            df_company, euro_list_company_name = companies_list_read_from_csv('euro_companies')
            index_name = request.form.get("euro_index_name")#get the name of the america index from font

            start_time_string = request.form.get("start_date_sp")#get time string from form
            end_time_string = request.values.get("end_date_sp")#get end time string from form
            start_sp=datetime.datetime.strptime(start_time_string,"%Y-%m-%d")#convert start time string type to datime type
            end_sp=datetime.datetime.strptime(end_time_string,"%Y-%m-%d")#convert end time string type to datime type

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, euro_index_name_meaning[index_name])

            #get the variable for america's company plot from session dict
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'euro_companies')

            #CREATE THE SESSION DICTIONARY TO SAVE VARIABLE
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]#create the key_list
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]#create the value list
            #pair keys and values to session dict
            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("euro_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,euro_list_company_name=euro_list_company_name)

      #get the name of the company, start date and end date from html form
        elif (request.form.get("action")=="submit_company")&(request.form.get('start_date_company')!="")&(request.form.get("end_date_company")!="")&(request.form.get("company_name_index")!=""):
            #get the company's name from csv file
            df_company, euro_list_company_name = companies_list_read_from_csv('euro_companies')
            company_name_index = request.form.get("euro_company_name_index")

            start_time_string_1 = request.form.get("start_date_company")
            end_time_string_1 = request.form.get("end_date_company")
            start_company=datetime.datetime.strptime(start_time_string_1,"%Y-%m-%d")
            end_company=datetime.datetime.strptime(end_time_string_1,"%Y-%m-%d")
            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'euro_companies')

            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,euro_index_name_meaning[index_name])

            #send variables to save in SESSION
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]

            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("euro_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,euro_list_company_name=euro_list_company_name)

        else:
            #get the company's name from csv file
            df_company, euro_list_company_name = companies_list_read_from_csv('euro_companies')
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)
            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,america_index_name_meaning[index_name])

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'euro_companies')

            return render_template("euro_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,euro_list_company_name=euro_list_company_name)

@app.route('/asia_index',methods=['GET','POST'])
def asian_index():
    asia_index_name_meaning = {"0388.HK":"HONGKONG EXCHANGES AND CLEARING LIMITED","^DJAT":"DOW JONES TITANS 50","ES3.SG":"SPDR STRAITS TIMES","FSTM.SI":"FTSE ST MID CAP","FSTS.SI":"FTSE ST SMALL CAP","000001.SS":"SHANGHAI STOCK EXCHANGES"}


    if request.method == 'GET':
        #get the company's name from csv file
        df_company, asia_list_company_name = companies_list_read_from_csv('asia_companies')

        #get the company's name from csv file
        #defaul company and code index for company in S&P 500
        company_name_index="TCS.NS"
        index_name="0388.HK"
        #default time for the first time get data from yahoo
        start_sp = start_company = datetime.datetime(2016,1,2)
        end_sp = end_company = datetime.datetime(2016,3,10)

        #Get the request from user
        script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, asia_index_name_meaning[index_name])

        script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'asia_companies')

        key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
        values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]
        for i in range(0,len(key_list)):
            session[key_list[i]] = values_list[i]

        return render_template("asia_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,asia_list_company_name=asia_list_company_name)
    elif request.method =='POST':

        #get the name of the index, start date and end date for america index from  html form
        if (request.values.get('action')=="submit_sp")&(request.values.get('start_date_sp')!="")&(request.values.get("end_date_sp")!="")&(request.values.get("index_name")!=""):
            #get the company's name from csv file
            df_company, asia_list_company_name = companies_list_read_from_csv('asia_companies')
            index_name = request.form.get("asia_index_name")#get the name of the america index from font

            start_time_string = request.form.get("start_date_sp")#get time string from form
            end_time_string = request.values.get("end_date_sp")#get end time string from form
            start_sp=datetime.datetime.strptime(start_time_string,"%Y-%m-%d")#convert start time string type to datime type
            end_sp=datetime.datetime.strptime(end_time_string,"%Y-%m-%d")#convert end time string type to datime type

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, asia_index_name_meaning[index_name])

            #get the variable for america's company plot from session dict
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'asia_companies')

            #CREATE THE SESSION DICTIONARY TO SAVE VARIABLE
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]#create the key_list
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]#create the value list
            #pair keys and values to session dict
            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("aisa_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,asia_list_company_name=asia_list_company_name)

      #get the name of the company, start date and end date from html form
        elif (request.form.get("action")=="submit_company")&(request.form.get('start_date_company')!="")&(request.form.get("end_date_company")!="")&(request.form.get("company_name_index")!=""):
            #get the company's name from csv file
            df_company, asia_list_company_name = companies_list_read_from_csv('asia_companies')
            company_name_index = request.form.get("asia_company_name_index")

            start_time_string_1 = request.form.get("start_date_company")
            end_time_string_1 = request.form.get("end_date_company")
            start_company=datetime.datetime.strptime(start_time_string_1,"%Y-%m-%d")
            end_company=datetime.datetime.strptime(end_time_string_1,"%Y-%m-%d")
            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'asia_companies')

            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,asia_index_name_meaning[index_name])

            #send variables to save in SESSION
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]

            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("asia_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,asia_list_company_name=asia_list_company_name)

        else:
            #get the company's name from csv file
            df_company, asia_list_company_name = companies_list_read_from_csv('asia_companies')
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)
            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,asia_index_name_meaning[index_name])

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'euro_companies')

            return render_template("asia_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,asia_list_company_name=asia_list_company_name)


@app.route('/japan_index',methods=['GET','POST'])
def japan_index():
    japan_index_name_meaning = {"^N225":"NIKKEI 225","^NJAQ.OS":"NEKKEI JASDAQ STOCK AVERAGE","1551.T":"NEKKEI JASDAQ 20","1364.T":"JPX-NEKKEI 400","^N1000":"NIKKEI JAPAN 1000","^N300":"NEKKEI 300","^N500":"NEKKEI 500","1306.T":"NEKKEI TOPIX","101280.KS":"TOPIX 100"}


    if request.method == 'GET':
        #get the company's name from csv file
        df_company, japan_list_company_name = companies_list_read_from_csv('japan_companies')

        #get the company's name from csv file
        #defaul company and code index for company in S&P 500
        company_name_index="7203.T"
        index_name="^N225"
        #default time for the first time get data from yahoo
        start_sp = start_company = datetime.datetime(2016,1,2)
        end_sp = end_company = datetime.datetime(2016,3,10)

        #Get the request from user
        script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, japan_index_name_meaning[index_name])

        script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'japan_companies')

        key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
        values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]
        for i in range(0,len(key_list)):
            session[key_list[i]] = values_list[i]

        return render_template("japan_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,japan_list_company_name=japan_list_company_name)


    elif request.method =='POST':
        #get the name of the index, start date and end date for america index from  html form
        if (request.values.get('action')=="submit_sp")&(request.values.get('start_date_sp')!="")&(request.values.get("end_date_sp")!="")&(request.values.get("index_name")!=""):
            #get the company's name from csv file
            df_company, japan_list_company_name = companies_list_read_from_csv('japan_companies')
            index_name = request.form.get("japan_index_name")#get the name of the america index from font

            start_time_string = request.form.get("start_date_sp")#get time string from form
            end_time_string = request.values.get("end_date_sp")#get end time string from form
            start_sp=datetime.datetime.strptime(start_time_string,"%Y-%m-%d")#convert start time string type to datime type
            end_sp=datetime.datetime.strptime(end_time_string,"%Y-%m-%d")#convert end time string type to datime type

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp, japan_index_name_meaning[index_name])

            #get the variable for america's company plot from session dict
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'japan_companies')

            #CREATE THE SESSION DICTIONARY TO SAVE VARIABLE
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]#create the key_list
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]#create the value list
            #pair keys and values to session dict
            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("japan_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,japan_list_company_name=japan_list_company_name)

      #get the name of the company, start date and end date from html form
      #get the name of the company, start date and end date from html form
        elif (request.form.get("action")=="submit_company")&(request.form.get('start_date_company')!="")&(request.form.get("end_date_company")!="")&(request.form.get("company_name_index")!=""):
            #get the company's name from csv file
            df_company, japan_list_company_name = companies_list_read_from_csv('japan_companies')
            company_name_index = request.form.get("japan_company_name_index")

            start_time_string_1 = request.form.get("start_date_company")
            end_time_string_1 = request.form.get("end_date_company")
            start_company=datetime.datetime.strptime(start_time_string_1,"%Y-%m-%d")
            end_company=datetime.datetime.strptime(end_time_string_1,"%Y-%m-%d")
            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'japan_companies')

            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,japan_index_name_meaning[index_name])

            #send variables to save in SESSION
            key_list = ["company_name_index","index_name","start_sp","end_sp","start_company","end_company"]
            values_list =[company_name_index,index_name,start_sp,end_sp,start_company,end_company]

            for i in range(0,len(key_list)):
                session[key_list[i]] = values_list[i]


            return render_template("japan_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,japan_list_company_name=japan_list_company_name)


        else:
            #get the company's name from csv file
            df_company, japan_list_company_name = companies_list_read_from_csv('japan_companies')
            company_name_index = session.get("company_name_index",None)
            start_company = session.get("start_company",None)
            end_company = session.get("end_company",None)
            index_name = session.get("index_name",None)
            start_sp = session.get("start_sp",None)
            end_sp = session.get("end_sp",None)

            script1, div1, cdn_js, cdn_css = get_index_data(index_name, start_sp, end_sp,japan_index_name_meaning[index_name])

            script2, div2, cdn_js, cdn_css = get_companies_index(company_name_index, start_company, end_company,'japan_companies')

            return render_template("japan_index.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_css=cdn_css,cdn_js=cdn_js,japan_list_company_name=japan_list_company_name)


@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":

    app.run(debug=True)
