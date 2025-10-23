class Componente:
    def __init__(self, marca, modelo, preco):
        if not all([marca, modelo]):
            raise ValueError("Marca e modelo são obrigatórios.")
        if not isinstance(preco, (int, float)) or preco <= 0:
            raise ValueError("Preço deve ser um número positivo.")
        
        self.marca = marca
        self.modelo = modelo
        self.preco = float(preco)

    def to_dict(self):
        return {
            'tipo': self.__class__.__name__,
            'marca': self.marca,
            'modelo': self.modelo,
            'preco': self.preco
        }
        
    def get_info(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Preço: R${self.preco:.2f}"

class Processador(Componente):
    def __init__(self, marca, modelo, preco, nucleos, frequencia):
        super().__init__(marca, modelo, preco)
        if not isinstance(nucleos, int) or nucleos <= 0:
            raise ValueError("Número de núcleos deve ser um inteiro positivo.")
        if not isinstance(frequencia, (int, float)) or frequencia <= 0:
            raise ValueError("Frequência deve ser um número positivo.")
        
        self.nucleos = nucleos
        self.frequencia = float(frequencia)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'nucleos': self.nucleos,
            'frequencia': self.frequencia
        })
        return data

    def get_info(self):
        return f"{super().get_info()}, Núcleos: {self.nucleos}, Frequência: {self.frequencia}GHz"

class PlacaDeVideo(Componente):
    def __init__(self, marca, modelo, preco, memoria_vram, tipo_memoria):
        super().__init__(marca, modelo, preco)
        if not isinstance(memoria_vram, int) or memoria_vram <= 0:
            raise ValueError("Memória VRAM deve ser um inteiro positivo.")
        if not tipo_memoria:
            raise ValueError("Tipo de memória é obrigatório.")
            
        self.memoria_vram = memoria_vram
        self.tipo_memoria = tipo_memoria

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'memoria_vram': self.memoria_vram,
            'tipo_memoria': self.tipo_memoria
        })
        return data

    def get_info(self):
        return f"{super().get_info()}, VRAM: {self.memoria_vram}GB, Tipo: {self.tipo_memoria}"

class MemoriaRAM(Componente):
    def __init__(self, marca, modelo, preco, capacidade, velocidade):
        super().__init__(marca, modelo, preco)
        if not isinstance(capacidade, int) or capacidade <= 0:
            raise ValueError("Capacidade deve ser um inteiro positivo.")
        if not isinstance(velocidade, int) or velocidade <= 0:
            raise ValueError("Velocidade deve ser um inteiro positivo.")
            
        self.capacidade = capacidade
        self.velocidade = velocidade

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'capacidade': self.capacidade,
            'velocidade': self.velocidade
        })
        return data

    def get_info(self):
        return f"{super().get_info()}, Capacidade: {self.capacidade}GB, Velocidade: {self.velocidade}MHz"