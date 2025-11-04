class Processador:
    ## Construtor com validações específicas para processadores Intel e AMD
    def __init__(self, modelo, fabricante, nucleos=None, ultima_geracao=False, perf_cores=0, eff_cores=0, hyperthread=False, integrated_gpu=False):
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
                raise ValueError("Processador: número de núcleos é obrigatório.")
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
        self.integrated_gpu = bool(integrated_gpu)
    ## Métodos para exibir informações e converter para dicionário
    def get_info(self):
        if self.fabricante == 'INTEL' and self.ultima_geracao:
            base = f"CPU: {self.modelo} (Intel, {self.perf_cores} P + {self.eff_cores} E = {self.nucleos} núcleos)"
        else:
            base = f"CPU: {self.modelo} ({self.fabricante}, {self.nucleos} núcleos)"

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
            'integrated_gpu': self.integrated_gpu,
        }
        if self.fabricante == 'INTEL' and self.ultima_geracao:
            data.update({'perf_cores': self.perf_cores, 'eff_cores': self.eff_cores})
        return data
# CLASSE DE UM COMPONENTE ADICIONAL (diferente de PC OFFICE, classe de GPU Dedicada)
class PlacaDeVideo:
    def __init__(self, modelo, memoria_vram, fabricante, profissional=False):
        if fabricante not in ('AMD', 'NVIDIA', 'INTEL'):
            raise ValueError("Placa de Vídeo: fabricante deve ser 'AMD', 'NVIDIA' ou 'INTEL'.")
        if not modelo or memoria_vram <= 0:
            raise ValueError("Placa de Vídeo: Modelo e VRAM são obrigatórios.")

        self.modelo = modelo
        self.memoria_vram = int(memoria_vram)
        self.fabricante = fabricante
        self.profissional = bool(profissional)
    # Métodos para exibir informações e converter para dicionário
    def get_info(self):
        tag = ' (Profissional)' if self.profissional else ''
        return f"GPU: {self.modelo} ({self.memoria_vram}GB VRAM, {self.fabricante}){tag}"
    # Método para converter o objeto em um dicionário
    def to_dict(self):
        return {'modelo': self.modelo, 'memoria_vram': self.memoria_vram, 'fabricante': self.fabricante, 'profissional': self.profissional}
# CLASSE DE MEMÓRIA RAM
class MemoriaRAM:
    # Construtor com validações para memória RAM
    def __init__(self, capacidade_gb, velocidade_mhz, num_modulos):
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
    # Métodos para exibir informações e converter para dicionário
    def get_info(self):
        return f"RAM: {self.capacidade_gb}GB ({self.num_modulos}x{self.tamanho_por_modulo}GB) {self.velocidade_mhz}MHz"
    # Método para converter o objeto em um dicionário
    def to_dict(self):
        return {
            'capacidade_gb': self.capacidade_gb,
            'velocidade_mhz': self.velocidade_mhz,
            'num_modulos': self.num_modulos,
            'tamanho_por_modulo': self.tamanho_por_modulo
        }

# CLASSE DE MONITOR
class Monitor:
    # Construtor com validações para monitor
    def __init__(self, marca, modelo, tamanho_polegadas, frequencia_hz):
        if not marca or not modelo:
            raise ValueError("Monitor: Marca e modelo são obrigatórios.")
        if float(tamanho_polegadas) <= 15:
            raise ValueError("Monitor: Tamanho em polegadas deve ser maior que 15.")

        self.marca = marca
        self.modelo = modelo
        self.tamanho_polegadas = float(tamanho_polegadas)
        freq = int(frequencia_hz)
        if freq < 60:
            raise ValueError("Monitor: frequência deve ser de pelo menos 60Hz.")
        self.frequencia_hz = freq
    # Métodos para exibir informações e converter para dicionário
    def get_info(self):
        return f"Monitor: {self.marca} {self.modelo} ({self.tamanho_polegadas}\", {self.frequencia_hz}Hz)"
    # Método para converter o objeto em um dicionário
    def to_dict(self):
        return {
            'tipo': self.__class__.__name__,
            'marca': self.marca,
            'modelo': self.modelo,
            'tamanho_polegadas': self.tamanho_polegadas,
            'frequencia_hz': self.frequencia_hz
        }
# CLASSE DE MONITOR GAMER (HERANÇA)
class MonitorGamer(Monitor):
    # Construtor com validações específicas para monitor gamer
    def __init__(self, marca, modelo, tamanho_polegadas, frequencia_hz):
        super().__init__(marca, modelo, tamanho_polegadas, frequencia_hz)

        if int(self.frequencia_hz) < 120:
            raise ValueError("Monitor Gamer: a frequência deve ser de no mínimo 120Hz.")


# CLASSE DISCO (SSD/HD)
class Disco:
    def __init__(self, tipo, capacidade_gb):
        if tipo not in ('SSD SATA', 'SSD NVMe', 'HD SATA'):
            raise ValueError(f"Disco: tipo inválido. Deve ser um de: SSD SATA, SSD NVMe, HD SATA")
        if not capacidade_gb or int(capacidade_gb) <= 0:
            raise ValueError("Disco: capacidade deve ser maior que zero.")
        self.tipo = tipo
        self.capacidade_gb = int(capacidade_gb)
    # Métodos para exibir informações e converter para dicionário
    def get_info(self):
        return f"{self.tipo}: {self.capacidade_gb}GB"
    # Método para converter o objeto em um dicionário
    def to_dict(self):
        return {'tipo': self.tipo, 'capacidade_gb': self.capacidade_gb}

# CLASSE PAI DE COMPUTADORES
class Computador:
    # Construtor com validações básicas
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, disco_principal: Disco, disco_secundario: Disco = None):
        if not tag_identificacao:
            raise ValueError("Tag de Identificação é obrigatória.")
        if not isinstance(disco_principal, Disco):
            raise ValueError("Disco principal (SSD) é obrigatório e deve ser um objeto Disco.")
        if not isinstance(processador, Processador):
            raise TypeError("O 'processador' fornecido não é um objeto Processador válido.")
        if not isinstance(memoria_ram, MemoriaRAM):
            raise TypeError("A 'memoria_ram' fornecida não é um objeto MemoriaRAM válido.")
        if not disco_principal.tipo.startswith('SSD'):
            raise ValueError("Disco principal deve ser um SSD (SSD SATA ou SSD NVMe).")

        self.tag_identificacao = tag_identificacao
        self.processador = processador
        self.memoria_ram = memoria_ram
        self.disco_principal = disco_principal
        self.disco_secundario = disco_secundario
    # Métodos para exibir informações e converter para dicionário
    def get_info_base(self):
        base = f"Tag: {self.tag_identificacao}\n  {self.processador.get_info()}\n  {self.memoria_ram.get_info()}"
        base += f"\n  {self.disco_principal.get_info()}"
        if self.disco_secundario:
            base += f"\n  {self.disco_secundario.get_info()}"
        return base
    # Método polimórfico para obter informações completas
    def get_info_completa(self):
        return f"[Computador Genérico]\n{self.get_info_base()}" # Nunca usado, porém necessário para polimorfismo
    # Método para converter o objeto em um dicionário
    def to_dict_base(self):
        data = {
            'tipo': self.__class__.__name__,
            'tag_identificacao': self.tag_identificacao,
            'processador': self.processador.to_dict(),
            'memoria_ram': self.memoria_ram.to_dict(),
            'disco_principal': self.disco_principal.to_dict(),
            'disco_secundario': self.disco_secundario.to_dict() if self.disco_secundario else None
        }
        return data
    # Método polimórfico para converter o objeto em um dicionário
    def to_dict(self):
        return self.to_dict_base()