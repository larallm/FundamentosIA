import streamlit as st
import google.generativeai as genai


# Configuração da API Key e Modelo (conforme solicitado)
api_key = "AIzaSyDNAWSkFfjtNWO8UZMbSWxyY1ymdWO-fYs"
genai.configure(api_key=api_key)

try:
    # Utilizando o modelo especificado
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'): # Tenta obter mais detalhes do erro da API do Gemini
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

# Título do aplicativo
st.title("Exercício IA 1 - Criador de Histórias Interativas com IA 📚 ")
st.markdown("Faça a sua história!")


# Entradas do usuário
nome_protagonista = st.text_input("Digite o nome do personagem principal:")


genero = st.selectbox(
    "Qual é o gênero que você deseja para a sua história",
    ["Fantasia", "Ficção Científica", "Mistério", "Aventura"]
)


local_inicial = st.radio(
    "Em qual local a história vai iniciar?",
    ["Uma floresta antiga", "Uma cidade futurista", "Um castelo assombrado", "Uma nave espacial à deriva"]
)

frase_desafio = st.text_area(
    "Adicione a história uma frase de efeito ou um desafio inicial:",
    placeholder="Ex: E de repente, tudo ficou escuro." "O mapa indicava um perigo iminente..."
)

if st.button("Gerar Sugestão de Roteiro"):
    if not nome_protagonista:
        st.warning("Por favor, digite o nome do personagem principal.")
    elif not genero:
        st.warning("Por favor, escolha o gênero da história.")
    elif not local_inicial:
        st.warning("Por favor, escolha o local inicial da história.")
    else:
        prompt_aluno = (
            f"Crie uma história de '{genero}'.\n"
            f"Que ira começar em {local_inicial} .\n"
            f"Em seguinte apresente a frase ou desafio: {frase_desafio}.\n"
            f"Após a apresente o personagem principal: '{nome_protagonista}'.\n"
            f"Com base nessas informações, por favor, gere uma história, onde o personagem principal tem caracteristicas e o que o conto prenda o leitor. "
            f"Apresente a resposta de forma organizada."
        )

        st.markdown("---")
        st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
        st.text_area("",prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está montando seu roteiro dos sonhos...")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### ✨ Gerador de história da IA:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar o roteiro. Verifique as mensagens acima ou tente novamente mais tarde.")