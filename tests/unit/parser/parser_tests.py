import unittest
import os
from capmonster_python import ImageToTextTask
from base_crawler import helper
from tests import test_helper
from parser import parser
from static import static
from base_crawler.helper import body_to_soup
class ParserTests(unittest.TestCase):

    def test_is_valid_input_return_true(self):
        valid_input_date = {
            "date": "2021-10-05"
        }

        self.assertTrue(parser.is_valid_input(valid_input_date))
    
    def test_is_valid_input_return_false(self):
        invalid_inputs = [
            {"aaaaa":"05/10/2021"},
            {"date":"05/10/2021"},
            {"date":None},
            {"dadawf":"2021-10-05"}
        ]

        for invalid_input in invalid_inputs:
            self.assertFalse(parser.is_valid_input(invalid_input))

    def test_get_search_return_valid_form_acordao(self):
        input_date = {
            "date": "2021-10-05"
        }
        expect_formdata = {
            "numDocsPagina": "50",
            "tipo_visualizacao": "",
            "p": "false",
            "data": "@DTPB >= 20211005 E @DTPB <= 20211005",
            "operador":"e",
            "l": "50",
            "i": "1",
            "b":"ACOR",
            "filtroPorNota":""
        }
        self.assertDictEqual(expect_formdata, parser.get_search_form(input_date,"1","ACORDAO"))

    def test_get_search_return_valid_form_acordao(self):
        input_date = {
            "date": "2021-10-05"
        }
        expect_formdata = {
            "numDocsPagina": "50",
            "tipo_visualizacao": "",
            "p": "false",
            "data": "@DTPB >= 20211005 E @DTPB <= 20211005",
            "operador":"e",
            "l": "50",
            "i": "1",
            "b":"DTXT",
            "filtroPorMinistro":""
        }
        self.assertDictEqual(expect_formdata, parser.get_search_form(input_date,"1","DESPACHO"))

    def test_get_search_form_return_empty_form_value(self):
        value_increment = None
        input_date = {
            "date": "2021-10-05"
        }
        self.assertDictEqual({}, parser.get_search_form(input_date,value_increment,"ACORDAO"))
    
    def test_is_valid_result_page_return_true(self):
        result_page = test_helper.read_test_file("result_page.html")
        self.assertTrue(parser.is_valid_result_page(result_page))
    
    # def test_transform_base64_in_image(self):
    #     result_page = test_helper.read_test_file("pdf_page.html")
    #     base = parser.transform_base64_in_image(result_page)
    #     imagem = open(f"/app/tests/files/tests_files/image.png", "wb")
    #     imagem.write(base)
    #     imagem.close()
    def test_captcha(self):
        result_page = test_helper.read_test_file("pdf_page.html")
        image = parser.transform_base64_in_image(result_page)
        capmonster = ImageToTextTask(os.environ.get("CAPTCHA_API_KEY"))
        #task_id = capmonster.create_task(image_path=image)
        #result = capmonster.join_task_result(task_id)
        #print(result)
    # def test_get_total_results_found(self):
    #     result_page = test_helper.read_test_file("result_page.html")
    #     total_results = 79
    #     self.assertEqual(parser.get_total_results_found(result_page,"ACORDAO"),total_results) 
    
    def test_parse_link_first_page(self):
        result_page = test_helper.read_test_file("first_url_page.html")
        expected_cited_jurisprudence = "LINK"
        #print(parser.parse_pdf_decision(expected_cited_jurisprudence,result_page))
    
    def test_find_multiple_links_to_full_content(self):
        result_page = test_helper.read_test_file("multiple_pdf.html")
        print(parser.verify_multiple_full_content_page(result_page))
        print(parser.find_multiple_links_to_full_content(result_page))

    def test_parse_repetitivo(self):
        result_page = test_helper.read_test_file("repetitivo_page.html")
        test_helper.save_test_file_as_json("repetitivos_result.json",parser.parse_outputs(result_page,"123"))

    def test_parse_date(self):  
        publication_date = "DJe 05/10/2021"
        correct_date = "2021-10-05"
        self.assertEqual(parser._parse_date(publication_date),correct_date)

    # def test_parse_acordao(self):
    #     result_page = test_helper.read_test_file("result_page_acordao.html")
    #     #outputs = parser.parse_outputs(result_page,"https://scon.stj.jus.br/")
    #     expected_outputs = test_helper.save_test_file_as_json("new_acordao",outputs)
    #     #self.assertEqual(expected_outputs, outputs)

    # def test_parse_legislative_reference(self):
    #     result_page = test_helper.read_test_file("result_reference.html")
    #     body_soup = body_to_soup(result_page)
    #     excepted_reference = ['LEG:FED SUM:****** ANO:****', '*****  SUM(STF)    SÚMULA DO SUPREMO TRIBUNAL FEDERAL', '        SUM:000718 SUM:000719', 'LEG:FED SUM:****** ANO:****', '*****  SUM(STJ)    SÚMULA DO SUPERIOR TRIBUNAL DE JUSTIÇA', '        SUM:000440', 'LEG:FED DEL:002848 ANO:1940', '*****  CP-40    CÓDIGO PENAL', '        ART:00033 PAR:00002 LET:C PAR:00003', 'LEG:FED LEI:011343 ANO:2006', '*****  LDR-06    LEI DE DROGAS', '        ART:00033 PAR:00004']
    #     self.assertListEqual(excepted_reference,parser._parse_legislative_reference(body_soup))

    # def test_parse_cited_jurisprudence(self):
    #     result_page = test_helper.read_test_file("result_reference.html")
    #     body_soup = body_to_soup(result_page)
    #     expected_cited_jurisprudence = "(CIRCUNSTÂNCIAS SUBJETIVAS E OBJETIVAS FAVORÁVEIS - REGIME ABERTO ESUBSTITUIÇÃO - CABIMENTO)   STJ - HC 412002-SP"
    #     self.assertEqual(expected_cited_jurisprudence,parser._parse_cited_jurisprudence(body_soup))

    # def test_parse_outputs_acordao(self):
    #     result_page = test_helper.read_test_file("result_page.html")
    #     outputs = parser.parse_outputs(result_page,static.FIRST_URL)
    #     expected_outputs_acordao = test_helper.read_test_file_as_json("expected_output_acordao")
    #     self.assertEqual(expected_outputs_acordao, outputs)
    
    # def test_parse_outputs_despacho(self):
    #     result_page = test_helper.read_test_file("result_despacho.html")
    #     outputs = parser.parse_outputs_despacho(result_page)
    #     expected_outputs = test_helper.read_test_file_as_json("expected_despacho_outputs")
    #     self.assertEqual(expected_outputs, outputs)

    # def test_parse_link_pdf_in_second_page(self):
    #     second_pdf_page = test_helper.read_test_file("second_pdf_page.html")
    #     except_url = "https://ww2.stj.jus.br/websecstj/cgi/revista/REJ.cgi/MON?seq=139310472&tipo=0&nreg=202103252444&SeqCgrmaSessao=&CodOrgaoJgdr=&dt=20211108&formato=PDF&salvar=false"
    #     self.assertEqual(except_url,parser.get_url_pdf_in_second_page(second_pdf_page))
    
    # def test_create_file_name(self):
    #     outputs = test_helper.read_test_file_as_json("expected_output_acordao")
    #     expected_file_names = [
    #         "STJ/2021-10-05/258f75d5042a9d7836210cc289ea8310.pdf",
    #         "STJ/2021-10-05/d527e5e48b7f2b9e33f2f4a54ff3a29f.pdf",
    #         "STJ/2021-10-05/f3402d8d2e1db0b16f607236c17a0ddc.pdf",
    #         "STJ/2021-10-05/3060c63142e3dabcae0f599537dbdfe7.pdf",
    #         "STJ/2021-10-05/c32e0432c18e6040814e1bd2540b5ad1.pdf",
    #         "STJ/2021-10-05/d540c2f255305190b7d05c3187ca0683.pdf",
    #         "STJ/2021-10-05/fe32eee639f4ae467e990308df0bb763.pdf",
    #         "STJ/2021-10-05/8d30cb8a22a4215d533d949a5304e151.pdf",
    #         "STJ/2021-10-05/59a429b229db3323a7a1b83579e550e3.pdf",
    #         "STJ/2021-10-05/d6cabd7d51ba25224764d1906a54e659.pdf"
    #         ]
    #     file_names = []
    #     for output in outputs:
    #         file_name = parser.create_file_name(output)
    #         file_names.append(file_name)
    #     self.assertListEqual(expected_file_names, file_names)

    # def test_clean_output(self):
    #     outputs = test_helper.read_test_file_as_json("expected_output_acordao")
    #     cleaned_outputs=[]
    #     for output in outputs:
    #         parser.clean_output(output)
    #         cleaned_outputs.append(output)
    #     expected_cleaned_outputs = test_helper.read_test_file_as_json("expected_cleaned_outputs")
    #     self.assertEqual(expected_cleaned_outputs, cleaned_outputs)
    
    # def test_set_parameters_to_file(self):
    #     outputs = test_helper.read_test_file_as_json("expected_output_acordao")
    #     outputs_with_parameters = []
    #     for output in outputs:
    #         parser.set_file_parameters_to_file(output, parser.create_file_name(output))
    #         outputs_with_parameters.append(output)
    #     expected_outputs_with_parameters = test_helper.read_test_file_as_json("expected_outputs_with_parameters")
    #     self.assertListEqual(expected_outputs_with_parameters, outputs_with_parameters)

if __name__ == "__main__":
    unittest.main()