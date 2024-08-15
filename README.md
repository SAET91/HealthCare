# HealthCare: Analisis de datos con SQLite y Python

Este proyecto se centra en el análisis de datos de salud utilizando un conjunto de datos ficticio generado por Synthea. Synthea es un simulador de datos de pacientes que proporciona registros clínicos sintéticos realistas. Los datos incluyen información sobre pacientes, condiciones médicas, encuentros médicos e inmunizaciones.

El objetivo del proyecto es explorar estos datos mediante consultas SQL ejecutadas en una base de datos SQLite, y visualizar los resultados utilizando Python y Matplotlib. A continuación, se detallan los pasos clave del proyecto:

## 1. Configuración de la Base de Datos:

 . Se crea una base de datos SQLite (hcare.db) y se configuran cuatro tablas principales: Patients, Conditions, Encounters, e Immunizations.
 . Los datos CSV se importan a estas tablas, permitiendo realizar análisis y consultas sobre los datos estructurados.

## 2. Consultas SQL y Análisis:

 .Se ejecutan varias consultas SQL para extraer información clave de los datos:
  1. Condiciones de un paciente específico.
  2. Condiciones diagnosticadas en un encuentro específico.
  3. Costo total de encuentros para un paciente.
  4. Paciente con mayor número de condiciones diagnosticadas.
  5. Encuentros más costosos por paciente.
  6. Condiciones más comunes entre pacientes.
  7. Edad promedio de los pacientes.
  8. Número de pacientes por estado.
  9. Proveedor que ha atendido más encuentros.
  10. Listado de pacientes fallecidos.

## 3. Visualización de Datos:

  .Se generan gráficos con Matplotlib para visualizar algunos de los resultados más relevantes:
   .Encuentros más costosos por paciente: Un gráfico de barras horizontal que muestra los 10 encuentros con mayor costo.
   .Condiciones más comunes: Un gráfico de barras vertical que muestra las 5 condiciones médicas más comunes entre los pacientes.

## 4. Conclusión:

El proyecto permite realizar un análisis profundo de los datos clínicos ficticios, identificando patrones y tendencias relevantes en la atención médica simulada.
Las visualizaciones facilitan la interpretación de los resultados, ofreciendo una visión clara de los datos más críticos.
