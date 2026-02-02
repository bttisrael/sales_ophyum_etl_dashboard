# 1. Instalação das bibliotecas necessárias
import pdfplumber
import pandas as pd
import re

def limpar_nome_cliente(nome_sujo):
    """Extrai apenas o nome, removendo TEL, CEL, DATA e ruídos de venda."""
    if not nome_sujo:
        return "VENDA A VISTA"
    padrao_parada = r'(?i)\s+TEL\s*:|\s+CEL\s*:|\s+DATA\s*:|\s+\d+VENDA\s*:|\s+\d{2}/\d{2}/\d{4}'
    partes = re.split(padrao_parada, str(nome_sujo))
    nome_limpo = partes[0].strip()
    nome_limpo = re.sub(r'^\d+VENDA:?\s*', '', nome_limpo)
    return nome_limpo if nome_limpo else "VENDA A VISTA"

def extrair_cor(descricao):
    """Detecta a cor predominante na descrição baseada em termos de moda."""
    desc = descricao.upper()
    cores_mapeadas = [
        "OFF WHITE", "AZUL MARINHO", "AZUL CLARO", "VERDE MILITAR", "VERDE MENTA",
        "VERDE NEON", "VERDE LIMA", "ROSA PINK", "ROSA CLARO", "CINZA MESCLA",
        "PRETO", "PRETA", "BRANCO", "BRANCA", "AZUL", "VERDE", "VERMELHO", "VERMELHA",
        "ROSA", "PINK", "BEGE", "NUDE", "CINZA", "GRAFITE", "CHUMBO", "MARROM",
        "BORDO", "VINHO", "LILAS", "ROXO", "CORAL", "LARANJA", "CARAMELO", "CARAMELHO",
        "AREIA", "MOSTARDA", "LIMA", "FUME", "PRATA", "DOURADO", "DOURADA", "CRU",
        "NATURAL", "ESTAMPADO", "ESTAMPADA", "LISTRADO", "LISTRADA", "COLORIDO"
    ]
    for cor in cores_mapeadas:
        if cor in desc:
            if cor == "CARAMELHO": return "CARAMELO"
            if cor in ["BRANCO", "BRANCA"]: return "BRANCO"
            if cor in ["PRETO", "PRETA"]: return "PRETO"
            if cor in ["VERMELHO", "VERMELHA"]: return "VERMELHO"
            return cor
    return "NÃO INFORMADO"

def categorizar_produto(descricao):
    desc = descricao.upper()

    # --- 1. PEÇAS ÚNICAS (Prioridade Máxima) ---
    if any(k in desc for k in ["VESTIDO", "SLIP DRESS", "CHEMISE", "CHAMISE","CHEMISIE","CHEMISIER","CHEMISSE","VSTIDO","VETSIDO"]):
        sub = "Premium/Noite" if any(k in desc for k in ["SEDA", "TULE", "LUREX", "PAETE"]) else "Casual/Dia"
        return "Peças Únicas", "Vestidos", sub

    if any(k in desc for k in ["MACACÃO", "MACACAO", "MACAÇAO", "JARDINEIRA", "MACAQUINHO"]):
        return "Peças Únicas", "Macacões", "Geral"

    # --- 2. BOTTOMWEAR (Antes de Blusas para evitar erro de substring em 'ALÇA') ---
    if any(k in desc for k in ["CALÇA", "CALCA", "LEGGING", "LEGGUNG", "JOGGER", "PANTALONA", "CIGARRETE", "MONTARIA", "WIDE", "LAPIZ","LEG"]):
        if "MASC" in desc: sub = "Masc Denim/Sarja"
        elif any(k in desc for k in ["LINHO", "COURO", "TRICOT"]): sub = "Fem Materiais Nobres"
        elif any(k in desc for k in ["LEGGING", "LEGGUNG","LEG"]): sub = "Fem Sport/Leg"
        else: sub = "Fem Jeans/Casual"
        return "Bottomwear", "Calças", sub

    if any(k in desc for k in ["SHORTS", "BERMUDA", "SHORT", "SHORTSAIA", "SHORTS-SAIA"]):
        sub = "Linho/Alfaiataria" if "LINHO" in desc else "Jeans/Casual"
        return "Bottomwear", "Shorts & Bermudas", sub

    if "SAIA" in desc:
        return "Bottomwear", "Saias", "Geral"

    # --- 6. INTIMATES, PRAIA E SLEEPWEAR (Restaurado com todos os seus termos originais) ---
    if any(k in desc for k in ["TRUNK","SOUTIEN","SITIA","SAMBA","PROTETOR","KIT MASC","CORSELET","CORPET","CALSINHA","CALÇINHA","SUTIA", "SUTIÃ", "SUTIEN", "SITIÃ", "CALCINHA", "CUECA", "FIO", "TANGA", "BOYSHORT", "BOYSHOR", "COMBINETE", "CAMISETE", "ANAGUA", "CINTA", "BOXER", "CALECON"]):
        sub = "Essentials/Kits" if "KIT" in desc else "Avulso"
        return "Intimates & Beachwear", "Moda Íntima", sub

    if any(k in desc for k in ["BIQUINI", "BIQUNI", "MAIO", "MAIÔ", "SUNGA", "SAIDA DE PRAIA", "SAIDADA DE PRAIA", "CANGA", "KIMONO", "KIMINO", "KOMONO", "CAFTAN"]):
        return "Intimates & Beachwear", "Moda Praia", "Beachwear"

    if any(k in desc for k in ["CAMIOLA","ROBE", "ROBÊ", "ROPÃO", "PIJAMA", "PIJMA", "JAMA", "SHORT DOLL", "CAMISOLA", "BABYDOLL"]):
        return "Intimates & Beachwear", "Sleepwear", "Nightwear"

    # --- 3. TOPWEAR: SOBRETUDOS E MALHAS ---
    if any(k in desc for k in ["TRENCH","SWEARTER","PALETO","CARDIGA","CARDIGÃ","CASAQUINHO","CASACO", "JAQUETA", "BLAZER", "BLASER", "BLZER", "CARDIGAN", "SUETER", "TRICOT", "PONCHO", "PARKA", "MOLETOM", "BOMBER", "COLETE", "CALETE", "CASO", "CASAQUETO", "CAPA", "SOBRE TUDO", "CORTA VENTO"]):
        if any(k in desc for k in ["BLAZER", "BLASER", "BLZER", "COLETE", "CALETE", "CASAQUETO"]): sub = "Blazers & Alfaiataria"
        elif any(k in desc for k in ["JAQUETA", "PARKA", "BOMBER", "CORTA VENTO"]): sub = "Jaquetas & Parkas"
        else: sub = "Tricot & Sueters"
        return "Topwear", "Sobretudos & Malhas", sub

    # --- 4. TOPWEAR: CAMISETAS, POLOS E CAMISAS ---
    if any(k in desc for k in ["CMISETA","CAMSIETA","CAMNISETA","T-SHIRT", "CAMISETA", "TSHIRT", "T-SHIORT", "TSHORT", "T-SIRT", "T=SHIRT"]):
        sub = "Masc Básica" if "MASC" in desc else ("Premium/Tricot" if "TRICO" in desc else "Fem Estampada")
        return "Topwear", "Camisetas", sub

    if any(k in desc for k in ["POLO", "MC CKJ"]):
        sub = "Masculina" if "MASC" in desc else "Feminina"
        return "Topwear", "Polos", sub

    if any(k in desc for k in ["CAMISE","CAMISA", "CAMISÃO", "COSTUME"]):
        sub = "Masc Social" if "MASC" in desc else "Fem Casual/Silk"
        return "Topwear", "Camisas", sub

    if any(k in desc for k in ["BODY", "BORY"]):
        return "Topwear", "Bodies", "Geral"

    # --- 5. TOPWEAR: BLUSAS & TOPS (Com proteção REGEX para palavras inteiras) ---
    keywords_blusa = ["TOMARA","RETA","REGTA","REGADA","REAGAT","CIGANINHA","BUSTO","BUSA","BLUSA", "REGATA", "TOP", "CROPPED", "BATA", "ALÇA", "TUNICA","BLUA","BLUS","BLUSÃO"]

    if any(re.search(r'\b' + re.escape(k) + r'\b', desc) for k in keywords_blusa):
        if "CROPPED" in desc or "TOMARA" in desc:
            sub = "Croppeds"
        elif "TUNICA" in desc or "REAGAT" in desc or "REGADA" in desc or "REGTA" in desc or "REGATA" in desc or "CIGANINHA" in desc:
            sub = "Regatas & Túnicas"  # <--- Este é o novo subgrupo
        else:
            sub = "Geral"

        return "Topwear", "Blusas & Tops", sub

    # --- 7. CALÇADOS E ACESSÓRIOS (Restaurado XARTEIRA, BONE, etc) ---
    if any(k in desc for k in ["TAMANCO","SANDÁLIA","RATEIRA","RASTEIRINHA","CHINELO", "TENIS", "TÊNIS", "BOTA", "SANDALIA", "RASTEIRA", "MULE", "MOCASSIM", "SCARPIN", "SAPATO", "PANTUFA", "COTURNO", "CHUKKA", "BIRKEN"]):
        return "Calçados & Acessórios", "Calçados", "Geral"

    if any(k in desc for k in ["XARTEIRA","PORTA CARTÕES","PORTA CARTÃO","MANGA", "LUVA","CHAPÉU","CACHICOL","BONE", "BONÉ", "BOLSA", "MOCHILA", "NECESSAIRE", "NECESSARIE", "CINTO", "LENÇO", "PASHMINA", "CACHECOL", "MANTA", "GOLA", "TOUCA", "TOCA", "MEIA", "VISEIRA", "GARRAFINHA", "CARTEIRA", "COLAR", "BRINCO", "PULSEIRA","BRACELETE", "SACOLA", "POLAINA"]):
        return "Calçados & Acessórios", "Acessórios", "Geral"

    return "Outros", "Não Categorizado", "Geral"

def extrair_base_completa(pdf_path):
    vendas = []
    current_cliente, current_data = None, None
    re_cliente = re.compile(r"CLIENTE:\s*(.*)")
    re_data = re.compile(r"DATA:\s*(\d{2}/\d{2}/\d{4})")
    # Captura: Código (8 dígitos), Descrição, Qtd e Valor Unitário
    re_produto = re.compile(r"^(\d{8})\s+(.*?)\s+(?:UND|PC|UN|PECA|PAR|PEÇA)\s+(\d+,\d{2}).*?R\$\s*([\d\.,]+)")

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue
            for line in text.split('\n'):
                m_cli = re_cliente.search(line)
                if m_cli: current_cliente = limpar_nome_cliente(m_cli.group(1))

                m_dat = re_data.search(line)
                if m_dat: current_data = m_dat.group(1).strip()

                m_prod = re_produto.search(line)
                if m_prod and current_cliente and current_data:
                    desc_raw = m_prod.group(2).strip()
                    fam, grp, sub = categorizar_produto(desc_raw)
                    vendas.append({
                        "Cliente": current_cliente,
                        "Data": current_data,
                        "Família": fam,
                        "Grupo": grp,
                        "Sub-Grupo": sub,
                        "Cor": extrair_cor(desc_raw),
                        "Código": m_prod.group(1),
                        "Descrição": desc_raw,
                        "Quantidade": m_prod.group(3),
                        "Unitário": m_prod.group(4)
                    })
    return pd.DataFrame(vendas)

# --- EXECUÇÃO ---
pdf_input = "vendas.pdf"
try:
    df_final = extrair_base_completa(pdf_input)
    if not df_final.empty:
        df_final.to_csv("base_vendas_limpa.csv", sep=';', index=False, encoding='utf-8-sig')
        print(f"Sucesso! {len(df_final)} registros processados.")
        print(df_final.head(15))
    else:
        print("Nenhum dado extraído.")
except Exception as e:
    print(f"Erro: {e}")