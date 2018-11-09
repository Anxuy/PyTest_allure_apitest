# -*- coding:utf-8 -*-
import os
import sys

import allure
import pytest
import yaml

from Common import init

# 读取测试用例
from Common.TestAndCheck import api_send_check
from config import ConfRelevance

PATH = os.path.split(os.path.realpath(__file__))[0]
with open(PATH+"/project.yaml", 'r', encoding="utf-8") as load_f:
    project_dict = yaml.load(load_f)

rel = ConfRelevance.ConfRelevance(PATH+"/relevance.ini")
relevance = rel.get_relevance_conf()


@allure.feature(project_dict["testinfo"]["title"])  # feature定义功能
class TestAddProject:
    def setup(self):
        global relevance
        relevance = init.ini_request(project_dict, relevance)

    # @pytest.mark.skipif(sys.version_info < (3, 6))  # 跳过条件
    @pytest.mark.parametrize("case_data", project_dict["test_case"])
    @allure.story("添加项目")
    @allure.issue("http://www.baidu.com")  # bug地址
    @allure.testcase("http://www.testlink.com")  # 用例连接地址
    def test_add_project(self, case_data):
        """
        添加项目测试  # 第一条用例描述
        :param case_data: 参数化用例的形参
        :return:
        """
        global relevance
        # 参数化修改test_add_project 注释
        for k, v in enumerate(project_dict["test_case"]): # 遍历用例文件中所有用例的索引和值
            try:
                if case_data == v:
                    # 修改方法的__doc__在下一次调用时生效，此为展示在报告中的用例描述
                    TestAddProject.test_add_project.__doc__ = project_dict["test_case"][k+1]["info"]
            except IndexError:
                pass
        # 发送测试请求
        relevance = api_send_check(case_data, project_dict, relevance)


if __name__ == "__main__":
    pytest.main()
