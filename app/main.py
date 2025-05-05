from collections import Counter
from pathlib import Path
from typing import Dict, List

import pandas as pd
import plotly.express as px  # type: ignore
import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard de Disponibilidade")

data_path = None

try:
    data_path = Path(__file__).resolve().parent.parent / "data" / "data.csv"
except NameError:
    st.warning("Não foi possível determinar o caminho do script automaticamente.")


@st.cache_data  # type: ignore
def load_data(data_path: Path) -> tuple[pd.DataFrame, list[str]]:
    """Loads and preprocesses the questionnaire data."""
    try:
        df = pd.read_csv(data_path)  # type: ignore
        df.columns = [
            "ID_Aluno",
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
            "N1_Satisfatoria",
            "Desafios",
        ]
        weekdays = [
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
        ]
        for day in weekdays:
            if day in df.columns:
                df[day] = df[day].fillna("Indisponível")  # type: ignore
            else:
                st.warning(
                    (
                        f"Coluna '{day}' não encontrada no arquivo CSV. "
                        "Pulando preenchimento de nulos."
                    )
                )
        return df, weekdays  # type: ignore
    except FileNotFoundError:
        st.error(f"Erro Crítico: O arquivo de dados não foi encontrado em: {data_path}")
        st.stop()
    except Exception as e:
        st.error(f"Erro inesperado ao carregar ou processar os dados: {e}")
        st.stop()


if data_path is not None:
    data_frame, weekdays_list = load_data(data_path)
else:
    st.error("Erro Crítico: Caminho para o arquivo de dados não foi definido.")
    st.stop()

# --- Streamlit App ---
st.title("📊 Dashboard de Análise do Questionário")
st.markdown("Visualização da disponibilidade dos alunos e resultados da N1.")

st.header("🕒 Disponibilidade dos Alunos")
st.markdown("""
Analisamos a disponibilidade dos alunos ao longo da semana. Os gráficos abaixo mostram
quantos alunos estão disponíveis em cada período (Manhã, Tarde, Noite) para cada dia.
""")

overall_availability_data: List[Dict[str, object]] = []
periods_list = ["Manhã", "Tarde", "Noite", "Indisponível"]

for day in weekdays_list:
    period_counts: Counter[str] = Counter()
    if day in data_frame.columns:
        for student_availability in data_frame[day].astype(str):
            slots = [s.strip() for s in student_availability.split(",")]
            for slot in slots:
                if slot in periods_list:
                    period_counts[slot] += 1
                elif slot == "":
                    period_counts["Indisponível"] += 1
            else:
                period_counts["Indisponível"] += 1
    else:
        for period in periods_list:
            overall_availability_data.append(
                {
                    "Dia": day,
                    "Periodo": period,
                    "Alunos": 0 if period != "Indisponível" else len(data_frame),
                }
            )
        continue

    for period in periods_list:
        overall_availability_data.append(
            {
                "Dia": day,
                "Periodo": period,
                "Alunos": period_counts[period],
            }
        )

df_availability = pd.DataFrame(overall_availability_data)
df_availability_filtered = df_availability[df_availability["Periodo"] != "Indisponível"]

if not df_availability_filtered.empty:
    fig_availability = px.bar(  # type: ignore
        df_availability_filtered,
        x="Dia",
        y="Alunos",
        color="Periodo",
        title="Disponibilidade dos Alunos por Dia e Período",
        labels={
            "Alunos": "Número de Alunos Disponíveis",
            "Dia": "Dia da Semana",
            "Periodo": "Período",
        },
        category_orders={
            "Periodo": ["Manhã", "Tarde", "Noite"],
            "Dia": weekdays_list,
        },
        color_discrete_map={
            "Manhã": "#1f77b4",
            "Tarde": "#ff7f0e",
            "Noite": "#2ca02c",
        },
        barmode="group",
    )
    fig_availability.update_layout(  # type: ignore
        xaxis_title="Dia da Semana",
        yaxis_title="Número de Alunos",
    )
    st.plotly_chart(  # type: ignore
        fig_availability,
        use_container_width=True,  # type: ignore
    )
else:
    st.warning("Não foi possível gerar o gráfico de disponibilidade.")

st.header("📝 Análise da N1")

if "N1_Satisfatoria" in data_frame.columns and "Desafios" in data_frame.columns:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Satisfação com a Nota")
        st.markdown(
            "Percentual de alunos que consideraram sua nota na N1 satisfatória."
        )
        n1_satisfaction_counts = (
            data_frame["N1_Satisfatoria"].value_counts().reset_index()
        )
        n1_satisfaction_counts.columns = [
            "Satisfacao",
            "Contagem",
        ]

        fig_n1_satisfaction = px.pie(  # type: ignore
            n1_satisfaction_counts,
            names="Satisfacao",
            values="Contagem",
            title="Satisfação com a Nota da N1",
            color_discrete_map={"Sim": "green", "Não": "red"},
        )
        fig_n1_satisfaction.update_traces(  # type: ignore
            textposition="inside", textinfo="percent+label"
        )
        st.plotly_chart(fig_n1_satisfaction, use_container_width=True)  # type: ignore

    with col2:
        st.subheader("Maiores Desafios na Prova")
        st.markdown("Principais dificuldades apontadas pelos alunos na prova N1.")
        n1_challenge_counts = data_frame["Desafios"].value_counts().reset_index()
        n1_challenge_counts.columns = ["Desafio", "Contagem"]

        fig_n1_challenge = px.bar(  # type: ignore
            n1_challenge_counts,
            x="Desafio",
            y="Contagem",
            title="Maiores Desafios Enfrentados na N1",
            labels={"Contagem": "Número de Alunos", "Desafio": "Desafio Apontado"},
            text_auto=True,
        )
        fig_n1_challenge.update_layout(  # type: ignore
            xaxis_title="Desafio", yaxis_title="Número de Alunos"
        )
        st.plotly_chart(  # type: ignore
            fig_n1_challenge,
            use_container_width=True,
        )
else:
    st.warning(
        (
            "Colunas 'N1_Satisfatoria' e/ou 'Desafios' não encontradas nos dados. "
            "Não é possível gerar a análise da N1."
        )
    )

st.header("👨‍🏫 Informações sobre as Monitorias")
st.info("""
**Formato:** As sessões de monitoria serão focadas na **resolução de exercícios** e em
**tirar dúvidas** sobre os conteúdos abordados.

**Modalidade:** A prioridade será para encontros **online**,
visando maior flexibilidade e acesso.

**Recursos:** As questões resolvidas durante as monitorias serão
**disponibilizadas posteriormente** para consulta e revisão dos alunos.
""")

st.header("📄 Dados Completos")
st.markdown("Tabela com os dados originais carregados (colunas em português).")
st.dataframe(data_frame)  # type: ignore

st.header("💡 Conclusões Preliminares")

try:
    if not df_availability.empty:
        available_slots_df = df_availability[
            df_availability["Periodo"] != "Indisponível"
        ].copy()  # type: ignore
        sorted_available_slots = available_slots_df.sort_values(  # type: ignore
            by="Alunos", ascending=False
        )
        top_5_available = sorted_available_slots.head(5)

        if not top_5_available.empty:
            conclusion_items = [
                "- **Top 5 Horários por Disponibilidade (Dia - Período):**"
            ]
            for i, (index, row) in enumerate(top_5_available.iterrows(), 1):  # type: ignore
                day = row["Dia"]  # type: ignore
                period = row["Periodo"]  # type: ignore
                count = int(row["Alunos"]) if pd.notna(row["Alunos"]) else 0  # type: ignore
                plural_s = "s" if count != 1 else ""
                conclusion_items.append(
                    f"  {i}. **{day} - {period}** ({count} aluno{plural_s})"
                )
            availability_conclusion = "\n".join(conclusion_items)
        else:
            availability_conclusion = (
                "- **Disponibilidade:** Nenhum horário com alunos disponíveis "
                "encontrado nos dados."
            )

    else:
        availability_conclusion = (
            "- **Disponibilidade:** Não foi possível analisar a disponibilidade "
            "(dados ausentes ou erro)."
        )

    if "n1_satisfaction_counts" in locals() and not n1_satisfaction_counts.empty:  # type: ignore
        unsatisfied_count_series = n1_satisfaction_counts.loc[  # type: ignore
            n1_satisfaction_counts["Satisfacao"] == "Não", "Contagem"  # type: ignore
        ]
        unsatisfied_count = (  # type: ignore
            unsatisfied_count_series.iloc[0]  # type: ignore
            if not unsatisfied_count_series.empty
            else 0
        )
        total_students = len(data_frame)
        satisfaction_conclusion = f"""- **Satisfação N1:** {unsatisfied_count}
        de {total_students} aluno(s) ({unsatisfied_count / total_students:.1%}) **não**
        considerou(aram) sua nota N1 satisfatória.
        """
    else:
        satisfaction_conclusion = """
        - **Satisfação N1:** Não foi possível analisar a
        satisfação (dados ausentes ou erro).
        """

    if "n1_challenge_counts" in locals() and not n1_challenge_counts.empty:  # type: ignore
        top_challenge = (  # type: ignore
            n1_challenge_counts["Desafio"].iloc[0]  # type: ignore
            if not n1_challenge_counts.empty  # type: ignore
            else "N/A"
        )
        second_challenge = (  # type: ignore
            n1_challenge_counts["Desafio"].iloc[1]  # type: ignore
            if len(n1_challenge_counts) > 1  # type: ignore
            else None
        )
        challenge_text = f'O desafio mais citado foi **"{top_challenge}"**'
        if second_challenge:
            challenge_text += f', seguido por **"{second_challenge}"**'
        challenge_conclusion = f"- **Desafios N1:** {challenge_text}."
    else:
        challenge_conclusion = "- **Desafios N1:** Não foi possível analisar."

    st.markdown(f"""
{availability_conclusion}
{satisfaction_conclusion}
{challenge_conclusion}
""")

except Exception as e:
    st.error(f"Erro ao gerar as conclusões: {e}")
    st.exception(e)

st.markdown("---")

try:
    assets_path = Path(__file__).resolve().parents[1] / "assets"
    st.image(image=assets_path / "nr-logo.png", width=250)
except FileNotFoundError:
    st.warning(
        """
        Logo não encontrada. Verifique se o arquivo 'nr-logo.png'
        está na pasta 'assets'.
        """
    )
