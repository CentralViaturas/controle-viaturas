import streamlit as st
import json


def carregar_estado_viaturas(arquivo="estado_viaturas.json"):
    """Carrega o estado das viaturas de um arquivo JSON."""
    try:
        with open(arquivo, "r") as f:
            estado = json.load(f)
        return estado
    except FileNotFoundError:
        return None


def obter_cor_estado(estado):
    """Retorna a cor correspondente ao estado da viatura."""
    if estado == "Dentro":
        return "green"
    elif estado == "Fora":
        return "red"
    elif estado == "Reservada":
        return "yellow"


def main():
    st.title("Controle de Viaturas - Visualização Online")

    # Carregar o estado das viaturas
    estado_viaturas = carregar_estado_viaturas()

    if estado_viaturas:
        st.write("### Estado das Viaturas")
        for viatura in estado_viaturas:
            cor = obter_cor_estado(viatura["estado"])
            st.markdown(
                f"""
                <div style="background-color: {cor}; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <strong>Placa:</strong> {viatura["placa"]}<br>
                    <strong>Modelo:</strong> {viatura["modelo"]}<br>
                    <strong>Cor:</strong> {viatura["cor"]}<br>
                    <strong>Estado:</strong> {viatura["estado"]}<br>
                    <strong>Motorista:</strong> {viatura["motorista"] if viatura["motorista"] else "N/A"}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Nenhum dado de viatura encontrado.")


if __name__ == "__main__":
    main()