#!/usr/bin/env bash
docker run --rm						\
--name test_system					\
--network myapp						\
-v "$PWD"/allure_dir:/allure_dir	\
test_system -n auto --alluredir=/allure_dir --clean-alluredir /tests