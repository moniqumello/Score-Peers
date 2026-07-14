import streamlit as st
import anthropic

st.set_page_config(
    page_title="Peers Content Studio",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #011334 !important;
    color: #FFFFFF !important;
}

.stApp { background-color: #011334 !important; }

section[data-testid="stSidebar"] {
    background-color: #0a2156 !important;
    border-right: 1px solid rgba(255,255,255,0.12) !important;
}

section[data-testid="stSidebar"] * {
    color: #D8E8EE !important;
}

section[data-testid="stSidebar"] label {
    color: #8899aa !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] input {
    background-color: #011334 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

.stTextArea textarea {
    background-color: #0a2156 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}

.stTextArea textarea:focus {
    border-color: #E1FF00 !important;
    box-shadow: 0 0 0 1px #E1FF00 !important;
}

.stSelectbox > div > div {
    background-color: #0a2156 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

.stButton > button {
    background-color: #E1FF00 !important;
    color: #011334 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    width: 100% !important;
}

.stButton > button:hover {
    background-color: #c8e600 !important;
    transform: translateY(-1px) !important;
}

.stDownloadButton > button {
    background-color: transparent !important;
    color: #D8E8EE !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #0a2156 !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #8899aa !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 12px 24px !important;
    border-bottom: 2px solid transparent !important;
}

.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: #E1FF00 !important;
    border-bottom: 2px solid #E1FF00 !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background-color: #011334 !important;
    padding-top: 24px !important;
}

.stAlert {
    background-color: rgba(225,255,0,0.08) !important;
    border: 1px solid rgba(225,255,0,0.3) !important;
    color: #E1FF00 !important;
    border-radius: 8px !important;
}

.stMarkdown p { color: rgba(255,255,255,0.8) !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #FFFFFF !important; }
.stMarkdown code { background: rgba(0,0,0,0.4) !important; color: #a0c4ff !important; }

label {
    color: #8899aa !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

div[data-testid="stMarkdownContainer"] p { color: rgba(255,255,255,0.7) !important; }

.result-box {
    background: #0a2156;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
    color: rgba(255,255,255,0.85);
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
}

.code-box {
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #a0c4ff;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-all;
    margin-top: 16px;
}

.char-ok { color: #4ade80; font-size: 12px; text-align: right; }
.char-warn { color: #E1FF00; font-size: 12px; text-align: right; }
.char-bad { color: #f87171; font-size: 12px; text-align: right; }

.warn-travessao {
    background: rgba(225,255,0,0.08);
    border: 1px solid rgba(225,255,0,0.3);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    color: #E1FF00;
    margin-bottom: 10px;
}

.sidebar-info {
    background: rgba(216,232,238,0.08);
    border: 1px solid rgba(216,232,238,0.2);
    border-radius: 8px;
    padding: 12px;
    font-size: 12px;
    color: #D8E8EE;
    line-height: 1.6;
    margin-top: 8px;
}

.sidebar-section-title {
    font-size: 11px;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    margin-top: 16px;
}

.sidebar-desc {
    font-size: 12px;
    color: rgba(216,232,238,0.6);
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

OFFERING_OPTIONS = [
    "Selecione a offering...",
    "Analytics + IA",
    "Customer Experience",
    "Cyber Security",
    "Digital",
    "Finance",
    "Tech Strategy",
    "Strategy e M&A",
    "Supply Chain",
    "Sustainability",
    "Talent & Organization",
    "Value Creation"
]

PROMPT_SCORE = """
RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar o sinal gráfico travessão em nenhuma parte do output. Isso inclui justificativas, scores, recomendações e versão corrigida.

RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar construções do tipo "não é X, é Y", "não se trata de X, mas de Y", "não apenas X, mas Y". Reformule sempre em afirmativo direto.

Analise o artigo abaixo e atribua um score de 0 a 100. Se a nota for inferior a 80, reescreva automaticamente os trechos problemáticos e entregue a versão corrigida.

BLOCO 1: CONFORMIDADE COM PROMPT 2 (38 pontos)

1. Travessão (4 pts): nenhuma ocorrência do sinal gráfico travessão.
2. Construção negativa de contraste (4 pts): nenhuma construção do tipo "não é X, é Y".
3. Dados distribuídos (4 pts): pelo menos 1 dado na abertura, 1 no meio e 1 em outra seção.
4. Variação de raciocínio (4 pts): cada seção cumpre papel analítico distinto.
5. Links internos (4 pts): exatamente 3 links internos distribuídos ao longo do texto.
6. Subtítulos como perguntas (4 pts): todos os H2 formulados como perguntas reais de busca.
7. Frase de manchete (4 pts): pelo menos 1 frase com potencial de manchete.
8. Leitura contraintuitiva (4 pts): pelo menos 1 análise que desafia o senso comum.
9. Porta-voz (4 pts): nome completo, cargo oficial e citação literal presentes, nunca como frase de abertura.
10. Estrutura (4 pts): sequência Key Takeaways, resumo, desenvolvimento, FAQ e encerramento sem CTA.
11. Tamanho (2 pts): entre 5.000 e 6.000 caracteres.

SUBTOTAL BLOCO 1: X/38

BLOCO 2: QUALIDADE DE CONTEÚDO (62 pontos)

1. Clareza e intenção (6 pts)
2. Profundidade e estratégia (12 pts)
3. Tom consultivo Peers (12 pts)
4. SEO (6 pts)
5. AEO e LLM (20 pts)
6. Execução e fluidez (6 pts)

SUBTOTAL BLOCO 2: X/62

SCORE FINAL: X/100

Classificação: 90-100 aprovado. 80-89 aprovado com ajustes. Abaixo de 80 reprovado com versão corrigida.

Entregue: score, pontos fortes (até 3), pontos de melhoria (até 3) e ajustes recomendados trecho a trecho.

ARTIGO PARA AVALIAÇÃO:
"""

PROMPT_CODIGO = """
Você vai agir como um Editor de Conteúdo e Conversor de Dados Especialista e depois como Classificador de Taxonomia.

RESTRIÇÕES ABSOLUTAS:
- Nunca usar o sinal gráfico travessão.
- Nunca usar construções do tipo "não é X, é Y". Reformule sempre em afirmativo direto.

Processe o artigo e organize no formato de tags abaixo para importação em CMS via WYSIWYG.

REGRAS:
1. Preserve formatação HTML: <b>, <strong>, <i>, <em>, <ul>, <ol>, <li>, <a href>, <img>, <blockquote>.
2. RESUMO: texto curto (até 5 linhas) vai para [resumo]. Texto longo vai para [introducao] e sintetize novo resumo.
3. KEY TAKEAWAYS: gere lista <ul> com 3 a 4 bullets se não houver.
4. SETORES: até 5 setores. [setor_n] = título resumido (menu). [campo_de_texto_n] começa com <h2> com título completo.
5. TABELA: quando houver comparação ou framework com mais de 2 atributos, use:
[tabela]
Coluna 1 | Coluna 2 | Coluna 3
Linha 1A | Linha 1B | Linha 1C
[/tabela]
6. FAQ: até 5 perguntas em [pergunta_n] e [resposta_n].
7. Conteúdo após FAQ vai em [conteudo_final].

OFFERING DEFINIDA PELO EDITOR: {offering}

Tags disponíveis (obrigatório incluir "modelo-artigo"):
Inteligência Artificial & Dados, Arquitetura & Sistemas, Cibersegurança & Privacidade, Governança & Gestão de TI, Impostos & Tributos, Reforma Tributária, Gestão & Planejamento, Planejamento & Resultados, Custos & Preços, Controles & Transações, Logística & Transportes, Cadeia de Suprimentos, Estoque & Produtos, Estratégia & Execução, Governança Risco & ESG, Processos & Performance, Varejo & Canais, Experiência (CX) & Jornada, Comportamento & Produtos, Agro & Indústria, Saúde & Farma, Serviços & Finanças, Outros Setores & Marcos

TEMPLATE DE SAÍDA:

[titulo_do_artigo]Título[/titulo_do_artigo]
[resumo]Resumo[/resumo]
[introducao]Introdução original[/introducao]
[key_takeaways]<ul><li>...</li></ul>[/key_takeaways]
[setor_1] Título Resumido [/setor_1]
[campo_de_texto_1]
<h2>Título Completo</h2>
Conteúdo...
[/campo_de_texto_1]
[pergunta_1] Pergunta [/pergunta_1]
[resposta_1] Resposta [/resposta_1]
[conteudo_final] Conteúdo final [/conteudo_final]

[Offering] {offering} [/Offering]
Justificativa: uma linha

[Industries] Indústria 1, Indústria 2 [/Industries]
Justificativa: uma linha

[Category] {offering} [/Category]
Justificativa: categoria sempre repete a offering.

[Tags] modelo-artigo, Tag2, Tag3, Tag4 [/Tags]
Justificativa: uma linha

ARTIGO PARA CODIFICAR:
"""

PROMPT_TAXONOMIA = """
Você é um Classificador de Taxonomia especialista em conteúdo B2B corporativo da Peers Consulting + Technology.

RESTRIÇÕES ABSOLUTAS:
- Nunca usar travessão.
- Nunca usar construções do tipo "não é X, é Y".

OFFERING DEFINIDA PELO EDITOR: {offering}

Indústrias disponíveis (escolha até 2 com aderência direta, deixe em branco se não houver):
Agribusiness, Agro, Alimentos e Bebidas, Banking, Cross-Industry, Educação, Financial Services, Food & Beverage, Healthcare, Indústria, Insurance, Logística, Payment, Private Education, Public Education, Retail, Saúde, Seguros, Serviços financeiros, Tecnologia, Varejo

Tags disponíveis (obrigatório incluir "modelo-artigo", escolha 3 a 5):
Inteligência Artificial & Dados, Arquitetura & Sistemas, Cibersegurança & Privacidade, Governança & Gestão de TI, Impostos & Tributos, Reforma Tributária, Gestão & Planejamento, Planejamento & Resultados, Custos & Preços, Controles & Transações, Logística & Transportes, Cadeia de Suprimentos, Estoque & Produtos, Estratégia & Execução, Governança Risco & ESG, Processos & Performance, Varejo & Canais, Experiência (CX) & Jornada, Comportamento & Produtos, Agro & Indústria, Saúde & Farma, Serviços & Finanças, Outros Setores & Marcos

FORMATO DE SAÍDA:

[Offering] {offering} [/Offering]
Justificativa: uma linha

[Industries] Indústria 1, Indústria 2 [/Industries]
Justificativa: uma linha

[Category] {offering} [/Category]
Justificativa: categoria sempre repete a offering.

[Tags] modelo-artigo, Tag2, Tag3, Tag4 [/Tags]
Justificativa: uma linha

CONTEÚDO PARA CLASSIFICAR:
"""


def check_travessao(texto):
    return "—" in texto or "–" in texto


def contar_caracteres(texto):
    return len(texto)


def chamar_api(api_key, prompt, artigo):
    
    
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(model="claude-sonnet-4-6", max_tokens=4000, messages=[{"role": "user", "content": prompt + artigo}])
    return message.content[0].text


# Header
st.markdown("""
<div style="display:flex; align-items:center; gap:14px; padding:0 0 20px 0; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:24px;">
    <div style="width:40px; height:40px; background:#E1FF00; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0;">📊</div>
    <div>
        <div style="font-size:17px; font-weight:600; color:#FFFFFF; letter-spacing:0.01em;">Peers Content Studio</div>
        <div style="font-size:12px; color:#8899aa; margin-top:2px;">Avaliação, codificação e taxonomia de artigos</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">Configuração</div>', unsafe_allow_html=True)
    api_key = st.text_input("Chave de API Anthropic", type="password", placeholder="sk-ant-...")
    st.markdown("""
    <div class="sidebar-info">
        🔒 A chave fica salva só no seu navegador. Nunca enviada para servidores externos.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Como obter a chave</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-desc">Acesse <strong style="color:#D8E8EE;">console.anthropic.com</strong>, faça login com sua conta Google, clique em <strong style="color:#D8E8EE;">"API Keys" e clique em "Create Key"</strong> e copie a chave gerada.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Sobre</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-desc">Ferramenta editorial da Peers Consulting + Technology. Baseada nos Prompts 2, 3 e no framework de código CMS.</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Avaliar score", "💻 Codificar", "🏷️ Taxonomia"])

# TAB 1: AVALIAR SCORE
with tab1:
    artigo_score = st.text_area(
        "Artigo para avaliação",
        height=280,
        placeholder="Cole o texto do artigo aqui...",
        key="artigo_score"
    )

    if artigo_score:
        chars = contar_caracteres(artigo_score)
        if 5000 <= chars <= 6000:
            st.markdown(f'<div class="char-ok" style="text-align:right;">{chars:,} caracteres — dentro do limite (5.000–6.000) ✓</div>', unsafe_allow_html=True)
        elif chars < 5000:
            st.markdown(f'<div class="char-warn" style="text-align:right;">{chars:,} caracteres — abaixo do mínimo de 5.000</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="char-bad" style="text-align:right;">{chars:,} caracteres — acima do limite de 6.000</div>', unsafe_allow_html=True)

        if check_travessao(artigo_score):
            st.markdown('<div class="warn-travessao">⚠️ Travessão detectado no texto. Revise antes de avaliar.</div>', unsafe_allow_html=True)

    avaliar = st.button("▶ Avaliar artigo", key="btn_avaliar")

    if avaliar:
        if not api_key:
            st.error("Insira sua chave de API Gemini no menu lateral.")
        elif not artigo_score:
            st.error("Cole o artigo antes de avaliar.")
        else:
            with st.spinner("Analisando artigo..."):
                try:
                    resultado = chamar_api(api_key, PROMPT_SCORE, artigo_score)
                    st.markdown("---")
                    st.markdown("### Resultado da avaliação")
                    st.markdown(f'<div class="result-box">{resultado}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Baixar resultado",
                        data=resultado,
                        file_name="score_peers.txt",
                        mime="text/plain",
                        key="dl_score"
                    )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")

# TAB 2: CODIFICAR
with tab2:
    artigo_codigo = st.text_area(
        "Artigo aprovado para codificação",
        height=280,
        placeholder="Cole o artigo aprovado aqui. O sistema vai gerar o código CMS completo com tags, taxonomia e formatação HTML para o WordPress...",
        key="artigo_codigo"
    )

    offering_codigo = st.selectbox(
        "Offering (obrigatório)",
        OFFERING_OPTIONS,
        key="offering_codigo"
    )

    codificar = st.button("💻 Gerar código CMS", key="btn_codificar")

    if codificar:
        if not api_key:
            st.error("Insira sua chave de API Gemini no menu lateral.")
        elif not artigo_codigo:
            st.error("Cole o artigo antes de codificar.")
        elif offering_codigo == "Selecione a offering...":
            st.error("Selecione a offering antes de codificar.")
        else:
            with st.spinner("Gerando código CMS..."):
                try:
                    prompt_com_offering = PROMPT_CODIGO.replace("{offering}", offering_codigo)
                    resultado = chamar_api(api_key, prompt_com_offering, artigo_codigo)
                    st.markdown("---")
                    st.markdown("### Código gerado")
                    st.markdown(f'<div class="code-box">{resultado}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Baixar código",
                        data=resultado,
                        file_name="codigo_cms_peers.txt",
                        mime="text/plain",
                        key="dl_codigo"
                    )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")

# TAB 3: TAXONOMIA
with tab3:
    artigo_tax = st.text_area(
        "Conteúdo para classificar",
        height=280,
        placeholder="Cole o artigo ou resumo aqui para classificar a taxonomia...",
        key="artigo_tax"
    )

    offering_tax = st.selectbox(
        "Offering (definida pelo editor)",
        OFFERING_OPTIONS,
        key="offering_tax"
    )

    classificar = st.button("🏷️ Classificar taxonomia", key="btn_tax")

    if classificar:
        if not api_key:
            st.error("Insira sua chave de API Gemini no menu lateral.")
        elif not artigo_tax:
            st.error("Cole o conteúdo antes de classificar.")
        elif offering_tax == "Selecione a offering...":
            st.error("Selecione a offering antes de classificar.")
        else:
            with st.spinner("Classificando taxonomia..."):
                try:
                    prompt_com_offering = PROMPT_TAXONOMIA.replace("{offering}", offering_tax)
                    resultado = chamar_api(api_key, prompt_com_offering, artigo_tax)
                    st.markdown("---")
                    st.markdown("### Resultado da classificação")
                    st.markdown(f'<div class="code-box">{resultado}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Baixar classificação",
                        data=resultado,
                        file_name="taxonomia_peers.txt",
                        mime="text/plain",
                        key="dl_tax"
                    )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")
