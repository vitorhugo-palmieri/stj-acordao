import unittest
from twisted.internet import defer
from freezegun import freeze_time

from tests import mock_data
from tests import test_helper
from spiders.spider import Spider
from tests.integration_test_fixture import IntegrationTestFixture


class SpiderTests(IntegrationTestFixture):
    maxDiff = None

    def setUp(self):
        self.setup_crawler()

    # def tearDown(self):
    #     self.tear_down_outputs_database("crawler-juris-stj-acordao")
    #     self.tear_down_errors_database("crawler-juris-stj-acordao")

    @defer.inlineCallbacks
    def _run_crawler(self, crawler):
        yield self.process.crawl(crawler["crawler"], input=crawler["input"])
        defer.returnValue(self._assert_crawler(crawler))

    def _create_crawler(self, crawler_class, **kwargs):
        finish_reason = kwargs.get("finish_reason")
        pipeline_error = kwargs.get("pipeline_error")
        assert_item_found = kwargs.get("assert_item_found")
        assert_multiple_items = kwargs.get("assert_multiple_items")
        crawler_input = kwargs.get("crawler_input")
        expected_item = kwargs.get("expected_item")
        lookup = kwargs.get("lookup")
        return {
            "crawler": self.process.create_crawler(crawler_class),
            "input": crawler_input,
            "finish_reason": finish_reason,
            "pipeline_error": pipeline_error,
            "assert_item_found": assert_item_found,
            "assert_multiple_items": assert_multiple_items,
            "expected_item": expected_item,
            "lookup": lookup,
        }

    def _create_crawlers(self):
        expected_items = test_helper.read_test_file_as_json("mongo_outputs")
        lookups = mock_data.GET_LOOKUPS
        list_date = [
        
            
            '2022-04-27' #{"date": "2022-04-27","recrawl":"True"}
        ]

        lista_input = []
        for data in list_date:
            lista_input.append(
                self._create_crawler(
                    Spider,
                    finish_reason="finished",
                    pipeline_error=False,
                    assert_multiple_items=True,
                    crawler_input={"date": f"{data}","recrawl":True},
                    expected_item={},
                    lookup={},
                )
            )
        return lista_input

    def _assert_crawler(self, crawler):
        # Create your assertions here
        if crawler["assert_item_found"]:
            self._assert_item_found(
                crawler["crawler"].spider.name,
                crawler["expected_item"],
                crawler["lookup"],
            )
        elif crawler["assert_multiple_items"]:
            self._assert_multiple_items_found(
                crawler["crawler"].spider.name,
                crawler["expected_item"],
                crawler["lookup"],
            )
        else:
            self._assert_item_not_found(
                crawler["crawler"].spider.name, crawler["lookup"]
            )
        if crawler["pipeline_error"]:
            self._assert_pipeline_error(
                crawler["crawler"].spider.name,
                crawler["crawler"].stats,
                crawler["lookup"],
            )

        self._assert_spider_finish_reason(
            crawler["crawler"].stats, crawler["finish_reason"]
        )

    @freeze_time(
        "2021-01-01 00:00:00", ignore=["logging", "scrapy", "requests", "twisted"]
    )
    def test_spiders(self):
        crawlers = self._create_crawlers()
        for crawler in crawlers:
            self._run_crawler(crawler)
        self.process.start()


if __name__ == "__main__":
    unittest.main()
