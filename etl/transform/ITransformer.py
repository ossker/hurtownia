from abc import ABC, abstractmethod

import pandas as pd


class ITransformer(ABC):
    @abstractmethod
    def transform(self, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        pass