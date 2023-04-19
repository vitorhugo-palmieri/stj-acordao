import scrapy
import os
from capmonster_python import ImageToTextTask
from base_crawler.helper import get_decisions_to_ignore
from scrapy.exceptions import CloseSpider
from base_crawler.spiders.base_spider import BaseSpider
import base_crawler.exceptions.spider_exceptions as spider_exceptions
from base_crawler.bucket.oci_bucket import OracleBucketManager
from queue import Queue
from static import static
from parser import parser




class Spider(BaseSpider):
    name = os.environ.get("SPIDER_NAME", "crawler-juris-stj-acordao-d-1")
    required_keys = [
        "relator",
        "tribunal",
        "tipoDecisao",
        "dataPublicacao",
        "nomeProcesso",
    ]
    id_fields = ["relator", "tribunal", "tipoDecisao", "dataPublicacao", "nomeProcesso"]
    custom_settings = {
        "DOWNLOAD_DELAY": 0.3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "ROBOTSTXT_OBEY": False,
        "STATS_CLASS": "base_crawler.stats_collector.MongoStatsCollector",
        "SPIDERMON_SPIDER_CLOSE_MONITORS": "base_crawler.monitors.SpiderCloseMonitorSuite",
        "SPIDERMON_DISCORD_WEBHOOK_URL": os.environ.get("DISCORD_WEBHOOK")
        or static.DISCORD_WEBHOOK_DEV,
    }
    if 'd-1' in name:
        custom_settings = {
        "DOWNLOAD_DELAY": 0.3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "ROBOTSTXT_OBEY": False,
        "STATS_CLASS": "base_crawler.stats_collector.MongoStatsCollector",
        "SPIDERMON_SPIDER_CLOSE_MONITORS": "base_crawler.monitors.SpiderCloseMonitorSuite",
        "SPIDERMON_DISCORD_WEBHOOK_URL": os.environ.get("DISCORD_WEBHOOK")
        or static.DISCORD_WEBHOOK_DEV,
                "ITEM_PIPELINES":{
                    "base_crawler.pipelines.item_prepare_pipeline.ItemPreparePipeline": 100,
                    "base_crawler.pipelines.schema_validation_pipeline.SchemaValidationPipeline": 200,
                    "base_crawler.pipelines.mongo_pipeline.MongoPipeline": 300,
                    "base_crawler.pipelines.transformer.transformer_pipeline.TransformerPipeline": 400,
                    #'base_crawler.pipelines.elastic_pipeline.ElasticPipeline': 500
                }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not parser.is_valid_input(kwargs["input"]):
            raise spider_exceptions.InvalidInput(kwargs["input"])
        print(f'Input = {self.input.get("date")}')
        self.input = kwargs["input"]
        self.bucket_manager = OracleBucketManager()
        self._current_request_errors = 0
        self.decisions_to_ignore = get_decisions_to_ignore(self.name, kwargs["input"])
        

    def start_requests(self):
        self.decisions = {}
        self.logger.info("START REQUESTS")
        self.crawler.stats.set_value("spider_name", self.name)
        self.crawler.stats.set_value("input", self.input)
        self.case_file_queues = {}
        yield scrapy.Request(
            url=static.FIRST_URL,
            callback=self._on_first_page,
            errback=self._on_request_error,
        )

    def _on_first_page(self, response):
        self.logger.info("ON FIRST PAGE")
        search_form_acordao = parser.get_search_form(self.input, "1", "ACORDAO")
        yield scrapy.FormRequest(
            url=f"{static.SEARCH_URL}{static.JUDGMENT_URL}",
            headers=static.HEADERS_SEARCH,
            method="POST",
            formdata=search_form_acordao,
            callback=self._on_result_page,
            errback=self._on_request_error,
        )

    def _on_result_page(self, response):
        atual_index = 1
        self.logger.info("ON RESULT PAGE")
        self.debug_response_file(response, file_name="on_result_page.html")

        if parser.is_valid_captcha_page(response.body):
            raise CloseSpider("captcha_not_resolved")

        total_results_judgment = parser.get_total_results_found(
            response.body, "ACORDAO"
        )
        total_results =  total_results_judgment
        expected_num_items = total_results_judgment - len(self.decisions_to_ignore)

        self.crawler.stats.set_value("expected_num_items", expected_num_items)
        self.crawler.stats.set_value("total_results", total_results_judgment, 0)
        self.logger.info(
            f"\n--------------------------INPUT INFO--------------------------\nINPUT = {self.input}\nTOTAL DOCUMENTOS = {total_results}\nTOTAL DOCUMENTOS JA CRAWLEADOS = {len(self.decisions_to_ignore)}\nTOTAL DE DOCUMENTOS RESTANTES = {expected_num_items}\n----------------------------------------------------------------"
        )

        if total_results_judgment == 0:
            raise CloseSpider("all_data_scraped")

        if expected_num_items == 0:
            raise CloseSpider("all_data_scraped")

        for index in range(
            atual_index, total_results_judgment + 1, static.QUANTITY_REGISTRY
        ):
            search_form_acordao = parser.get_search_form(
                self.input, str(index), "ACORDAO"
            )
            yield scrapy.FormRequest(
                url=f"{static.SEARCH_URL}{static.JUDGMENT_URL}",
                headers=static.HEADERS_SEARCH,
                method="POST",
                formdata=search_form_acordao,
                callback=self._on_download_output_files,
                errback=self._on_request_error,
                dont_filter=True,
            )

    def _on_download_output_files(self, response):
        self.logger.info("RESULTS ANOTHER PAGE")
        if parser.is_valid_captcha_page(response.body):
            raise CloseSpider("captcha_not_resolved")

        self.debug_response_file(response, file_name="on_result_another_page.html")
        outputs = parser.parse_outputs(response.body, static.ACORDAO_PDF, self.decisions_to_ignore, self.id_fields)
        for output in outputs:
            yield output

    

    def _on_uploaded_file(self, response, **cb_kwargs):
        self.logger.info("ON UPLOADED FILE")
        output = cb_kwargs["output"]
        parser.set_file_parameters_to_file(
            output, response.meta["file_name"], cb_kwargs["file_idx"]
        )
        parser.clean_url_pdf(output)
        if not self.case_file_queues[output["numeroProcesso"]].empty():
            self.case_file_queues[output["numeroProcesso"]].get_nowait()

        if self.case_file_queues[output["numeroProcesso"]].empty():
            yield output
    
    def _on_request_error(self, response):
        self.logger.info(f"REQUEST ERROR [{response}]")
        if self._current_request_errors < static.MAX_ERRORS_ATTEMPTS:
            self._current_request_errors += 1
            return self.start_requests()
        raise spider_exceptions.InvalidPage()
