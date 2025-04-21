from injector import Binder

from etl_implementation.ETLPipeline import ETLPipeline
from etl_implementation.StopienEnum import StopienEnum
from etl_implementation.extract import *
from etl_implementation.transform import *
from etl_implementation.load import *


class ETLModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ETLPipeline, ETLPipeline)

        binder.install(ExtractorModule())
        binder.install(TransformerModule())
        binder.install(LoaderModule())
