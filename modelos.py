## CLASSES DOS COMPONENTES DE HARDWARE
class Processador:
    ## Construtor com validações específicas para processadores Intel e AMD
    def __init__(self, modelo, fabricante='AMD', nucleos=None, ultima_geracao=False, perf_cores=0, eff_cores=0, hyperthread=False):
        if not modelo:
            raise ValueError("Processador: Modelo é obrigatório.")
        if fabricante not in ('AMD', 'INTEL'):
            raise ValueError("Processador: Fabricante deve ser 'AMD' ou 'INTEL'.")
        
        self.modelo = modelo
        self.fabricante = fabricante
        self.ultima_geracao = bool(ultima_geracao)

        perf = int(perf_cores) if perf_cores is not None else 0
        eff = int(eff_cores) if eff_cores is not None else 0

        self.perf_cores = max(0, perf)
        self.eff_cores = max(0, eff)

        if fabricante == 'INTEL' and self.ultima_geracao:
            if (self.perf_cores + self.eff_cores) <= 0:
                raise ValueError("Processador Intel (última geração): é necessário informar núcleos de performance e/ou eficiência.")
            self.nucleos = self.perf_cores + self.eff_cores
        else:
            if nucleos is None:
                raise ValueError("Processador: número de núcleos é obrigatório quando não se usa o formato E/P.")
            n = int(nucleos)
            if n <= 0:
                raise ValueError("Processador: número de núcleos deve ser maior que zero.")
            self.nucleos = n
        # Hyperthread/SMT: dobra o número de threads lógicas quando ativo
        self.hyperthread = bool(hyperthread)

        if self.hyperthread:
            self.threads = int(self.nucleos) * 2
        else:
            self.threads = int(self.nucleos)
    ## Métodos para exibir informações e converter para dicionário
    def get_info(self):
        if self.fabricante == 'INTEL' and self.ultima_geracao:
            base = f"CPU: {self.modelo} (Intel, {self.perf_cores} P + {self.eff_cores} E = {self.nucleos} núcleos)"
        else:
            base = f"CPU: {self.modelo} ({self.nucleos} núcleos, {self.fabricante})"

        if self.hyperthread and not self.ultima_geracao:
            return f"{base} - Hyperthread/SMT ativo ({self.threads} threads lógicas)"
        return base
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        data = {
            'modelo': self.modelo,
            'fabricante': self.fabricante,
            'ultima_geracao': self.ultima_geracao,
            'nucleos': self.nucleos,
            'hyperthread': self.hyperthread,
        }
        if self.fabricante == 'INTEL' and self.ultima_geracao:
            data.update({'perf_cores': self.perf_cores, 'eff_cores': self.eff_cores})
        return data
## CLASSE DE UM COMPONENTE ADICIONAL
class PlacaDeVideo:
    def __init__(self, modelo, memoria_vram, fabricante='NVIDIA', profissional=False):
        if fabricante not in ('AMD', 'NVIDIA', 'INTEL'):
            raise ValueError("Placa de Vídeo: fabricante deve ser 'AMD', 'NVIDIA' ou 'INTEL'.")
        if not modelo or memoria_vram <= 0:
            raise ValueError("Placa de Vídeo: Modelo e VRAM são obrigatórios.")
        if profissional and fabricante not in ('AMD', 'NVIDIA'):
            raise ValueError("Placa de Vídeo Profissional: apenas AMD ou NVIDIA são suportadas como profissionais.")

        self.modelo = modelo
        self.memoria_vram = int(memoria_vram)
        self.fabricante = fabricante
        self.profissional = bool(profissional)

    def get_info(self):
        tag = ' (Profissional)' if self.profissional else ''
        return f"GPU: {self.modelo} ({self.memoria_vram}GB VRAM, {self.fabricante}){tag}"

    def to_dict(self):
        return {'modelo': self.modelo, 'memoria_vram': self.memoria_vram, 'fabricante': self.fabricante, 'profissional': self.profissional}
## CLASSE DE MEMÓRIA RAM
class MemoriaRAM:
    ## Construtor com validações para memória RAM
    def __init__(self, capacidade_gb, velocidade_mhz, num_modulos=1):
        if capacidade_gb <= 0 or velocidade_mhz <= 0:
            raise ValueError("Memória RAM: Capacidade e velocidade são obrigatórias.")
        if num_modulos not in (1, 2, 4, 8):
            raise ValueError("Memória RAM: número de módulos deve ser 1, 2, 4 ou 8.")

        self.capacidade_gb = int(capacidade_gb)
        self.velocidade_mhz = int(velocidade_mhz)
        self.num_modulos = int(num_modulos)

        if self.capacidade_gb % self.num_modulos != 0:
            raise ValueError("Memória RAM: a capacidade total deve ser divisível pelo número de módulos (tamanho por módulo inteiro).")

        self.tamanho_por_modulo = self.capacidade_gb // self.num_modulos
    ## Métodos para exibir informações e converter para dicionário
    def get_info(self):
        return f"RAM: {self.capacidade_gb}GB ({self.num_modulos}x{self.tamanho_por_modulo}GB) {self.velocidade_mhz}MHz"
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        return {
            'capacidade_gb': self.capacidade_gb,
            'velocidade_mhz': self.velocidade_mhz,
            'num_modulos': self.num_modulos,
            'tamanho_por_modulo': self.tamanho_por_modulo
        }

## CLASSE DE MONITOR
class Monitor:
    ## Construtor com validações para monitor
    def __init__(self, marca, modelo='Padrao', tamanho_polegadas=0, frequencia_hz=60):
        if not marca:
            raise ValueError("Monitor: Marca é obrigatória")
        if not float(tamanho_polegadas) > 0:
            raise ValueError("Monitor: Tamanho em polegadas deve ser maior que zero.")

        self.marca = marca
        self.modelo = modelo or 'Padrao'
        self.tamanho_polegadas = float(tamanho_polegadas)
        freq = int(frequencia_hz)
        if freq < 60:
            raise ValueError("Monitor: frequência deve ser de pelo menos 60Hz.")
        self.frequencia_hz = freq
    ## Métodos para exibir informações e converter para dicionário
    def get_info(self):
        return f"Monitor: {self.marca} {self.modelo} ({self.tamanho_polegadas}\", {self.frequencia_hz}Hz)"
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        return {
            'tipo': self.__class__.__name__,
            'marca': self.marca,
            'modelo': self.modelo,
            'tamanho_polegadas': self.tamanho_polegadas,
            'frequencia_hz': self.frequencia_hz
        }
## CLASSE DE MONITOR GAMER (HERANÇA)
class MonitorGamer(Monitor):
    ## Construtor com validações específicas para monitor gamer
    def __init__(self, marca, modelo, tamanho_polegadas, frequencia_hz):
        super().__init__(marca, modelo, tamanho_polegadas, frequencia_hz)

        if not int(self.frequencia_hz) >= 120:
            raise ValueError("Monitor Gamer: a frequência deve ser de no mínimo 120Hz.")

# CLASSES DE COMPUTADORES (PRINCIPAL COM HERANÇA E POLIMORFISMO)
## CLASSE PAI DE COMPUTADORES
class Computador:
    ## Construtor com validações básicas
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, capacidade_ssd_gb: int, tipo_ssd: str, hdd_secundario_gb: int = 0):
        if not tag_identificacao:
            raise ValueError("Tag de Identificação é obrigatória.")
        if not capacidade_ssd_gb or int(capacidade_ssd_gb) <= 0:
            raise ValueError("Capacidade do SSD é obrigatória e deve ser maior que zero.")
        if tipo_ssd not in ('SATA', 'NVMe'):
            raise ValueError("Tipo de SSD inválido. Deve ser 'SATA' ou 'NVMe'.")

        self.tag_identificacao = tag_identificacao
        self.processador = processador
        self.memoria_ram = memoria_ram
        self.capacidade_ssd_gb = int(capacidade_ssd_gb)
        self.tipo_ssd = tipo_ssd
        self.hdd_secundario_gb = int(hdd_secundario_gb) if hdd_secundario_gb else 0
    ## Métodos para exibir informações e converter para dicionário
    def get_info_base(self):
        base = f"Tag: {self.tag_identificacao}\n  {self.processador.get_info()}\n  {self.memoria_ram.get_info()}"
        base += f"\n  SSD: {self.capacidade_ssd_gb}GB ({self.tipo_ssd})"
        if self.hdd_secundario_gb and self.hdd_secundario_gb > 0:
            base += f"\n  HDD Secundário: {self.hdd_secundario_gb}GB"
        return base
    ## Método polimórfico para obter informações completas
    def get_info_completa(self):
        return f"[Computador Genérico]\n{self.get_info_base()}"
    ## Método para converter o objeto em um dicionário
    def to_dict_base(self):
        data = {
            'tipo': self.__class__.__name__,
            'tag_identificacao': self.tag_identificacao,
            'processador': self.processador.to_dict(),
            'memoria_ram': self.memoria_ram.to_dict(),
            'capacidade_ssd_gb': self.capacidade_ssd_gb,
            'tipo_ssd': self.tipo_ssd,
            'hdd_secundario_gb': self.hdd_secundario_gb
        }
        return data
    ## Método polimórfico para converter o objeto em um dicionário
    def to_dict(self):
        return self.to_dict_base()

## CLASSES FILHAS DE COMPUTADORES
class ComputadorOffice(Computador):
    ## Construtor com validações específicas para computador de escritório
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, capacidade_ssd_gb: int, tipo_ssd: str, hdd_secundario_gb: int, monitor: Monitor):
        super().__init__(tag_identificacao, processador, memoria_ram, capacidade_ssd_gb, tipo_ssd, hdd_secundario_gb)
        if not isinstance(monitor, Monitor):
            raise ValueError("PC Office deve ter um monitor simples (marca/polegadas).")
        self.monitor = monitor
    ## Métodos para exibir informações e converter para dicionário
    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC de Escritório]\n{info_base}\n  {self.monitor.get_info()}"
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        data = super().to_dict_base()
        data.update({'monitor': self.monitor.to_dict()})
        return data

## CLASSE FILHA QUE HERDA DE COMPUTADOR
class ComputadorGamer(Computador):
    ## Construtor com validações específicas para computador gamer
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, 
                 placa_de_video: PlacaDeVideo, potencia_fonte_w: int, monitor: MonitorGamer, capacidade_ssd_gb: int, tipo_ssd: str, hdd_secundario_gb: int = 0):
        super().__init__(tag_identificacao, processador, memoria_ram, capacidade_ssd_gb, tipo_ssd, hdd_secundario_gb)
        if not placa_de_video:
            raise ValueError("PC Gamer deve ter uma placa de vídeo dedicada.")
        if not potencia_fonte_w >= 500:
            raise ValueError("Fonte para PC Gamer deve ser de 500W ou mais.")
        if not isinstance(monitor, MonitorGamer):
            raise ValueError("PC Gamer deve ter um Monitor Gamer.")
            
        self.placa_de_video = placa_de_video
        self.potencia_fonte_w = int(potencia_fonte_w)
        self.monitor = monitor

    ## Métodos para exibir informações e converter para dicionário
    def get_info_completa(self):
        info_base = super().get_info_base()
        return (f"[PC Gamer]\n{info_base}\n  {self.placa_de_video.get_info()}"
                f"\n  {self.monitor.get_info()}\n  Fonte: {self.potencia_fonte_w}W")

    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict(),
            'potencia_fonte_w': self.potencia_fonte_w,
            'monitor': self.monitor.to_dict()
        })
        return data

## CLASSE FILHA QUE HERDA DE COMPUTADOR
class ComputadorIntermediario(Computador):
    ## Construtor com validações específicas para computador intermediário
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, placa_de_video: PlacaDeVideo, monitor: Monitor, capacidade_ssd_gb: int, tipo_ssd: str, hdd_secundario_gb: int = 0):
        super().__init__(tag_identificacao, processador, memoria_ram, capacidade_ssd_gb, tipo_ssd, hdd_secundario_gb)
        if not placa_de_video:
            raise ValueError("PC Intermediário deve ter uma placa de vídeo.")
        if not isinstance(monitor, Monitor):
            raise ValueError("PC Intermediário deve ter um monitor simples (marca/polegadas).")
        self.placa_de_video = placa_de_video
        self.monitor = monitor
    ## Métodos para exibir informações e converter para dicionário
    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC Intermediário]\n{info_base}\n  {self.placa_de_video.get_info()}\n  {self.monitor.get_info()}"
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict()
        })
        data.update({'monitor': self.monitor.to_dict()})
        return data


class ComputadorWorkstation(Computador):
    ## Construtor com validações específicas para workstation
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, placa_de_video: PlacaDeVideo, potencia_fonte_w: int, monitor: Monitor, capacidade_ssd_gb: int, tipo_ssd: str, hdd_secundario_gb: int = 0):
        super().__init__(tag_identificacao, processador, memoria_ram, capacidade_ssd_gb, tipo_ssd, hdd_secundario_gb)
        if not placa_de_video:
            raise ValueError("Workstation deve ter uma placa de vídeo profissional.")
        if not getattr(placa_de_video, 'profissional', False):
            raise ValueError("Workstation requer uma GPU profissional (ex: Quadro, Radeon Pro).")
        if potencia_fonte_w is None or int(potencia_fonte_w) < 600:
            raise ValueError("Fonte para Workstation deve ser de 600W ou mais.")
        if not isinstance(monitor, Monitor):
            raise ValueError("Workstation deve ter um monitor (pode ser não-gamer).")

        self.placa_de_video = placa_de_video
        self.potencia_fonte_w = int(potencia_fonte_w)
        self.monitor = monitor
    ## Métodos para exibir informações e converter para dicionário
    def get_info_completa(self):
        info_base = super().get_info_base()
        return (f"[Workstation]\n{info_base}\n  {self.placa_de_video.get_info()}\n  {self.monitor.get_info()}\n  Fonte: {self.potencia_fonte_w}W")
    ## Método para converter o objeto em um dicionário
    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict(),
            'potencia_fonte_w': self.potencia_fonte_w,
            'monitor': self.monitor.to_dict()
        })
        return data
