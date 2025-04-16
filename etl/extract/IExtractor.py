from abc import ABC, abstractmethod

import pandas as pd


class IExtractor(ABC):
    @abstractmethod
    def extract(self) -> dict[str, pd.DataFrame]:
        pass
