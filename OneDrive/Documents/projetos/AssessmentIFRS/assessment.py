# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="IFRS S1/S2 Readiness Check (Autoavaliação sobre o nível de preparação para divulgações de sustentabilidade. Ferramenta educacional para fins informativos.)", 
    layout="wide",
    page_icon="♻️"
)

st.markdown("<a id='top'></a>", unsafe_allow_html=True)

# ── CSS ────
st.markdown("""
<style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #1a3c5e; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; font-size: 0.93rem; }
    .card {
        background: #ffff;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .gap-card {
        background: #fff8f0;
        border-left: 5px solid #d62728;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 4px;
        font-size: 0.91rem;
    }
    .action-card {
        background: #e8f5e9;
        border-left: 5px solid #2ca02c;
        border-radius: 6px;
        padding: 12px 18px;
        margin-bottom: 14px;
        font-size: 0.91rem;
    }
    .coso-card {
        background: #f0f4ff;
        border-left: 5px solid #1f77b4;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 0.91rem;
    }
    .exemplo-card {
        background: #f6fff6;
        border-left: 5px solid #2ca02c;
        border-radius: 6px;
        padding: 12px 16px;
        margin-top: 10px;
        font-size: 0.88rem;
    }
    .nota-desc {
        font-size: 0.82rem;
        color: #555;
        margin-top: 4px;
        padding-left: 8px;
        border-left: 3px solid #ccc;
    }
    .diagnostico-box {
        background: #ffff;
        border-left: 5px solid #1f77b4;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 10px;
        font-size: 0.92rem;
    }
    .interpretacao-box {
        background: #ffff;
        border-top: 4px solid #1a3c5e;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        font-size: 0.95rem;
    }
    .benchmark-table th {
        background-color: #1a3c5e;
        color: white;
        padding: 8px 12px;
        text-align: left;
    }
    .benchmark-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    .benchmark-table tr:nth-child(even) { background-color: #f4f6f9; }
    .gap-positivo { color: #2ca02c; font-weight: 700; }
    .gap-negativo { color: #d62728; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── DADOS POR SETOR ────
SETORES = {
    "🏦 Financeiro (Bancos, Seguradoras, Asset Managers)": "financeiro",
    "⚡ Energia & Utilities": "energia",
    "🏭 Indústria & Manufatura": "industria",
    "🛒 Varejo & Consumo": "varejo"
}

BENCHMARKS = {
    "financeiro": {"🏛️ Governança": 62, "🗺️ Estratégia": 48, "⚙️ Gestão de Riscos": 55, "📊 Métricas e Metas": 44},
    "energia":    {"🏛️ Governança": 58, "🗺️ Estratégia": 52, "⚙️ Gestão de Riscos": 60, "📊 Métricas e Metas": 65},
    "industria":  {"🏛️ Governança": 45, "🗺️ Estratégia": 38, "⚙️ Gestão de Riscos": 42, "📊 Métricas e Metas": 35},
    "varejo":     {"🏛️ Governança": 40, "🗺️ Estratégia": 32, "⚙️ Gestão de Riscos": 38, "📊 Métricas e Metas": 30}
}

EXEMPLOS_REAIS = {
    "🏛️ Governança": {
        "financeiro": [
            ("Deutsche Bank / DWS — Greenwashing (2023)", "A DWS, gestora do Deutsche Bank, pagou USD 19M à SEC por afirmar que integrava critérios ESG em investimentos sem ter processos de governança formalizados para isso. O Conselho não tinha supervisão documentada sobre as alegações ESG feitas ao mercado."),
            ("Bradesco — Relatório de Clima (2024)", "O Bradesco foi um dos primeiros bancos brasileiros a publicar relatório alinhado ao TCFD com aprovação formal do Conselho, criando um subcomitê de clima com reporte trimestral à Diretoria Executiva — modelo que tende a virar padrão mínimo exigido pela CVM.")
        ],
        "energia": [
            ("Shell — Decisão Judicial Holanda (2021)", "Um tribunal holandês ordenou que a Shell reduzisse suas emissões em 45% até 2030, citando ausência de governança climática adequada no Conselho. O caso estabeleceu precedente global sobre responsabilidade fiduciária de diretores em relação ao clima."),
            ("Petrobras — Plano Estratégico 2024–2028", "A Petrobras incluiu metas de descarbonização com aprovação do Conselho e vinculação à remuneração variável de executivos — movimento que responde diretamente às exigências do IFRS S2 sobre governança.")
        ],
        "industria": [
            ("Vale — Governança Pós-Mariana e Brumadinho", "Após as tragédias, a Vale reestruturou completamente sua governança de riscos, criando um Comitê de Sustentabilidade no Conselho com reuniões mensais e reporte público. Hoje é referência em como uma crise pode forçar maturidade de governança."),
            ("3M — Litígios PFAS (2023)", "A 3M enfrentou acordos de USD 10,3 bilhões por contaminação química. Investigações apontaram que o Conselho tinha informações sobre os riscos há décadas sem processo formal de escalada e decisão — gap clássico de governança de riscos de sustentabilidade.")
        ],
        "varejo": [
            ("H&M — Greenwashing (2023)", "A H&M foi processada na Noruega e nos EUA por usar selos de sustentabilidade sem metodologia auditável aprovada pela governança. O caso mostrou que alegações ESG sem processo de Conselho geram risco jurídico concreto."),
            ("Natura — Governança ESG Integrada", "A Natura é referência global em governança ESG integrada ao negócio, com metas de clima aprovadas pelo Conselho e vinculadas à remuneração. Listada no Dow Jones Sustainability Index por mais de 10 anos consecutivos.")
        ]
    },
    "🗺️ Estratégia": {
        "financeiro": [
            ("HSBC — Análise de Cenários Climáticos", "O HSBC publicou análise de cenários climáticos (1,5°C, 2°C e 4°C) mostrando impacto de até USD 35 bilhões em perdas de crédito em carteiras de energia e imóveis em cenário de aquecimento descontrolado — exatamente o que o IFRS S2 exige."),
            ("Itaú — Risco Climático em Crédito (2024)", "O Itaú Unibanco incorporou variáveis climáticas nos modelos de concessão de crédito para agronegócio, avaliando exposição a secas e eventos extremos. Estratégia que antecipa exigências do Banco Central (Resolução BCB 4.557).")
        ],
        "energia": [
            ("BP — Reversão de Estratégia (2023)", "A BP recuou em suas metas de redução de petróleo após pressão de acionistas por retorno financeiro, expondo a tensão entre estratégia de transição e resultado de curto prazo. Caso real de como a falta de integração entre estratégia climática e financeira gera inconsistência."),
            ("Engie Brasil — Portfólio de Transição", "A Engie Brasil desinvestiu 100% de ativos termelétricos a carvão e reorientou CAPEX para renováveis, documentando o processo como parte da estratégia de resiliência climática — modelo de integração estratégia-clima.")
        ],
        "industria": [
            ("ArcelorMittal — Plano de Descarbonização", "A ArcelorMittal comprometeu USD 10 bilhões em CAPEX para tecnologias de aço verde até 2030, integrando o plano de transição ao planejamento financeiro de longo prazo — referência de como indústria pesada pode estruturar estratégia climática crível."),
            ("Embraer — Aviação Sustentável", "A Embraer incluiu análise de cenários de transição energética (SAF — Sustainable Aviation Fuel) no planejamento estratégico 2030, avaliando impacto regulatório europeu (EU ETS) nas receitas de exportação.")
        ],
        "varejo": [
            ("Walmart — Projeto Gigaton (Escopo 3)", "O Walmart lançou o Projeto Gigaton para reduzir 1 bilhão de toneladas de emissões na cadeia de fornecimento até 2030 — reconhecendo que 95% das emissões do varejo estão no Escopo 3, não nas operações próprias."),
            ("Magazine Luiza — Logística e Clima", "O Magalu mapeou riscos climáticos físicos (enchentes, calor extremo) sobre sua rede logística e centros de distribuição, integrando o resultado ao planejamento de expansão — exemplo de estratégia climática aplicada ao varejo brasileiro.")
        ]
    },
    "⚙️ Gestão de Riscos": {
        "financeiro": [
            ("Banco Central do Brasil — Resolução 4.557", "O BCB exige desde 2022 que bancos integrem riscos socioambientais ao ICAAP (processo de avaliação de capital). Bancos sem ERM integrado a riscos climáticos estão em não conformidade regulatória — não apenas com IFRS S2, mas com o próprio regulador prudencial."),
            ("Zurich Insurance — Risco Físico em Subscrição", "A Zurich desenvolveu modelos proprietários de risco físico climático para precificação de seguros, integrando dados de eventos extremos ao processo de underwriting. Referência de como gestão de riscos climáticos gera vantagem competitiva no setor financeiro.")
        ],
        "energia": [
            ("Texas — Apagão de Fevereiro 2021", "O colapso da rede elétrica do Texas durante onda de frio extremo causou prejuízo de USD 195 bilhões. Investigações mostraram que as utilities não tinham riscos físicos climáticos integrados ao ERM — o evento era considerado improvável, mas não impossível."),
            ("Enel — Gestão de Riscos Físicos", "A Enel mapeou 100% de seus ativos de geração contra cenários de risco físico (seca, calor, inundação) e criou KRIs específicos para monitoramento contínuo — modelo que o IFRS S2 usa como referência de boas práticas.")
        ],
        "industria": [
            ("BASF — Escassez Hídrica no Reno (2018)", "A BASF perdeu EUR 250 milhões em receita quando o nível do Rio Reno caiu a ponto de impedir o transporte de matérias-primas. O evento não estava no mapa de riscos da empresa — gap clássico de risco físico climático não integrado ao ERM."),
            ("Suzano — Gestão de Riscos Hídricos", "A Suzano, maior produtora de celulose do mundo, integrou riscos hídricos ao ERM com KRIs de disponibilidade de água por bacia hidrográfica, dado que água é insumo crítico. Referência de gestão de risco físico em indústria de base.")
        ],
        "varejo": [
            ("Carrefour Brasil — Riscos na Cadeia de Fornecimento", "O Carrefour implementou due diligence climática em fornecedores de alimentos frescos após perdas por eventos climáticos extremos afetarem a disponibilidade de produtos. Caso real de risco de transição (reputacional) e físico combinados."),
            ("Amazon — Riscos Logísticos Climáticos", "A Amazon mapeou exposição de seus centros de distribuição a riscos físicos (inundações, calor extremo) após eventos em 2021–2022 causarem interrupções operacionais. O resultado foi integrado ao planejamento de novos CDs.")
        ]
    },
    "📊 Métricas e Metas": {
        "financeiro": [
            ("Net-Zero Banking Alliance — Metas SBTi", "Dos 140 bancos signatários da NZBA, menos de 30% publicaram metas validadas pelo SBTi até 2024. O gap entre compromisso público e métrica auditável é o principal risco de greenwashing no setor financeiro global."),
            ("Santander Brasil — Inventário GHG", "O Santander Brasil publica inventário de GHG de Escopo 1, 2 e 3 (incluindo carteira de crédito financiada) com asseguração limitada da PwC — modelo que tende a virar padrão mínimo para bancos brasileiros sob CVM 193.")
        ],
        "energia": [
            ("TotalEnergies — Metas de Emissões Contestadas", "A TotalEnergies foi processada por acionistas por publicar metas de redução de emissões sem metodologia auditável e sem incluir Escopo 3 (uso dos combustíveis vendidos). O caso mostra que métricas incompletas geram risco jurídico maior do que não ter metas."),
            ("Copel — Inventário GHG Verificado", "A Copel publica inventário de GHG verificado por terceiros desde 2009, com Escopo 1, 2 e 3, e metas alinhadas ao Acordo de Paris. Referência de maturidade em métricas para o setor elétrico brasileiro.")
        ],
        "industria": [
            ("Volkswagen — Escândalo Dieselgate (2015)", "O caso Dieselgate não foi apenas fraude em emissões de veículos — foi a maior falha de controles internos sobre dados de sustentabilidade da história corporativa, custando mais de EUR 30 bilhões em multas e acordos. Demonstra o risco de métricas sem auditoria independente."),
            ("Gerdau — Intensidade de Carbono", "A Gerdau adotou métrica de intensidade de carbono (tCO₂/t de aço) em vez de meta absoluta, argumentando que crescimento de produção tornaria metas absolutas inatingíveis. O IFRS S2 exige transparência sobre a escolha metodológica — não apenas o número.")
        ],
        "varejo": [
            ("Unilever — Metas de Escopo 3 (Cadeia de Fornecimento)", "A Unilever foi uma das primeiras empresas a publicar metas de Escopo 3 para fornecedores, mas admitiu em 2023 que não conseguiria atingi-las por falta de dados confiáveis dos fornecedores — lição sobre o gap entre meta e capacidade de mensuração."),
            ("Grupo Pão de Açúcar — Métricas de Desperdício", "O GPA integrou métricas de desperdício alimentar ao relatório de sustentabilidade com metodologia auditável, conectando a meta de redução de desperdício à redução de emissões de Escopo 3 — exemplo de métrica setorial relevante para varejo.")
        ]
    }
}


perguntas = {
    "🏛️ Governança": {
        "referencia": "IFRS S1 §5–9 | COSO: Ambiente de Controle & Monitoramento",
        "coso_componente": "Ambiente de Controle",
        "coso_risco": "Sem tom adequado no topo (tone at the top), os controles sobre sustentabilidade carecem de legitimidade e recursos para funcionar.",
        "itens": [
            {
                "pergunta": "O Conselho de Administração possui responsabilidade formal e documentada pela supervisão de riscos e oportunidades de sustentabilidade — não apenas como menção no estatuto, mas com processo, frequência e evidência?",
                "acao": "Formalizar em regimento interno do Conselho a periodicidade mínima (trimestral) de pauta de sustentabilidade, com modelo de ata e responsável nomeado para consolidar o reporte.",
                "notas": {
                    0: "Não existe nenhuma atribuição formal. Sustentabilidade não aparece na pauta do Conselho.",
                    1: "O tema é discutido informalmente, mas sem processo, responsável ou registro formal.",
                    2: "Existe menção no estatuto ou política, mas sem processo operacional definido (frequência, pauta, evidência).",
                    3: "O Conselho discute sustentabilidade com frequência definida e há atas, mas o processo ainda não foi auditado.",
                    4: "Processo documentado, com frequência definida, atas formais, responsável nomeado e evidência auditável."
                }
            },
            {
                "pergunta": "Se um investidor institucional pedisse hoje as atas das últimas 4 reuniões do Conselho sobre clima e sustentabilidade, você conseguiria entregar em 48 horas com conteúdo substantivo (não apenas menção protocolar)?",
                "acao": "Criar template padronizado de ata para pautas de sustentabilidade, incluindo decisões tomadas, responsáveis e prazos — e aplicar retroativamente nas próximas 2 reuniões.",
                "notas": {
                    0: "Não existem atas com conteúdo de sustentabilidade.",
                    1: "Existem menções pontuais, mas sem substância ou decisões registradas.",
                    2: "Algumas reuniões têm pauta de sustentabilidade, mas a documentação é inconsistente.",
                    3: "A maioria das reuniões tem registro adequado, mas há gaps de conteúdo ou periodicidade.",
                    4: "Documentação completa, consistente e pronta para due diligence de investidor ou regulador."
                }
            },
            {
                "pergunta": "Existe um comitê ou subcomitê dedicado a ESG/clima com mandato formal, membros nomeados e reporte regular à Diretoria Executiva?",
                "acao": "Constituir formalmente um Comitê de Sustentabilidade com mandato aprovado pelo Conselho, definindo composição mínima, frequência de reuniões e formato de reporte à Diretoria.",
                "notas": {
                    0: "Não existe nenhum comitê ou grupo de trabalho formal.",
                    1: "Existe um grupo informal ou task force sem mandato documentado.",
                    2: "Comitê criado, mas sem reuniões regulares ou reporte estruturado.",
                    3: "Comitê ativo com reuniões regulares, mas sem integração formal ao ciclo de governança corporativa.",
                    4: "Comitê com mandato formal, membros nomeados, reuniões regulares e reporte documentado ao Conselho."
                }
            },
            {
                "pergunta": "A remuneração variável (bônus, PLR, stock options) de executivos C-level inclui métricas de sustentabilidade ou clima com peso e metodologia de cálculo transparentes?",
                "acao": "Incluir ao menos uma métrica de clima (ex: redução de emissões Escopo 1+2 ou meta de inventário GHG) com peso mínimo de 10% no bônus anual dos executivos responsáveis, com metodologia publicada no relatório de remuneração.",
                "notas": {
                    0: "Nenhuma métrica de sustentabilidade na remuneração variável.",
                    1: "Há intenção declarada, mas nenhuma métrica implementada.",
                    2: "Existe alguma métrica ESG na remuneração, mas com peso irrelevante (< 5%) ou sem metodologia clara.",
                    3: "Métricas ESG com peso relevante, mas metodologia de cálculo não é pública ou auditável.",
                    4: "Métricas ESG com peso relevante, metodologia transparente e divulgada no relatório de remuneração."
                }
            },
            {
                "pergunta": "A empresa possui um executivo (CRO, CSO, CDO ou equivalente) com mandato explícito, recursos e acesso ao Conselho para tratar riscos e oportunidades de sustentabilidade?",
                "acao": "Formalizar o mandato do responsável por sustentabilidade em job description aprovado pelo CEO, com linha de reporte direta ao Conselho e orçamento dedicado documentado no planejamento anual.",
                "notas": {
                    0: "Não existe responsável formal. O tema é tratado de forma difusa ou inexistente.",
                    1: "Existe um responsável informal ou acumulado com outras funções sem recursos dedicados.",
                    2: "Existe um responsável formal, mas sem acesso direto ao Conselho ou recursos adequados.",
                    3: "Responsável com mandato e recursos, mas sem reporte regular ao Conselho.",
                    4: "Executivo com mandato explícito, recursos dedicados e acesso formal ao Conselho."
                }
            },
            {
                "pergunta": "Quando a empresa faz uma aquisição, lança um produto ou entra em novo mercado, existe um processo formal de avaliação de riscos e oportunidades de sustentabilidade como parte do gate de aprovação?",
                "acao": "Inserir checklist de due diligence ESG/clima como etapa obrigatória no processo de aprovação de M&A e novos projetos estratégicos, com critério mínimo de aprovação e registro da avaliação.",
                "notas": {
                    0: "Sustentabilidade não faz parte do processo de aprovação de novos negócios.",
                    1: "É considerada informalmente em alguns casos, sem processo ou critério definido.",
                    2: "Existe checklist ou critério básico, mas não é obrigatório ou não tem peso na decisão.",
                    3: "Processo formal existe para grandes decisões, mas não é aplicado consistentemente.",
                    4: "Processo obrigatório, documentado e auditável para todas as decisões estratégicas relevantes."
                }
            },
            {
                "pergunta": "A empresa divulga publicamente como sua governança de sustentabilidade funciona — não apenas que ela existe, mas como opera, com que frequência e quais decisões foram tomadas?",
                "acao": "Incluir seção dedicada à governança de sustentabilidade no próximo relatório anual, descrevendo estrutura, frequência de reuniões, exemplos de decisões tomadas e alinhamento ao IFRS S1 §5–9.",
                "notas": {
                    0: "Nenhuma divulgação sobre governança de sustentabilidade.",
                    1: "Menção genérica no relatório anual sem substância operacional.",
                    2: "Divulgação básica de estrutura, mas sem detalhes de processo ou decisões.",
                    3: "Divulgação razoável, mas sem evidência de como as decisões são tomadas.",
                    4: "Divulgação completa, alinhada ao IFRS S1 §5–9, com exemplos concretos de decisões e processos."
                }
            }
        ]
    },
    "🗺️ Estratégia": {
        "referencia": "IFRS S1 §10–17 | IFRS S2 §10–21 | COSO: Avaliação de Riscos",
        "coso_componente": "Avaliação de Riscos",
        "coso_risco": "Sem identificação e análise de riscos de sustentabilidade integrada à estratégia, os objetivos corporativos são definidos sem considerar ameaças e oportunidades materiais de longo prazo.",
        "itens": [
            {
                "pergunta": "Se o seu maior cliente exigir amanhã um relatório completo de emissões da sua cadeia de fornecimento (Escopo 3) como condição para renovar o contrato, você consegue entregar em 60 dias?",
                "acao": "Iniciar mapeamento de fornecedores críticos (top 80% do gasto) e solicitar dados de emissões usando questionário baseado no GHG Protocol — priorizando os 10 maiores fornecedores como piloto.",
                "notas": {
                    0: "Não temos dados de Escopo 3 e não teríamos como coletar em 60 dias.",
                    1: "Temos estimativas parciais, mas sem metodologia ou dados de fornecedores.",
                    2: "Temos dados de alguns fornecedores relevantes, mas a cobertura é inferior a 50%.",
                    3: "Temos dados de mais de 70% da cadeia, mas com gaps metodológicos.",
                    4: "Temos inventário de Escopo 3 completo, com metodologia documentada e dados de fornecedores."
                }
            },
            {
                "pergunta": "A empresa realizou análise de cenários climáticos (ex: 1,5°C, 2°C, transição desordenada) com impacto quantificado em receita, EBITDA ou valor de ativos — não apenas uma análise qualitativa?",
                "acao": "Contratar análise de cenários climáticos com pelo menos dois cenários (transição ordenada e desordenada), quantificando impacto em receita e CAPEX para horizonte de 5 e 10 anos — integrando o resultado ao próximo ciclo de planejamento estratégico.",
                "notas": {
                    0: "Nenhuma análise de cenários climáticos foi realizada.",
                    1: "Análise qualitativa básica, sem quantificação financeira.",
                    2: "Análise com alguma quantificação, mas limitada a um cenário ou horizonte de tempo.",
                    3: "Análise com múltiplos cenários e quantificação financeira, mas não integrada ao planejamento.",
                    4: "Análise robusta, com múltiplos cenários, quantificação financeira e integrada ao planejamento estratégico."
                }
            },
            {
                "pergunta": "Os impactos financeiros dos riscos climáticos (físicos e de transição) estão refletidos nas projeções financeiras, no CAPEX e no planejamento de longo prazo aprovado pelo Conselho?",
                "acao": "Incluir premissas de risco climático (ex: preço de carbono, custo de adaptação de ativos) nas próximas projeções financeiras de longo prazo, com aprovação formal do Conselho e divulgação das premissas utilizadas.",
                "notas": {
                    0: "Riscos climáticos não aparecem nas projeções financeiras.",
                    1: "Há reconhecimento verbal, mas sem reflexo nos números.",
                    2: "Alguns riscos estão refletidos em premissas, mas de forma não sistemática.",
                    3: "Riscos climáticos integrados ao planejamento, mas sem aprovação formal do Conselho.",
                    4: "Integração completa, com aprovação do Conselho e divulgação das premissas utilizadas."
                }
            },
            {
                "pergunta": "A empresa possui um plano de transição para uma economia de baixo carbono com metas, ações, responsáveis, cronograma e orçamento definidos — não apenas uma declaração de intenção?",
                "acao": "Desenvolver plano de transição com metas de redução de emissões por escopo, ações específicas por área de negócio, responsáveis nomeados, cronograma anual e orçamento aprovado pelo Conselho — publicando o plano no próximo relatório anual.",
                "notas": {
                    0: "Não existe plano de transição.",
                    1: "Existe declaração pública de compromisso, mas sem plano operacional.",
                    2: "Existe plano com metas, mas sem orçamento, responsáveis ou cronograma detalhado.",
                    3: "Plano estruturado com metas, responsáveis e cronograma, mas sem orçamento aprovado.",
                    4: "Plano completo, com metas, ações, responsáveis, cronograma, orçamento e aprovação do Conselho."
                }
            },
            {
                "pergunta": "A empresa avaliou como mudanças regulatórias climáticas (ex: precificação de carbono, taxonomia verde, restrições de financiamento) podem afetar seu modelo de negócio nos próximos 5–10 anos?",
                "acao": "Realizar análise de impacto regulatório climático cobrindo as principais jurisdições onde a empresa opera, com foco em precificação de carbono e taxonomia verde — integrando os resultados ao planejamento estratégico e criando planos de contingência documentados.",
                "notas": {
                    0: "Nenhuma avaliação de riscos regulatórios climáticos foi realizada.",
                    1: "Monitoramento informal de regulações, sem análise de impacto.",
                    2: "Análise de impacto realizada para algumas regulações, mas não de forma sistemática.",
                    3: "Análise sistemática de riscos regulatórios, mas sem integração ao planejamento estratégico.",
                    4: "Análise completa, integrada ao planejamento e com planos de contingência documentados."
                }
            },
            {
                "pergunta": "A empresa identificou oportunidades de negócio geradas pela transição climática (ex: novos produtos, novos mercados, eficiência energética) e as incorporou ao planejamento estratégico?",
                "acao": "Mapear e quantificar as 3 principais oportunidades de negócio geradas pela transição climática para o setor, incorporando ao planejamento estratégico com KPIs de acompanhamento e responsável por cada oportunidade.",
                "notas": {
                    0: "Foco exclusivo em riscos; oportunidades não foram mapeadas.",
                    1: "Oportunidades identificadas informalmente, sem análise de viabilidade.",
                    2: "Algumas oportunidades analisadas, mas não incorporadas ao planejamento.",
                    3: "Oportunidades incorporadas ao planejamento, mas sem métricas de acompanhamento.",
                    4: "Oportunidades mapeadas, quantificadas, incorporadas ao planejamento e monitoradas por KPIs."
                }
            },
            {
                "pergunta": "A estratégia de sustentabilidade da empresa é consistente com o que é comunicado ao mercado, ao regulador e internamente — ou existem versões diferentes da narrativa para públicos diferentes?",
                "acao": "Estabelecer processo de revisão cruzada (jurídico + RI + sustentabilidade) para toda comunicação ESG antes da publicação, garantindo consistência entre relatório anual, apresentações a investidores e comunicação interna.",
                "notas": {
                    0: "Narrativas inconsistentes entre relatório anual, apresentações a investidores e comunicação interna.",
                    1: "Há esforço de alinhamento, mas inconsistências materiais ainda existem.",
                    2: "Narrativa razoavelmente consistente, mas com gaps em detalhes técnicos ou métricas.",
                    3: "Narrativa consistente na maioria dos canais, com pequenas divergências.",
                    4: "Narrativa completamente consistente, revisada por equipe jurídica e de RI antes de qualquer divulgação."
                }
            }
        ]
    },
    "⚙️ Gestão de Riscos": {
        "referencia": "IFRS S1 §18–20 | IFRS S2 §22–30 | COSO: Atividades de Controle & Informação",
        "coso_componente": "Atividades de Controle",
        "coso_risco": "Sem controles operacionais sobre dados e processos de sustentabilidade, a empresa não consegue garantir a confiabilidade das informações divulgadas — expondo-se a risco de greenwashing involuntário.",
        "itens": [
            {
                "pergunta": "Os riscos de sustentabilidade (físicos e de transição) estão formalmente integrados ao mapa de riscos corporativo (ERM) com a mesma metodologia, escala e processo de escalada dos demais riscos?",
                "acao": "Incluir riscos climáticos físicos e de transição na próxima revisão do mapa de riscos corporativo, usando a mesma escala de impacto financeiro e probabilidade dos demais riscos, com processo de escalada definido para riscos acima do apetite.",
                "notas": {
                    0: "Riscos de sustentabilidade não aparecem no ERM corporativo.",
                    1: "Existem em documento separado, sem integração ao ERM.",
                    2: "Parcialmente integrados, mas com metodologia diferente dos demais riscos.",
                    3: "Integrados ao ERM com mesma metodologia, mas sem processo de escalada definido.",
                    4: "Totalmente integrados, com mesma metodologia, processo de escalada e revisão periódica."
                }
            },
            {
                "pergunta": "A empresa possui um processo para identificar e avaliar riscos físicos climáticos (ex: inundações, secas, calor extremo) sobre seus ativos, operações e cadeia de fornecimento com critérios de materialidade definidos?",
                "acao": "Realizar mapeamento de exposição física climática dos principais ativos e fornecedores críticos usando dados de risco físico, definindo critérios de materialidade e revisão anual.",
                "notas": {
                    0: "Nenhum processo de identificação de riscos físicos climáticos.",
                    1: "Riscos físicos identificados informalmente, sem critérios de materialidade.",
                    2: "Processo básico para ativos próprios, sem cobertura da cadeia de fornecimento.",
                    3: "Processo estruturado para ativos e cadeia, mas sem critérios de materialidade formalizados.",
                    4: "Processo completo, com critérios de materialidade, cobertura de cadeia e revisão periódica."
                }
            },
            {
                "pergunta": "A empresa possui um processo para identificar e avaliar riscos de transição (ex: novas regulações, mudanças de mercado, litígios climáticos, mudanças tecnológicas) com horizonte de pelo menos 10 anos?",
                "acao": "Estruturar processo anual de identificação de riscos de transição com horizonte de 10 anos, cobrindo regulação, mercado, tecnologia e litígios — integrando ao ERM com revisão pelo Comitê de Riscos.",
                "notas": {
                    0: "Nenhum processo de identificação de riscos de transição.",
                    1: "Monitoramento reativo de regulações, sem análise prospectiva.",
                    2: "Análise de riscos de transição para horizonte de 1–3 anos, sem visão de longo prazo.",
                    3: "Análise com horizonte de 5–10 anos, mas sem integração ao ERM.",
                    4: "Processo completo, com horizonte de 10+ anos, integrado ao ERM e revisado anualmente."
                }
            },
            {
                "pergunta": "Os controles internos sobre dados de sustentabilidade (coleta, cálculo, consolidação, revisão) foram mapeados, documentados e testados — com a mesma rigorosidade aplicada aos controles financeiros?",
                "acao": "Mapear e documentar os controles internos sobre os 5 principais indicadores de sustentabilidade divulgados, testando sua efetividade e registrando evidências.",
                "notas": {
                    0: "Não existem controles internos formais sobre dados de sustentabilidade.",
                    1: "Existem controles informais, sem documentação ou teste.",
                    2: "Controles mapeados, mas não testados ou com cobertura parcial.",
                    3: "Controles mapeados e testados, mas com gaps em áreas críticas.",
                    4: "Controles completos, documentados, testados e com evidência auditável — equivalente ao rigor financeiro."
                }
            },
            {
                "pergunta": "A empresa possui KRIs (Key Risk Indicators) específicos para riscos climáticos com limites de tolerância definidos, monitoramento periódico e processo de escalada quando os limites são atingidos?",
                "acao": "Definir ao menos 3 KRIs climáticos com limites de tolerância e processo de escalada documentado.",
                "notas": {
                    0: "Não existem KRIs para riscos climáticos.",
                    1: "Existem indicadores informais, sem limites de tolerância ou processo de escalada.",
                    2: "KRIs definidos, mas sem limites de tolerância ou monitoramento regular.",
                    3: "KRIs com limites de tolerância e monitoramento, mas sem processo de escalada formalizado.",
                    4: "KRIs completos, com limites, monitoramento periódico e processo de escalada documentado."
                }
            },
            {
                "pergunta": "Quando a empresa concede crédito, faz um investimento ou subscreve um seguro, existe um processo de due diligence de riscos climáticos do tomador/ativo como parte do processo de aprovação?",
                "acao": "Desenvolver checklist de due diligence climática e integrar ao processo de aprovação, com registro obrigatório.",
                "notas": {
                    0: "Riscos climáticos não fazem parte do processo de aprovação de crédito/investimento.",
                    1: "Considerados informalmente em casos específicos, sem processo.",
                    2: "Existe checklist básico para setores de alto risco, mas não é aplicado sistematicamente.",
                    3: "Processo formal para setores de alto risco, mas sem cobertura completa da carteira.",
                    4: "Due diligence climática integrada ao processo de aprovação para toda a carteira relevante."
                }
            },
            {
                "pergunta": "A empresa realizou um exercício de stress test ou simulação de impacto de um evento climático extremo (ex: seca severa, inundação, choque regulatório) sobre suas operações e resultados financeiros?",
                "acao": "Realizar stress test climático em ao menos dois cenários e integrar os resultados ao planejamento, com reporte ao Conselho.",
                "notas": {
                    0: "Nenhum stress test climático foi realizado.",
                    1: "Discussão qualitativa sobre impactos, sem simulação quantitativa.",
                    2: "Stress test realizado para um cenário específico, sem abrangência.",
                    3: "Stress tests realizados para múltiplos cenários, mas não integrados ao planejamento de capital.",
                    4: "Stress tests regulares, com múltiplos cenários, integrados ao planejamento de capital e aprovados pelo Conselho."
                }
            }
        ]
    },
    "📊 Métricas e Metas": {
        "referencia": "IFRS S2 §29–37 | COSO: Informação & Comunicação & Monitoramento",
        "coso_componente": "Informação & Comunicação",
        "coso_risco": "Sem métricas confiáveis e auditáveis, a empresa não consegue demonstrar progresso em relação às metas — e qualquer divulgação se torna um risco de greenwashing, não um ativo de reputação.",
        "itens": [
            {
                "pergunta": "A empresa mensura emissões de GEE de Escopo 1 (diretas) e Escopo 2 (energia) com metodologia documentada (ex: GHG Protocol), fator de emissão rastreável e processo de revisão anual?",
                "acao": "Implementar inventário de GHG Escopo 1 e 2 com metodologia GHG Protocol e asseguração limitada para as métricas principais.",
                "notas": {
                    0: "Não mensuramos emissões de GEE.",
                    1: "Estimativas informais, sem metodologia documentada.",
                    2: "Inventário básico de Escopo 1 e 2, mas com gaps metodológicos ou sem revisão anual.",
                    3: "Inventário completo de Escopo 1 e 2 com metodologia documentada, mas sem asseguração externa.",
                    4: "Inventário completo, metodologia documentada, fator de emissão rastreável e asseguração externa."
                }
            },
            {
                "pergunta": "A empresa possui inventário de emissões de Escopo 3 (cadeia de valor) ou, ao menos, um plano com cronograma, responsável e orçamento para sua implementação nos próximos 24 meses?",
                "acao": "Elaborar plano de implementação de Escopo 3 com cronograma, responsável e orçamento, priorizando categorias materiais.",
                "notas": {
                    0: "Não temos inventário de Escopo 3 e não há plano para implementação.",
                    1: "Reconhecemos a necessidade, mas não há plano formal.",
                    2: "Existe plano básico, mas sem cronograma, responsável ou orçamento definidos.",
                    3: "Plano estruturado com cronograma e responsável, mas sem orçamento aprovado.",
                    4: "Inventário de Escopo 3 existente ou plano completo com cronograma, responsável e orçamento aprovado."
                }
            },
            {
                "pergunta": "As métricas de sustentabilidade utilizadas seguem padrões reconhecidos (ex: SASB para o setor, GRI, métricas específicas do IFRS S2) e são consistentes entre períodos para permitir comparabilidade?",
                "acao": "Padronizar KPIs usando SASB/IFRS S2, documentar metodologia e garantir consistência de cálculo entre períodos.",
                "notas": {
                    0: "Métricas definidas internamente sem referência a padrões externos.",
                    1: "Referência a padrões externos, mas sem aplicação sistemática.",
                    2: "Padrões aplicados parcialmente, com inconsistências entre períodos.",
                    3: "Padrões aplicados de forma consistente, mas sem divulgação da metodologia.",
                    4: "Padrões aplicados, metodologia divulgada, consistência entre períodos e comparabilidade garantida."
                }
            },
            {
                "pergunta": "A empresa definiu metas de redução de emissões com base científica (ex: SBTi) ou alinhadas a acordos internacionais, com ano-base, horizonte temporal e trajetória de redução definidos?",
                "acao": "Definir metas com ano-base e trajetória, e submeter à validação externa (ex: SBTi), com metas intermediárias.",
                "notas": {
                    0: "Não existem metas de redução de emissões.",
                    1: "Compromisso público de neutralidade/net-zero sem metas intermediárias ou metodologia.",
                    2: "Metas definidas, mas sem base científica, ano-base claro ou trajetória de redução.",
                    3: "Metas com base científica e trajetória definida, mas sem validação externa (ex: SBTi).",
                    4: "Metas validadas externamente (ex: SBTi), com ano-base, trajetória e metas intermediárias divulgadas."
                }
            },
            {
                "pergunta": "Os dados de sustentabilidade passam por processo de asseguração (interna ou externa) antes da divulgação — com escopo, critérios e conclusão documentados?",
                "acao": "Contratar asseguração limitada para métricas materiais e evoluir para asseguração razoável no ciclo de obrigatoriedade.",
                "notas": {
                    0: "Nenhum processo de asseguração sobre dados de sustentabilidade.",
                    1: "Revisão interna informal, sem critérios ou documentação.",
                    2: "Revisão interna formal, mas sem asseguração externa.",
                    3: "Asseguração externa limitada (limited assurance) para algumas métricas.",
                    4: "Asseguração externa razoável (reasonable assurance) para as métricas principais, com relatório publicado."
                }
            },
            {
                "pergunta": "Existe rastreabilidade completa dos dados que alimentam as métricas de sustentabilidade — ou seja, é possível ir do número publicado até a fonte primária (medidor, fatura, sistema) com trilha de auditoria?",
                "acao": "Implementar trilha de auditoria para KPIs (versionamento, evidências e ligação do número publicado à fonte primária).",
                "notas": {
                    0: "Não existe rastreabilidade. Os números são calculados em planilhas sem controle de versão.",
                    1: "Rastreabilidade parcial para algumas métricas, sem trilha de auditoria formal.",
                    2: "Rastreabilidade para as métricas principais, mas com gaps em fontes secundárias.",
                    3: "Rastreabilidade completa para as métricas principais, com trilha de auditoria básica.",
                    4: "Rastreabilidade completa, trilha de auditoria formal e sistema de controle de versão para todos os dados."
                }
            },
            {
                "pergunta": "A empresa monitora o progresso em relação às metas de sustentabilidade com a mesma frequência e rigor que monitora metas financeiras — com reporte regular ao Conselho e plano de ação quando há desvio?",
                "acao": "Criar rotina trimestral de monitoramento, reporte ao Conselho e plano de ação para desvios, com governança equivalente às metas financeiras.",
                "notas": {
                    0: "Metas de sustentabilidade não são monitoradas regularmente.",
                    1: "Monitoramento anual, apenas para o relatório de sustentabilidade.",
                    2: "Monitoramento semestral, mas sem reporte ao Conselho ou plano de ação para desvios.",
                    3: "Monitoramento trimestral com reporte ao Conselho, mas sem plano de ação formalizado para desvios.",
                    4: "Monitoramento com mesma frequência das metas financeiras, reporte ao Conselho e plano de ação para desvios."
                }
            }
        ]
    }
}

COSO_COMPONENTES = {
    "Ambiente de Controle": "Define o tom da organização. Sem comprometimento da liderança, nenhum controle de sustentabilidade funciona de forma sustentada.",
    "Avaliação de Riscos": "Identifica e analisa riscos relevantes para os objetivos. Riscos climáticos não identificados não podem ser gerenciados.",
    "Atividades de Controle": "Políticas e procedimentos que garantem que as diretrizes da gestão sejam executadas. Inclui controles sobre dados de sustentabilidade.",
    "Informação & Comunicação": "Informações relevantes identificadas, capturadas e comunicadas. Métricas de sustentabilidade confiáveis são o produto deste componente.",
    "Monitoramento": "Avaliação contínua da qualidade do controle interno. Inclui asseguração interna e externa sobre dados de sustentabilidade."
}

EMOJIS_NOTA = ["🔴", "🟠", "🟡", "🔵", "🟢"]
LABELS_NOTA = ["Não iniciado", "Em discussão", "Planejado", "Implementado parcialmente", "Implementado e auditável"]

# ════════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO DO SESSION_STATE - SOLUÇÃO ROBUSTA PARA PRESERVAR RESPOSTAS
# ════════════════════════════════════════════════════════════════════════════════
# 
# PROBLEMA: O Streamlit perde os valores dos sliders quando eles não são renderizados
# (ao mudar de pilar). Isso acontece porque:
# 1. Os widgets só existem no session_state enquanto estão sendo renderizados
# 2. Quando o usuário muda de pilar, os sliders do pilar anterior não são renderizados
# 3. O Streamlit pode limpar esses valores do session_state
#
# SOLUÇÃO: 
# 1. Criar uma estrutura de dados dedicada ('respostas_assessment') no session_state
# 2. Inicializar TODOS os valores ANTES de renderizar qualquer widget
# 3. Usar callbacks para sincronizar os valores do widget com a estrutura dedicada
# 4. Os sliders sempre leem da estrutura dedicada, não diretamente do session_state
# ════════════════════════════════════════════════════════════════════════════════

def inicializar_respostas():
    """
    Inicializa a estrutura de respostas no session_state.
    Esta função deve ser chamada ANTES de qualquer widget ser renderizado.
    """
    if 'respostas_assessment' not in st.session_state:
        st.session_state.respostas_assessment = {}
    
    # Inicializar todas as chaves de resposta com valor padrão 0
    for pilar, info in perguntas.items():
        for idx in range(1, len(info["itens"]) + 1):
            chave = f"{pilar}_{idx}"
            if chave not in st.session_state.respostas_assessment:
                st.session_state.respostas_assessment[chave] = 0

def obter_resposta(pilar: str, idx: int) -> int:
    """
    Obtém o valor da resposta da estrutura dedicada.
    Sempre retorna um valor válido (0-4).
    """
    chave = f"{pilar}_{idx}"
    return st.session_state.respostas_assessment.get(chave, 0)

def salvar_resposta(pilar: str, idx: int):
    """
    Callback para salvar o valor do slider na estrutura dedicada.
    Esta função é chamada automaticamente quando o slider muda.
    """
    chave_slider = f"slider_{pilar}_{idx}"
    chave_resposta = f"{pilar}_{idx}"
    
    if chave_slider in st.session_state:
        st.session_state.respostas_assessment[chave_resposta] = st.session_state[chave_slider]

# ════════════════════════════════════════════════════════════════════════════════
# CHAMAR INICIALIZAÇÃO ANTES DE QUALQUER WIDGET
# ════════════════════════════════════════════════════════════════════════════════
inicializar_respostas()

# ── SIDEBAR ────
with st.sidebar:
    st.markdown(" 🌿 IFRS S1 & S2 Assessment")
    st.markdown("Selecione o setor da empresa:")
    setor_label = st.selectbox("Setor", list(SETORES.keys()), label_visibility="collapsed", key="setor_selectbox")
    setor_key = SETORES[setor_label]
    st.markdown("---")
    st.markdown("Escala de maturidade (0–4):")
    for k, v in {
        "🔴 0": "Não iniciado — não existe processo, dado ou responsável",
        "🟠 1": "Em discussão — reconhecido, mas sem ação formal",
        "🟡 2": "Planejado — estruturado, mas não implementado",
        "🔵 3": "Implementado parcialmente — funciona, mas com gaps",
        "🟢 4": "Implementado e auditável — evidência completa"
    }.items():
        st.markdown(f"{k} — {v}")
    st.markdown("---")
    st.markdown("Framework: IFRS S1 & S2 (ISSB) + TCFD + COSO")
    st.markdown("Regulação BR: Resolução CVM 193/2023")
    st.caption("🔒 Nenhum dado é armazenado. Sessão 100% local.")

# ── HEADER ────
st.title("🌿 IFRS S1 & S2 — Readiness Assessment")
st.markdown(f"Diagnóstico de Maturidade para Divulgações de Sustentabilidade e Clima | Setor selecionado: {setor_label}")
st.caption("Baseado no framework TCFD, normas ISSB (IFRS S1 & S2) e componentes COSO | Resolução CVM 193/2023")

with st.expander("📘 Entenda o IFRS S1 & S2: O que muda e quem é obrigado?", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        🎯 O que é?
        As normas IFRS S1 (Requisitos Gerais) e IFRS S2 (Clima) foram emitidas pelo International Sustainability Standards Board (ISSB) para criar uma linguagem global comum para divulgações de sustentabilidade.

        🔄 O que muda?
        - Rigor Contábil: A sustentabilidade sai do "marketing" e entra no relatório financeiro, com o mesmo nível de governança e controle dos números contábeis.
        - Conectividade: Exige que a empresa explique como riscos e oportunidades de sustentabilidade podem afetar seus fluxos de caixa, posição financeira e acesso a capital.
        - Consolidação: As normas consolidam frameworks anteriores (TCFD, SASB, CDSB) em uma única norma global.
        """)
    with col_b:
        st.markdown("""
        ⚖️ Obrigatoriedade no Brasil (Resolução CVM 193/2023)
        - 2024–2025: adoção voluntária por companhias abertas, fundos de investimento e securitizadoras.
        - A partir de 2026: divulgação obrigatória para companhias abertas registradas na CVM.
        - Asseguração: limitada no período voluntário e razoável a partir da obrigatoriedade.

        🚩 O que a norma obriga?
        Divulgar informações materiais sobre riscos e oportunidades em 4 pilares: Governança, Estratégia, Gestão de Riscos e Métricas/Metas. No pilar climático (S2), exige ainda análise de cenários, plano de transição e inventário de emissões (Escopos 1, 2 e 3).
        """)


# ──  BARRA DE PROGRESSO GLOBAL ────
# Usar a estrutura dedicada para calcular o progresso
total_perguntas = sum(len(info["itens"]) for info in perguntas.values())

respondidas = sum(
    1 for pilar, info in perguntas.items()
    for idx in range(1, len(info["itens"]) + 1)
    if obter_resposta(pilar, idx) != 0
)

pct_progresso = respondidas / total_perguntas if total_perguntas else 0
col_prog1, col_prog2 = st.columns([3, 1])
with col_prog1:
    st.markdown(f"📋 Progresso do diagnóstico — {respondidas} de {total_perguntas} questões")
    st.progress(pct_progresso)
with col_prog2:
    st.markdown(
        f"<div style='text-align:center; font-size:1.8rem; font-weight:700; color:#1a3c5e; padding-top:4px'>{int(pct_progresso*100)}%</div>",
        unsafe_allow_html=True
    )

st.divider()


# ── PERGUNTAS ────
scores = {}
respostas_detalhe = []

pilares_lista = list(perguntas.keys())

pilar_selecionado = st.radio(
    "Selecione o pilar:",
    pilares_lista,
    horizontal=True,
    format_func=lambda x: x,
    key="radio_pilar_main"
)

st.markdown("---")

# Calculate scores for all pilares, using the dedicated response structure
for pilar in pilares_lista:
    info = perguntas[pilar]
    pilar_scores_calc = [
        obter_resposta(pilar, idx)
        for idx in range(1, len(info["itens"]) + 1)
    ]
    scores[pilar] = (sum(pilar_scores_calc) / (len(pilar_scores_calc) * 4)) * 100 if pilar_scores_calc else 0

# Construir respostas_detalhe para TODOS os pilares usando a estrutura dedicada
for pilar in pilares_lista:
    info = perguntas[pilar]
    for idx, item in enumerate(info["itens"], 1):
        nota = obter_resposta(pilar, idx)
        respostas_detalhe.append({
            "Pilar": pilar.split(" ", 1)[1],
            "Pergunta": item["pergunta"],
            "Nota (0-4)": nota,
            "Nível": LABELS_NOTA[nota]
        })

# Display questions for the selected pilar
pilar = pilar_selecionado
info = perguntas[pilar]

# progresso por pilar
total_pilar = len(info["itens"])
respondidas_pilar = sum(
    1 for idx in range(1, total_pilar + 1)
    if obter_resposta(pilar, idx) != 0
)
pct_pilar = respondidas_pilar / total_pilar if total_pilar else 0
st.markdown(f"*Progresso neste pilar: {respondidas_pilar}/{total_pilar}*")
st.progress(pct_pilar)

col_ref, col_coso = st.columns([1, 1])
with col_ref:
    st.markdown(f"📌 Referência normativa: `{info['referencia']}`")
with col_coso:
    st.markdown(f"🏗️ COSO: {info['coso_componente']}")
st.caption(f"*{info['coso_risco']}*")
st.markdown("---")

pilar_scores = []
for idx, item in enumerate(info["itens"], 1):
    st.markdown(f"{idx}. {item['pergunta']}")

    with st.expander("📖 O que significa cada nota?", expanded=False):
        for nota_val, nota_desc in item["notas"].items():
            st.markdown(f"{EMOJIS_NOTA[nota_val]} Nota {nota_val}: {nota_desc}")

    # ════════════════════════════════════════════════════════════════════════════════
    # SLIDER COM CALLBACK PARA PRESERVAR VALORES
    # ════════════════════════════════════════════════════════════════════════════════
    # O slider usa:
    # 1. value: lê da estrutura dedicada (respostas_assessment)
    # 2. on_change: callback que salva o valor na estrutura dedicada quando muda
    # 3. key: chave única para o widget (necessária para o Streamlit)
    # ════════════════════════════════════════════════════════════════════════════════
    
    valor_atual = obter_resposta(pilar, idx)
    
    nota = st.select_slider(
        f"Nota — questão {idx}",
        options=[0, 1, 2, 3, 4],
        value=valor_atual,  # Lê da estrutura dedicada
        format_func=lambda x: f"{EMOJIS_NOTA[x]} {x} — {LABELS_NOTA[x]}",
        key=f"slider_{pilar}_{idx}",
        on_change=salvar_resposta,  # Callback para salvar quando muda
        args=(pilar, idx),  # Argumentos para o callback
        label_visibility="collapsed"
    )

    pilar_scores.append(nota)

    st.markdown("")

# Update the score for the current pilar
scores[pilar] = (sum(pilar_scores) / (len(pilar_scores) * 4)) * 100 if pilar_scores else 0

st.markdown("---")
st.markdown(" 🌍 Casos Reais — O que o mercado já observou neste pilar")
for titulo, descricao in EXEMPLOS_REAIS[pilar][setor_key]:
    st.markdown(
        f'<div class="exemplo-card"><strong>📌 {titulo}</strong><br>{descricao}</div>',
        unsafe_allow_html=True
    )

# ── RESULTADO ────
st.divider()
st.subheader("📋 Resultado do Diagnóstico")

benchmark = BENCHMARKS[setor_key]
media_geral = sum(scores.values()) / len(scores) if scores else 0
media_benchmark = sum(benchmark.values()) / len(benchmark) if benchmark else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Índice Geral de Maturidade",
        f"{media_geral:.1f}%",
        delta=f"{media_geral - media_benchmark:+.1f}% vs benchmark do setor"
    )
with col2:
    pilar_mais_forte = max(scores, key=scores.get)
    st.metric("Pilar mais forte", pilar_mais_forte.split(" ", 1)[1], f"{scores[pilar_mais_forte]:.0f}%")
with col3:
    pilar_mais_fraco = min(scores, key=scores.get)
    st.metric("Pilar mais crítico", pilar_mais_fraco.split(" ", 1)[1], f"{scores[pilar_mais_fraco]:.0f}%")

if media_geral < 30:
    estagio = "🔴 Estágio: Inicial"
    estagio_msg = "Exposição regulatória alta. Risco de não conformidade com CVM 193 em 2026."
    interpretacao = (
        "A empresa apresenta estruturas iniciais (ou inexistentes) para governança e gestão de riscos climáticos. "
        "As lacunas são materiais principalmente em formalização de responsabilidades, integração com planejamento financeiro "
        "e métricas auditáveis, elevando o risco regulatório e reputacional."
    )
elif media_geral < 55:
    estagio = "🟠 Estágio: Estruturação"
    estagio_msg = "Gaps materiais identificados. Plano de ação urgente necessário."
    interpretacao = (
        "A empresa já reconhece os requisitos de IFRS S1/S2 e possui iniciativas em andamento, "
        "mas ainda apresenta lacunas relevantes em integração estratégia–finanças, consistência de processos "
        "e evidências auditáveis (especialmente em métricas e metas)."
    )
elif media_geral < 75:
    estagio = "🔵 Estágio: Desenvolvimento"
    estagio_msg = "Fundamentos presentes. Foco em formalização e evidência."
    interpretacao = (
        "A empresa possui fundamentos de governança, estratégia e gestão de riscos climáticos, "
        "com necessidade de reforçar controles internos, rastreabilidade e consistência metodológica para suportar asseguração."
    )
else:
    estagio = "🟢 Estágio: Avançado"
    estagio_msg = "Foco em asseguração externa e consistência de divulgação."
    interpretacao = (
        "A empresa demonstra maturidade elevada e alinhamento robusto aos pilares IFRS S1/S2, "
        "com condições de avançar para asseguração externa e otimização contínua de comparabilidade e transparência."
    )

if "🟢" in estagio:
    st.success(estagio)
elif "🔵" in estagio:
    st.info(estagio)
elif "🟠" in estagio:
    st.warning(estagio)
else:
    st.error(estagio)
st.caption(estagio_msg)

st.markdown(
    f'<div class="interpretacao-box"><strong>Interpretação (executiva)</strong><br>{interpretacao}</div>',
    unsafe_allow_html=True
)

st.markdown(" 📌 Benchmark por Pilar (Sua empresa vs. setor)")
rows_bench = []
for p in scores.keys():
    sua = round(scores[p], 1)
    bmk = float(benchmark[p])
    gap = round(sua - bmk, 1)
    rows_bench.append({
        "Pilar": p.split(" ", 1)[1],
        "Sua empresa (%)": sua,
        "Benchmark setor (%)": bmk,
        "Gap": gap
    })

df_benchmark = pd.DataFrame(rows_bench)

df_benchmark_display = df_benchmark.copy()
df_benchmark_display["Sua empresa (%)"] = df_benchmark_display["Sua empresa (%)"].apply(lambda x: f"{x:.1f}%")
df_benchmark_display["Benchmark setor (%)"] = df_benchmark_display["Benchmark setor (%)"].apply(lambda x: f"{x:.0f}%")
df_benchmark_display["Gap"] = df_benchmark_display["Gap"].apply(lambda x: f"+{x:.1f}" if x >= 0 else f"{x:.1f}")

st.dataframe(
    df_benchmark_display,
    use_container_width=True,
    hide_index=True
)

# Radar Chart
st.markdown(" 🕸️ Radar de Maturidade vs. Benchmark do Setor")
pilares_nomes = [p.split(" ", 1)[1] for p in scores.keys()]
valores_empresa = list(scores.values())
valores_benchmark = [benchmark[p] for p in scores.keys()]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=valores_empresa + [valores_empresa[0]],
    theta=pilares_nomes + [pilares_nomes[0]],
    fill='toself',
    name='Sua Empresa',
    line_color='#1f77b4',
    fillcolor='rgba(31,119,180,0.2)'
))
fig.add_trace(go.Scatterpolar(
    r=valores_benchmark + [valores_benchmark[0]],
    theta=pilares_nomes + [pilares_nomes[0]],
    fill='toself',
    name=f'Benchmark (setor)',
    line_color='#ff7f0e',
    fillcolor='rgba(255,127,14,0.1)',
    line_dash='dash'
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    height=420,
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig, use_container_width=True)

# COSO Analysis
st.markdown(" 🏗️ Análise COSO — Componente Mais Crítico")
coso_scores = {}
for pilar, info in perguntas.items():
    comp = info["coso_componente"]
    coso_scores.setdefault(comp, []).append(scores.get(pilar, 0))

coso_medias = {k: sum(v)/len(v) for k, v in coso_scores.items()}
coso_critico = min(coso_medias, key=coso_medias.get)

for comp, media in sorted(coso_medias.items(), key=lambda x: x[1]):
    emoji = "🔴" if media < 30 else "🟠" if media < 55 else "🔵" if media < 75 else "🟢"
    st.markdown(
        f'<div class="coso-card"><strong>{emoji} {comp} — {media:.0f}%</strong><br>'
        f'<span style="font-size:0.85rem">{COSO_COMPONENTES.get(comp,"")}</span></div>',
        unsafe_allow_html=True
    )

# Top 3 Gaps + Ação sugerida
st.markdown(" 🚨 Top 3 Gaps Críticos — Onde agir primeiro e o que fazer?")

todos_gaps = []
for pilar, info in perguntas.items():
    for idx, item in enumerate(info["itens"], 1):
        nota_atual = obter_resposta(pilar, idx)
        todos_gaps.append({
            "pilar": pilar.split(" ", 1)[1],
            "pergunta": item["pergunta"],
            "nota": nota_atual,
            "nota_desc": item["notas"][nota_atual],
            "impacto": item["notas"][4],
            "acao": item.get("acao", "Definir e executar um plano de remediação para atingir o nível 4, com evidências e responsáveis.")
        })

top_gaps = sorted(todos_gaps, key=lambda x: x["nota"])[:3]
for i, gap in enumerate(top_gaps, 1):
    st.markdown(
        f'<div class="gap-card">'
        f'<strong>#{i} — {gap["pilar"]}</strong><br>'
        f'<em>{gap["pergunta"]}</em><br><br>'
        f'<strong>Situação atual (nota {gap["nota"]}):</strong> {gap["nota_desc"]}<br>'
        f'<strong>Estado ideal (nota 4):</strong> {gap["impacto"]}'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="action-card"><strong>✅ Ação sugerida:</strong> {gap["acao"]}</div>',
        unsafe_allow_html=True
    )

st.divider()
st.subheader("⬇️ Exportar Resultados")

df_detalhe = pd.DataFrame(respostas_detalhe)

df_resumo = pd.DataFrame([
    {
        "Pilar": p.split(" ", 1)[1],
        "Maturidade (%)": round(v, 1),
        "Benchmark Setor (%)": benchmark[p],
        "Delta vs Benchmark": round(v - benchmark[p], 1),
        "COSO Componente": perguntas[p]["coso_componente"]
    }
    for p, v in scores.items()
])

# incluir interpretação e ações no TXT
resumo_txt = f"""IFRS S1 & S2 — Readiness Assessment
Setor: {setor_label}
Data: {pd.Timestamp.now().strftime('%d/%m/%Y')}

ÍNDICE GERAL DE MATURIDADE: {media_geral:.1f}%
Benchmark do setor: {media_benchmark:.1f}%
Delta: {media_geral - media_benchmark:+.1f}%

{estagio}
{estagio_msg}

INTERPRETAÇÃO (executiva):
{interpretacao}

RESULTADO POR PILAR:
{chr(10).join([f'  {p.split(" ", 1)[1]}: {v:.1f}% (benchmark: {benchmark[p]}%) | gap: {v-benchmark[p]:+.1f}' for p, v in scores.items()])}

COMPONENTE COSO MAIS CRÍTICO: {coso_critico} ({coso_medias[coso_critico]:.0f}%)

TOP 3 GAPS CRÍTICOS (com ação sugerida):
{chr(10).join([f'  #{i+1} [{g["pilar"]}] Nota {g["nota"]} — {g["pergunta"]} | Ação: {g["acao"]}' for i, g in enumerate(top_gaps)])}

---
Framework: IFRS S1 & S2 (ISSB) + TCFD + COSO | Resolução CVM 193/2023
"""

col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    st.download_button(
        "📥 Resumo por Pilar (CSV)",
        data=df_resumo.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="ifrs_assessment_resumo.csv",
        mime="text/csv"
    )
with col_e2:
    st.download_button(
        "📥 Respostas Detalhadas (CSV)",
        data=df_detalhe.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="ifrs_assessment_detalhes.csv",
        mime="text/csv"
    )
with col_e3:
    st.download_button(
        "📄 Relatório Executivo (TXT)",
        data=resumo_txt.encode("utf-8"),
        file_name="relatorio_ifrs_assessment.txt",
        mime="text/plain"
    )

st.markdown("---")
st.markdown(
    "<div style='text-align:center;'>© 2026 Cristiane Vaz | IFRS S1/S2 Readiness Tool | "
    "<a href='https://www.linkedin.com/in/cristianevaz/' target='_blank'>LinkedIn</a></div>",
    unsafe_allow_html=True
)
st.caption("Framework baseado em IFRS S1, IFRS S2 (ISSB), TCFD e COSO | Resolução CVM 193/2023 | Desenvolvido para profissionais de Riscos, Controles e Contabilidade.")
