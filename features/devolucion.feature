@HU-C3 @EPIC-C
Feature: Devolver herramienta
  Como arrendatario
  Quiero devolver la herramienta
  Para cerrar el alquiler y recuperar la fianza según corresponda

  Background:
    Given existe un alquiler "ALQ-1001" con fianza de 200.00
    And la herramienta "Rotomartillo-01" fue entregada con checklist y fotos
    And la política de mora es S/ 10.00 por hora de retraso
    And existe catálogo de daños con "Broca rota" = 80.00, "Carcasa rayada" = 30.00

  @HU-C3-P1 @puntual @sin-danos
  Scenario: Devolución puntual sin daños
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And devuelvo a las "2025-11-07 17:50"
    And no se registran daños
    When proceso la devolución de "ALQ-1001"
    Then el estado del alquiler es "Cerrado"
    And la mora calculada es 0.00
    And la fianza liberada es 200.00

  @HU-C3-P2 @tardia @mora
  Scenario: Devolución tardía con mora
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And devuelvo a las "2025-11-07 20:15"
    And no se registran daños
    When proceso la devolución de "ALQ-1001"
    Then la mora calculada es 25.00
    And la fianza liberada es 175.00
    And el estado del alquiler es "Cerrado"

  @HU-C3-P3 @danos
  Scenario: Devolución con daños
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And devuelvo a las "2025-11-07 17:55"
    And se registra daño "Broca rota"
    When proceso la devolución de "ALQ-1001"
    Then la penalidad por daños es 80.00
    And la fianza liberada es 120.00
    And el estado del alquiler es "Cerrado"

  @HU-C3-P4 @tardia @danos
  Scenario: Devolución tardía y con daños (retención total si excede)
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And devuelvo a las "2025-11-07 22:30"
    And se registra daño "Carcasa rayada"
    When proceso la devolución de "ALQ-1001"
    Then el total de cargos (mora + daños) es 75.00
    And la fianza liberada es 125.00
    And el estado del alquiler es "Cerrado"

  @HU-C3-P5 @anticipada
  Scenario: Devolución anticipada
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And devuelvo a las "2025-11-07 12:00"
    And no se registran daños
    When proceso la devolución de "ALQ-1001"
    Then la mora calculada es 0.00
    And la fianza liberada es 200.00
    And si la política admite prorrateo Then se calcula reembolso de alquiler

  @HU-C3-P6 @no-show
  Scenario: No-show del arrendatario en devolución
    Given la hora de devolución pactada es "2025-11-07 18:00"
    And no hay encuentro en el punto acordado
    When el dueño marca "No recibido"
    Then se reprograma ventana de devolución
    And si expira la ventana Then aplica mora hasta recepción

  @HU-C3-P7 @punto-alterno
  Scenario: Devolución en punto alterno autorizado
    Given existe autorización para punto alterno con costo de S/ 15.00
    And devuelvo a las "2025-11-07 18:00"
    And devuelvo en el punto alterno
    When proceso la devolución de "ALQ-1001"
    Then se descuenta 15.00 adicionales
    And se actualiza la liquidación final