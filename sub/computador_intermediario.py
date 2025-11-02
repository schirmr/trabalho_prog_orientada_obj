from modelos import Computador, PlacaDeVideo, Monitor

class ComputadorIntermediario(Computador):
    ## Construtor com validações específicas para computador intermediário
    def __init__(self, tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario, placa_de_video: PlacaDeVideo, monitor: Monitor):
        super().__init__(tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario)
        if not placa_de_video:
            raise ValueError("PC Intermediário deve ter uma placa de vídeo.")
        if not isinstance(monitor, Monitor):
            raise ValueError("PC Intermediário deve ter um monitor simples (marca/polegadas).")
        self.placa_de_video = placa_de_video
        self.monitor = monitor

    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC Intermediário]\n{info_base}\n  {self.placa_de_video.get_info()}\n  {self.monitor.get_info()}"

    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict()
        })
        data.update({'monitor': self.monitor.to_dict()})
        return data
