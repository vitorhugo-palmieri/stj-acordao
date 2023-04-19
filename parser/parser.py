import re
import base64


from base_crawler import helper
from base_crawler.helper import convert_date_from_br_to_iso
from base_crawler.helper import create_item_id
from base_crawler.helper import body_to_soup
from base_crawler.helper import remove_non_digit
from base_crawler.helper import validate_date_format
from static.static import PDF_URL


_re_found_results_acordao = re.compile(r"(\d+.\d+|\d+) acórdãos encontrados")
_re_found_results_monocratic_decisions = re.compile(r"(\d+.\d+|\d+) decisões")
_re_find_date = re.compile(r"(\d{2}/\d{2}/\d{4})")
_re_find_only_number = re.compile(r"([0-9]+)")
_re_replace_rapporteur = re.compile(r"\(\d+\)")


def is_valid_input(input_data):
    valid_input_conditions = [
        "date" in input_data,
        validate_date_format(input_data.get("date", "")),
    ]
    return all(valid_input_conditions)


def get_search_form(input_data, value_increment, type_decision):
    date = input_data["date"].replace("-", "")
    if date is None or value_increment is None:
        return {}

    form_data = {
        "numDocsPagina": "50",
        "tipo_visualizacao": "",
        "processo": "",
        "p": "false",
        "data": f"@DTPB >= {date} E @DTPB <= {date}",
        "operador": "e",
        "l": "50",
        "i": value_increment,
        "b": "ACOR",
        "filtroPorNota": "",
    }

    return form_data


def transform_base64_in_image(body):
    body_soup = body_to_soup(body)
    try:
        img_tag = body_soup.find("img", attrs={"alt": "Red dot"}).get("src")
        _base64 = img_tag.split("base64,")[1]
        #print(f"BASE64 = {_base64}")
        # image = base64.b64decode((_base64))
        # img_file = open("image.jpeg", "wb")
        # img_file.write(image)
        # img_file.close()
        return _base64
    except:
        return ""


def is_valid_result_page(body):
    try:
        body_soup = body_to_soup(body)
        return body_soup.find("div", id="infopesquisa") is not None
    except:
        return False


def _find_total_results(body_soup, rgx):
    results = body_soup.find("div", class_="clsCriterioPesquisa").get_text()
    result = rgx.search(results).group(1).strip()
    return result


def get_total_results_found(body, type_decision):
    try:
        body_soup = body_to_soup(body)
        if type_decision == "ACORDAO":
            result = _find_total_results(body_soup, _re_found_results_acordao)
        else:
            result_float = _find_total_results(
                body_soup, _re_found_results_monocratic_decisions
            )
            result = result_float.replace(".", "")
        return int(result)
    except:
        return 0


def _parse_rapporteur(document):
    try:
        rapporteur = _find_next_text_element(document, r"Relator").strip()
        removed_ministro_rapporteur = rapporteur.replace("Ministro", "")
        rapporteur_formated = _re_replace_rapporteur.sub(
            "", removed_ministro_rapporteur
        )
        return rapporteur_formated
    except:
        rapporteur = _find_next_text_element(document, r"Relator").strip()


def _parse_organ_judgmental(document):
    return _find_next_text_element(document, "Órgão Julgador").strip()


def _parse_judgment(document):
    return _find_next_text_element(document, "Acórdão").strip()


def _parse_summary(document):
    return _find_next_text_element(document, "Ementa").strip()


def _parse_process(document):
    return _find_next_text_element(document, "Processo").strip()


def _parse_decision(document):
    return _find_next_text_element(document, "Decis").strip()


def _parse_publication_date(document):
    publication_date = _find_next_text_element(document, "Data da Publicação/Fonte")
    return _parse_date(publication_date).strip()


def _parse_judgment_date(document):
    judgmment_date = _find_next_text_element(document, "Data do Julgamento")
    return _parse_date(judgmment_date).strip()


def parse_pdf_decision(pdf_url, body):
    # try:
    body_soup = body_to_soup(body)
    tag_a = (
        body_soup.find("ul", class_="arvore_documentos")
        .find("ul")
        .find("a")
        .get("href")
    )
    content_href = tag_a.split("('")[1].strip("')")
    return build_pdf_decision(pdf_url, content_href)
    # return tag_a


# except:
#     return ""


def build_pdf_decision(pdf_url, content_href):
    try:
        url = "{pdf_url}{href}"
        url_format = url.format(pdf_url=pdf_url, href=content_href)
        return url_format
    except:
        return ""


def get_process_name_to_pdf(body):
    try:
        body_soup = body_to_soup(body)
        tag_a = (
            body_soup.find("ul", class_="arvore_documentos")
            .find("b")
            .find("a")
            .get_text()
        )
        content_a = tag_a.split("(")[0]
        return " ".join(content_a.split())
    except:
        return None


def _parse_date(date):
    try:
        date_string = _re_find_date.search(date).group(1).strip()
        return convert_date_from_br_to_iso(date_string).strip()
    except:
        return ""


def _find_case_element(body_soup, text):
    try:
        div_element = body_soup.find(
            "div", class_="docTitulo", text=re.compile(rf"{text}")
        )
        return div_element.find_next_sibling("div", class_="docTexto").contents
    except:
        return ""


def _find_next_text_element(body_soup, element_label):
    try:
        div_element = body_soup.find(
            "div", class_="docTitulo", text=re.compile(rf"{element_label}")
        )
        return (
            div_element.find_next_sibling("div", class_="docTexto").get_text().strip()
        )
    except:
        return ""


def _find_addition_information(document, text_to_find):
    div_element = document.find_all("div", class_="docTitulo")
    for element in div_element:
        find_element = re.findall(rf"{text_to_find}", element.get_text())
        if len(find_element) != 0:
            text = element.find_next_sibling("div", class_="docTexto")
    return text


def _parse_notes(document):
    try:
        return _find_addition_information(document, "Notas").get_text().strip()
    except:
        return ""


def _parse_info_complementary_to_summary(document):
    try:
        info_complementary_to_summary = []
        div_texto = (
            _find_addition_information(document, "Informações").find("p").contents
        )
        for line in div_texto:
            if line.get_text() != "" and line.get_text() != "\n":
                info_complementary_to_summary.append(line.get_text().strip())
        return info_complementary_to_summary
    except:
        return []


def _parse_legislative_reference(document):
    legislative_reference = []
    try:
        div_texto = (
            _find_addition_information(document, "Referência").find("pre").contents
        )
        for line in div_texto:
            string = "".join(x for x in line if x not in "<br/>")
            if string != "":
                legislative_reference.append(string)
        return legislative_reference
    except:
        return legislative_reference


def _parse_cited_jurisprudence(document):
    try:
        div_texto = _find_addition_information(
            document, "Jurisprudência\s+Citada"
        ).get_text()
        text = re.sub(r"\s+", " ", div_texto)
        return text
    except:
        return ""


def _parse_legal_these(document):
    try:
        return _find_addition_information(document, "Tese").get_text().strip()
    except:
        return ""


def _get_in_banner_text(body_soup, tag_html):
    try:
        return (
            body_soup.find("div", class_="bannerTexto")
            .find(f"{tag_html}")
            .get_text()
            .strip()
        )
    except:
        return ""


def _findAll_documents(body_soup):
    return body_soup.findAll("div", class_="documento")


def _get_element_to_full_content(body_soup):
    return body_soup.find(
        "a", attrs={"title": re.compile(r"Exibir o inteiro teor do acórdão.")}
    ).get("href")


def _clean_element_to_only_string(full_content):
    return full_content.split("_teor('/")[1].replace("'", "").replace(")", "")


def _find_pdf_url(body_soup, url):
    try:
        full_content = _get_element_to_full_content(body_soup)
        full_content_formatted = _clean_element_to_only_string(full_content)
        url_full_content = f"{url}{full_content_formatted}"
        return url_full_content
    except:
        return None


def get_url_pdf_in_second_page(body):
    try:
        body_soup = body_to_soup(body)
        iframe_src = body_soup.find("iframe", id="idFrameDocumento").get("src")
        return iframe_src.strip()
    except:
        return ""


def _content_decision(decision):
    return decision.split(r"DECISÃO" if "DECISÃO" in decision else "DESPACHO")[0]


def _parse_procedural_class(body_soup):
    try:
        decision = _parse_decision(body_soup)
        content_decision = _content_decision(decision)
        parse_procedural_class = content_decision.split("Nº")[0]
        return parse_procedural_class.strip()
    except:
        return ""


def _parse_number_appeal(text_line):
    try:
        number_appeal = _re_find_only_number.search(text_line).group(1)
        return number_appeal.strip()
    except:
        return ""


def find_multiple_links_to_full_content(body):
    # try:
    body_soup = body_to_soup(body)
    full_content_list = body_soup.find("div", id="listaInteiroTeor").find_all("a")
    a = []
    for text in full_content_list:
        text_a = text.get("href").replace("®", "&reg")
        if text_a in a:
            a.remove(text_a)
        a.append(text_a)
    return a
    # except:
    #     return ""


def verify_multiple_full_content_page(body):
    soup_body = body_to_soup(body)
    return (
        soup_body is not None
        and b"Classe" in body
        and soup_body.find("div", id="listaInteiroTeor") is not None
    )


def parse_outputs(body, url,decisions_to_ignore,id_fields):
    outputs = []
    last_element = -1
    second_element_in_process = 2
    first_element_in_process = 0
    # try:
    body_soup = body_to_soup(body)
    documents = _findAll_documents(body_soup)
    for document in documents:
        case_element = _find_case_element(document, "Processo")
        # ADD
        # fontePublicacao = ok, recurso = ok, infoComplementarEmenta, numeroTemaRepetitivo = OK
        # observacao = +/-, teseJuridica = ok
        item={
                "numeroProcesso": remove_non_digit(case_element[last_element].strip()),
                "nomeProcesso": case_element[first_element_in_process].strip(),
                "nomeExtenso": case_element[second_element_in_process].strip(),
                "numeroRecurso": _parse_number_appeal(
                    case_element[first_element_in_process]
                ),
                # "uf": case_element[first_element_in_process].split("/")[1].strip(),
                "relator": _parse_rapporteur(document),
                "teseJuridica": _parse_legal_these(document),
                "observacao": _parse_notes(document),
                "fontePublicacao": "",
                "infoComplementarEmenta": _parse_info_complementary_to_summary(
                    document
                ),
                "numeroTema": _get_in_banner_text(document, "a"),
                "recurso": _get_in_banner_text(document, "h4"),
                "orgaoJulgador": _parse_organ_judgmental(document),
                "dataPublicacao": _parse_publication_date(document),
                "dataJulgamento": _parse_judgment_date(document),
                "ementa": _parse_summary(document),
                "acordao": _parse_judgment(document),
                "referenciaLegislativa": _parse_legislative_reference(document),
                "jurisprudenciaCitada": _parse_cited_jurisprudence(document),
                "inteiroTeorArquivo": [
                    {"urlOriginal": _find_pdf_url(document, url), "extensao": "pdf"}
                ],
                "tipoDecisao": "Acórdão",
                "tribunal": "STJ",
            }
        
        item_id = create_item_id(item,id_fields)
        if item_id not in decisions_to_ignore:
            outputs.append(item)

    return outputs
    # except:
    #     return outputs


def create_file_name(output, file_idx):
    id_parameters = {
        "nomeProcesso": output["nomeProcesso"],
        "dataPublicacao": output["dataPublicacao"],
        "tribunal": output["tribunal"],
        "relator": output["relator"],
    }
    bucket_parameters = {
        "tribunal": output["tribunal"],
        "dataPublicacao": output["dataPublicacao"],
        "extensao": output["inteiroTeorArquivo"][file_idx]["extensao"],
    }
    return helper.create_file_name(id_parameters, bucket_parameters)


def clean_url_pdf(output):
    if "first_url_to_find_pdf" in output:
        del output["first_url_to_find_pdf"], output["second_url_to_find_pdf"]
        return output
    else:
        return output


def clean_output(output, file_idx):
    if output["inteiroTeorArquivo"][file_idx]["urlOriginal"] is None:
        del output["inteiroTeorArquivo"][file_idx]


def set_inteiro_teor(output, inteiro_teor):
    output["inteiroTeorArquivo"][0]["urlOriginal"] = inteiro_teor


def set_sencod_url(output, second_url):
    output["second_url_to_find_pdf"] = second_url


def set_file_parameters_to_file(output, file_name, file_idx):
    output["inteiroTeorArquivo"][file_idx]["nomeArquivo"] = file_name


def is_valid_process_page(body):
    return b"/processo/dj" in body


def is_valid_link_page(body):
    return b"/processo/julgamento/" in body


def is_valid_captcha_page(body):
    return b"[#BPROCESSO#]" in body
    
