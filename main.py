# importar bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# função para carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("employee_performance.csv", sep=";")  # 👈 Atenção: separador ;
    df.columns = df.columns.str.strip()  # tira espaços escondidos
    return df

# função para calcular KPIs
def calcular_kpis(df):
    kpis = {
        "Total Funcionários": df["Employee_ID"].nunique(),
        "Média de Desempenho": df["Performance_Score"].mean(),
        "Horas de Treinamento Média": df["Training_Hours"].mean(),
        "Salário Médio": df["Salary"].mean()
    }
    return kpis

# carregar os dados
df = carregar_dados()

# converter coluna de data
df["Date_of_Joining"] = pd.to_datetime(df["Date_of_Joining"], errors='coerce')

# criar coluna de ano de entrada para Cohort
df["Ano_de_Entrada"] = df["Date_of_Joining"].dt.year

# calcular KPIs
kpis = calcular_kpis(df)

# 🎨 construir a interface Streamlit
st.set_page_config(page_title="Dashboard Funcionários", layout="wide")
st.title("📊 Dashboard de Performance de Funcionários")

# KPIs - linha superior
st.header("🔎 Indicadores Principais (KPIs)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍💼 Total Funcionários", kpis["Total Funcionários"])
col2.metric("🏆 Média de Desempenho", f"{kpis['Média de Desempenho']:.2f}")
col3.metric("⏳ Horas Treinamento", f"{kpis['Horas de Treinamento Média']:.2f}")
col4.metric("💰 Salário Médio", f"R$ {kpis['Salário Médio']:,.2f}")

# 💵 nova análise: Média Salarial por Departamento
st.header("💵 Média Salarial por Departamento")
salario_departamento = df.groupby("Department")["Salary"].mean().round(2).reset_index()

col5, col6 = st.columns([2, 3])

with col5:
    st.dataframe(salario_departamento.style.format({"Salary": "R$ {:,.2f}"}), use_container_width=True)

with col6:
    fig_salario = px.bar(
        salario_departamento,
        x="Salary",
        y="Department",
        orientation='h',
        title="Média Salarial por Departamento",
        text_auto=".2f",
        color="Department",
        labels={"Salary": "Salário (R$)"}
    )
    st.plotly_chart(fig_salario, use_container_width=True)

# 🏢 gráfico de desempenho por departamento
st.header("🏢 Performance Média por Departamento")
col7, col8 = st.columns([2, 3])

desempenho_departamento = df.groupby("Department")["Performance_Score"].mean().round(2).reset_index()

with col7:
    st.dataframe(desempenho_departamento.style.format({"Performance_Score": "{:.2f}"}), use_container_width=True)

with col8:
    fig_performance = px.bar(
        desempenho_departamento, 
        x="Performance_Score", 
        y="Department",
        orientation='h',
        color="Department",
        title="Média de Desempenho por Departamento",
        text_auto=".2f"
    )
    st.plotly_chart(fig_performance, use_container_width=True)

# 📅 Análise de Cohorts: Contratações ao longo do tempo
st.header("📅 Análise de Cohorts: Contratações por Ano e Departamento")

cohort = df.groupby(["Ano_de_Entrada", "Department"]).size().reset_index(name="Contratacoes")

col9, col10 = st.columns([2, 3])

with col9:
    st.dataframe(cohort.style.format({"Contratacoes": "{:.0f}"}), use_container_width=True)

with col10:
    fig_cohort = px.bar(
        cohort,
        x="Ano_de_Entrada",
        y="Contratacoes",
        color="Department",
        title="Número de Contratações por Ano e Departamento",
        labels={"Ano_de_Entrada": "Ano de Entrada", "Contratacoes": "Nº de Contratações"},
        text_auto=True
    )
    st.plotly_chart(fig_cohort, use_container_width=True)

# 📋 Base de Dados Completa
st.header("📋 Base de Dados Completa")
st.dataframe(df, use_container_width=True)
