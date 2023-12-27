# -*- coding: utf-8 -*-
"""
Created on Wed May 24 20:53:18 2023

Need to drop duplicates when uploading a new xml file.
When I add a new SAFT file and then go to Dashboard, the dashboard is missing the data from the new file. WHen I put the update inside the function I give to layout
it is working. But then I miss the df variables for the other callbacks. How to solve.


@author: pmbfe
"""

import os
from random import randint
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
# from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functions_vs1_1 import getBasicData, getGeneralLedger, getTransactions, getDataTables, getDataKPI, calculateKPI
# from functions import getBasicData, getGeneralLedger, getTransactions, getDataTables, getDataKPI, calculateKPI
from flask import session
import pandas as pd
# import numpy as np
# from lxml import etree as ET
# from openpyxl import load_workbook
from dashboard_vs3 import init_dashboard
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, current_user, logout_user, LoginManager, UserMixin

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'supersecretkey'  # Set a secret key for flashing messages

basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'instance/users.db')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)



app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lppf.consultoria@gmail.com'
app.config['MAIL_PASSWORD'] = 'uvwqnfdqoqkckexf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

otp = randint(0000,9999)
path_saldos_final = 'static/db/saldos_final.xlsx'
records_df = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,12)])
unique = records_df[['Nome','NIF','Trim','Ano']].drop_duplicates().reset_index(drop=True)



dash_app = init_dashboard(app)


@app.before_request
def before_request():
    if not current_user.is_authenticated and request.endpoint and request.endpoint not in ['login', 'forget_password', 'verify', 'validate', 'change_password', 'static']:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    # Enter User in the database (not working)
    # new_user = User(username="pfe", email="pmb.feliciano@gmail.com", password = "feliciano")
    # db.session.add(new_user)
    # db.session.commit()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and (user.password == password):
            login_user(user)
            return redirect(url_for('options'))
        # if username == 'fundbox' and password == 'fundbox_savi2023':
        #     return redirect(url_for('options'))
        else:
            return render_template('login.html', msg = 'Dados incorretos. Tente novamente.')
    return render_template('login.html')

@app.route('/forget_password', methods = ['GET'])
def forget_password():
    return render_template('forgetpassword.html')


@app.route('/verify', methods = ['POST'])
def verify():
    if request.method == 'POST':
        email = request.form['email']

        user = User.query.filter_by(email = email).first()

        if user:
            msg = Message('FELICE - alteração de password', sender='lppf.consultoria@gmail.com', recipients=[email])
            msg.body = 'Password de utilização única: '+str(otp)
            mail.send(msg)
            session['email'] = email
            return render_template('verify.html')
        else:
            return render_template('forgetpassword.html', msg="Wrong Email!")
    return render_template('verify.html')
    

@app.route('/validate', methods = ['POST'])
def validate():
    if request.method == 'POST':
        userotp = request.form['otp']
        if otp == int(userotp):
            return render_template('passwordchange.html')
        else:
            return render_template('verify.html', msg = "Wrong OTP!")
    return render_template('login.html')

@app.route('/change_password', methods = ['POST'])
def change_password():
    if request.method == 'POST':
        confirm_password = request.form['changepassword']
        email = session.get('email')
        user = User.query.filter_by(email = email).first()
        user.password = confirm_password
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/options')
@login_required
def options():
    return render_template('options.html')

@app.route('/add_data', methods=['GET','POST'])
@login_required
def add_data():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash( 'No file uploaded.')

        xml_file = request.files['file']            

        # if xml_file.filename == '':
        #     flash( 'No file selected.')

        # if not xml_file.filename.endswith('.xml'):
        #     flash( 'Invalid file format. Please upload an XML file.')        

        
        name, nif, start_dt, end_dt = getBasicData(xml_file)
        xml_file.seek(0)
        general_ledger, gl_resumo = getGeneralLedger(xml_file)
        xml_file.seek(0)
        transactions_final = getTransactions(xml_file)
        
        if transactions_final.empty==True:
            flash('SAFT sem transações. SAFT não foi importado.')
        else:
            
            pivot_pcl_trim, pivot_top_custos, pivot_top_proveitos, pivot_top_fornecedores, pivot_top_clients, pivot_sum_secondid,inv_final = getDataTables(general_ledger, transactions_final, name, nif,end_dt)
            saldos_final2 = getDataKPI(pivot_sum_secondid,gl_resumo,name,nif )
            kpi_trim = calculateKPI(pivot_top_custos,pivot_top_proveitos,saldos_final2,general_ledger,gl_resumo)
            
            # Save each dataframe in a different excel spreadsheet
            path_pcl = 'static/db/pcl.xlsx'
            path_custos = 'static/db/custos.xlsx'
            path_proveitos = 'static/db/proveitos.xlsx'
            path_fornecedores = 'static/db/fornecedores.xlsx'
            path_clientes = 'static/db/clientes.xlsx'
            path_saldos_final = 'static/db/saldos_final.xlsx'
            path_kpi ='static/db/kpi.xlsx'
            path_invest = 'static/db/investimentos.xlsx'
            
        
        
            # Read old data
            pcl_old = pd.read_excel(path_pcl,usecols=[i for i in range(1,9)])
            custos_old = pd.read_excel(path_custos,usecols=[i for i in range(1,9)])
            proveitos_old = pd.read_excel(path_proveitos,usecols=[i for i in range(1,9)])
            fornecedores_old = pd.read_excel(path_fornecedores,usecols=[i for i in range(1,9)])
            clientes_old = pd.read_excel(path_clientes,usecols=[i for i in range(1,9)])
            saldos_final_old = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,12)])
            kpi_old = pd.read_excel(path_kpi,usecols=[i for i in range(1,9)])
            invest_old = pd.read_excel(path_invest,usecols=[i for i in range(1,9)])
    
            
            # Save old data in old db
            path_pcl_old = 'static/db/old/pcl.xlsx'
            path_custos_old = 'static/db/old/custos.xlsx'
            path_proveitos_old = 'static/db/old/proveitos.xlsx'
            path_fornecedores_old = 'static/db/old/fornecedores.xlsx'
            path_clientes_old = 'static/db/old/clientes.xlsx'
            path_saldos_final_old = 'static/db/old/saldos_final.xlsx'
            path_kpi_old ='static/db/old/kpi.xlsx'
            path_invest_old = 'static/db/old/investimentos.xlsx'
    
    
            pcl_old.to_excel(path_pcl_old)
            custos_old.to_excel(path_custos_old)
            proveitos_old.to_excel(path_proveitos_old)
            fornecedores_old.to_excel(path_fornecedores_old)
            clientes_old.to_excel(path_clientes_old)
            saldos_final_old.to_excel(path_saldos_final_old)
            kpi_old.to_excel(path_kpi_old)   
            invest_old.to_excel(path_invest_old)
            
            # Append new data & drop duplicates if existent
            pcl_new = pcl_old.append(pd.DataFrame(pivot_pcl_trim), ignore_index=True)        
            pcl_new['NIF']=pcl_new['NIF'].astype(str)       
            pcl_new.drop_duplicates(subset=['Nome','NIF','Data'],keep='last',inplace=True)
    
            custos_new = custos_old.append(pd.DataFrame(pivot_top_custos), ignore_index=True)
            custos_new['NIF']=custos_new['NIF'].astype(str)       
            custos_new.drop_duplicates(subset=['Nome','NIF','Data','Third_ID'],keep='last',inplace=True)
    
            proveitos_new = proveitos_old.append(pd.DataFrame(pivot_top_proveitos), ignore_index=True)
            proveitos_new['NIF']=proveitos_new['NIF'].astype(str)       
            proveitos_new.drop_duplicates(subset=['Nome','NIF','Data','Second_ID'],keep='last',inplace=True)
    
            fornecedores_new = fornecedores_old.append(pd.DataFrame(pivot_top_fornecedores), ignore_index=True)
            fornecedores_new['NIF']=fornecedores_new['NIF'].astype(str)       
            fornecedores_new.drop_duplicates(subset=['Nome','NIF','Data','Account_ID'],keep='last',inplace=True)
    
            clientes_new = clientes_old.append(pd.DataFrame(pivot_top_clients), ignore_index=True)
            clientes_new['NIF']=clientes_new['NIF'].astype(str)       
            clientes_new.drop_duplicates(subset=['Nome','NIF','Data','Account_ID'],keep='last',inplace=True)
    
            saldos_final_new = saldos_final_old.append(pd.DataFrame(saldos_final2), ignore_index=True)
            saldos_final_new['NIF']=saldos_final_new['NIF'].astype(str)       
            saldos_final_new.drop_duplicates(subset=['Nome','NIF','Data','Second_ID'],keep='last',inplace=True)
    
            kpi_new = kpi_old.append(pd.DataFrame(kpi_trim), ignore_index=True)
            kpi_new['NIF']=kpi_new['NIF'].astype(str)       
            kpi_new.drop_duplicates(subset=['Nome','NIF','Data','KPI'],keep='last',inplace=True)
    
            invest_new = invest_old.append(pd.DataFrame(inv_final), ignore_index=True)
            invest_new['NIF']=invest_new['NIF'].astype(str)       
            invest_new.drop_duplicates(subset=['Nome','NIF','Data','sum_id'],keep='last',inplace=True)
    
    
    
            # Save the new files in excel
            pcl_new.to_excel(path_pcl)
            custos_new.to_excel(path_custos)
            proveitos_new.to_excel(path_proveitos)
            fornecedores_new.to_excel(path_fornecedores)
            clientes_new.to_excel(path_clientes)
            saldos_final_new.to_excel(path_saldos_final)
            kpi_new.to_excel(path_kpi)
            invest_new.to_excel(path_invest)
            flash('Dados adicionados.')
    
        
        # por aqui as funções que transformam o ficheiro nos dataframes que têm de ser guardados.
    return render_template('add_data.html')

@app.route('/delete_data')
@login_required
def delete_data():
    # path_saldos_final = 'static/db/saldos_final.xlsx'
    # records_df = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,9)])
    # unique = records_df[['Nome','NIF','Trim','Ano']].drop_duplicates().reset_index(drop=True)
    # importar no html a tabela da dataframe
    path_saldos_final = 'static/db/saldos_final.xlsx'
    global unique    
    records_df = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,12)])
    unique = records_df[['Nome','NIF','Data','Trim','Ano']].drop_duplicates()
    unique.sort_values(by=['Nome','Data'],inplace=True)
    unique.reset_index(drop=True,inplace=True)

    unique['Apagar'] = unique.index.map(lambda x: f'<a href="/delete/{x}" onclick="return confirm(\'De certeza que pretende eliminar este registo?\')">Apagar</a>')
  
    return render_template('delete_data.html', table=unique)

@app.route('/delete/<int:index>')
@login_required
def delete_row(index):
    global unique
    # Delete the row from the DataFrame
    # unique = unique.drop(index)
    # index=1
    del_row = unique.iloc[index]

    path_pcl = 'static/db/pcl.xlsx'
    path_custos = 'static/db/custos.xlsx'
    path_proveitos = 'static/db/proveitos.xlsx'
    path_fornecedores = 'static/db/fornecedores.xlsx'
    path_clientes = 'static/db/clientes.xlsx'
    path_saldos_final = 'static/db/saldos_final.xlsx'
    path_kpi ='static/db/kpi.xlsx'
    path_invest = 'static/db/investimentos.xlsx'


    # Read old data
    pcl_old = pd.read_excel(path_pcl,usecols=[i for i in range(1,9)])
    custos_old = pd.read_excel(path_custos,usecols=[i for i in range(1,9)])
    proveitos_old = pd.read_excel(path_proveitos,usecols=[i for i in range(1,9)])
    fornecedores_old = pd.read_excel(path_fornecedores,usecols=[i for i in range(1,9)])
    clientes_old = pd.read_excel(path_clientes,usecols=[i for i in range(1,9)])
    saldos_final_old = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,12)])
    kpi_old = pd.read_excel(path_kpi,usecols=[i for i in range(1,9)])
    invest_old = pd.read_excel(path_invest,usecols=[i for i in range(1,9)])


    # Delete the record from all the dataframes
    df_list = [pcl_old,custos_old,proveitos_old,fornecedores_old,clientes_old,saldos_final_old,kpi_old,invest_old]

    for i, df in enumerate(df_list):
        condicao_drop = (df['NIF']== del_row['NIF']) & (df['Trim']== del_row['Trim']) & (df['Ano']== del_row['Ano'])  
        df_list[i] = df[~condicao_drop].copy()
    pcl_new, custos_new, proveitos_new, fornecedores_new, clientes_new, saldos_final_new, kpi_new, invest_new = df_list

    # Save the new files in excel
    pcl_new.to_excel(path_pcl)
    custos_new.to_excel(path_custos)
    proveitos_new.to_excel(path_proveitos)
    fornecedores_new.to_excel(path_fornecedores)
    clientes_new.to_excel(path_clientes)
    saldos_final_new.to_excel(path_saldos_final)
    kpi_new.to_excel(path_kpi)
    invest_new.to_excel(path_invest)

    records_df = pd.read_excel(path_saldos_final,usecols=[i for i in range(1,12)])
    unique = records_df[['Nome','NIF','Data','Trim','Ano']].drop_duplicates()
    unique.sort_values(by=['Nome','Data'],inplace=True)
    unique.reset_index(drop=True,inplace=True)

    unique['Apagar'] = unique.index.map(lambda x: f'<a href="/delete/{x}" onclick="return confirm(\'De certeza que pretende eliminar este registo?\')">Apagar</a>')

   
    # Redirect back to the table page after deletion
    return redirect('/delete_data')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# with app.app_context():
#         # Import Dash application
#         from dashboard import init_dashboard
#         app = init_dashboard(app)


if __name__ == '__main__':
    
    app.run(debug=True)
