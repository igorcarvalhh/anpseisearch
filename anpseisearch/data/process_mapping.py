class ProcessMapping:
    IDS = {
        "Aquisição de Bens e Serviços: Licitação": 101,
        "Convênio de Pesquisa": 102,
    }

    @classmethod
    def get(cls, name: str) -> str:
        return cls.IDS.get(name, "")