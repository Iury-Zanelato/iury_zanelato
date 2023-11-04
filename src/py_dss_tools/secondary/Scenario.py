# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd
from py_dss_interface import DSS


from ..utils import Utils

from py_dss_tools.model.ModelData import ModelData
from py_dss_tools.results.PowerFlowResults import PowerFlowResults
from dataclasses import dataclass, field
from typing import Union, Optional

from py_dss_tools.algorithms.LoadAllocation.load_allocation import LoadAllocation
from py_dss_tools.dss_utils import DSSUtils
from py_dss_tools.visualization.VoltageProfile import VoltageProfile


@dataclass(kw_only=True)
class Scenario(DSSUtils):
    _name: str = field(default='scenario_' + Utils.generate_random_string(), init=True, repr=True)
    _dss_file: str = field(init=True, repr=True)
    _frequency_base: Union[int, float] = field(default=60, init=True)
    _dll: str = field(default=None, init=True)
    _results: PowerFlowResults = field(init=False, repr=False)
    _modeldata: ModelData = field(init=False, repr=False)

    def __post_init__(self):
        # Objects
        if self._dll:
            self._dss = DSS(self._dll)
        else:
            self._dss = DSS("C:\OpenDSS_rep\Version8\Source")
        self._dss.text(f"compile [{self._dss_file}]")
        self._name = Utils.remove_blank_spaces(self._name)
        self._results = PowerFlowResults(_dss=self._dss)

        # self.dss_utils = DSSUtils(self._dss)
        DSSUtils.__init__(self, self._dss)
        # ModelData.__init__(self, self._dss)

        self._model = ModelData(self._dss)


    def to_dict(self) -> dict:
        return self.__dict__

    def to_list(self) -> list:
        return list(self.__dict__)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        Utils.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def dss(self):
        return self._dss

    @property
    def model(self):
        return self._model

    @property
    def results(self):
        return self._results

    def allocate_load(self):
        load_allocation = LoadAllocation(self)
        load_allocation.run_load_allocation_kw(5000)
        print(load_allocation.get_status())

    def plot_profile(self):
        VoltageProfile(self).plot_profile()

