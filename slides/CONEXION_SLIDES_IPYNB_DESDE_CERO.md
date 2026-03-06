# Conexión slides ↔ notebooks (desde 0)

Este mapa sirve para estudiar el curso en orden, conectando teoría y práctica.

## 1) Fundamentos de aprendizaje (Día 1)

### Idea base
Aprender significa ajustar parámetros para minimizar una función de pérdida.

$$
\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}(\theta)
$$

### Cuadernos
- `dia1/1_gradiente_descendente.ipynb`: intuición de gradiente descendente y efecto del learning rate.
- `dia1/2_los_tres_ingredientes.ipynb`: modelo + pérdida + optimizador; mini-batches.
- `dia1/3_regularizacion.ipynb`: overfitting y técnicas (L1/L2, dropout, early stopping).
- `dia1/4_ejercicio_final.ipynb`: pipeline completo de entrenamiento/evaluación.

## 2) Texto secuencial clásico (Día 2)

### Idea base
Un LM asigna probabilidad a secuencias y predice el siguiente token:

$$
P(w_{1:T})=\prod_{t=1}^{T} P(w_t\mid w_{<t})
$$

Pérdida (NLL):
$$
\mathcal{L}=-\sum_t\log P(w_t\mid w_{<t})
$$

Perplexity:
$$
\mathrm{PPL}=\exp\Big(\frac{1}{N}\sum_t -\log P(w_t\mid w_{<t})\Big)
$$

### Cuadernos
- `dia2/tokenizer_rnn_lstm_gru.ipynb`: tokenización + RNN/LSTM/GRU + LM y comparación de estabilidad/rendimiento.

## 3) Encoders y Transformer (Día 3)

### Idea base
Un encoder produce representaciones contextuales para tareas discriminativas (clasificación, NER).

Atención:
$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### Cuadernos
- `dia3/1_encoder.ipynb`: encoder para clasificación.
- `dia3/2_encoder_random.ipynb`: comparación con baseline aleatorio.
- `dia3/3_ejercicio_encoder.ipynb`: fine-tuning completo (dataset, tokenización, trainer, métricas).
- `dia3/token_classification.ipynb`: clasificación por token (NER-like).
- `dia3/transformer.ipynb`: bloques Transformer y atención.
- `dia3/transformer_solucion.ipynb`: versión completa/solución.

## 4) Decoders, ajuste fino y agentes (Día 4)

### Idea base
Los decoders generan texto token a token, y se pueden adaptar por SFT o LoRA.

SFT:
$$
\mathcal{L}_{SFT}=-\sum_t\log P_\theta(y_t\mid x,y_{<t})
$$

LoRA:
$$
W' = W + BA,\quad r\ll d,k
$$

Decoding con temperatura:
$$
p_t=\mathrm{softmax}(z_t/\tau)
$$

### Cuadernos
- `dia4-1/4_decoder.ipynb`: fundamentos de decoder y prompting.
- `dia4-1/5_decoder_sft_1.ipynb`: SFT clásico.
- `dia4-1/5_decoder_sft_lora.ipynb`: SFT eficiente con LoRA.
- `dia4-1/6_numero_parametros.ipynb`: coste de parámetros totales vs entrenables.
- `dia4-1/7_inferencia_hf.ipynb`: inferencia y estrategias de decoding.
- `dia4-2/0_ollama.ipynb`: inferencia local con Ollama.
- `dia4-2/1_smolagents.ipynb`: agente con tools (razonamiento + acción).
- `dia4-2/2_langchain_agent.ipynb`: orquestación de agentes con LangChain.

## Cómo estudiar (ruta recomendada)
1. Lee la teoría en `slides/` del bloque correspondiente.
2. Abre el notebook del bloque y ejecuta celdas en orden.
3. Anota: entrada, salida, métrica y por qué cambia.
4. Cierra cada bloque respondiendo: qué aprende el modelo, cómo lo aprende y cómo se evalúa.

## Checklist de comprensión mínima (desde 0)
- Entiendes qué es una función de pérdida y por qué se minimiza.
- Puedes explicar diferencia entre encoder y decoder.
- Sabes interpretar accuracy/F1 y también perplexity.
- Sabes cuándo usar SFT completo o LoRA.
- Entiendes qué aporta un agente frente a un LLM “solo chat”.