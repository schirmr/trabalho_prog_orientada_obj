class Processador:
    def __init__(self, modelo, fabricante='AMD', nucleos=None, ultima_geracao=False, perf_cores=0, eff_cores=0, hyperthread=False):
        """Representa um processador.
        Para AMD: usa-se 'nucleos' (int).
        Para INTEL: pode usar 'nucleos' (int) ou, se 'ultima_geracao' for True, usar 'perf_cores' e 'eff_cores'.
        """
        if not modelo:
            raise ValueError("Processador: Modelo é obrigatório.")

        if fabricante not in ('AMD', 'INTEL'):
            raise ValueError("Processador: Fabricante deve ser 'AMD' ou 'INTEL'.")

        self.modelo = modelo
        self.fabricante = fabricante
        self.ultima_geracao = bool(ultima_geracao)

        try:
            perf = int(perf_cores)
        except Exception:
            perf = 0
        try:
            eff = int(eff_cores)
        except Exception:
            eff = 0

        self.perf_cores = max(0, perf)
        self.eff_cores = max(0, eff)

        if fabricante == 'INTEL' and self.ultima_geracao:
            if (self.perf_cores + self.eff_cores) <= 0:
                raise ValueError("Processador Intel (última geração): é necessário informar núcleos de performance e/ou eficiência.")
            self.nucleos = self.perf_cores + self.eff_cores
        else:
            # usa-se o campo 'nucleos'
            if nucleos is None:
                raise ValueError("Processador: número de núcleos é obrigatório quando não se usa o formato E/P.")
            try:
                n = int(nucleos)
            except Exception:
                raise ValueError("Processador: número de núcleos deve ser inteiro.")
            if n <= 0:
                raise ValueError("Processador: número de núcleos deve ser maior que zero.")
            self.nucleos = n
        # Hyperthread/SMT: dobra o número de threads lógicas quando ativo
        self.hyperthread = bool(hyperthread)
        # número lógico de threads (apenas informativo)
        try:
            self.threads = int(self.nucleos) * (2 if self.hyperthread else 1)
        except Exception:
            self.threads = self.nucleos

    def get_info(self):
        if self.fabricante == 'INTEL' and self.ultima_geracao:
            base = f"CPU: {self.modelo} (Intel, {self.perf_cores} P + {self.eff_cores} E = {self.nucleos} núcleos)"
        else:
            base = f"CPU: {self.modelo} ({self.nucleos} núcleos, {self.fabricante})"

        if self.hyperthread and not self.ultima_geracao:
            return f"{base} - Hyperthread/SMT ativo ({self.threads} threads lógicas)"
        return base
    
    def to_dict(self):
        """Converte o objeto para um dicionário para salvar em JSON."""
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

class PlacaDeVideo:
    def __init__(self, modelo, memoria_vram, fabricante='NVIDIA'):
        # fabricante opcional para compatibilidade com dados antigos; aceita AMD/NVIDIA/INTEL
        fabricante = (fabricante or '').upper()
        if fabricante not in ('AMD', 'NVIDIA', 'INTEL'):
            raise ValueError("Placa de Vídeo: fabricante deve ser 'AMD', 'NVIDIA' ou 'INTEL'.")
        if not modelo or not memoria_vram > 0:
            raise ValueError("Placa de Vídeo: Modelo e VRAM são obrigatórios.")
        self.modelo = modelo
        self.memoria_vram = int(memoria_vram)
        self.fabricante = fabricante

    def get_info(self):
        return f"GPU: {self.modelo} ({self.memoria_vram}GB VRAM, {self.fabricante})"

    def to_dict(self):
        return {'modelo': self.modelo, 'memoria_vram': self.memoria_vram, 'fabricante': self.fabricante}

class MemoriaRAM:
    def __init__(self, capacidade_gb, velocidade_mhz):
        if not capacidade_gb > 0 or not velocidade_mhz > 0:
            raise ValueError("Memória RAM: Capacidade e velocidade são obrigatórias.")
        self.capacidade_gb = int(capacidade_gb)
        self.velocidade_mhz = int(velocidade_mhz)

    def get_info(self):
        return f"RAM: {self.capacidade_gb}GB {self.velocidade_mhz}MHz"
    
    def to_dict(self):
        return {'capacidade_gb': self.capacidade_gb, 'velocidade_mhz': self.velocidade_mhz}

# --- PARTE 2: CLASSES DE COMPUTADOR (HERANÇA E POLIMORFISMO) ---

class Computador:
    """Superclasse (Classe Pai) que define um computador."""
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM):
        # MUDANÇA AQUI
        if not tag_identificacao:
            raise ValueError("Tag de Identificação é obrigatória.")
        self.tag_identificacao = tag_identificacao
        self.processador = processador
        self.memoria_ram = memoria_ram

    def get_info_base(self):
        """Retorna as informações comuns a todos os computadores."""
        # MUDANÇA AQUI
        return f"Tag: {self.tag_identificacao}\n  {self.processador.get_info()}\n  {self.memoria_ram.get_info()}"

    def get_info_completa(self):
        """Método polimórfico a ser sobrescrito pelas classes filhas."""
        return f"[Computador Genérico]\n{self.get_info_base()}"

    def to_dict_base(self):
        """Converte as informações base para um dicionário."""
        # MUDANÇA AQUI
        return {
            'tipo': self.__class__.__name__,
            'tag_identificacao': self.tag_identificacao,
            'processador': self.processador.to_dict(),
            'memoria_ram': self.memoria_ram.to_dict()
        }

    def to_dict(self):
        """Método polimórfico para serialização completa."""
        return self.to_dict_base()


class ComputadorOffice(Computador):
    """Subclasse 1: Computador de Escritório."""
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, capacidade_ssd_gb: int):
        # MUDANÇA AQUI
        super().__init__(tag_identificacao, processador, memoria_ram)
        if not capacidade_ssd_gb > 0:
            raise ValueError("Capacidade do SSD é obrigatória.")
        self.capacidade_ssd_gb = int(capacidade_ssd_gb)

    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC de Escritório]\n{info_base}\n  SSD: {self.capacidade_ssd_gb}GB"

    def to_dict(self):
        data = super().to_dict_base()
        data.update({'capacidade_ssd_gb': self.capacidade_ssd_gb})
        return data


class ComputadorGamer(Computador):
    """Subclasse 2: Computador Gamer."""
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, placa_de_video: PlacaDeVideo, potencia_fonte_w: int):
        # MUDANÇA AQUI
        super().__init__(tag_identificacao, processador, memoria_ram)
        if not placa_de_video:
            raise ValueError("PC Gamer deve ter uma placa de vídeo dedicada.")
        if not potencia_fonte_w >= 500:
             raise ValueError("Fonte para PC Gamer deve ser de 500W ou mais.")
        self.placa_de_video = placa_de_video
        self.potencia_fonte_w = int(potencia_fonte_w)

    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC Gamer]\n{info_base}\n  {self.placa_de_video.get_info()}\n  Fonte: {self.potencia_fonte_w}W"

    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict(),
            'potencia_fonte_w': self.potencia_fonte_w
        })
        return data


class ComputadorIntermediario(Computador):
    """Subclasse 3: Computador Intermediário."""
    def __init__(self, tag_identificacao, processador: Processador, memoria_ram: MemoriaRAM, placa_de_video: PlacaDeVideo):
        # MUDANÇA AQUI
        super().__init__(tag_identificacao, processador, memoria_ram)
        if not placa_de_video:
            raise ValueError("PC Intermediário deve ter uma placa de vídeo.")
        self.placa_de_video = placa_de_video

    def get_info_completa(self):
        info_base = super().get_info_base()
        return f"[PC Intermediário]\n{info_base}\n  {self.placa_de_video.get_info()}"

    def to_dict(self):
        data = super().to_dict_base()
        data.update({
            'placa_de_video': self.placa_de_video.to_dict()
        })
        return data
