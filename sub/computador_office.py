from modelos import Computador, Processador, MemoriaRAM, Disco, Monitor

class ComputadorOffice(Computador):
    ## Construtor com validações específicas para computador de escritório
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, disco_principal: Disco, disco_secundario: Disco, monitor: Monitor):
        super().__init__(tag_identificacao, processador, memoria_ram, disco_principal, disco_secundario)
        if not getattr(processador, 'integrated_gpu', False):
            raise ValueError("PC Office requer um processador com gráficos integrados (iGPU).")
        if not isinstance(monitor, Monitor):
            raise ValueError("PC Office deve ter um monitor simples (marca/polegadas).")
        if not (memoria_ram.num_modulos == 1 or memoria_ram.num_modulos == 2):
            raise ValueError("PC Office deve ter 1 ou 2 módulos de memória RAM.")
        self.monitor = monitor

    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC de Escritório]\n{info_base}\n  {self.monitor.get_info()}"

    def to_dict(self):
        data = super().to_dict_base()
        data.update({'monitor': self.monitor.to_dict()})
        return data
