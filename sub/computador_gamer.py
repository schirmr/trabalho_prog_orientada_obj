from modelos import Computador, PlacaDeVideo, MonitorGamer

class ComputadorGamer(Computador):
    ## Construtor com validações específicas para computador gamer
    def __init__(self, tag_identificacao, processador, memoria_ram,
                 disco_principal, disco_secundario, placa_de_video: PlacaDeVideo, monitor: MonitorGamer):
        super().__init__(tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario)
        if not placa_de_video:
            raise ValueError("PC Gamer deve ter uma placa de vídeo dedicada.")
        if not isinstance(monitor, MonitorGamer):
            raise ValueError("PC Gamer deve ter um Monitor Gamer.")

        self.placa_de_video = placa_de_video
        self.monitor = monitor

    def get_info_completa(self):
        info_base = super().get_info_base()
        return (f"[PC Gamer]\n{info_base}\n  {self.placa_de_video.get_info()}"
                f"\n  {self.monitor.get_info()}")

    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict(),
            'monitor': self.monitor.to_dict()
        })
        return data
