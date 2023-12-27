# -*- coding: utf-8 -*-
"""
Created on Fri May 26 22:29:16 2023

@author: pmbfe
"""

import numpy as np
import pandas as pd
from lxml import etree as ET

# xml_file = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/SAFT_EQTY2020_01012022_31122022.xml" # EQTY Capital Lda.
# xml_file = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/SAFT_EQTY2020_01012022_30092022.xml" # EQTY Capital Lda.
# xml_file = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/BGPE 1T 2022.xml" # EQTY Capital Lda.
# xml_file = "C:/Users/pmbfe/Downloads/SAF-T EQTY I a 31122022.xml"
# xml_file = "C:/Users/pmbfe/Downloads/SAFT_C EQTY I 4ºT 2021.xml"
# xml_file = "C:/Users/pmbfe/Documents/Consultoria e Formação/SAFT Automatic Insights ENI/Exemplos SAFT/Manu/saft_ct_2020_515060933.xml" # Vascprime Lda.
# path = "C:/Users/pmbfe/Documents/Python Projects/fundbox/app_vs2_05_2023/demo/"
# file = "SAF-T Tejo 2 a 31122022.xml"
# path = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/ficheiros out 2023/"
# path = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/ficheiros out 2023/Safts Eqty/xml/"
path = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/ficheiros out 2023/"
# path = "C:/Users/pmbfe/Documents/Python Projects/fundbox/exemplos_saft/"
# file = "SAF-T EQTY II 2022.xml"
# file = 'SAFT_EQBRAV2022_01012023_30062023.xml'
# file = 'SAFT_EQTERI2023_01012023_30062023.xml'
# file = 'SAF-T Tejo 1º Sem 2023.xml'
file = 'SAF-T EQTY I 1º Sem 2023.xml'
# file = 'SAFT_EQTY2020_01012022_31122022.xml'
# file = 'SAF-T EQTY I 2022.xml'
#file = 'SAF-T TGV 2022.xml'
# file = "SAF-T F3 New Frontiers 1º Sem 2023.xml"
# file = 'SAF-T IRC 2022.xml'
# file = 'SAFT_C EQTY I 4ºT 2021.xml'
# file = 'saft_ct_2020_515060933_vascprime.xml'
xml_file = path+file

def getBasicData(xml_file): #está a funcionar
    tree = ET.parse(xml_file) #valido para testes
    # tree = ET.ElementTree(xml_file) #valido para a aplicação
    root = tree.getroot()
    
    
    name = root[0].find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}CompanyName').text
    nif = root[0].find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}TaxRegistrationNumber').text
    start_dt = root[0].find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}StartDate').text
    end_dt = root[0].find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}EndDate').text
    
    return name, nif, start_dt, end_dt

def getGeneralLedger(xml_file):
    # start = datetime.now()
    
    tree = ET.parse(xml_file) #valido para testes
    # tree = ET.ElementTree(xml_file) #valido para aplicação
    root = tree.getroot()

    general_ledger = pd.DataFrame([])
    
    master_files = root.index(root.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}MasterFiles'))
    
    # for account in root[1][0].findall('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Account'): #parece ok
    for account in root[master_files][0].findall('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Account'): #parece ok
        acc_id = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}AccountID').text
        acc_desc = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}AccountDescription').text
        op_dbt_bal = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}OpeningDebitBalance').text
        op_crd_bal = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}OpeningCreditBalance').text
        cl_dbt_bal = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}ClosingDebitBalance').text
        cl_crd_bal = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}ClosingCreditBalance').text
        grp_cat = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}GroupingCategory').text
        try:
            grp_code = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}GroupingCode').text
        except:
            grp_code = np.nan
        try:
            txnmy_code = account.find('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}TaxonomyCode').text
        except:
            txnmy_code = np.nan
    
        # print(acc_id.text,acc_desc.text,op_dbt_bal.text,op_crd_bal.text,cl_dbt_bal.text,cl_crd_bal.text,grp_cat.text,grp_code.text)
    
        array = pd.DataFrame([acc_id,acc_desc,op_dbt_bal,op_crd_bal,cl_dbt_bal,cl_crd_bal,grp_cat,grp_code,txnmy_code]).transpose()
        general_ledger= general_ledger.append(array,ignore_index=True)
    
    general_ledger.columns = ['AccountID','AccountDescription','OpeningDebitBalance','OpeningCreditBalance','ClosingDebitBalance','ClosingCreditBalance',
                              'GroupingCategory','GroupingCode','TaxonomyCode']
    
    for i in ['OpeningDebitBalance','OpeningCreditBalance','ClosingDebitBalance','ClosingCreditBalance']:
        general_ledger[i]=general_ledger.apply(lambda row: float(row[i]),axis=1)

    general_ledger['Second_ID'] = general_ledger.apply(lambda row: row['AccountID'][0:2],axis=1)

    condition1 = (general_ledger['OpeningDebitBalance']!=0.0) | (general_ledger['OpeningCreditBalance']!=0.0) | (general_ledger['ClosingDebitBalance']!=0.0) | (general_ledger['ClosingCreditBalance']!=0.0)
    
    general_ledger_final = general_ledger[condition1].copy()
    general_ledger_final['AccountID'] = general_ledger_final.apply(lambda row: int(row['AccountID']),axis=1)
    
    
    # Teste aos saldos do Balanço
    general_ledger_final['LenAccountID'] = general_ledger_final.apply(lambda row: len(str(row['AccountID'])),axis=1)
    
    condition = general_ledger_final['LenAccountID']==2
    
    gl_resumo = general_ledger_final[condition].copy()
    
    general_ledger_final['AccountID'] = general_ledger_final.apply(lambda row: str(row['AccountID']),axis=1)
    
    
    
    # gl_resumo['OpenNetDebitBalance'] = gl_resumo.apply(lambda row: row['OpeningDebitBalance']-row['OpeningCreditBalance'] if row['OpeningDebitBalance']-row['OpeningCreditBalance']>0 else 0,axis=1) 
    # gl_resumo['OpenNetCreditBalance'] = gl_resumo.apply(lambda row: row['OpeningCreditBalance']-row['OpeningDebitBalance'] if row['OpeningCreditBalance']-row['OpeningDebitBalance']>0 else 0,axis=1) 
    gl_resumo['OpenNetDebitBalance'] = gl_resumo.apply(lambda row: row['OpeningDebitBalance']-row['OpeningCreditBalance'] if row['OpeningDebitBalance']-row['OpeningCreditBalance']>0 else 0,axis=1) 
    gl_resumo['OpenNetCreditBalance'] = gl_resumo.apply(lambda row: row['OpeningCreditBalance']-row['OpeningDebitBalance'] if row['OpeningCreditBalance']-row['OpeningDebitBalance']>0 else 0,axis=1) 
    
    
    gl_resumo['NetDebitBalance'] = gl_resumo.apply(lambda row: row['ClosingDebitBalance']-row['ClosingCreditBalance'] if row['ClosingDebitBalance']-row['ClosingCreditBalance']>0 else 0,axis=1) 
    gl_resumo['NetCreditBalance'] = gl_resumo.apply(lambda row: row['ClosingCreditBalance']-row['ClosingDebitBalance'] if row['ClosingCreditBalance']-row['ClosingDebitBalance']>0 else 0,axis=1) 
    
    return general_ledger, gl_resumo

def getTransactions(xml_file): #necessária para a aplicação
    
    transactions = pd.DataFrame([])
    #iterwalk para aplicação ou iterparse para testes

    for _, trans in ET.iterparse(xml_file, events=("end",), tag='{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Transaction'):
        transaction_id = trans.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}TransactionID')
        period = trans.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Period')
        for line in trans.findall('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Lines'):
            for credit_line in line.findall('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}CreditLine'):
                account_id = credit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}AccountID')
                description = credit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Description')
                credit_amount = credit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}CreditAmount')
                debit_amount = 0.0
                array = pd.DataFrame([transaction_id,period,description,account_id,debit_amount,credit_amount]).transpose()
                transactions= transactions.append(array,ignore_index=True)
    
                
            for debit_line in line.findall('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}DebitLine'):
                account_id = debit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}AccountID')
                description = debit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}Description')
                debit_amount = debit_line.findtext('{urn:OECD:StandardAuditFile-Tax:PT_1.04_01}DebitAmount')
                credit_amount = 0.0
                
                array = pd.DataFrame([transaction_id,period,description,account_id,debit_amount,credit_amount]).transpose()
                transactions= transactions.append(array,ignore_index=True)
    
        # dict_list.append(elem.attrib)      # ALTERNATIVELY, PARSE ALL ATTRIBUTES
        trans.clear()
        line.clear()
        credit_line.clear()
        debit_line.clear()
    
    if transactions.empty==False:
        transactions.columns = ['Trans_ID','Trans_Per','Trans_Des','Account_ID','Debit_Amt','Credit_Amt']
        transactions.Debit_Amt = transactions.apply(lambda row: float(row['Debit_Amt']),axis=1)
        transactions.Credit_Amt = transactions.apply(lambda row: float(row['Credit_Amt']),axis=1)
        transactions.Trans_Per = transactions.apply(lambda row: int(row['Trans_Per']),axis=1)
        
        transactions.sort_values(by=['Trans_ID'],inplace=True) # transaction table for analysis ok
    
        transactions['Second_ID'] = transactions.apply(lambda row: row['Account_ID'][0:2],axis=1)
        
        exc_trans = np.unique(transactions[transactions['Second_ID']=='81'].Trans_ID)
        
        transactions_final = transactions[~transactions.Trans_ID.isin(exc_trans)]
        
        transactions_final['Data'] = transactions_final.apply(lambda row: row['Trans_ID'][0:10],axis=1)
        transactions_final['Data'] = pd.to_datetime(transactions_final['Data'])
        transactions_final['Ano'] = transactions_final['Data'].dt.year.astype(str)
    else:
        transactions_final = pd.DataFrame([])
    return transactions_final

def sum_id_transactions(accountid,second_level_length):
    first4 = accountid[0:4]
    last3 = accountid[-3:]
    first7 = accountid[0:7]
    first_snd_lvl = accountid[0:second_level_length]
    length = len(accountid)

    if (first4 == '4141') and (length>7):
        sumid = first4+last3
    elif (first4 == '4142') and (length>second_level_length):
        sumid = first_snd_lvl
    elif (first4 == '4111') and (length>7):
        sumid = first7
    elif (first4 == '4192') and (length>7):
        sumid = first7
    else:
        sumid = accountid
    return sumid


def sum_id_balances(accountid, second_level_length):
    first4 = accountid[0:4]
    last3 = accountid[-3:]
    # first7 = accountid[0:7]
    length = len(accountid)

    if (first4 == '4141') and (length>7):
        sumid = first4+last3
    elif (first4 == '4141') and (length==7):
        sumid = accountid
    elif (first4 == '4142') and (length==second_level_length):
        sumid = accountid
#    elif (first4 == '4143') and (length>7):
#        sumid = first7
    elif (first4 == '4143') and (length==7):
        sumid = accountid
    elif (first4 == '4111') and (length==7):
        sumid = accountid
    elif (first4 == '4113') and (length==6):
        sumid = accountid
    elif (first4 == '4191') and (length>=7):
        sumid = accountid
    elif (first4 == '4192') and (length==7):
        sumid = accountid
    elif (first4 == '4155') and (length==4):
        sumid = accountid
    elif (first4 == '4158') and (length>=5):
        sumid = accountid
    else:
        sumid = np.nan
    return sumid



def getDataTables(general_ledger, transactions_final, name, nif,end_dt):
    
    pivot_mensal = pd.pivot_table(data=transactions_final,index=['Trans_Per','Account_ID','Ano'],aggfunc='sum')
    pivot_mensal.reset_index(inplace=True)
    pivot_mensal['First_ID']=pivot_mensal.apply(lambda row: row['Account_ID'][0],axis=1)
    pivot_mensal['Second_ID']=pivot_mensal.apply(lambda row: row['Account_ID'][0:2],axis=1)
    pivot_mensal['Trim']=pivot_mensal.apply(lambda row: np.select([row['Trans_Per']==1,row['Trans_Per']==2,row['Trans_Per']==3,row['Trans_Per']==4,row['Trans_Per']==5,row['Trans_Per']==6,
                                                                   row['Trans_Per']==7,row['Trans_Per']==8,row['Trans_Per']==9,row['Trans_Per']==10,row['Trans_Per']==11],
                                                                   ['1T','1T','1T','2T','2T','2T','3T','3T','3T','4T','4T'],'4T'),axis=1)
    pivot_mensal['Trim'] = pivot_mensal['Trim'].astype(str)

    
    pivot_sum_firstid = pd.pivot_table(data=pivot_mensal,index=['Trans_Per','First_ID','Ano'],aggfunc='sum')
    pivot_sum_firstid.reset_index(inplace=True)
    pivot_sum_firstid['Net_Credit_Amt'] = pivot_sum_firstid['Credit_Amt']-pivot_sum_firstid['Debit_Amt']
    pivot_sum_firstid['Net_Debit_Amt'] = pivot_sum_firstid['Debit_Amt']-pivot_sum_firstid['Credit_Amt']

    pivot_sum_firstid['Trim']=pivot_sum_firstid.apply(lambda row: np.select([row['Trans_Per']==1,row['Trans_Per']==2,row['Trans_Per']==3,row['Trans_Per']==4,row['Trans_Per']==5,row['Trans_Per']==6,
                                                                             row['Trans_Per']==7,row['Trans_Per']==8,row['Trans_Per']==9,row['Trans_Per']==10,row['Trans_Per']==11],
                                                                            ['1T','1T','1T','2T','2T','2T','3T','3T','3T','4T','4T'],'4T'),axis=1)
    # fazer a tabela com os custos por trimestre
    pivot_sum_firstid['First_ID'] = pivot_sum_firstid['First_ID'].astype(str)
    pivot_sum_firstid['Trim'] = pivot_sum_firstid['Trim'].astype(str)

    pivot_custos_trim = pd.pivot_table(data=pivot_sum_firstid[pivot_sum_firstid.First_ID=='6'],index=['Trim','Ano'],aggfunc='sum')
    pivot_custos_trim.reset_index(inplace=True)

    # fazer a tabela com os proveitos por trimestre
    pivot_proveitos_trim = pd.pivot_table(data=pivot_sum_firstid[pivot_sum_firstid.First_ID=='7'],index=['Trim','Ano'],aggfunc='sum')
    pivot_proveitos_trim.reset_index(inplace=True)

    #fazer o merge dos custos e proveitos
    if pivot_proveitos_trim.empty==False:
        pivot_prov_trim = pivot_proveitos_trim[['Trim','Ano','Net_Credit_Amt']].copy()
        pivot_prov_trim.columns=['Trim','Ano','Proveitos']
    else:
        pivot_prov_trim = pd.DataFrame([])
    
    if pivot_custos_trim.empty==False:
        pivot_cust_trim = pivot_custos_trim[['Trim','Ano','Net_Debit_Amt']].copy()
        pivot_cust_trim.columns=['Trim','Ano','Custos']
    else:
        pivot_cust_trim = pd.DataFrame([])

    if (pivot_prov_trim.empty==True) and (pivot_cust_trim.empty==True):
        pivot_pcl_trim = pd.DataFrame([])
    elif pivot_prov_trim.empty==True:
        pivot_pcl_trim = pivot_cust_trim
        pivot_pcl_trim['Proveitos']=0
        pivot_pcl_trim['Lucros'] = pivot_pcl_trim['Proveitos'] - pivot_pcl_trim['Custos'] #falta por o nome e o nif
        pivot_pcl_trim['Data'] = pivot_pcl_trim.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)

    elif pivot_cust_trim.empty==True:
        pivot_pcl_trim = pivot_prov_trim
        pivot_pcl_trim['Custos']=0
        pivot_pcl_trim['Lucros'] = pivot_pcl_trim['Proveitos'] - pivot_pcl_trim['Custos'] #falta por o nome e o nif
        pivot_pcl_trim['Data'] = pivot_pcl_trim.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)

    else:
        pivot_pcl_trim = pivot_prov_trim.merge(pivot_cust_trim,on=['Trim','Ano'],how='left')
        pivot_pcl_trim['Lucros'] = pivot_pcl_trim['Proveitos'] - pivot_pcl_trim['Custos'] #falta por o nome e o nif
        pivot_pcl_trim['Data'] = pivot_pcl_trim.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)

    pivot_pcl_trim['Nome'] = name
    pivot_pcl_trim['NIF'] = nif
    #pivot_pcl_trim = pivot_pcl_trim[['Nome', 'NIF', 'Data','Trim', 'Ano', 'Proveitos', 'Custos', 'Lucros']].copy()

    # Custos mais importantes
    pivot_top_custos = pd.pivot_table(data=pivot_mensal[pivot_mensal.First_ID=='6'],index=['Trim','Ano','Account_ID'],aggfunc='sum')
    if pivot_top_custos.empty==False:
        pivot_top_custos.reset_index(inplace=True)
        pivot_top_custos['Net_Debit_Amt'] = pivot_top_custos['Debit_Amt']-pivot_top_custos['Credit_Amt']
        pivot_top_custos['Third_ID'] = pivot_top_custos.apply(lambda row: row['Account_ID'][0:3],axis=1)
        pivot_top_custos = pivot_top_custos.merge(general_ledger[['AccountID','AccountDescription']],left_on='Third_ID',right_on='AccountID',how='left')
        pivot_top_custos = pd.pivot_table(pivot_top_custos[['Trim','Ano','Third_ID','AccountDescription','Net_Debit_Amt']],index=['Trim','Ano','Third_ID','AccountDescription'],aggfunc='sum')
        pivot_top_custos.reset_index(inplace=True)
        pivot_top_custos['Nome'] = name
        pivot_top_custos['NIF'] = nif
        pivot_top_custos['Data'] = pivot_top_custos.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
        pivot_top_custos = pivot_top_custos[['Nome','NIF','Data','Trim','Ano','Third_ID','AccountDescription','Net_Debit_Amt']].copy()
    
    # Proveitos mais importantes
    pivot_top_proveitos = pd.pivot_table(data=pivot_mensal[pivot_mensal.First_ID=='7'],index=['Trim','Ano','Account_ID'],aggfunc='sum')
    if pivot_top_proveitos.empty==False:
        pivot_top_proveitos.reset_index(inplace=True)
        pivot_top_proveitos['Second_ID'] = pivot_top_proveitos.apply(lambda row: row['Account_ID'][0:2],axis=1)
        pivot_top_proveitos['Net_Credit_Amt'] = pivot_top_proveitos['Credit_Amt']-pivot_top_proveitos['Debit_Amt']
        pivot_top_proveitos = pivot_top_proveitos.merge(general_ledger[['AccountID','AccountDescription']],left_on='Second_ID',right_on='AccountID',how='left')
        pivot_top_proveitos = pd.pivot_table(pivot_top_proveitos[['Trim','Ano','Second_ID','AccountDescription','Net_Credit_Amt']],index=['Trim','Ano','Second_ID','AccountDescription'],aggfunc='sum')
        pivot_top_proveitos.reset_index(inplace=True)
        pivot_top_proveitos['Nome'] = name
        pivot_top_proveitos['NIF'] = nif
        pivot_top_proveitos['Data'] = pivot_top_proveitos.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
        pivot_top_proveitos = pivot_top_proveitos[['Nome','NIF','Data','Trim','Ano','Second_ID','AccountDescription','Net_Credit_Amt']].copy()


    # Fornecedores mais importantes
    pivot_top_fornecedores = pd.pivot_table(data=pivot_mensal[pivot_mensal.Second_ID=='22'],index=['Trim','Ano','Account_ID'],aggfunc='sum')
    if pivot_top_fornecedores.empty==False:
        pivot_top_fornecedores.reset_index(inplace=True)
        pivot_top_fornecedores = pivot_top_fornecedores.merge(general_ledger[['AccountID','AccountDescription']],left_on='Account_ID',right_on='AccountID',how='left')
        pivot_top_fornecedores.drop(columns=['Trans_Per','Debit_Amt','AccountID'],inplace=True)  
        pivot_top_fornecedores['Nome'] = name
        pivot_top_fornecedores['NIF'] = nif
        pivot_top_fornecedores['Data'] = pivot_top_fornecedores.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
        pivot_top_fornecedores = pivot_top_fornecedores[['Nome','NIF','Data','Trim','Ano','Account_ID','AccountDescription','Credit_Amt']].copy()


    # Clientes mais importantes
    pivot_top_clients = pd.pivot_table(data=pivot_mensal[pivot_mensal.Second_ID=='21'],index=['Trim','Ano','Account_ID'],aggfunc='sum')
    if pivot_top_clients.empty==False:
        pivot_top_clients.reset_index(inplace=True)
        pivot_top_clients = pivot_top_clients.merge(general_ledger[['AccountID','AccountDescription']],left_on='Account_ID',right_on='AccountID',how='left')
        pivot_top_clients.drop(columns=['Trans_Per','Credit_Amt','AccountID'],inplace=True)
        pivot_top_clients['Nome'] = name
        pivot_top_clients['NIF'] = nif
        pivot_top_clients['Data'] = pivot_top_clients.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
        pivot_top_clients = pivot_top_clients[['Nome','NIF','Data','Trim','Ano','Account_ID','AccountDescription','Debit_Amt']].copy()


    # Investimentos
    # pivot_top_invest = pd.pivot_table(data=pivot_mensal[pivot_mensal.Second_ID=='41'],index=['Trim','Ano','Account_ID'],aggfunc='sum')
    # if pivot_top_invest.empty==False:
    #     pivot_top_invest.reset_index(inplace=True)
    #     pivot_top_invest = pivot_top_invest.merge(general_ledger[['AccountID','AccountDescription']],left_on='Account_ID',right_on='AccountID',how='left')
    #     pivot_top_invest.drop(columns=['Trans_Per','AccountID'],inplace=True)
    #     pivot_top_invest['Nome'] = name
    #     pivot_top_invest['NIF'] = nif
    #     pivot_top_invest['Data'] = pivot_top_invest.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
    #     pivot_top_invest = pivot_top_invest[['Nome','NIF','Data','Trim','Ano','Account_ID','AccountDescription','Debit_Amt','Credit_Amt']].copy()













    # Investimentos da conta 41
    pivot_invest = pivot_mensal[pivot_mensal.Second_ID=='41']
    if pivot_invest.empty==False:
        # pivot_invest['Forth_ID'] = pivot_invest.apply(lambda row: row['Account_ID'][0:4],axis=1)
        # pivot_invest['Last_3_ID'] = pivot_invest.apply(lambda row: row['Account_ID'][-3:],axis=1)
        # pivot_invest['Seventh_ID'] = pivot_invest.apply(lambda row: row['Account_ID'][0:7],axis=1)
        # pivot_invest['len'] = pivot_invest.apply(lambda row: len(row['Account_ID']),axis=1)
        # pivot_invest['ID_sum'] = pivot_invest.apply(lambda row: row['Forth_ID']+row['Last_3_ID'] if (row['len']>7) and (row['Forth_ID']=='4141') else np.nan,axis=1)
        # pivot_invest['ID_sum_II'] = pivot_invest.apply(lambda row: row['Account_ID'] if row['len']==7 else row['ID_sum'],axis=1)
        # pivot_invest['ID_sum_final'] = pivot_invest.apply(lambda row: row['Seventh_ID'] if (row['len']>7) and (row['Forth_ID']=='4142') else row['ID_sum_II'],axis=1)
        # table_4142_trans = pivot_invest[pivot_invest['Forth_ID']=='4142']
        # if table_4142_trans.empty == False:
            # second_level_length_trans = np.sort(np.unique(table_4142_trans.len))[1]
        # else:
            # second_level_length_trans = 0
        
        
        # pivot_invest['test'] = pivot_invest['ID_sum_final'] == pivot_invest['sum_id']
        
        # pivot_invest['ID_sum'] = pivot_invest['Forth_ID']+pivot_invest['Last_3_ID']
    
        gl_invest = general_ledger[general_ledger.Second_ID=='41']
        gl_invest['Forth_ID'] = gl_invest.apply(lambda row: row['AccountID'][0:4],axis=1)
        # gl_invest['Last_3_ID'] = gl_invest.apply(lambda row: row['AccountID'][-3:],axis=1)
        gl_invest['len'] = gl_invest.apply(lambda row: len(row['AccountID']),axis=1)
        # gl_invest['ID_sum'] = gl_invest.apply(lambda row: row['Forth_ID']+row['Last_3_ID'] if (row['len']>7) and (row['Forth_ID']=='4141') else np.nan,axis=1)
        # gl_invest['ID_sum_final'] = gl_invest.apply(lambda row: row['AccountID'] if row['len']==7 else row['ID_sum'],axis=1)

        table_4142_bal = gl_invest[gl_invest['Forth_ID']=='4142']
        if table_4142_bal.empty == False:
            second_level_length_bal = np.sort(np.unique(table_4142_bal.len))[1]
        else:
            second_level_length_bal = 0

        pivot_invest['sum_id'] = pivot_invest.apply(lambda row: sum_id_transactions(row['Account_ID'],second_level_length_bal),axis=1)
        pivot_invest_sum = pd.pivot_table(data=pivot_invest,index=['Trim','Ano','sum_id'],aggfunc='sum')

        gl_invest['sum_id'] = gl_invest.apply(lambda row: sum_id_balances(row['AccountID'],second_level_length_bal),axis=1)
        
        # gl_invest['test'] = gl_invest['ID_sum_final'] == gl_invest['sum_id']

        
        # gl_invest['number'] = gl_invest.apply(lambda row: len(row['AccountID']),axis=1)
        # gl_invest_final = gl_invest[gl_invest['number']>=7].copy()    
        # gl_invest_final['Forth_ID'] = gl_invest_final.apply(lambda row: row['AccountID'][0:4],axis=1)
        # gl_invest_final['Last_3_ID'] = gl_invest_final.apply(lambda row: row['AccountID'][-3:],axis=1)
        # gl_invest_final['ID_sum'] = gl_invest_final['Forth_ID']+gl_invest_final['Last_3_ID']
        gl_invest_final = gl_invest[~gl_invest['sum_id'].isna()]
        
        gl_invest_saldo_ini = pd.pivot_table(data=gl_invest_final[['sum_id','AccountDescription','OpeningDebitBalance']],index=['sum_id','AccountDescription'],aggfunc='sum')
        pivot_invest_sum.reset_index(inplace=True)
        gl_invest_saldo_ini.reset_index(inplace=True)
    
        trim = '1T'
        inv_1t = pivot_invest_sum[pivot_invest_sum.Trim==trim]
        inv_1t_final = gl_invest_saldo_ini.merge(inv_1t,on='sum_id',how='outer')
        inv_1t_final['Trim'] = trim
        # ano_x = [x for x in un if isinstance(x, str)][0]
        # inv_1t_final['Ano'] = inv_1t_final['Ano'].unique()
        inv_1t_final.fillna(0,inplace=True)
        inv_1t_final['Amount'] = inv_1t_final['OpeningDebitBalance']+inv_1t_final['Debit_Amt']-inv_1t_final['Credit_Amt']
        inv_1t_final['Amount'] = round(inv_1t_final['Amount'],2)
    
        if (end_dt[-5:] == '06-30') | (end_dt[-5:] == '09-30') | (end_dt[-5:] == '12-31'):
            inv_2t = pivot_invest_sum[(pivot_invest_sum.Trim=='1T') | (pivot_invest_sum.Trim=='2T')]
            inv_2t_pvt = pd.pivot_table(inv_2t,index='sum_id',aggfunc='sum')
            inv_2t_pvt.reset_index(inplace=True)
            inv_2t_final = gl_invest_saldo_ini.merge(inv_2t_pvt,on='sum_id',how='outer')
            # inv_2t_final['Ano'] = inv_2t['Ano'].unique()[0]
            inv_2t_final.fillna(0,inplace=True)
            inv_2t_final['Trim']='2T'
            inv_2t_final['Amount'] = inv_2t_final['OpeningDebitBalance']+inv_2t_final['Debit_Amt']-inv_2t_final['Credit_Amt']
            inv_2t_final['Amount'] = round(inv_2t_final['Amount'],2)
        else:
            inv_2t_final = []
     
        if (end_dt[-5:] == '09-30') | (end_dt[-5:] == '12-31'):
            inv_3t = pivot_invest_sum[(pivot_invest_sum.Trim=='1T') | (pivot_invest_sum.Trim=='2T') | (pivot_invest_sum.Trim=='3T')]
            inv_3t_pvt = pd.pivot_table(inv_3t,index='sum_id',aggfunc='sum')
            inv_3t_pvt.reset_index(inplace=True)
            inv_3t_final = gl_invest_saldo_ini.merge(inv_3t_pvt,on='sum_id',how='outer')
            # inv_3t_final['Ano'] = inv_3t['Ano'].unique()[0]
            inv_3t_final.fillna(0,inplace=True)
            inv_3t_final['Trim']='3T'
            inv_3t_final['Amount'] = inv_3t_final['OpeningDebitBalance']+inv_3t_final['Debit_Amt']-inv_3t_final['Credit_Amt']
            inv_3t_final['Amount'] = round(inv_3t_final['Amount'],2)
        else:
            inv_3t_final = []
    
        if (end_dt[-5:] == '12-31'):
            inv_4t = pivot_invest_sum[(pivot_invest_sum.Trim=='1T') | (pivot_invest_sum.Trim=='2T') | (pivot_invest_sum.Trim=='3T') | (pivot_invest_sum.Trim=='4T')]
            inv_4t_pvt = pd.pivot_table(inv_4t,index='sum_id',aggfunc='sum')
            inv_4t_pvt.reset_index(inplace=True)
            inv_4t_final = gl_invest_saldo_ini.merge(inv_4t_pvt,on='sum_id',how='outer')
            inv_4t_final.fillna(0,inplace=True)
            inv_4t_final['Trim']='4T'
            # inv_4t_final['Ano'] = inv_4t['Ano'].unique()[0]
            inv_4t_final['Amount'] = inv_4t_final['OpeningDebitBalance']+inv_4t_final['Debit_Amt']-inv_4t_final['Credit_Amt']
            inv_4t_final['Amount'] = round(inv_4t_final['Amount'],2)
        else:
            inv_4t_final = []
        
        
        if (end_dt[-5:] == '12-31'):
            inv_final = pd.concat([inv_1t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_2t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_3t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_4t_final[['sum_id','AccountDescription','Trim','Amount']].copy()])
        elif (end_dt[-5:] == '09-30'):
            inv_final = pd.concat([inv_1t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_2t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_3t_final[['sum_id','AccountDescription','Trim','Amount']].copy()])
        elif (end_dt[-5:] == '06-30'):
            inv_final = pd.concat([inv_1t_final[['sum_id','AccountDescription','Trim','Amount']].copy(),inv_2t_final[['sum_id','AccountDescription','Trim','Amount']].copy()])
        else:
            inv_final = pd.concat([inv_1t_final[['sum_id','AccountDescription','Trim','Amount']].copy()])
        
        inv_final['Nome'] = name
        inv_final['NIF'] = nif
        inv_final['Ano'] = pivot_invest_sum['Ano'].unique()[0]
        inv_final['Data'] = inv_final.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
    else:
        inv_final = pd.DataFrame([])

    # Preparar os dados para calcular os KPI
    pivot_sum_secondid = pd.pivot_table(data=pivot_mensal,index=['Trim','Ano','Second_ID'],aggfunc='sum')
    pivot_sum_secondid.reset_index(inplace=True)
    
    pivot_sum_secondid['Net_Credit_Amt'] = pivot_sum_secondid.apply(lambda row: row['Credit_Amt']-row['Debit_Amt'] if row['Credit_Amt']-row['Debit_Amt']>0 else 0,axis=1)
    pivot_sum_secondid['Net_Debit_Amt'] = pivot_sum_secondid.apply(lambda row: row['Debit_Amt']-row['Credit_Amt'] if row['Debit_Amt']-row['Credit_Amt']>0 else 0,axis=1)
    pivot_sum_secondid['Second_ID'] =  pivot_sum_secondid['Second_ID'].astype(int)
    
    # pivot_init_bal = pd.pivot_table(data=general_ledger,index='Second_ID',aggfunc='sum')
    # pivot_init_bal.reset_index(inplace=True)

    return pivot_pcl_trim, pivot_top_custos, pivot_top_proveitos, pivot_top_fornecedores, pivot_top_clients, pivot_sum_secondid, inv_final


# conta = 11
# trim = '4T'
def calc_saldos(gl_resumo,pivot_sum_secondid,conta,trim): #função acessória
    condicao1trim = (pivot_sum_secondid['Second_ID']==conta) & (pivot_sum_secondid['Trim']=='1T')
    condicao2trim = (pivot_sum_secondid['Second_ID']==conta) & ((pivot_sum_secondid['Trim']=='1T') | (pivot_sum_secondid['Trim']=='2T'))
    condicao3trim = (pivot_sum_secondid['Second_ID']==conta) & ((pivot_sum_secondid['Trim']=='1T') | (pivot_sum_secondid['Trim']=='2T') | (pivot_sum_secondid['Trim']=='3T'))
    condicao4trim = (pivot_sum_secondid['Second_ID']==conta)
    
    condicao2 = np.select([trim=='1T',trim=='2T',trim=='3T'],[condicao1trim,condicao2trim,condicao3trim],condicao4trim)
    
    condicao = gl_resumo['AccountID']==conta
    if gl_resumo[condicao].empty:
        init_bal_deb = 0
        init_bal_cred = 0
    else:
        init_bal_deb = gl_resumo[condicao]['OpeningDebitBalance'].sum()
        init_bal_cred = gl_resumo[condicao]['OpeningCreditBalance'].sum()
    if pivot_sum_secondid[condicao2].empty:
        trans_deb = 0
        trans_cred = 0 
    else:
        trans_deb = pivot_sum_secondid[condicao2]['Debit_Amt'].sum()
        trans_cred = pivot_sum_secondid[condicao2]['Credit_Amt'].sum()
    end_bal_deb = init_bal_deb + trans_deb
    end_bal_cred = init_bal_cred + trans_cred
    
    return trim, pivot_sum_secondid['Ano'].iloc[0],conta,end_bal_deb,end_bal_cred


def getDataKPI(pivot_sum_secondid,gl_resumo,name,nif ):
        # Criar dataframes com os saldos finais de todos os second id de cada trimestre
        # len(np.unique(pivot_sum_secondid['Second_ID']))
        # len(np.unique(pivot_init_bal['Second_ID']))
        list_trims = pivot_sum_secondid['Trim'].unique()
        list_accounts = pd.concat([pivot_sum_secondid['Second_ID'],gl_resumo['AccountID']]).drop_duplicates().sort_values().reset_index(drop=True)
        
        # i='25'
        
        saldos1_trim = pd.DataFrame([],columns=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance'])
        if '1T' in list_trims:
            for i in np.unique(list_accounts):
                trim,ano,conta,cl_debit,cl_credit = calc_saldos(gl_resumo,pivot_sum_secondid,i,'1T')
                temp = [trim,ano,conta,cl_debit,cl_credit]
                temp_df = pd.DataFrame(temp,index=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance']).T
                saldos1_trim = saldos1_trim.append(temp_df)
                # print(i)

        saldos2_trim = pd.DataFrame([],columns=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance'])
        if '2T' in list_trims:
            for i in np.unique(list_accounts):
                trim,ano,conta,cl_debit,cl_credit = calc_saldos(gl_resumo,pivot_sum_secondid,i,'2T')
                temp = [trim,ano,conta,cl_debit,cl_credit]
                temp_df = pd.DataFrame(temp,index=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance']).T
                saldos2_trim = saldos2_trim.append(temp_df)
                # print(i)

        saldos3_trim = pd.DataFrame([],columns=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance'])
        if '3T' in list_trims:
            for i in np.unique(list_accounts):
                trim,ano,conta,cl_debit,cl_credit = calc_saldos(gl_resumo,pivot_sum_secondid,i,'3T')
                temp = [trim,ano,conta,cl_debit,cl_credit]
                temp_df = pd.DataFrame(temp,index=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance']).T
                saldos3_trim = saldos3_trim.append(temp_df)
                # print(i)

        saldos4_trim = pd.DataFrame([],columns=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance'])
        if '4T' in list_trims:
            for i in np.unique(list_accounts):
                trim,ano,conta,cl_debit,cl_credit = calc_saldos(gl_resumo,pivot_sum_secondid,i,'4T')
                temp = [trim,ano,conta,cl_debit,cl_credit]
                temp_df = pd.DataFrame(temp,index=['Trim','Ano','Second_ID','ClosingDebitBalance','ClosingCreditBalance']).T
                saldos4_trim = saldos4_trim.append(temp_df)
                # print(i)
        
        if '4T' in list_trims:
            saldos = pd.concat([saldos1_trim,saldos2_trim,saldos3_trim,saldos4_trim])
        elif '3T' in list_trims:
            saldos = pd.concat([saldos1_trim,saldos2_trim,saldos3_trim])
        elif '2T' in list_trims:
            saldos = pd.concat([saldos1_trim,saldos2_trim])
        else:
            saldos = saldos1_trim


        saldos['Second_ID'] = saldos['Second_ID'].astype(str)
        # saldos['First_ID'] = saldos.apply(lambda row: row['Second_ID'][0], axis=1)
        # condicao3 = (saldos['First_ID']!='6') & (saldos['First_ID']!='7') & (saldos['First_ID']!='8')
        # saldos_final = saldos[condicao3]
        # saldos_final.drop(columns='First_ID',inplace=True)
        saldos_final = saldos.copy()
        saldos_final.reset_index(drop=True,inplace=True)
        saldos_final['Nome'] = name
        saldos_final['NIF'] = nif
        saldos_final['Data'] = saldos_final.apply(lambda row: np.select([row['Trim']=='1T',row['Trim']=='2T',row['Trim']=='3T'],[row['Ano']+'-03-31',row['Ano']+'-06-30',row['Ano']+'-09-30'],row['Ano']+'-12-31').item(),axis=1)
        saldos_final['NetDebitBalance']=saldos_final.apply(lambda row: row['ClosingDebitBalance']-row['ClosingCreditBalance'] if row['ClosingDebitBalance']-row['ClosingCreditBalance']>0 else 0,axis=1)
        saldos_final['NetCreditBalance']=saldos_final.apply(lambda row: row['ClosingCreditBalance']-row['ClosingDebitBalance'] if row['ClosingCreditBalance']-row['ClosingDebitBalance']>0 else 0,axis=1)
        saldos_final2 = saldos_final[['Nome','NIF','Data','Trim', 'Ano', 'Second_ID', 'ClosingDebitBalance','ClosingCreditBalance','NetDebitBalance','NetCreditBalance']].copy()
        
        return saldos_final2

        
def calculateKPI(pivot_top_custos,pivot_top_proveitos,saldos_final2,general_ledger,gl_resumo):
    
    saldos_final2['Second_ID'] = saldos_final2['Second_ID'].astype(int)
    
    kpi_trim = pd.DataFrame([],columns=['Nome','NIF','Data','Trim','Ano','KPI','Valor'])
    # =============================================================================
    # Calcular algumas métricas simples e importantes
    # =============================================================================
    # LIQUIDEZ - calcular o current ratio
    #CURRENT ASSETS = somar o Closing Debit Balance de 11,12,13,14,15,21,24,25,26
    #CURRENT LIABILITIES = somar o Closing Credit Balance de 22,24,25,26
    #CURRENT RATIO = CURRENT ASSETS / CURRENT LIABILITIES
    cur_assets = (saldos_final2['Second_ID']==11) | (saldos_final2['Second_ID']==12) | (saldos_final2['Second_ID']==13) | (saldos_final2['Second_ID']==14) | (saldos_final2['Second_ID']==15) | (saldos_final2['Second_ID']==21) | (saldos_final2['Second_ID']==24) | (saldos_final2['Second_ID']==25) | (saldos_final2['Second_ID']==26)
    cur_liab = (saldos_final2['Second_ID']==22) | (saldos_final2['Second_ID']==23) | (saldos_final2['Second_ID']==24) | (saldos_final2['Second_ID']==25)

    for i in ['1T','2T','3T','4T']:
        condicao4 = saldos_final2['Trim']==i
        temp_df2 = saldos_final2[condicao4]
        if temp_df2.empty==False:
            current_assets = temp_df2[cur_assets].NetDebitBalance.sum()
            current_liabilities = temp_df2[cur_liab].NetCreditBalance.sum()
            current_ratio = current_assets / current_liabilities
            nome = temp_df2['Nome'].iloc[0]
            nif = temp_df2['NIF'].iloc[0]
            data = temp_df2['Data'].iloc[0]
            ano = temp_df2['Ano'].iloc[0]
            row = pd.DataFrame([nome,nif,data,i,ano,'CurrentRatio',current_ratio], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            kpi_trim = kpi_trim.append(row)
    
    #SOLVABILIDADE
    #DEBT-TO-ASSETS
    #DEBT-TO-EQUITY - incluir a divida a accionistas como equity. Para todos os efeitos é dinheiro do acionista que este pode tirar sem pagar imposto
    debt = (saldos_final2['Second_ID']==22) |(saldos_final2['Second_ID']==23) |(saldos_final2['Second_ID']==24) | (saldos_final2['Second_ID']==25) | (saldos_final2['Second_ID']==27) | (saldos_final2['Second_ID']==28) | (saldos_final2['Second_ID']==29)
    assets = (saldos_final2['Second_ID']==11) | (saldos_final2['Second_ID']==12) | (saldos_final2['Second_ID']==13) | (saldos_final2['Second_ID']==14) | (saldos_final2['Second_ID']==15) | (saldos_final2['Second_ID']==21) | (saldos_final2['Second_ID']==24) | (saldos_final2['Second_ID']==25) | (saldos_final2['Second_ID']==26) | (saldos_final2['Second_ID']==27) | (saldos_final2['Second_ID']==28) |(saldos_final2['Second_ID']==29) | (saldos_final2['Second_ID']==32) | (saldos_final2['Second_ID']==33) | (saldos_final2['Second_ID']==34) | (saldos_final2['Second_ID']==35) | (saldos_final2['Second_ID']==36) | (saldos_final2['Second_ID']==37) |(saldos_final2['Second_ID']==38) |(saldos_final2['Second_ID']==39) | (saldos_final2['Second_ID']==41) | (saldos_final2['Second_ID']==42) | (saldos_final2['Second_ID']==43) | (saldos_final2['Second_ID']==44) | (saldos_final2['Second_ID']==45) |(saldos_final2['Second_ID']==46)
    
    equity_pos = (saldos_final2['Second_ID']==51) | (saldos_final2['Second_ID']==52) | (saldos_final2['Second_ID']==53) | (saldos_final2['Second_ID']==54) | (saldos_final2['Second_ID']==55) | (saldos_final2['Second_ID']==56) | (saldos_final2['Second_ID']==57) | (saldos_final2['Second_ID']==58) | (saldos_final2['Second_ID']==59) | (saldos_final2['Second_ID']==26) | (saldos_final2['Second_ID']==71) | (saldos_final2['Second_ID']==72) | (saldos_final2['Second_ID']==73) | (saldos_final2['Second_ID']==74) | (saldos_final2['Second_ID']==75) | (saldos_final2['Second_ID']==76) | (saldos_final2['Second_ID']==77) | (saldos_final2['Second_ID']==78) | (saldos_final2['Second_ID']==79) | (saldos_final2['Second_ID']==81)
    equity_neg = (saldos_final2['Second_ID']==51) | (saldos_final2['Second_ID']==52) | (saldos_final2['Second_ID']==53) | (saldos_final2['Second_ID']==54) | (saldos_final2['Second_ID']==55) | (saldos_final2['Second_ID']==56) | (saldos_final2['Second_ID']==57) | (saldos_final2['Second_ID']==58) | (saldos_final2['Second_ID']==59) | (saldos_final2['Second_ID']==61) | (saldos_final2['Second_ID']==62) | (saldos_final2['Second_ID']==63) | (saldos_final2['Second_ID']==64) | (saldos_final2['Second_ID']==65) | (saldos_final2['Second_ID']==66) | (saldos_final2['Second_ID']==67) | (saldos_final2['Second_ID']==68) | (saldos_final2['Second_ID']==69)
    
    ebitda_contrib_pos = (saldos_final2['Second_ID']==71) | (saldos_final2['Second_ID']==72) | (saldos_final2['Second_ID']==73) | (saldos_final2['Second_ID']==74) | (saldos_final2['Second_ID']==75) | (saldos_final2['Second_ID']==76)
    ebitda_contrib_neg = (saldos_final2['Second_ID']==61) | (saldos_final2['Second_ID']==62) | (saldos_final2['Second_ID']==63) | (saldos_final2['Second_ID']==64) | (saldos_final2['Second_ID']==65)

    cash = (saldos_final2['Second_ID']==11) | (saldos_final2['Second_ID']==12)
    
    i='4T'
    for i in ['1T','2T','3T','4T']:
        condicao5 = saldos_final2['Trim']==i
        temp_df3 = saldos_final2[condicao5]
        if temp_df3.empty==False:
            assets_value = temp_df3[assets].NetDebitBalance.sum()
            debt_value = temp_df3[debt].NetCreditBalance.sum()
            equity_pos_value = temp_df3[equity_pos].NetCreditBalance.sum()
            equity_neg_value = temp_df3[equity_neg].NetDebitBalance.sum()
            equity_value = equity_pos_value - equity_neg_value
            ebitda_pos_value = temp_df3[ebitda_contrib_pos].NetCreditBalance.sum()
            ebitda_neg_value = temp_df3[ebitda_contrib_neg].NetDebitBalance.sum()
            ebitda_value = ebitda_pos_value - ebitda_neg_value
            cash_value = temp_df3[cash].NetDebitBalance.sum()
            net_debt_ebitda = (debt_value - cash_value) / ebitda_value
            debt_to_assets = debt_value / assets_value
            # debt_to_equity = debt_value / equity_value
            nome = temp_df3['Nome'].iloc[0]
            nif = temp_df3['NIF'].iloc[0]
            data = temp_df3['Data'].iloc[0]
            ano = temp_df3['Ano'].iloc[0]
            row1 = pd.DataFrame([nome,nif,data,i,ano,'DebtToAssets',debt_to_assets], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            row2 = pd.DataFrame([nome,nif,data,i,ano,'NetDebtToEBITDA',net_debt_ebitda], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            kpi_trim = kpi_trim.append(row1)
            kpi_trim = kpi_trim.append(row2)
        
    # agora estou na fase em que é necessário interagir com rubricas de DR e de Balanço para calcular os rácios.     
    # para já nesta fase o que vou fazer é anualizar as rubricas que vem da DR.    
    # RENTABILIDADE
    #MARGEM LIQUIDA
    try:
        cond_irc1 = (general_ledger['AccountDescription']=='Imposto Estimado') & (general_ledger['AccountID'].str.contains('24'))
        estimativa_irc = general_ledger[cond_irc1].ClosingCreditBalance.iloc[0]
    except:
        try:    
            cond_irc2 = (general_ledger['AccountDescription'].str.contains('Imposto estimado')) & (general_ledger['AccountID'].str.contains('24'))
            estimativa_irc = general_ledger[cond_irc2].ClosingCreditBalance.iloc[0]
        except:
            try:    
                cond_irc3 = (general_ledger['AccountDescription'].str.contains('Imposto Estimado')) & (general_ledger['AccountID'].str.contains('24'))
                estimativa_irc = general_ledger[cond_irc3].ClosingCreditBalance.iloc[0]
            except:
                try:    
                    cond_irc4 = (general_ledger['AccountDescription'].str.contains('imposto estimado')) & (general_ledger['AccountID'].str.contains('24'))
                    estimativa_irc = general_ledger[cond_irc4].ClosingCreditBalance.iloc[0]
                except:
                    estimativa_irc = 0
    
    saldos_final2['Second_ID']= saldos_final2['Second_ID'].astype(str)
    saldos_final2['First_ID']=saldos_final2.apply(lambda row: row['Second_ID'][0],axis=1)
    
    rev = saldos_final2['First_ID']=='7'
    cos = saldos_final2['First_ID']=='6'
    ebitda_contrib_pos = (saldos_final2['Second_ID']=='71') | (saldos_final2['Second_ID']=='72') | (saldos_final2['Second_ID']=='73') | (saldos_final2['Second_ID']=='74') | (saldos_final2['Second_ID']=='75') | (saldos_final2['Second_ID']=='76')
    ebitda_contrib_neg = (saldos_final2['Second_ID']=='61') | (saldos_final2['Second_ID']=='62') | (saldos_final2['Second_ID']=='63') | (saldos_final2['Second_ID']=='64') | (saldos_final2['Second_ID']=='65')

    
    for i in ['1T','2T','3T','4T']:
        condicao6 = saldos_final2['Trim']==i
        temp_df4 = saldos_final2[condicao6]
        if temp_df4.empty==False:
            mult = np.select([i=='1T',i=='2T',i=='3T'],[4,2,4/3],1)
            revenues = temp_df4[rev].NetCreditBalance.sum()*mult
            costs = temp_df4[cos].NetDebitBalance.sum()*mult
            net_income = revenues - costs -estimativa_irc
            # net_income_margin = net_income / revenues
            assets_value = temp_df4[assets].NetDebitBalance.sum()
            equity_pos_value = temp_df4[equity_pos].NetCreditBalance.sum()
            equity_neg_value = temp_df4[equity_neg].NetDebitBalance.sum()
            ebitda_pos_value = temp_df4[ebitda_contrib_pos].NetCreditBalance.sum()
            ebitda_neg_value = temp_df4[ebitda_contrib_neg].NetDebitBalance.sum()
            ebitda_value = ebitda_pos_value - ebitda_neg_value
            equity_value = equity_pos_value - equity_neg_value
            return_on_equity = net_income / equity_value
            return_on_assets = net_income / assets_value
            # net_income_margin = net_income / revenues
            ebitda_margin = ebitda_value / revenues
            nome = temp_df4['Nome'].iloc[0]
            nif = temp_df4['NIF'].iloc[0]
            data = temp_df4['Data'].iloc[0]
            ano = temp_df4['Ano'].iloc[0]
            row1 = pd.DataFrame([nome,nif,data,i,ano,'ReturnOnEquity',return_on_equity], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            row2 = pd.DataFrame([nome,nif,data,i,ano,'ReturnOnAssets',return_on_assets], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            row3 = pd.DataFrame([nome,nif,data,i,ano,'EBITDAMargin',ebitda_margin], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            kpi_trim = kpi_trim.append(row1)
            kpi_trim = kpi_trim.append(row2)
            kpi_trim = kpi_trim.append(row3)

    #FLUXO DE CAIXA
    #Prazo médio de recebimento e de pagamento fim do período
    recebimentos = (saldos_final2['Second_ID']==21) | (saldos_final2['Second_ID']==24)
    pagamentos = (saldos_final2['Second_ID']==22) | (saldos_final2['Second_ID']==24)
    mercadorias = (saldos_final2['Second_ID']==32) | (saldos_final2['Second_ID']==33) | (saldos_final2['Second_ID']==34) | (saldos_final2['Second_ID']==35)
    accion = saldos_final2['Second_ID']==26
    outros = (saldos_final2['Second_ID']==27) | (saldos_final2['Second_ID']==28)
    amort = saldos_final2['Second_ID']==64
    
    recebimentos2 = (gl_resumo['AccountID']==21) | (gl_resumo['AccountID']==24)
    pagamentos2 = (gl_resumo['AccountID']==22) | (gl_resumo['AccountID']==24)
    mercadorias2 = (gl_resumo['AccountID']==32) | (gl_resumo['AccountID']==33) | (gl_resumo['AccountID']==34) | (gl_resumo['AccountID']==35)
    accion2 = gl_resumo['AccountID']==26
    outros2 = (gl_resumo['AccountID']==27) | (gl_resumo['AccountID']==28)
    
    for i in ['1T','2T','3T','4T']:
        condicao7 = saldos_final2['Trim']==i
        temp_df5 = saldos_final2[condicao7]
        if temp_df5.empty==False:
            mult = np.select([i=='1T',i=='2T',i=='3T'],[4,2,4/3],1)
            receber = temp_df5[recebimentos].NetDebitBalance.sum() 
            pagar = temp_df5[pagamentos].NetCreditBalance.sum()
            inventario = temp_df5[mercadorias].NetDebitBalance.sum()
            #Working capital final do período
            working_capital_final = round(receber + inventario - pagar,2)
            #Prazo médio de recebimento e de pagamento início do período
            receber_inicio = gl_resumo[recebimentos2].OpenNetDebitBalance.sum() 
            pagar_inicio = gl_resumo[pagamentos2].OpenNetCreditBalance.sum()
            inventario_inicio = gl_resumo[mercadorias2].OpenNetDebitBalance.sum()
            working_capital_inicio = round(receber_inicio + inventario_inicio - pagar_inicio,2)
            var_wc = working_capital_final - working_capital_inicio
            # Cálculo do Cash Flow Operacional - conta do accionista
            accionista_inicio = gl_resumo[accion2].OpenNetCreditBalance.sum()
            accionista_fim = temp_df5[accion].NetCreditBalance.sum()
            var_accionista = accionista_fim - accionista_inicio # no caso de ser a empresa a dever ao acionista
            if var_accionista == 0:
                var_accionista = (temp_df5[accion].NetDebitBalance.sum() - gl_resumo[accion2].OpenNetDebitBalance.sum()) * -1
            # Calculo do Cash FLow Operacional - outros (conta 27 e 28)
            receber_inicio = gl_resumo[outros2].OpenNetDebitBalance.sum()
            receber_fim = temp_df5[outros].NetDebitBalance.sum()
            var_receber_outrs = receber_fim - receber_inicio
            pagar_inicio = gl_resumo[outros2].OpenNetCreditBalance.sum()
            pagar_fim = temp_df5[outros].NetCreditBalance.sum()
            var_pagar_outrs = pagar_fim - pagar_inicio
            amortizacoes = temp_df5[amort].NetDebitBalance.sum()*mult
            revenues = temp_df5[rev].NetCreditBalance.sum()*mult
            costs = temp_df5[cos].NetDebitBalance.sum()*mult
            net_income = revenues - costs -estimativa_irc
            cfo = net_income + amortizacoes - var_wc + var_accionista + var_pagar_outrs - var_receber_outrs
            cfo_to_sales = cfo / revenues
            nome = temp_df5['Nome'].iloc[0]
            nif = temp_df5['NIF'].iloc[0]
            data = temp_df5['Data'].iloc[0]
            ano = temp_df5['Ano'].iloc[0]
            row1 = pd.DataFrame([nome,nif,data,i,ano,'CFOtoSales',cfo_to_sales], index=['Nome','NIF','Data','Trim','Ano','KPI','Valor']).T
            kpi_trim = kpi_trim.append(row1)

    return kpi_trim







