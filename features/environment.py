from models import GestorAlquileres

def before_scenario(context, scenario):
    context.gestor = GestorAlquileres()
    context.alquiler = None
    context.resultado_devolucion = None
    context.no_show = False
    context.punto_alterno = False
    context.costo_punto_alterno = None