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

:root {
    --peers-blue: #011334;
    --peers-lime: #E1FF00;
    --peers-serene: #D8E8EE;
    --peers-white: #FFFFFF;
    --peers-blue-light: #0a2156;
    --peers-text-muted: #8899aa;
    --peers-border: rgba(255,255,255,0.12);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #011334 !important;
    color: #FFFFFF !important;
}

.stApp {
    background-color: #011334 !important;
}

.stTextArea textarea {
    background-color: #0a2156 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextArea textarea:focus {
    border-color: #E1FF00 !important;
    box-shadow: 0 0 0 1px #E1FF00 !important;
}

.stTextInput input {
    background-color: #0a2156 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
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
    padding: 10px 20px !important;
}

.stButton > button:hover {
    background-color: #c8e600 !important;
}

div[data-testid="stSidebar"] {
    background-color: #0a2156 !important;
    border-right: 1px solid rgba(255,255,255,0.12) !important;
}

.result-card {
    background: #0a2156;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
}

.score-display {
    font-size: 48px;
    font-weight: 700;
    color: #E1FF00;
    line-height: 1;
}

.badge-approved {
    background: rgba(74,222,128,0.15);
    color: #4ade80;
    border: 1px solid rgba(74,222,128,0.3);
    padding: 5px 14px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
}

.badge-warning {
    background: rgba(225,255,0,0.1);
    color: #E1FF00;
    border: 1px solid rgba(225,255,0,0.3);
    padding: 5px 14px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
}

.badge-danger {
    background: rgba(248,113,113,0.12);
    color: #f87171;
    border: 1px solid rgba(248,113,113,0.3);
    padding: 5px 14px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
}

.info-box {
    background: rgba(225,255,0,0.06);
    border: 1px solid rgba(225,255,0,0.2);
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
    color: rgba(225,255,0,0.8);
    line-height: 1.6;
}

.warn-box {
    background: rgba(225,255,0,0.08);
    border: 1px solid rgba(225,255,0,0.3);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    color: #E1FF00;
    margin-bottom: 10px;
}

.code-box {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #a0c4ff;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-all;
}

.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.peers-header {
    background: #011334;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    padding: 16px 0;
    margin-bottom: 24px;
}

hr {
    border-color: rgba(255,255,255,0.1) !important;
}

.stMarkdown p { color: rgba(255,255,255,0.8) !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #FFFFFF !important; }

label { color: #8899aa !important; font-size: 12px !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; }
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
RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar o sinal gráfico travessão em nenhuma parte do output gerado por você, avaliador. Isso inclui justificativas, scores, recomendações e versão corrigida.

RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar construções do tipo "não é X, é Y", "não se trata de X, mas de Y", "não apenas X, mas Y" ou qualquer variação dessa estrutura de contraste negativo. Reformule sempre em afirmativo direto.

Analise o artigo abaixo e atribua um score de 0 a 100 com base em dois blocos de avaliação. Se a nota final for inferior a 80, reescrever automaticamente os trechos problemáticos e entregar a versão corrigida antes de declarar o resultado.

BLOCO 1: CONFORMIDADE COM PROMPT 2 (38 pontos)
São 11 itens. Antes de pontuar qualquer item, escanear ativamente o artigo submetido em busca do sinal gráfico travessão e de construções do tipo "não é X, é Y". Se encontrados em qualquer trecho, os itens correspondentes recebem 0 pontos automaticamente e os trechos são indicados na seção de ajustes recomendados.

Pontuação por item: cumprido integralmente: pontuação máxima do item. Cumprido parcialmente: metade. Não cumprido: 0.
Para cada item, informar a nota e justificar em 1 linha.

1. Travessão (vale até 4 pontos): escanear o artigo submetido ativamente. Nenhuma ocorrência do sinal gráfico travessão em qualquer parte do texto avaliado.
2. Construção negativa de contraste (vale até 4 pontos): escanear ativamente o artigo em busca de construções do tipo "não é X, é Y" ou variações. Nenhuma ocorrência permitida.
3. Dados distribuídos (vale até 4 pontos): há pelo menos 1 dado na abertura, 1 no meio do desenvolvimento e 1 em outra seção.
4. Variação de raciocínio (vale até 4 pontos): cada seção cumpre um papel analítico distinto. Nenhuma seção repete a lógica de outra.
5. Links internos (vale até 4 pontos): há exatamente 3 links internos, sendo 2 artigos e 1 case, distribuídos ao longo do texto e inseridos em palavras ou expressões relevantes.
6. Subtítulos como perguntas (vale até 4 pontos): todos os H2 estão formulados como perguntas reais de busca.
7. Frase de manchete (vale até 4 pontos): há pelo menos 1 frase com potencial de manchete, direta e impactante.
8. Leitura contraintuitiva (vale até 4 pontos): há pelo menos 1 análise que desafia o senso comum do mercado.
9. Porta-voz (vale até 4 pontos): se indicado no outline, nome completo, cargo oficial e citação literal presentes na seção indicada, nunca como frase de abertura. Se não indicado no outline, nenhuma referência inventada.
10. Estrutura (vale até 4 pontos): sequência Key Takeaways, resumo, desenvolvimento, FAQ e encerramento sem CTA respeitada integralmente. Sugestão de imagem de destaque com alt text presente ao final. Sugestão de infográfico ou declaração explícita de ausência presente ao final.
11. Tamanho (vale até 2 pontos): o artigo está entre 5.000 e 6.000 caracteres com espaços.

SUBTOTAL BLOCO 1: X/38

BLOCO 2: QUALIDADE DE CONTEÚDO (62 pontos)
Avaliar cada critério com justificativa objetiva em 1 a 2 linhas.

1. Clareza e intenção (vale até 6 pontos): o texto deixa claro qual problema está sendo tratado e para quem ele é relevante?
2. Profundidade e estratégia (vale até 12 pontos): existe uma tese clara? Vai além do óbvio? Traz implicações reais de negócio?
3. Tom consultivo Peers (vale até 12 pontos): soa como especialista? Evita hype e superficialidade? Tem leitura crítica?
4. SEO (vale até 6 pontos): responde o que o usuário realmente quer saber? Todos os H2 estão formulados como perguntas diretas de busca? Usa termos relevantes de forma natural?
5. AEO e LLM (vale até 20 pontos): tem respostas claras e citáveis? Conceitos estão bem explicados? Dá para extrair trechos facilmente fora de contexto? O conteúdo seria uma boa fonte para um motor de resposta? Há tabela onde o conteúdo justifica comparação ou framework?
6. Execução e fluidez (vale até 6 pontos): o texto flui bem? As ideias se conectam? Não parece truncado, repetitivo ou mecânico?

SUBTOTAL BLOCO 2: X/62

SCORE FINAL: X/100

Classificação: 90 a 100 aprovado para publicação. 80 a 89 aprovado com ajustes pontuais indicados. Abaixo de 80 reprovado, reescrever automaticamente os trechos problemáticos e entregar versão corrigida completa junto com o score.

RESULTADO FINAL
Score final com classificação. Pontos fortes: até 3, com justificativa objetiva. Pontos de melhoria: até 3, com justificativa objetiva. Ajustes recomendados: listar exatamente o que deve ser feito, trecho por trecho. Se reprovado, entregar versão corrigida completa.

REGRA FINAL
Seja direto e crítico. Não suavizar problemas. Não elogiar sem justificar. Priorizar clareza e utilidade.

ARTIGO PARA AVALIAÇÃO:
"""

PROMPT_CODIGO = """
Você vai agir como um Editor de Conteúdo e Conversor de Dados Especialista. E depois como um Classificador de Taxonomia.

Vou fornecer o código HTML bruto de um artigo. Sua tarefa é processar esse conteúdo e organizá-lo estritamente no formato de tags especificado abaixo, GARANTINDO QUE NENHUM CONTEÚDO SEJA CORTADO, preparando-o para importação em um CMS via editor WYSIWYG.

RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar o sinal gráfico travessão em nenhuma parte do output gerado. Isso inclui resumos, introduções, campos de texto, key takeaways e qualquer outro elemento gerado ou reescrito por você.

RESTRIÇÃO INEGOCIÁVEL E ABSOLUTA: nunca usar construções do tipo "não é X, é Y", "não se trata de X, mas de Y", "não apenas X, mas Y" ou qualquer variação dessa estrutura de contraste negativo em nenhum conteúdo gerado ou reescrito. Reformule sempre em afirmativo direto.

REGRAS CRÍTICAS DE EXECUÇÃO:

1. PRESERVAÇÃO RIGOROSA DO HTML (WYSIWYG):
Dentro dos campos de conteúdo, você NÃO DEVE remover a formatação rica.
Mantenha tags como: <b>, <strong>, <i>, <em>, <ul>, <ol>, <li>, <blockquote>.
Links: Mantenha todas as tags <a href="..."> intactas e funcionais.
Mídia: Se houver tags <img>, <video>, <iframe> ou shortcodes, mantenha-os exatamente como estão.
Headings: Preserve a hierarquia de títulos original, ajustando-a para H2 para setores, H3 para subtópicos.

2. LÓGICA DE INTRODUÇÃO E RESUMO:
CASO A (Texto Longo > 5 linhas): Mantenha na tag [introducao] e sintetize novo resumo de 2 a 3 linhas para [resumo].
CASO B (Texto Curto <= 5 linhas): Mova para [resumo]. Deixe [introducao] vazia.
CASO C (Sem texto introdutório): Gere um resumo de 2 a 3 linhas para [resumo]. Deixe [introducao] vazia.

3. GERAÇÃO OBRIGATÓRIA DE KEY TAKEAWAYS:
Se não houver lista no início, GERE uma lista com 3 a 4 bullet points destacando os principais aprendizados.

4. ESTRUTURAÇÃO DOS SETORES (H1 > H2 > H3):
Suporta até 5 setores ([setor_1] a [setor_5]).
[setor_n]: versão resumida do título (estilo menu de navegação).
[campo_de_texto_n]: inicia com o título completo dentro de <h2>.
EVITE KEYWORD STUFFING: use variações semânticas nos subtítulos.

5. TABELA (CONDICIONAL):
Quando houver comparação, framework ou estágios com mais de dois atributos, estruture em:
[tabela]
Coluna 1 | Coluna 2 | Coluna 3
Linha 1A | Linha 1B | Linha 1C
[/tabela]

6. FAQ: Mapeie perguntas e respostas para [pergunta_n] e [resposta_n]. Até 5 perguntas.

7. CONTEÚDO FINAL: Se houver conteúdo após o FAQ, adicione em [conteudo_final].

DIRECIONAL DE TAXONOMIA:
A OFFERING DEFINIDA PELO EDITOR ESTÁ INDICADA ABAIXO. Use-a como âncora.

OFFERING DEFINIDA PELO EDITOR: {offering}

Indústrias disponíveis: Agribusiness, Agro, Alimentos e Bebidas, Banking, Cross-Industry, Educação, Financial Services, Food & Beverage, Healthcare, Indústria, Insurance, Logística, Payment, Payments, Private Education, Public Education, Retail, Saúde, Seguros, Serviços financeiros, Serviços financeiros (bancos), Serviços financeiros (pagamentos), Setor público, Tecnologia, Varejo

Tags disponíveis (obrigatório incluir "modelo-artigo"):
Inteligência Artificial & Dados, Arquitetura & Sistemas, Cibersegurança & Privacidade, Governança & Gestão de TI, Impostos & Tributos, Reforma Tributária, Gestão & Planejamento, Planejamento & Resultados, Custos & Preços, Controles & Transações, Logística & Transportes, Cadeia de Suprimentos, Estoque & Produtos, Estratégia & Execução, Governança Risco & ESG, Processos & Performance, Varejo & Canais, Experiência (CX) & Jornada, Comportamento & Produtos, Agro & Indústria, Saúde & Farma, Serviços & Finanças, Outros Setores & Marcos

TEMPLATE DE SAÍDA:

[titulo_do_artigo]Título principal[/titulo_do_artigo]

[resumo]Conteúdo do resumo.[/resumo]

[introducao]Conteúdo da introdução original[/introducao]

[key_takeaways]Lista <ul> com os destaques.[/key_takeaways]

[setor_1] Título Resumido [/setor_1]
[campo_de_texto_1]
<h2>Título Completo</h2>
Conteúdo HTML...
[/campo_de_texto_1]

[pergunta_1] Pergunta [/pergunta_1]
[resposta_1] Resposta [/resposta_1]

[conteudo_final] Conteúdo após FAQ [/conteudo_final]

[Offering] {offering} [/Offering]
Justificativa: [uma linha]

[Industries] Indústria 1, Indústria 2 [/Industries]
Justificativa: [uma linha]

[Category] {offering} [/Category]
Justificativa: A categoria sempre repete a offering definida pelo editor.

[Tags] modelo-artigo, Tag2, Tag3, Tag4 [/Tags]
Justificativa: [uma linha]

ARTIGO PARA CODIFICAR:
"""

PROMPT_TAXONOMIA = """
Você vai agir como um Classificador de Taxonomia especialista em conteúdo B2B corporativo da Peers Consulting + Technology.

Com base no conteúdo fornecido, classifique seguindo estritamente o framework abaixo.

A offering já foi definida pelo editor: {offering}

Use as regras de desempate abaixo para classificar as demais dimensões:

- Analytics + IA: foco em estruturação técnica de dados, modelos preditivos ou adoção de IA. Se a IA resolver dor de outra área, a categoria é a área de negócio e IA vira Tag.
- Customer Experience: foco na jornada do cliente final, NPS, fidelização. Se tratar de processos que impactam o cliente sem focar na jornada, vai para Value Creation.
- Cyber Security: foco na defesa técnica. Adequação jurídica, LGPD vão para Value Creation.
- Digital: foco em inovação na ponta e construção de software. Back-office e governança de TI vão para Tech Strategy.
- Finance: foco puramente no dinheiro (caixa, DRE, tesouraria). PMO vai para Value Creation.
- Tech Strategy: foco na gestão do departamento de TI, ERPs, nuvem corporativa.
- Strategy + M&A: fusões, aquisições, go-to-market, precificação.
- Supply Chain: cadeia de suprimentos, logística, fornecedores e manufatura.
- Sustainability: ESG, descarbonização, diversidade e governança verde.
- Talent & Organization: pessoas, lideranças, cultura e gestão da mudança.
- Value Creation: eficiência operacional, PMO e maximização de retorno.

Indústrias disponíveis:
Agribusiness, Agro, Alimentos e Bebidas, Banking, Cross-Industry, Educação, Financial Services, Food & Beverage, Healthcare, Indústria, Insurance, Logística, Payment, Payments, Private Education, Public Education, Retail, Saúde, Seguros, Serviços financeiros, Tecnologia, Varejo

Tags disponíveis (obrigatório incluir "modelo-artigo"):
Inteligência Artificial & Dados, Arquitetura & Sistemas, Cibersegurança & Privacidade, Governança & Gestão de TI, Impostos & Tributos, Reforma Tributária, Gestão & Planejamento, Planejamento & Resultados, Custos & Preços, Controles & Transações, Logística & Transportes, Cadeia de Suprimentos, Estoque & Produtos, Estratégia & Execução, Governança Risco & ESG, Processos & Performance, Varejo & Canais, Experiência (CX) & Jornada, Comportamento & Produtos, Agro & Indústria, Saúde & Farma, Serviços & Finanças, Outros Setores & Marcos

FORMATO DE SAÍDA (siga estritamente):

[Offering] {offering} [/Offering]
Justificativa: [uma linha confirmando a aderência]

[Industries] Indústria 1, Indústria 2 [/Industries]
Justificativa: [uma linha explicando a aderência direta]

[Category] {offering} [/Category]
Justificativa: A categoria sempre repete a offering definida pelo editor.

[Tags] modelo-artigo, Tag2, Tag3, Tag4 [/Tags]
Justificativa: [uma linha explicando o critério]

CONTEÚDO PARA CLASSIFICAR:
"""


def check_travessao(texto):
    return "—" in texto or "–" in texto


def contar_caracteres(texto):
    return len(texto)


def chamar_api(api_key, prompt, artigo):
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt + artigo}]
    )
    return message.content[0].text


st.markdown("""
<div style="display:flex; align-items:center; gap:12px; padding:0 0 20px 0; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:24px;">
    <div style="width:36px; height:36px; background:#E1FF00; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px;">📊</div>
    <div>
        <div style="font-size:16px; font-weight:600; color:#FFFFFF;">Peers Content Studio</div>
        <div style="font-size:12px; color:#8899aa;">Avaliação, codificação e taxonomia de artigos</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="font-size:11px; color:#8899aa; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Configuração</div>', unsafe_allow_html=True)
    api_key = st.text_input("Chave de API Anthropic", type="password", placeholder="sk-ant-...")
    st.markdown("""
    <div class="info-box" style="margin-top:8px;">
        🔒 A chave fica salva só no seu navegador. Nunca enviada para servidores externos.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:11px; color:#8899aa; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Sobre</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:rgba(255,255,255,0.5); line-height:1.6;">Ferramenta editorial da Peers Consulting + Technology. Baseada nos Prompts 2, 3 e no framework de código CMS.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Avaliar score", "💻 Codificar", "🏷️ Taxonomia"])

with tab1:
    artigo_score = st.text_area(
        "Artigo para avaliação",
        height=250,
        placeholder="Cole o texto do artigo aqui...",
        key="artigo_score"
    )

    if artigo_score:
        chars = contar_caracteres(artigo_score)
        if 5000 <= chars <= 6000:
            st.markdown(f'<div style="text-align:right; font-size:12px; color:#4ade80;">{chars:,} caracteres — dentro do limite (5.000–6.000)</div>', unsafe_allow_html=True)
        elif chars < 5000:
            st.markdown(f'<div style="text-align:right; font-size:12px; color:#E1FF00;">{chars:,} caracteres — abaixo do mínimo (5.000)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:right; font-size:12px; color:#f87171;">{chars:,} caracteres — acima do limite (6.000)</div>', unsafe_allow_html=True)

        if check_travessao(artigo_score):
            st.markdown('<div class="warn-box">⚠️ Travessão detectado no texto. Revise antes de avaliar.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        avaliar = st.button("▶ Avaliar artigo", key="btn_avaliar", use_container_width=True)

    if avaliar:
        if not api_key:
            st.error("Insira sua chave de API no menu lateral.")
        elif not artigo_score:
            st.error("Cole o artigo antes de avaliar.")
        else:
            with st.spinner("Analisando artigo..."):
                try:
                    resultado = chamar_api(api_key, PROMPT_SCORE, artigo_score)
                    st.markdown("---")
                    st.markdown("### Resultado da avaliação")
                    st.markdown(f'<div class="result-card">{resultado}</div>', unsafe_allow_html=True)

                    col_copy, _ = st.columns([1, 4])
                    with col_copy:
                        st.download_button(
                            "⬇ Baixar resultado",
                            data=resultado,
                            file_name="score_peers.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")

with tab2:
    artigo_codigo = st.text_area(
        "Artigo aprovado para codificação",
        height=250,
        placeholder="Cole o artigo aprovado aqui. O sistema vai gerar o código CMS completo com tags, taxonomia e formatação HTML para o WordPress...",
        key="artigo_codigo"
    )

    offering_codigo = st.selectbox(
        "Offering (obrigatório)",
        OFFERING_OPTIONS,
        key="offering_codigo"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        codificar = st.button("💻 Gerar código CMS", key="btn_codificar", use_container_width=True)

    if codificar:
        if not api_key:
            st.error("Insira sua chave de API no menu lateral.")
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

                    col_copy, _ = st.columns([1, 4])
                    with col_copy:
                        st.download_button(
                            "⬇ Baixar código",
                            data=resultado,
                            file_name="codigo_cms_peers.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")

with tab3:
    artigo_tax = st.text_area(
        "Conteúdo para classificar",
        height=250,
        placeholder="Cole o artigo ou resumo aqui para classificar a taxonomia...",
        key="artigo_tax"
    )

    offering_tax = st.selectbox(
        "Offering (definida pelo editor)",
        OFFERING_OPTIONS,
        key="offering_tax"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        classificar = st.button("🏷️ Classificar taxonomia", key="btn_tax", use_container_width=True)

    if classificar:
        if not api_key:
            st.error("Insira sua chave de API no menu lateral.")
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
                    st.markdown(f'<div class="result-card"><div class="code-box">{resultado}</div></div>', unsafe_allow_html=True)

                    col_copy, _ = st.columns([1, 4])
                    with col_copy:
                        st.download_button(
                            "⬇ Baixar classificação",
                            data=resultado,
                            file_name="taxonomia_peers.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Erro ao chamar a API: {str(e)}")
