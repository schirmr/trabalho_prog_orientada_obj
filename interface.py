import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

from modelos import Processador, PlacaDeVideo, MemoriaRAM, Monitor, MonitorGamer, Disco
# Carrega as subclasses que herdam da classe computador presente na pasta sub
from sub.computador_office import ComputadorOffice
from sub.computador_gamer import ComputadorGamer
from sub.computador_intermediario import ComputadorIntermediario
from sub.computador_workstation import ComputadorWorkstation

## Configuração do Formulário de cada campo
class InventarioApp(tk.Tk):
    FORM_CONFIG = [
        {'name': 'Tipo', 'type': ttk.Combobox, 'grid': {'row': 0, 'col': 0, 'colspan': 5}, 'options': {'state': 'readonly', 'values': ['ComputadorOffice', 'ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']}, 'targets': ['all']},
        {'name': 'Tag de Identificação', 'type': ttk.Entry, 'grid': {'row': 1, 'col': 0, 'colspan': 5}, 'targets': ['all']},
        {'name': 'CPU Fabricante', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 0}, 'options': {'values': ['AMD', 'INTEL'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Família', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Modelo', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Núcleos', 'type': ttk.Entry, 'grid': {'row': 4, 'col': 0}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Hyperthread', 'type': ttk.Checkbutton, 'grid': {'row': 4, 'col': 2}, 'options': {'text': 'Hyperthread/SMT', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Gráficos Integrados', 'type': ttk.Checkbutton, 'grid': {'row': 4, 'col': 4}, 'options': {'text': 'iGPU', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Última Geração', 'type': ttk.Checkbutton, 'grid': {'row': 5, 'col': 0}, 'options': {'text': 'Arquitetura P+E', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Núcleos Performance', 'type': ttk.Entry, 'grid': {'row': 5, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Núcleos Eficiência', 'type': ttk.Entry, 'grid': {'row': 5, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'Módulos RAM', 'type': ttk.Combobox, 'grid': {'row': 6, 'col': 0}, 'options': {'values': ['1', '2', '4', '8'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'Tamanho por Módulo (GB)', 'type': ttk.Entry, 'grid': {'row': 6, 'col': 2}, 'targets': ['all']},
        {'name': 'RAM (MHz)', 'type': ttk.Entry, 'grid': {'row': 6, 'col': 4}, 'targets': ['all']},
        {'name': 'SSD Tipo', 'type': ttk.Combobox, 'grid': {'row': 8, 'col': 0}, 'options': {'values': ['SSD SATA', 'SSD NVMe'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'SSD Capacidade (GB)', 'type': ttk.Entry, 'grid': {'row': 8, 'col': 2}, 'targets': ['all']},
        {'name': 'HD (GB)', 'type': ttk.Entry, 'grid': {'row': 8, 'col': 4}, 'targets': ['all']},
        {'name': 'GPU Fabricante', 'type': ttk.Combobox, 'grid': {'row': 9, 'col': 0}, 'options': {'values': ['AMD', 'NVIDIA', 'INTEL'], 'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'GPU Modelo', 'type': ttk.Combobox, 'grid': {'row': 9, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'GPU VRAM (GB)', 'type': ttk.Entry, 'grid': {'row': 9, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'Monitor Marca', 'type': ttk.Entry, 'grid': {'row': 11, 'col': 0}, 'targets': ['all']},
        {'name': 'Monitor Modelo', 'type': ttk.Entry, 'grid': {'row': 11, 'col': 2}, 'targets': ['all']},
        {'name': 'Monitor Polegadas (")', 'type': ttk.Entry, 'grid': {'row': 12, 'col': 0}, 'targets': ['all']},
        {'name': 'Monitor Frequência (Hz)', 'type': ttk.Entry, 'grid': {'row': 12, 'col': 2}, 'targets': ['all']},
    ]
    ## Construtor da Interface Gráfica
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventário de Computadores")
        self.geometry("1280x720")
        
        self.lista_computadores = []
        self.item_selecionado_index = None
        self.widgets = {}
        
        self.cpu_ultima_geracao_var = tk.BooleanVar(value=False)
        self.cpu_hyper_var = tk.BooleanVar(value=False)
        self.cpu_integrated_var = tk.BooleanVar(value=False)
        self.gpus_db = self._carregar_gpus()

        self.processadores_db = self._carregar_processadores()
        self._criar_widgets()
        self._atualizar_lista()
        self._update_form_visibility()
    ## Carrega a base de dados de processadores a partir do arquivo JSON
    def _carregar_processadores(self):
        try:
            with open('processadores.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar 'processadores.json': {e}")
            self.destroy()
            return []

    def _carregar_gpus(self):
        try:
            with open('gpus.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar 'gpus.json': {e}")
            return []
    ## Cria os widgets da interface gráfica
    def _criar_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Computador", padding="10")
        form_frame.pack(fill="x", pady=5)
        for i in [1, 3, 5]: form_frame.columnconfigure(i, weight=1)

        for config in self.FORM_CONFIG:
            name, grid_info = config['name'], config['grid']
            label = ttk.Label(form_frame, text=f"{name}:")
            label.grid(row=grid_info['row'], column=grid_info['col'], padx=5, pady=5, sticky="w")
            options = config.get('options', {}).copy()
            if name == 'CPU Última Geração': options['variable'] = self.cpu_ultima_geracao_var
            elif name == 'CPU Hyperthread': options['variable'] = self.cpu_hyper_var
            elif name == 'CPU Gráficos Integrados': options['variable'] = self.cpu_integrated_var
            widget = config['type'](form_frame, **options)
            widget.grid(row=grid_info['row'], column=grid_info['col'] + 1, columnspan=grid_info.get('colspan', 1), sticky="ew", padx=5, pady=5)
            self.widgets[name] = {'label': label, 'widget': widget, 'config': config}

        ttk.Separator(form_frame, orient='horizontal').grid(row=2, column=0, columnspan=6, sticky='ew', pady=10)
        ttk.Separator(form_frame, orient='horizontal').grid(row=7, column=0, columnspan=6, sticky='ew', pady=10)
        ttk.Separator(form_frame, orient='horizontal').grid(row=10, column=0, columnspan=6, sticky='ew', pady=10)
        
        self.widgets['Tipo']['widget'].bind("<<ComboboxSelected>>", self._update_form_visibility)
        self.widgets['CPU Fabricante']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['CPU Família']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['CPU Modelo']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['GPU Fabricante']['widget'].bind("<<ComboboxSelected>>", self._update_gpu_models)
        self.widgets['GPU Modelo']['widget'].bind("<<ComboboxSelected>>", self._update_gpu_vram)
        self.cpu_ultima_geracao_var.trace_add('write', lambda *args: self._update_form_visibility())
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=99, column=0, columnspan=6, pady=10)
        ttk.Button(button_frame, text="Adicionar", command=self._adicionar_computador).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar Campos", command=self._limpar_campos).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Salvar em Arquivo", command=self._salvar_arquivo).pack(side="right", padx=5)
        
        list_frame = ttk.LabelFrame(main_frame, text="Inventário de Computadores", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)
        self.lista_widget = tk.Text(list_frame, wrap="none", height=15)
        self.lista_widget.pack(side="left", fill="both", expand=True)
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.lista_widget.yview); v_scrollbar.pack(side="right", fill="y")
        self.lista_widget.config(yscrollcommand=v_scrollbar.set)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.lista_widget.xview); h_scrollbar.pack(fill="x", pady=2)
        self.lista_widget.config(xscrollcommand=h_scrollbar.set)
    ## Métodos Auxiliares
    def _set_widget_state(self, widget_name, state):
        widget = self.widgets[widget_name]['widget']
        if isinstance(widget, ttk.Checkbutton):
            widget.config(state=state)
        else:
            widget.config(state=state)
    ## Define o valor de um campo, respeitando seu estado atual
    def _set_field_value(self, widget_name, value, is_manual_mode=False):
        widget = self.widgets[widget_name]['widget']
        current_state = widget.cget('state')
        if current_state == 'readonly' and not is_manual_mode:
            widget.config(state='normal')
        
        widget.delete(0, tk.END)
        widget.insert(0, str(value))

        if current_state == 'readonly' and not is_manual_mode:
            widget.config(state='readonly')

    ## Atualiza os campos relacionados ao processador com base nas seleções feitas
    def _update_cpu_fields(self, event=None):
        fabricante = self.widgets['CPU Fabricante']['widget'].get()
        familia = self.widgets['CPU Família']['widget'].get()
        modelo = self.widgets['CPU Modelo']['widget'].get()

        if fabricante:
            familias = sorted(list(set(p['familia'] for p in self.processadores_db if p['fabricante'] == fabricante)))
            self.widgets['CPU Família']['widget']['values'] = ["Outro"] + familias
        else:
            self.widgets['CPU Família']['widget']['values'] = ["Outro"]
        
        if familia and familia != "Outro":
            tipo_selecionado = self.widgets['Tipo']['widget'].get()
            if tipo_selecionado == 'ComputadorOffice':
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia and p.get('integrated_gpu', False)])
            else:
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia])
            self.widgets['CPU Modelo']['widget']['values'] = ["Outro"] + modelos
        else:
            self.widgets['CPU Modelo']['widget']['values'] = ["Outro"]

        if event:
            if event.widget == self.widgets['CPU Fabricante']['widget']:
                self.widgets['CPU Família']['widget'].set('')
                self.widgets['CPU Modelo']['widget'].set('')
            if event.widget == self.widgets['CPU Família']['widget']:
                self.widgets['CPU Modelo']['widget'].set('')

        cpu_spec_fields = ['CPU Núcleos', 'CPU Núcleos Performance', 'CPU Núcleos Eficiência']
        cpu_check_fields = ['CPU Hyperthread', 'CPU Última Geração', 'CPU Gráficos Integrados']

        if modelo == 'Outro' or familia == 'Outro':
            for field in cpu_spec_fields: self._set_widget_state(field, 'normal')
            for field in cpu_check_fields: self._set_widget_state(field, 'normal')
            if event:
                for field in cpu_spec_fields: self._set_field_value(field, '', True)
                self.cpu_hyper_var.set(False)
                self.cpu_ultima_geracao_var.set(False)
                self.cpu_integrated_var.set(False)
        else:
            for field in cpu_spec_fields: self._set_widget_state(field, 'readonly')
            for field in cpu_check_fields: self._set_widget_state(field, 'disabled')

            proc_data = next((p for p in self.processadores_db if p['modelo'] == modelo), None)
            if proc_data:
                ultima = proc_data.get('ultima_geracao', False)
                self.cpu_ultima_geracao_var.set(ultima)
                self.cpu_hyper_var.set(proc_data.get('hyperthread', False))
                self.cpu_integrated_var.set(proc_data.get('integrated_gpu', False))
                if ultima:
                    perf = int(proc_data.get('perf_cores', 0) or 0)
                    eff = int(proc_data.get('eff_cores', 0) or 0)
                    total = perf + eff
                    self._set_field_value('CPU Núcleos', total)
                    self._set_field_value('CPU Núcleos Performance', perf)
                    self._set_field_value('CPU Núcleos Eficiência', eff)
                else:
                    self._set_field_value('CPU Núcleos', proc_data.get('nucleos', 'N/A'))
                    self._set_field_value('CPU Núcleos Performance', '')
                    self._set_field_value('CPU Núcleos Eficiência', '')
            else:
                for field in cpu_spec_fields: self._set_field_value(field, '')
                self.cpu_hyper_var.set(False)
                self.cpu_ultima_geracao_var.set(False)

        self._update_form_visibility()

    def _update_gpu_models(self, event=None):
        fab = self.widgets['GPU Fabricante']['widget'].get()
        tipo_selecionado = self.widgets['Tipo']['widget'].get()
        if not fab:
            self.widgets['GPU Modelo']['widget']['values'] = []
            try: self.widgets['GPU Modelo']['widget'].set('')
            except Exception: pass
            return
        if tipo_selecionado == 'ComputadorWorkstation':
            modelos = sorted([g['modelo'] for g in self.gpus_db if g['fabricante'] == fab and g.get('profissional', False)])
        else:
            modelos = sorted([g['modelo'] for g in self.gpus_db if g['fabricante'] == fab and not g.get('profissional', False)])
        self.widgets['GPU Modelo']['widget']['values'] = modelos
        try:
            if modelos:
                self.widgets['GPU Modelo']['widget'].set(modelos[0])
            else:
                self.widgets['GPU Modelo']['widget'].set('')
        except Exception:
            pass
        try:
            self._update_gpu_vram()
        except Exception:
            pass

    def _is_professional_gpu(self, modelo: str, fabricante: str) -> bool:
        if not modelo or modelo == 'Outro':
            return False
        for g in self.gpus_db:
            if g.get('modelo') == modelo and g.get('fabricante') == fabricante:
                return bool(g.get('profissional', False))
        return False

    def _update_gpu_vram(self, event=None):
        try:
            modelo = self.widgets['GPU Modelo']['widget'].get()
            fabricante = self.widgets['GPU Fabricante']['widget'].get()
        except Exception:
            return
        if not modelo or not fabricante:
            try: self._set_field_value('GPU VRAM (GB)', '')
            except Exception: pass
            return
        entry = next((g for g in self.gpus_db if g.get('modelo') == modelo and g.get('fabricante') == fabricante), None)
        if entry:
            vram = entry.get('memoria_vram', entry.get('vram_gb', ''))
            try:
                self._set_field_value('GPU VRAM (GB)', int(vram) if vram != '' else '')
            except Exception:
                try: self._set_field_value('GPU VRAM (GB)', vram)
                except Exception: pass
        else:
            try: self._set_field_value('GPU VRAM (GB)', '')
            except Exception: pass
    ## Cria um objeto Processador a partir de um dicionário de dados
    def _create_processador_from_dict(self, data: dict):
        if not data:
            raise ValueError('Dados do processador inválidos')
        modelo = data.get('modelo')
        fabricante = data.get('fabricante', 'AMD')
        ultima = bool(data.get('ultima_geracao', False))
        if ultima:
            perf = data.get('perf_cores', 0)
            eff = data.get('eff_cores', 0)
            return Processador(modelo=modelo, fabricante=fabricante, ultima_geracao=True, perf_cores=perf, eff_cores=eff, integrated_gpu=data.get('integrated_gpu', False))
        else:
            nucleos = data.get('nucleos')
            hyper = bool(data.get('hyperthread', False))
            return Processador(modelo=modelo, fabricante=fabricante, nucleos=nucleos, hyperthread=hyper, integrated_gpu=data.get('integrated_gpu', False))
    ## Adiciona um novo computador ao inventário
    def _adicionar_computador(self):
        try:
            modelo_cpu = self._get_valor('CPU Modelo')
            familia_cpu = self._get_valor('CPU Família')
            
            if modelo_cpu == 'Outro' or familia_cpu == 'Outro':
                is_ultima_geracao = self.cpu_ultima_geracao_var.get()
                cpu_data = {
                    "fabricante": self._get_valor('CPU Fabricante'),
                    "familia": "Custom",
                    "modelo": "Custom",
                    "ultima_geracao": is_ultima_geracao,
                    "hyperthread": self.cpu_hyper_var.get(),
                    "nucleos": self._get_valor('CPU Núcleos', int, False) if not is_ultima_geracao else 0,
                    "perf_cores": self._get_valor('CPU Núcleos Performance', int, False) if is_ultima_geracao else 0,
                    "eff_cores": self._get_valor('CPU Núcleos Eficiência', int, False) if is_ultima_geracao else 0,
                    "integrated_gpu": self.cpu_integrated_var.get(),
                }
                cpu = self._create_processador_from_dict(cpu_data)
            else:
                proc_data = next((p for p in self.processadores_db if p['modelo'] == modelo_cpu), None)
                if not proc_data: raise ValueError("Selecione um processador válido.")
                cpu = self._create_processador_from_dict(proc_data)

            mod_count = int(self._get_valor('Módulos RAM'))
            tamanho_por_mod = self._get_valor('Tamanho por Módulo (GB)', int)
            if tamanho_por_mod <= 0:
                raise ValueError('Tamanho por módulo deve ser um número positivo.')
            ram_total = mod_count * int(tamanho_por_mod)
            ram = MemoriaRAM(capacidade_gb=ram_total, velocidade_mhz=self._get_valor('RAM (MHz)', int), num_modulos=mod_count)
            
            tipo = self._get_valor('Tipo')
            tag = self._get_valor('Tag de Identificação')
            novo_computador = None

            ssd_tipo = self._get_valor('SSD Tipo')
            ssd_capacidade = self._get_valor('SSD Capacidade (GB)', int)
            hdd_sec = self._get_valor('HD (GB)', int, False) or 0

            disco_principal = Disco(ssd_tipo, ssd_capacidade)
            disco_sec = Disco('HD SATA', hdd_sec) if hdd_sec and int(hdd_sec) > 0 else None

            if tipo == "ComputadorOffice":
                monitor = Monitor(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int, False) or 60)
                novo_computador = ComputadorOffice(tag, cpu, ram, disco_principal, disco_sec, monitor)
            elif tipo in ("ComputadorGamer", "ComputadorIntermediario"):
                gpu_model = self._get_valor('GPU Modelo')
                gpu_fab = self._get_valor('GPU Fabricante')
                profissional_flag = self._is_professional_gpu(gpu_model, gpu_fab)
                gpu_entry = next((g for g in self.gpus_db if g.get('modelo') == gpu_model and g.get('fabricante') == gpu_fab), None)
                if gpu_entry:
                    memoria_vram = int(gpu_entry.get('memoria_vram', gpu_entry.get('vram_gb', 0) or 0))
                else:
                    memoria_vram = self._get_valor('GPU VRAM (GB)', int)
                gpu = PlacaDeVideo(modelo=gpu_model, memoria_vram=memoria_vram, fabricante=gpu_fab, profissional=profissional_flag)
                monitor_class = MonitorGamer if tipo == "ComputadorGamer" else Monitor
                monitor = monitor_class(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int))
                if tipo == "ComputadorGamer": novo_computador = ComputadorGamer(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
                else: novo_computador = ComputadorIntermediario(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
            elif tipo == "ComputadorWorkstation":
                gpu_model = self._get_valor('GPU Modelo')
                gpu_fab = self._get_valor('GPU Fabricante')
                profissional_flag = self._is_professional_gpu(gpu_model, gpu_fab)
                gpu_entry = next((g for g in self.gpus_db if g.get('modelo') == gpu_model and g.get('fabricante') == gpu_fab), None)
                if gpu_entry:
                    memoria_vram = int(gpu_entry.get('memoria_vram', gpu_entry.get('vram_gb', 0) or 0))
                else:
                    memoria_vram = self._get_valor('GPU VRAM (GB)', int)
                gpu = PlacaDeVideo(modelo=gpu_model, memoria_vram=memoria_vram, fabricante=gpu_fab, profissional=profissional_flag)
                monitor = Monitor(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int))
                novo_computador = ComputadorWorkstation(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
            
            if novo_computador:
                if any(c.tag_identificacao.lower() == tag.lower() for c in self.lista_computadores):
                    raise ValueError(f"A tag '{tag}' já está em uso.")
                self.lista_computadores.append(novo_computador)
                self._atualizar_lista()
                self._limpar_campos()
        except ValueError as e: messagebox.showerror("Erro de Entrada", f"Dado inválido: {e}")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
    ## Limpa todos os campos do formulário
    def _limpar_campos(self):
        for data in self.widgets.values():
            widget = data['widget']
            if isinstance(widget, ttk.Combobox): widget.set('')
            elif isinstance(widget, ttk.Entry):
                is_readonly = widget.cget('state') == 'readonly'
                if is_readonly: widget.config(state='normal')
                widget.delete(0, tk.END)
                if is_readonly: widget.config(state='readonly')
        self.item_selecionado_index = None
        self._update_cpu_fields()
        self._update_form_visibility()
    ## Atualiza a visibilidade dos campos do formulário com base nas seleções feitas
    def _update_form_visibility(self, event=None):
        tipo_selecionado = self.widgets['Tipo']['widget'].get()
        is_ultima_geracao = self.cpu_ultima_geracao_var.get()
        try:
            ram_widget = self.widgets['Módulos RAM']['widget']
            if tipo_selecionado == 'ComputadorOffice':
                ram_widget['values'] = ['1', '2']
            elif tipo_selecionado in ('ComputadorGamer', 'ComputadorIntermediario'):
                ram_widget['values'] = ['1', '2', '4']
            elif tipo_selecionado == 'ComputadorWorkstation':
                ram_widget['values'] = ['1', '2', '4', '8']
            else:
                ram_widget['values'] = ['1', '2', '4']
        except Exception:
            pass
        try:
            if 'GPU Fabricante' in self.widgets:
                if tipo_selecionado == 'ComputadorWorkstation':
                    self.widgets['GPU Fabricante']['widget']['values'] = ['AMD', 'NVIDIA']
                else:
                    self.widgets['GPU Fabricante']['widget']['values'] = ['AMD', 'NVIDIA', 'INTEL']
                fab = self.widgets['GPU Fabricante']['widget'].get()
                if fab:
                    self._update_gpu_models()
        except Exception:
            pass
        for name, data in self.widgets.items():
            targets = data['config']['targets']; is_visible = 'all' in targets or tipo_selecionado in targets
            (data['label'].grid, data['label'].grid_remove)[not is_visible](); (data['widget'].grid, data['widget'].grid_remove)[not is_visible]()
        campos_ultima_geracao = ['CPU Última Geração', 'CPU Núcleos Performance', 'CPU Núcleos Eficiência']
        campos_legado = ['CPU Hyperthread']
        for name in campos_ultima_geracao:
            (self.widgets[name]['label'].grid, self.widgets[name]['label'].grid_remove)[not is_ultima_geracao]()
            (self.widgets[name]['widget'].grid, self.widgets[name]['widget'].grid_remove)[not is_ultima_geracao]()
        for name in campos_legado:
            (self.widgets[name]['label'].grid_remove, self.widgets[name]['label'].grid)[not is_ultima_geracao]()
            (self.widgets[name]['widget'].grid_remove, self.widgets[name]['widget'].grid)[not is_ultima_geracao]()
        try:
            familia_atual = self.widgets['CPU Família']['widget'].get()
            if familia_atual and familia_atual != 'Outro':
                if tipo_selecionado == 'ComputadorOffice':
                    modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia_atual and p.get('integrated_gpu', False)])
                else:
                    modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia_atual])
                self.widgets['CPU Modelo']['widget']['values'] = ['Outro'] + modelos
        except Exception:
            pass
    def _get_valor(self, nome_campo, tipo=str, obrigatorio=True):
        try:
            if nome_campo == 'CPU Última Geração': return self.cpu_ultima_geracao_var.get()
            if nome_campo == 'CPU Hyperthread': return self.cpu_hyper_var.get()
            if nome_campo == 'CPU Gráficos Integrados': return self.cpu_integrated_var.get()
            widget = self.widgets[nome_campo]['widget']
            if not widget.winfo_ismapped(): return None
            valor = widget.get()
            if not valor:
                if obrigatorio: raise ValueError(f"Campo '{nome_campo}' é obrigatório.")
                return None
            return tipo(valor)
        except (ValueError, TypeError): raise ValueError(f"Campo '{nome_campo}' deve ser um número válido.")
        except KeyError: return None
    ## Atualiza a lista de computadores exibida na interface
    def _atualizar_lista(self):
        self.lista_widget.config(state=tk.NORMAL); self.lista_widget.delete('1.0', tk.END)
        for i, comp in enumerate(self.lista_computadores):
            try: info = comp.get_info_completa()
            except AttributeError: info = f"Tag: {comp.tag_identificacao}"
            tag_id, header = f"item_{i}", f"--- Item {i+1}: {comp.tag_identificacao} ({comp.__class__.__name__}) ---\n"
            self.lista_widget.tag_configure(f"header_{i}", font=("TkDefaultFont", 10, "bold"))
            self.lista_widget.insert(tk.END, header, (f"header_{i}", tag_id)); self.lista_widget.insert(tk.END, f"{info}\n\n", (tag_id,))
        self.lista_widget.config(state=tk.DISABLED)
    ## Salva o inventário em um arquivo JSON
    def _salvar_arquivo(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")], title="Salvar inventário como...")
        if not filepath: return
        try:
            lista_serializada = [c.to_dict() for c in self.lista_computadores]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lista_serializada, f, indent=4, default=lambda o: o.to_dict())
            messagebox.showinfo("Sucesso", "Inventário salvo com sucesso!")
        except Exception as e: messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar o arquivo: {e}")