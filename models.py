from datetime import datetime
from decimal import Decimal, ROUND_UP
from typing import List, Dict, Optional

class Alquiler:
    def __init__(self, codigo: str, fianza: Decimal, herramienta: str):
        self.codigo = codigo
        self.fianza = fianza
        self.herramienta = herramienta
        self.estado = "Activo"
        self.hora_pactada: Optional[datetime] = None
        self.checklist_entrega = False
        self.mora_por_hora = Decimal('10.00')
        self.danos: List[str] = []
        self.punto_alterno = False
        self.costo_punto_alterno = Decimal('15.00')

    def establecer_hora_devolucion(self, hora_pactada: datetime):
        self.hora_pactada = hora_pactada

    def registrar_entrega_con_checklist(self):
        self.checklist_entrega = True

    def registrar_dano(self, tipo_dano: str):
        if tipo_dano not in self.danos:
            self.danos.append(tipo_dano)

    def calcular_horas_retraso(self, hora_devolucion: datetime) -> Decimal:
        if not self.hora_pactada or hora_devolucion <= self.hora_pactada:
            return Decimal('0')

        delta = hora_devolucion - self.hora_pactada
        horas = Decimal(delta.total_seconds() / 3600)

        return (horas * 2).quantize(Decimal('1'), rounding=ROUND_UP) / 2

    def calcular_mora(self, hora_devolucion: datetime) -> Decimal:
        horas_retraso = self.calcular_horas_retraso(hora_devolucion)
        return (horas_retraso * self.mora_por_hora).quantize(Decimal('0.01'))

    def calcular_costo_danos(self, catalogo_danos: Dict[str, Decimal]) -> Decimal:
        total = Decimal('0')
        for dano in self.danos:
            if dano in catalogo_danos:
                total += catalogo_danos[dano]
        return total.quantize(Decimal('0.01'))

    def procesar_devolucion(self, hora_devolucion: datetime, 
                          catalogo_danos: Dict[str, Decimal],
                          usar_punto_alterno: bool = False) -> Dict:
        
        mora = self.calcular_mora(hora_devolucion)
        costo_danos = self.calcular_costo_danos(catalogo_danos)
        costo_extra = self.costo_punto_alterno if usar_punto_alterno else Decimal('0')
        
        total_cargos = mora + costo_danos + costo_extra
        
        fianza_liberada = max(Decimal('0'), self.fianza - total_cargos)
        
        self.estado = "Cerrado"
        
        return {
            'codigo': self.codigo,
            'estado': self.estado,
            'mora': mora,
            'costo_danos': costo_danos,
            'costo_extra': costo_extra,
            'total_cargos': total_cargos,
            'fianza_original': self.fianza,
            'fianza_liberada': fianza_liberada,
            'hora_devolucion': hora_devolucion,
            'danos_registrados': self.danos.copy()
        }
        
    def marcar_no_show(self):
        return {
            'reprogramado': True,
            'mensaje': 'Se reprograma ventana de devolución'
        }

class GestorAlquileres:
    def __init__(self):
        self.alquileres: Dict[str, Alquiler] = {}
        self.catalogo_danos = {
            "Broca rota": Decimal('80.00'),
            "Carcasa rayada": Decimal('30.00')
        }
        
    def crear_alquiler(self, codigo: str, fianza: Decimal, herramienta: str) -> Alquiler:
        alquiler = Alquiler(codigo, fianza, herramienta)
        self.alquileres[codigo] = alquiler
        return alquiler
        
    def obtener_alquiler(self, codigo: str) -> Optional[Alquiler]:
        return self.alquileres.get(codigo)
        
    def actualizar_catalogo_danos(self, dano: str, costo: Decimal):
        self.catalogo_danos[dano] = costo