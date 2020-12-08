FROM python

COPY tests /tests
COPY requirements /requirements

RUN pip install -r /requirements

COPY wait_for_myapp.sh /wait_for_myapp.sh

ENTRYPOINT ["/wait_for_myapp.sh", "pytest"]
CMD ["-n", "auto", "--alluredir=/allure_dir", "/tests"]
