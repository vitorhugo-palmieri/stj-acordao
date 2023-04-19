#FROM registry.gitlab.com/b252/base-crawler
#COPY --from=registry.gitlab.com/b252/base-crawler /app /app

FROM base-crawler
COPY --from=base-crawler /app /app

COPY spider.py /app/spiders/spider.py
COPY parser/ /app/parser/
COPY static/ /app/static/
COPY tests/ /app/tests/
COPY scripts/ /app/scripts/

#ENV SPIDER_NAME $SPIDER_NAME


WORKDIR /app

#ENTRYPOINT python run_crawler.py -name=$SPIDER_NAME
ENTRYPOINT ["python", "run_crawler.py", "-name=crawler-juris-stf-d-1"]


