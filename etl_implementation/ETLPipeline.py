from injector import inject

from etl.extract import IExtractor
from etl.load import ILoader
from etl.transform import ITransformer


class ETLPipeline:
    @inject
    def __init__(self,
                 extractors: list[IExtractor],
                 transformers: list[ITransformer],
                 loaders: list[ILoader],
                 ) -> None:
        self._extractors = extractors
        self._transformers = transformers
        self._loaders = loaders

    def run(self) -> None:
        print(f"Running: {self.__class__.__name__}")
        for extractor, transformer, loader in zip(self._extractors, self._transformers, self._loaders):
            print(f"Running: {extractor.__class__.__name__}")
            data = extractor.extract()
            print(f"Running: {transformer.__class__.__name__}")
            data_transformed = transformer.transform(data)
            print(f"Running: {loader.__class__.__name__}")
            loader.load(data_transformed)
            print(f"Completed.")

        # TODO join all above

        print(f"Completed: {self.__class__.__name__}")