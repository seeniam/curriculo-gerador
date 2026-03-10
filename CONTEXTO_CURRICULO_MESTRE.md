# Contexto Completo Para Construir Meu Curriculo Mestre

## Objetivo deste arquivo

Este documento consolida absolutamente todo o contexto necessário para eu pensar, planejar e depois construir meu `curriculo_verdade` dentro deste projeto.

Ele serve para eu colar em outra IA, discutir estratégia, organizar minha trajetória e voltar depois para implementar os arquivos finais com consistência.

---

## O que este projeto faz

Este repositório e um gerador de curriculos customizados por vaga.

A logica geral e:

1. Existe um curriculo mestre muito completo em HTML.
2. Existe uma descricao de vaga em `.md`.
3. Existe uma persona com regras de escrita e posicionamento profissional.
4. Um script Python envia tudo isso para o Gemini.
5. O Gemini devolve um novo HTML adaptado para a vaga.

Em resumo:

- `default_pt.html` = base mestre em portugues
- `default.html` = base mestre em ingles
- `persona_headhunter_pt.md` = regras de adaptacao em portugues
- `persona_headhunter_en.md` = regras de adaptacao em ingles
- `vaga*.md` ou `job*.md` = vaga alvo
- `gerador_de_cv.py` = script que junta tudo e chama a IA

---

## Como o projeto funciona tecnicamente

### Arquivos principais

- `default_pt.html`
- `default.html`
- `persona_headhunter_pt.md`
- `persona_headhunter_en.md`
- `vaga_exemplo.md`
- `gerador_de_cv.py`
- `gerar_cv_automatico.bat`
- `.env` com `GEMINI_API_KEY`

### Fluxo exato do script

O script:

1. Le o `.env` e pega a chave `GEMINI_API_KEY`.
2. Procura o arquivo de vaga mais recente com nome `vaga*.md` ou `job*.md`.
3. Le:
   - a persona em portugues
   - a persona em ingles
   - o curriculo base em portugues
   - o curriculo base em ingles
   - a descricao da vaga
4. Monta um prompt unico gigante com todo esse contexto.
5. Pede ao Gemini para gerar somente o HTML final.
6. Remove eventuais blocos markdown como ```html.
7. Salva um novo arquivo `.html` com timestamp.

### Consequencia pratica

O ponto mais importante do projeto nao e o Python.

O ponto mais importante e a qualidade do conteudo de:

- `default_pt.html`
- `default.html`
- `persona_headhunter_pt.md`
- `persona_headhunter_en.md`

Se o `default` estiver fraco, incompleto ou generico, a saida da IA tambem ficara fraca.

---

## O papel real do `default_pt.html` e `default.html`

Esses arquivos nao sao curriculos comuns.

Eles funcionam como:

- base de conhecimento
- data lake da carreira
- inventario de experiencias
- repositório de conquistas
- mapa de tecnologias
- biblioteca de provas de senioridade

Ou seja:

eles devem conter muito mais informacao do que um curriculo final tradicional.

### Regra central

O `default` deve ser amplo, profundo, verdadeiro e reutilizavel.

Ele nao precisa ser curto.
Ele nao precisa ser enxuto.
Ele nao precisa parecer o PDF final perfeito.

Ele precisa ser rico o bastante para permitir que a IA escolha, reordene, destaque e adapte.

---

## O que o meu curriculo mestre precisa conter

Precisa conter tudo o que pode ser util para diferentes vagas, mesmo que nem sempre apareca no curriculo final.

### 1. Identidade profissional

- nome completo
- titulo profissional principal
- titulos alternativos que ainda sejam honestos
- cidade / estado / pais
- telefone
- e-mail
- LinkedIn
- GitHub
- portfolio
- site pessoal

### 2. Resumo profissional mestre

Um resumo forte, honesto e abrangente contendo:

- anos totais de experiencia
- areas em que atuo
- senioridade
- perfil tecnico e/ou de lideranca
- stacks dominadas
- tipo de problema que resolvo
- setores onde ja trabalhei
- resultados que costumo gerar

### 3. Competencias centrais

Lista ampla de competencias como:

- arquitetura de software
- backend
- frontend
- full stack
- cloud
- seguranca
- devops
- dados
- automacao
- integracoes
- APIs
- engenharia de plataforma
- observabilidade
- performance
- escalabilidade
- lideranca tecnica
- gestao de stakeholders
- discovery tecnico
- governanca
- modernizacao de sistemas
- reducao de custos
- melhoria operacional

### 4. Skills tecnicas detalhadas

Separadas ou agrupadas por categoria:

- linguagens
- frameworks
- bibliotecas
- bancos de dados
- cloud providers
- ferramentas de CI/CD
- containerizacao
- infraestrutura
- seguranca
- analytics
- observabilidade
- testes
- design systems
- mensageria
- ERPs / CRMs / plataformas especificas

Exemplos:

- JavaScript
- TypeScript
- Python
- Node.js
- React
- Next.js
- PostgreSQL
- MySQL
- Redis
- Docker
- Kubernetes
- AWS
- GCP
- Azure
- Terraform
- GitHub Actions
- GitLab CI
- Jenkins
- Linux
- Nginx
- Splunk
- Elasticsearch
- Prometheus
- Grafana

### 5. Experiencia profissional completa

Para cada empresa / contrato / consultoria / freela / sociedade / projeto relevante:

- nome da empresa
- tipo da empresa
- setor
- cargo oficial
- cargo funcional real, se diferente
- cidade / pais / remoto
- data de inicio
- data de fim
- vinculo
- contexto da empresa
- tamanho do time
- a quem eu respondia
- se eu liderava pessoas
- responsabilidades principais
- projetos tocados
- produtos / plataformas atendidas
- stack usada
- desafios tecnicos
- desafios de negocio
- decisoes importantes que tomei
- impacto gerado
- metricas
- resultados financeiros, operacionais ou tecnicos

### 6. Projetos estrategicos

Projetos que merecem destaque proprio:

- nome do projeto
- problema de negocio
- contexto tecnico
- papel exercido
- time envolvido
- stack
- arquitetura
- integracoes
- restricoes
- resultados
- numeros

### 7. Formacao academica

- curso
- instituicao
- inicio e fim
- situacao
- pos-graduacao
- MBA
- tecnico
- cursos longos

### 8. Certificacoes

- nome
- emissor
- ano
- validade
- status
- se esta em andamento

### 9. Idiomas

- idioma
- nivel real
- contexto de uso

### 10. Publicacoes, comunidades e presenca profissional

Se houver:

- palestras
- artigos
- mentorias
- open source
- comunidades
- voluntariado
- associacoes profissionais

### 11. Diferenciais complementares

- setores em que ja atuei
- tipos de produto
- experiencia internacional
- experiencia com times distribuidos
- experiencia com compliance
- experiencia com clientes enterprise
- experiencia com startups
- experiencia com consultoria

---

## Como deve ser o conteudo dentro do `default`

### Principio 1: verdade acima de marketing

O arquivo deve ser forte, mas baseado em fatos reais.

Pode haver refinamento de linguagem.
Pode haver melhor enquadramento.
Pode haver consolidacao.

Nao deve haver invencao de empresa, cargo, tecnologia ou resultado inexistente.

### Principio 2: riqueza acima de brevidade

Melhor ter informacao sobrando do que faltando.

Se uma experiencia teve:

- 2 grandes entregas
- 4 pequenas melhorias
- 3 tecnologias importantes
- 1 resultado mensuravel

coloque tudo no `default`.

### Principio 3: bullets de impacto

Evitar frases vagas como:

- "Responsavel por desenvolvimento"
- "Atuacao com sistemas diversos"
- "Participacao em projetos"

Preferir:

- "Desenvolvi e mantive APIs em Node.js e PostgreSQL para fluxos criticos de operacao, reduzindo retrabalho manual em 35%."
- "Estruturei pipeline de CI/CD com GitHub Actions, encurtando o tempo medio de deploy de 40 para 10 minutos."
- "Modelei integracoes entre sistemas internos e parceiros externos, melhorando a confiabilidade de processamento e reduzindo falhas operacionais."

### Principio 4: sempre contextualizar tecnologia

Nao listar tecnologia so por listar.

Melhor:

- "React para interfaces internas de operacao"
- "Python para automacoes e rotinas de tratamento de dados"
- "AWS para hospedagem, storage e servicos de integracao"

### Principio 5: incluir metricas sempre que possivel

Tipos de metricas:

- economia de tempo
- reducao de custo
- aumento de conversao
- melhora de performance
- disponibilidade
- SLA
- reducao de erro
- aumento de produtividade
- volume processado
- usuarios impactados

Se nao houver numero exato, registrar ordem de grandeza ou impacto concreto em linguagem honesta.

---

## Como o HTML atual deve ser entendido

Os arquivos `default_pt.html` e `default.html` existentes hoje funcionam como molde estrutural e referencia de densidade.

Eles mostram que o curriculo mestre pode ter:

- cabecalho profissional
- resumo
- competencias
- experiencia profissional longa
- portfolio de projetos
- certificacoes
- educacao

Nao e obrigatorio copiar o texto atual.
O ideal e aproveitar:

- a ideia de estrutura
- a separacao de secoes
- o formato de bullets
- a nocao de um documento HTML pronto para ser transformado em PDF

---

## O que eu preciso decidir antes de construir meu `curriculo_verdade`

### 1. Meu posicionamento principal

Quais titulos me representam melhor, por exemplo:

- Software Engineer
- Senior Software Engineer
- Full Stack Engineer
- Backend Engineer
- Tech Lead
- Solutions Architect
- Product Engineer
- DevOps Engineer
- Security Engineer

### 2. Meu recorte de mercado

Quais vagas eu quero atacar:

- backend
- full stack
- arquitetura
- lideranca tecnica
- produto
- plataforma
- cloud
- seguranca
- dados

### 3. Meu nivel de senioridade

Como me posicionar com honestidade:

- pleno
- senior
- staff
- especialista
- lider tecnico

### 4. Minha narrativa profissional

Exemplos de narrativa:

- generalista forte com amplitude tecnica
- especialista em backend e integracoes
- perfil de produto com execucao tecnica
- arquiteto pragmático orientado a negocio
- engenheiro com foco em modernizacao e automacao

### 5. O que eu nao quero parecer

Tambem e importante listar:

- nao quero parecer inflado
- nao quero parecer generico
- nao quero parecer junior com linguagem rebuscada
- nao quero parecer gestor se meu foco for tecnico
- nao quero parecer full stack se meu ponto forte for backend

---

## Estrutura recomendada do meu futuro `curriculo_verdade`

### Secao 1. Header

Deve conter:

- nome
- titulo profissional
- localizacao
- contatos
- links

### Secao 2. Resumo profissional

Deve responder:

- quem sou profissionalmente
- quantos anos de experiencia tenho
- em que sou forte
- que tipo de resultado entrego
- em que nivel atuo

### Secao 3. Core Competencies / Competencias principais

Lista curta e estrategica de dominios.

### Secao 4. Technical Skills / Skills tecnicas

Lista mais objetiva e abrangente de tecnologias.

### Secao 5. Professional Experience / Experiencia profissional

Cada item com:

- cargo
- empresa
- periodo
- local
- bullets de impacto

### Secao 6. Strategic Projects / Projetos relevantes

Escolher projetos que mostrem:

- complexidade
- senioridade
- autonomia
- impacto

### Secao 7. Certifications

Lista limpa.

### Secao 8. Education

Lista limpa.

### Secao 9. Languages

Se fizer sentido.

---

## O que preciso levantar sobre cada experiencia da minha carreira

Para cada trabalho, eu deveria responder:

1. Qual era o nome da empresa?
2. Qual era meu cargo oficial?
3. Qual era meu papel real no dia a dia?
4. Qual era o periodo exato?
5. A empresa era de que setor?
6. O que eu construia ou mantinha?
7. Quem eram os usuarios ou clientes?
8. Quais tecnologias usei?
9. Quais integracoes existiam?
10. Quais problemas eu resolvi?
11. Quais melhorias entreguei?
12. Houve automacao?
13. Houve lideranca?
14. Houve desenho de arquitetura?
15. Houve contato com stakeholders?
16. Houve escala, performance, seguranca ou disponibilidade?
17. Quais metricas consigo citar?
18. O que dessa experiencia vale para vagas futuras?

---

## O que preciso levantar sobre meus projetos

Para cada projeto importante:

1. Nome do projeto
2. Objetivo
3. Problema de negocio
4. Papel exercido
5. Time envolvido
6. Stack tecnica
7. Decisoes arquiteturais
8. Integracoes
9. Complexidade principal
10. Resultado final
11. Metricas
12. O que esse projeto prova sobre mim

---

## O que preciso levantar sobre mim como profissional

### Identidade profissional

- Que tipo de engenheiro/profissional eu sou?
- Onde sou mais forte?
- O que me diferencia?
- Onde tenho mais profundidade?
- Onde tenho mais versatilidade?

### Evidencias de senioridade

- tomei decisoes tecnicas importantes?
- liderei entregas?
- destravei projetos?
- melhorei processos?
- reduzi incidentes?
- mentorei pessoas?
- falei com negocio?
- priorizei trade-offs?

### Evidencias de impacto

- economizei dinheiro?
- economizei tempo?
- aumentei confiabilidade?
- melhorei experiencia do usuario?
- acelerei entregas?
- reduzi risco?
- aumentei receita?

---

## O que um bom curriculo mestre nao pode deixar faltar

- experiencias antigas que sustentam base tecnica
- experiencias recentes que mostram maturidade
- tecnologias dominadas
- resultados concretos
- contexto de negocio
- sinais de senioridade
- projetos relevantes
- certificacoes e formacao
- versao em portugues
- versao em ingles

---

## O que normalmente falta quando alguem monta um `default` ruim

- bullets genericos
- falta de metricas
- falta de contexto de negocio
- lista de tecnologias sem prova de uso
- experiencias resumidas demais
- ausencia de projetos
- resumo profissional generico
- titulo profissional confuso
- ingles improvisado
- inconsistencias entre datas, cargos e stacks

---

## Como conversar com outra IA para me ajudar a pensar

Eu posso usar este contexto para pedir ajuda em etapas.

### Pedido 1. Descobrir minha narrativa profissional

"Com base neste contexto, me ajude a definir meu posicionamento profissional, meus titulos mais fortes, minhas narrativas possiveis e como eu devo me apresentar para o mercado."

### Pedido 2. Mapear lacunas de informacao

"Com base neste contexto, crie uma lista exaustiva de perguntas para eu responder sobre minha carreira, para que depois seja possivel montar um curriculo mestre muito completo."

### Pedido 3. Organizar experiencias

"Com base neste contexto, me ajude a transformar minhas experiencias profissionais brutas em bullets fortes, honestos, orientados a impacto e com densidade suficiente para um curriculo mestre."

### Pedido 4. Organizar projetos

"Me ajude a identificar quais projetos da minha carreira merecem uma secao propria e como descreve-los com contexto tecnico, impacto e senioridade."

### Pedido 5. Criar versao bilingue

"Me ajude a pensar como converter meu curriculo mestre em portugues para uma versao forte em ingles, sem traducoes literais ruins."

---

## Prompt sugerido para colar em outra IA

Use este prompt junto com este arquivo:

```text
Quero construir um curriculo mestre completo para ser usado por um gerador de curriculos customizados com IA.

Leia com atencao todo o contexto abaixo e me ajude a pensar estrategicamente antes de escrever os arquivos finais.

Eu ainda nao quero o HTML final.
Eu quero primeiro:

1. descobrir meu melhor posicionamento profissional
2. identificar tudo o que preciso levantar sobre minha carreira
3. montar uma estrutura exaustiva de informacoes
4. definir como transformar minha trajetoria em um curriculo mestre rico, honesto e reaproveitavel
5. listar perguntas importantes que eu devo responder
6. sugerir um plano para depois construir `default_pt.html` e `default.html`

Quero profundidade maxima, sem resumir demais e sem pular etapas.

[cole aqui o conteudo completo deste arquivo]
```

---

## Checklist do que eu preciso reunir antes de voltar para implementar

### Dados pessoais

- nome completo
- cidade / pais
- telefone
- e-mail
- LinkedIn
- GitHub
- portfolio

### Posicionamento

- titulo principal
- titulos alternativos
- senioridade
- foco de vagas
- narrativa profissional

### Carreira

- lista completa de experiencias
- cargos
- datas
- responsabilidades
- entregas
- stacks
- resultados
- metricas

### Projetos

- nome
- contexto
- papel
- stack
- impacto

### Formacao

- cursos
- instituicoes
- datas

### Certificacoes

- nome
- emissor
- ano
- status

### Idiomas

- idioma
- nivel

### Diferenciais

- open source
- comunidades
- palestras
- artigos
- lideranca
- mentoria

---

## Resultado esperado da proxima fase

Depois de refletir com ajuda de outra IA e reunir meus dados, a proxima etapa sera voltar a este projeto para:

1. construir meu `default_pt.html` completo
2. construir meu `default.html` equivalente
3. revisar a narrativa e a densidade do conteudo
4. validar coerencia entre cargos, datas, skills e projetos
5. preparar meu `curriculo_verdade` como base definitiva para customizacao por vaga

---

## Resumo final em uma frase

Eu nao estou tentando criar apenas um curriculo bonito.

Estou tentando construir uma base de conhecimento profissional completa, bilingue, estruturada e reutilizavel, que permita gerar versoes altamente adaptadas para vagas diferentes sem perder autenticidade, densidade tecnica e consistencia de carreira.
