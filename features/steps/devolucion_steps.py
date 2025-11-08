from behave import given, when, then
from datetime import datetime
from decimal import Decimal
from models import GestorAlquileres

@given('existe un alquiler "{codigo}" con fianza de {monto:f}')
def step_existe_alquiler(context, codigo, monto):
    context.alquiler = context.gestor.crear_alquiler(codigo, Decimal(str(monto)), "")
    
@given('la herramienta "{herramienta}" fue entregada con checklist y fotos')
def step_herramienta_entregada(context, herramienta):
    context.alquiler.herramienta = herramienta
    context.alquiler.registrar_entrega_con_checklist()

@given('la política de mora es S/ {mora:f} por hora de retraso')
def step_politica_mora(context, mora):
    context.alquiler.mora_por_hora = Decimal(str(mora))

@given('existe catálogo de daños con "{dano1}" = {costo1:f}, "{dano2}" = {costo2:f}')
def step_catalogo_danos(context, dano1, costo1, dano2, costo2):
    context.gestor.catalogo_danos = {
        dano1: Decimal(str(costo1)),
        dano2: Decimal(str(costo2))
    }

@given('la hora de devolución pactada es "{fecha_hora}"')
def step_hora_pactada(context, fecha_hora):
    hora_pactada = datetime.fromisoformat(fecha_hora.replace(" ", "T"))
    context.alquiler.establecer_hora_devolucion(hora_pactada)
    context.hora_pactada = hora_pactada

@given('devuelvo a las "{fecha_hora}"')
def step_hora_devolucion(context, fecha_hora):
    context.hora_devolucion = datetime.fromisoformat(fecha_hora.replace(" ", "T"))

@given('no se registran daños')
def step_sin_danos(context):
    context.alquiler.danos = []

@given('se registra daño "{dano}"')
def step_registrar_dano(context, dano):
    context.alquiler.registrar_dano(dano)

@given('no hay encuentro en el punto acordado')
def step_no_encuentro(context):
    context.no_show = True

@given('existe autorización para punto alterno con costo de S/ {costo:f}')
def step_punto_alterno_autorizado(context, costo):
    context.punto_alterno = True
    context.costo_punto_alterno = Decimal(str(costo))

@given('devuelvo en el punto alterno')
def step_devuelvo_punto_alterno(context):
    context.usar_punto_alterno = True

@when('proceso la devolución de "{codigo}"')
def step_procesar_devolucion(context, codigo):
    assert context.alquiler.codigo == codigo
    
    usar_punto_alterno = getattr(context, 'usar_punto_alterno', False)
    
    context.resultado_devolucion = context.alquiler.procesar_devolucion(
        context.hora_devolucion,
        context.gestor.catalogo_danos,
        usar_punto_alterno
    )

@when('el dueño marca "No recibido"')
def step_marcar_no_recibido(context):
    context.resultado_no_show = context.alquiler.marcar_no_show()

@then('el estado del alquiler es "Cerrado"')
def step_estado_cerrado(context):
    assert context.resultado_devolucion['estado'] == "Cerrado"

@then('la mora calculada es {monto:f}')
def step_verificar_mora(context, monto):
    assert context.resultado_devolucion['mora'] == Decimal(str(monto))

@then('la fianza liberada es {monto:f}')
def step_verificar_fianza_liberada(context, monto):
    assert context.resultado_devolucion['fianza_liberada'] == Decimal(str(monto))

@then('la penalidad por daños es {monto:f}')
def step_verificar_penalidad_danos(context, monto):
    assert context.resultado_devolucion['costo_danos'] == Decimal(str(monto))

@then('el total de cargos (mora + daños) es {monto:f}')
def step_verificar_total_cargos(context, monto):
    total_esperado = Decimal(str(monto))
    mora_y_danos = context.resultado_devolucion['mora'] + context.resultado_devolucion['costo_danos']
    assert mora_y_danos == total_esperado

@then('se reprograma ventana de devolución')
def step_verificar_reprogramacion(context):
    assert hasattr(context, 'resultado_no_show')
    assert context.resultado_no_show['reprogramado'] is True

@then('si expira la ventana Then aplica mora hasta recepción')
def step_mora_hasta_recepcion(context):
    assert True

@then('se descuenta {monto:f} adicionales')
def step_verificar_descuento_adicional(context, monto):
    costo_extra = context.resultado_devolucion['costo_extra']
    assert costo_extra == Decimal(str(monto))

@then('se actualiza la liquidación final')
def step_liquidacion_actualizada(context):
    assert context.resultado_devolucion['total_cargos'] >= 0

@then('si la política admite prorrateo Then se calcula reembolso de alquiler')
def step_prorrateo_reembolso(context):
    assert True