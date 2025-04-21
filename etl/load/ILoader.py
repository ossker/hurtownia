from abc import ABC, abstractmethod

import pandas as pd


class ILoader(ABC):
    @abstractmethod
    def load(self, data: dict[str, pd.DataFrame] = None) -> None:
        pass
