import time

import streamlit as st

from utils import cria_chain_conversa, PASTA_ARQUIVOS


def sidebar():
    uploaded_files = st.file_uploader(
        'Adicione seus arquivos PDF ou XLSX', 
        type=['pdf', 'xlsx'], 
        accept_multiple_files=True
    )
    
    if uploaded_files is not None:
        # Limpa arquivos existentes
        for ext in ['*.pdf', '*.xlsx']:
            for arquivo in PASTA_ARQUIVOS.glob(ext):
                arquivo.unlink()
        
        # Salva os novos arquivos
        for file in uploaded_files:
            with open(PASTA_ARQUIVOS / file.name, 'wb') as f:
                f.write(file.read())
    
    label_botao = 'Inicializar ChatBot' if 'chain' not in st.session_state else 'Atualizar ChatBot'
    
    if st.button(label_botao, use_container_width=True):
        if not any(PASTA_ARQUIVOS.glob('*.pdf')) and not any(PASTA_ARQUIVOS.glob('*.xlsx')):
            st.error('Adicione arquivos PDF ou XLSX para inicializar o chatbot')
        else:
            st.success('Inicializando o ChatBot...')
            cria_chain_conversa()
            st.rerun()



def chat_window():
    st.header('🤖 Bem-vindo ao Chat com PDFs da Ana Júlia', divider=True)

    if not 'chain' in st.session_state:
        st.error('Faça o upload de PDFs para começar!')
        st.stop()

    chain = st.session_state['chain']
    memory = chain.memory

    # Carregar mensagens anteriores do chat
    mensagens = memory.load_memory_variables({})['chat_history']

    container = st.container()
    
    # Adicionar mensagem inicial padronizada do humano, se o chat estiver vazio
    if len(mensagens) == 0:  
        # Criar mensagem de "bem-vindo" ao agente
        nova_mensagem = 'Me mostre as sugestões de correções para esse documento.'
        chat = container.chat_message('human')
        chat.markdown(nova_mensagem)
        
        # Enviar a mensagem para o agente
        chat = container.chat_message('ai')
        chat.markdown('Gerando resposta')

        # Simular o envio da primeira mensagem para o agente
        resposta = chain.invoke({'question': nova_mensagem})
        st.session_state['ultima_resposta'] = resposta
        st.rerun()

    # Exibir todas as mensagens anteriores
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    # Permitir nova entrada do usuário
    nova_mensagem = st.chat_input('Converse com seus documentos...')
    if nova_mensagem:
        chat = container.chat_message('human')
        chat.markdown(nova_mensagem)
        chat = container.chat_message('ai')
        chat.markdown('Gerando resposta')

        resposta = chain.invoke({'question': nova_mensagem})
        st.session_state['ultima_resposta'] = resposta
        st.rerun()


def main():
    with st.sidebar:
        sidebar()
    chat_window()

if __name__ == '__main__':
    st.set_page_config(
        page_title="ChatGPT - PDF",
        page_icon="💻",
        layout="wide")
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .block-container {
            padding-top: 3rem;
            padding-right: 3rem;
            padding-bottom: 5rem;
            padding-left: 3rem;
        }
        h1, h2, h3, h4, h5, h6 {
            pointer-events: none;
        }
        .stButton button{
            margin-bottom: 0px;
        }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    main()
