## Actividad 1 – Introducción a DevOps y DevSecOps

**Curso:** CC3S2 Desarrollo de Software  
**Estudiante:** <Tu nombre>  
**Fecha:** 30/08/2025  
**Tiempo invertido:** 1h:30min  

**Entorno usado (breve y sin datos sensibles):**  
Navegador web (DevTools), sitios públicos para DNS/TLS y diagramado en draw.io/Excalidraw.  
*(Sin credenciales ni tokens).*

---

### 1. DevOps vs. Cascada Tradicional

- **Imagen:** `imagenes/devops-vs-cascada.png`  
- **Síntesis:**  
  DevOps acelera y reduce riesgo en la nube al acortar ciclos de feedback, trabajar en lotes pequeños, automatizar pruebas y despliegues y alinear Dev–Ops. Esto reduce *lead time*, tasa de fallos y mejora MTTR (métricas DORA [1]).  
  La **configuración externa** y **port binding** (12-Factor [2]) favorecen reproducibilidad entre entornos.

- **Contexto válido para cascada:**  
  - Sistemas con certificaciones regulatorias estrictas (p. ej., médicos/aeronáuticos).  
  - *Criterio 1:* cada release requiere evidencia de conformidad (checklist firmado por QA externo).  
  - *Criterio 2:* cambios agrupados con aprobación regulatoria.  
  - *Trade-off:* velocidad baja vs. conformidad/seguridad alta.

---

### 2. Ciclo Tradicional y Silos

- **Imagen:** `imagenes/silos-equipos.png`  
- **Limitaciones sin CI:**  
  - Lotes grandes → más retrabajos y regresiones.  
  - Colas de defectos y costo de integración tardía.  
- **Anti-patrones:**  
  - *Throw over the wall:* Dev entrega sin contexto → MTTR alto.  
  - *Seguridad tardía:* hallazgos al final → bloqueos y retrabajos.

---

### 3. Principios y Beneficios de DevOps

- **CI/CD:** cambios pequeños, pruebas automatizadas, pipelines reproducibles, trunk-based y feature flags.  
- **Agile como precursor:** dailies y retrospectivas guían qué promover o bloquear.  
- **Indicador observable (no financiero):**  
  - Tiempo desde PR listo → despliegue en pruebas (p50).  
  - *Cómo medir:* metadatos de PR + bitácora de despliegue.  
  - *Meta:* reducir en **30%** en 4 iteraciones.

---

### 4. Evolución a DevSecOps

- **SAST:** análisis estático temprano en artefactos y dependencias.  
- **DAST:** dinámico, sobre la aplicación en ejecución.  
- **Gate mínimo de seguridad:**  
  - SAST: **0** vulnerabilidades críticas/altas (CVSS ≥ 7.0).  
  - DAST: **≥ 80%** de cobertura en rutas críticas.  
- **Política de excepción:**  
  - Máx. 7 días.  
  - Responsable: *Líder técnico (J. Díaz)*.  
  - Plan: mitigación temporal (WAF) + corrección.  
- **Evitar “teatro de seguridad”:**  
  - Hallazgos repetidos ≤ 5%.  
  - Tiempo de remediación ≤ 48h.  
- **Marco de apoyo:** NIST SSDF [3].

---

### 5. CI/CD y Estrategias de Despliegue

- **Imagen:** `imagenes/pipeline_canary.png`  
- Estrategia: **Canary** (ejemplo: microservicio de autenticación).  

**Riesgos vs. Mitigaciones**

| Riesgo                 | Mitigación                                                      |
|------------------------|-----------------------------------------------------------------|
| Regresión funcional    | Validación de contrato + smoke tests antes de promover           |
| Costo de convivencia   | Ventana de canary de 60 min + rollback automático                |
| Manejo de sesiones     | Draining de conexiones + esquemas compatibles + sticky sessions |

**KPIs de promoción/rollback**  
- KPI técnico: **Errores 5xx ≤ 0.1%** en la primera hora post-canary.  
- KPI de producto: **Conversión ≥ 95%** del baseline pre-release.  
- **Coexistencia:** aunque los KPIs técnicos estén “verdes”, una caída en conversión puede indicar regresión funcional/UX. Por ello, ambos métricas forman parte del gate.

---

### 6. Evidencia Práctica (sin comandos)

#### 6.1 HTTP – contrato observable
- **Imagen:** `imagenes/http-evidencia.png`  
- Ejemplo: GET → 200, cabeceras `Cache-Control: max-age=3600` y `X-Request-ID`.  
- Importancia: caché mejora latencia; request-id habilita trazabilidad.

#### 6.2 DNS – nombres y TTL
- **Imagen:** `imagenes/dns-ttl.png`  
- Ejemplo: registro A, TTL=3600s. TTL alto retrasa rollbacks; TTL bajo acelera cambios pero aumenta consultas.

#### 6.3 TLS – seguridad en tránsito
- **Imagen:** `imagenes/tls-cert.png`  
- Ejemplo: CN=example.com, SAN=www.example.com, válido hasta 2025.  
- Si falla cadena: errores de confianza y riesgo MITM.

#### 6.4 Puertos – estado de runtime
- **Imagen:** `imagenes/puertos.png`  
- Ejemplo: 80 (HTTP) y 443 (HTTPS). Falta de 443 = despliegue TLS incompleto.

#### 6.5 12-Factor
- **Port binding:** parametrizar el puerto externamente.  
- **Logs:** a stdout, no rotación manual.  
- **Anti-patrón:** credenciales en repo → rompe reproducibilidad y seguridad.

#### 6.6 Checklist de diagnóstico (intermitencia simulada)

| Paso | Objetivo | Evidencia esperada | Interpretación | Acción siguiente |
|-----:|----------|--------------------|----------------|------------------|
| 1 | Validar contrato HTTP | 2xx/3xx y cabeceras esperadas | 4xx/5xx o cabeceras faltantes = contrato roto | Revisar routing/backends |
| 2 | Verificar DNS y TTL | Registros A/CNAME consistentes | Divergencias o TTL alto → propagación lenta | Esperar ventana o ajustar rollback |
| 3 | Revisar TLS | Cert válido, CN/SAN correctos, emisora confiable | Cert caducado o mismatch → errores de confianza | Renovar o corregir cadena |
| 4 | Puertos en escucha | 80/443 expuestos por servicio correcto | 443 ausente = despliegue incompleto; conflicto de puerto | Exponer listener TLS o liberar puerto |
| 5 | Comparar canary vs control | 5xx ≤ 0.1% y p95 estable en 1h | KPI superado = regresión técnica | Rollback inmediato |
| 6 | Logs de correlación | Request-ID extremo a extremo | Falta correlación = no hay trazabilidad | Habilitar middleware de tracing |

---

### 7. Desafíos de DevOps y Mitigaciones

- **Imagen:** `imagenes/desafios_devops.png`  

**Riesgos y mitigaciones concretas:**  
- Cambios no observables → feature flags + rollback probado.  
- Blast radius amplio → canary + límites de tráfico.  
- Error humano → revisión cruzada + runbooks automatizados.  

**Experimento controlado (canary vs big-bang):**  
- Métrica: 5xx y p95 en 60 min.  
- Control: release big-bang previo.  
- Éxito: canary reduce fallos ≥ 50%.  
- Reversión: rollback si KPI supera umbral.

---

### 8. Arquitectura Mínima para DevSecOps

- **Imagen:** `imagenes/arquitectura-minima.png`  
- Flujo: Cliente → DNS → HTTP → TLS.  
- Controles: caché, validación de certificados, contratos API, rate limiting.  
- Principios 12-Factor aplicados:  
  - Config por entorno: diffs mínimos, fácil auditoría.  
  - Logs a stdout: trazabilidad (correlación con X-Request-ID).

---

### Evidencias Incluidas

- Estado HTTP + 2 cabeceras.  
- Registro DNS + TTL.  
- CN/SAN y vigencia TLS.  
- Puertos en escucha.  
- Gates de seguridad con umbrales.  
- KPI técnico + KPI de producto coexistentes.  
- Checklist operativo con decisiones claras.  
- Diagramas y capturas con marcas visuales.

---

### Trazabilidad de Commits

- Estructura de actividad 1  
- Día 1 – Comparativos e imágenes base  
- Día 2 – DevSecOps y estrategia de despliegue  
- Día 3 – Evidencia, diagramas y entrega final  
- Entrega actividad 1

---

## Referencias

[1] DORA – The Four Keys (Software Delivery Metrics). https://dora.dev/guides/dora-metrics-four-keys/  
[2] The Twelve-Factor App. https://12factor.net/  
[3] NIST SP 800-218 – Secure Software Development Framework (SSDF). https://csrc.nist.gov/pubs/sp/800/218/final  
[4] Google SRE Workbook – Canarying Releases. https://sre.google/workbook/canarying-releases/  
[5] OWASP ASVS. https://owasp.org/www-project-application-security-verification-standard/

