from abc import ABC, abstractmethod

import pandas as pd


class ITransformer(ABC):
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> dict:
        pass