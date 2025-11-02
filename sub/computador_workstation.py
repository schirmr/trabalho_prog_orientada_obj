from modelos import Computador, PlacaDeVideo, Monitor

class ComputadorWorkstation(Computador):
    ## Construtor com validações específicas para workstation
    def __init__(self, tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario, placa_de_video: PlacaDeVideo, monitor: Monitor):
        super().__init__(tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario)
        if not placa_de_video:
            raise ValueError("Workstation deve ter uma placa de vídeo profissional.")
        if not getattr(placa_de_video, 'profissional', False):
            raise ValueError("Workstation requer uma GPU profissional (ex: Quadro, Radeon Pro).")
        if not isinstance(monitor, Monitor):
            raise ValueError("Workstation deve ter um monitor (pode ser não-gamer).")

        self.placa_de_video = placa_de_video
        self.monitor = monitor

    def get_info_completa(self):
        info_base = super().get_info_base()
        return (f"[Workstation]\n{info_base}\n  {self.placa_de_video.get_info()}\n  {self.monitor.get_info()}")

    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict(),
            'monitor': self.monitor.to_dict()
        })
        return data
