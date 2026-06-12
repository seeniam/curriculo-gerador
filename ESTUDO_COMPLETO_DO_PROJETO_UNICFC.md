# Estudo Completo do Projeto `unicfcead-rs`

## 1. Resumo executivo

Este projeto é uma aplicação Ruby on Rails monolítica voltada para operação de uma plataforma EAD e de aulas remotas/presenciais para formação de condutores, com forte acoplamento a regras estaduais de DETRAN, gestão de matrículas, certificados, pagamentos, relatórios, biometria, vendas e operação de CFCs.

O sistema não é apenas um LMS. Ele funciona como:

- portal público de vendas e captação;
- backoffice administrativo;
- portal de CFC/empresa;
- portal de aluno;
- portal de instrutor;
- portal de palestrante;
- portal de empresa matriz/revenda;
- módulo de coleta biométrica;
- API de integração para sistemas terceiros;
- hub de integrações com DETRANs, pagamentos, videoconferência, armazenamento e faturamento.

## 2. Dados objetivos da base

Levantamento da estrutura atual do repositório:

- `116` arquivos em `app/controllers`
- `140` arquivos em `app/models`
- `29` arquivos em `app/services`
- `1303` arquivos em `app/views`
- `558` migrations em `db/migrate`
- não existe suíte automatizada em `test/` ou `spec/`

Isso indica um monólito maduro, grande, com muita regra de negócio acumulada e baixo isolamento automatizado para regressões.

## 3. Stack principal

### Backend

- Ruby `2.7.2`
- Rails `5.2.4.4`
- MySQL via `mysql2`
- Puma configurado, mas o deploy principal parece usar Nginx + Passenger no container
- ActiveRecord
- ActionCable habilitado
- Sprockets para assets
- Slim para templates

### Autenticação e sessão

- `devise`
- `devise-security`
- `google-authenticator-rails`
- MFA administrativo com fluxo dedicado
- `session_limitable` em alguns modelos

### Banco e particionamento

- MySQL
- `ar-octopus` para shard switching
- shards principais:
  - `production`
  - `production_sc`

### Uploads e arquivos

- `paperclip`
- `delayed_paperclip`
- armazenamento local em desenvolvimento
- AWS S3 em produção

### Integrações externas relevantes

- DETRAN RS
- DETRAN PR
- DETRAN SC
- DETRAN SP
- DETRAN MS
- DETRAN MG
- DETRAN MT
- DETRAN RJ
- DETRAN AL
- DETRAN AC
- DETRAN PE
- SERPRO
- Zoom
- Webex
- Microsoft Teams / Azure
- Conta Azul
- Pagar.me
- UnitegPag
- AWS Rekognition
- SendGrid

### Frontend e assets

- Rails assets pipeline
- CoffeeScript legado
- jQuery / jquery-ui
- CSS tradicional
- pequeno uso de Node: `@microsoft/teams-js`

## 4. Identidade do produto

A aplicação atende o ecossistema UniCFC EAD e parceiros. Os nomes, layouts, assets e domínios indicam operação multi-marca/multiportal, incluindo:

- `unicfcead`
- `parceirocfc`
- `ceatt`
- variações por UF como AC e PE

Há também suporte visual e operacional para diferentes layouts:

- `app`
- `admin`
- `student`
- `training_center`
- `coach`
- `teacher`
- `collection_user`
- `reseller`
- `contract`
- layouts de confirmação de senha e seleção de CFC

## 5. Arquitetura funcional por domínio

### 5.1 Domínio de usuários e perfis

Perfis autenticáveis encontrados:

- `Admin`
- `Institute`
- `TrainingCenter`
- `Coach`
- `Student`
- `Teacher`
- `Reseller`
- `CollectionUser`

Cada um possui portal próprio, rotas próprias e, em vários casos, regras específicas de primeiro acesso, troca obrigatória de senha, permissões, visualização de dados e workflows de negócio.

### 5.2 Domínio acadêmico / educacional

Entidades centrais:

- `Course`
- `Moduluse`
- `Unit`
- `Question`
- `QuestionAlternative`
- `Evaluation`
- `Valuation`
- `Simulate`
- `Testing`
- `TestingQuestion`
- `StudentUnit`
- `Matriculation`
- `Certificate`

Responsabilidades:

- cadastro de cursos;
- vínculo de módulos, unidades e questões;
- avaliações modulares;
- simulados;
- provas;
- progressão do aluno;
- geração e emissão de certificados;
- regras de curso EAD e curso remoto.

### 5.3 Domínio de aulas remotas e presenciais

Entidades centrais:

- `Classroom`
- `ClassroomStudent`
- `ClassroomCoachValidation`
- `ClassroomStudentValidation`
- `ClassroomVideo`
- `ClassroomParticipant`
- `ClassroomRandomImage`
- `ClassroomStudentControl`
- `ClassroomPresence`
- `ClassroomLesson`
- `ClassroomLessonParticipant`
- `ClassroomLessonImage`

Capacidades identificadas:

- agendamento de aulas remotas;
- controle de duração e intervalo;
- presenças;
- validação biométrica inicial, aleatória e final;
- gravação e armazenamento de evidências;
- controle por disciplina/módulo;
- suporte a aulas presenciais;
- contingência;
- fechamento manual/offline;
- relatórios de presença e permanência.

### 5.4 Domínio comercial e financeiro

Entidades centrais:

- `Order`
- `OrderItem`
- `CreditOrder`
- `CreditOrderQuantity`
- `FinancialOrder`
- `FinancialOrderItem`
- `FinancialOrderBillet`
- `FinancialOrderInvoice`
- `TrainingCenterCourse`
- `Contract`
- `TrainingCenterContract`

Capacidades:

- venda pública de cursos e documentos;
- pedidos por aluno;
- compra de créditos por CFC;
- recorrência;
- faturamento;
- geração de registros financeiros;
- integração Conta Azul;
- pagamento via boleto, pix e cartão;
- relatórios financeiros e de comissões;
- autorais e comissionamento.

### 5.5 Domínio institucional / conteúdo

Entidades:

- `Slider`
- `Banner`
- `Article`
- `ArticleImage`
- `FaqQuestion`
- `Tutorial`
- `Message`
- `Notification`
- `Event`
- `Archive`
- `Material`
- `Document`

Funções:

- home pública;
- blog;
- FAQ;
- banners por público/UF;
- tutoriais por tipo de usuário;
- biblioteca virtual;
- materiais didáticos;
- comunicação e avisos.

### 5.6 Domínio biométrico e coleta

Entidades:

- `Conductor`
- `ConductorImage`
- `ConductorSignature`
- `ConductorFingerprint`
- `StudentBiometricsMg`
- `UnitBiometric`
- `MatriculationValidation`

Capacidades:

- coleta facial;
- coleta de assinatura;
- coleta de digitais;
- prova de vida;
- biometria por aula;
- biometria por unidade;
- módulo de coleta separado para candidatos/condutores.

## 6. Estrutura de rotas e portais

O arquivo `config/routes.rb` é extenso e confirma o caráter multiportal.

### Portais/autenticação por path

- `/administrador`
- `/gerenciador`
- `/centro-de-formacao`
- `/instrutor`
- `/aluno`
- `/palestrante`
- `/empresa-matriz`
- `/sistema-coleta`

### Áreas funcionais maiores

- área pública
- área administrativa
- área de CFC
- área do aluno
- área do instrutor
- área do palestrante
- área do revendedor/matriz
- área de coleta
- API

### Observações relevantes

- há muitos endpoints customizados por recurso;
- várias rotas são específicas por UF;
- há rotas para exportações CSV/PDF;
- há rotas para reenvio de integração, bloqueio/desbloqueio, emissão de certificado, biometria, contingência e relatórios;
- a API mistura funções de cadastro, consulta, integração e callbacks.

## 7. Modelos centrais analisados

### `Student`

Pontos importantes:

- usa `devise` com autenticação por CPF ou e-mail;
- usa `friendly_id`;
- tem muitos relacionamentos: matrículas, certificados, fóruns, avaliações, provas, logs, presenças;
- aplica política de senha forte;
- possui upload de imagem e arquivo de log;
- envia e-mail de cadastro em alguns cenários;
- guarda vínculo com múltiplos CFCs.

Isso mostra que o aluno é uma entidade transversal do sistema.

### `TrainingCenter`

É uma das entidades mais complexas do projeto.

Responsabilidades observadas:

- autenticação própria;
- flags de comportamento por feature;
- configuração comercial, operacional e de integração;
- associação a cursos, salas, zoom users, webex users, contratos, créditos, admins e diretores;
- regras de vencimento contratual;
- regras de recorrência;
- regras de bloqueio financeiro;
- provas, aulas remotas, biometria e emissão.

O grande volume de scopes booleanas mostra alta parametrização por cliente/CFC.

### `Course`

Responsabilidades:

- estrutura do curso;
- preço;
- módulos, unidades, questões e estados;
- imagens e banner;
- plano de estudos;
- metadados de integração por UF;
- tipos de curso, curso livre, curso remoto, certificado remoto, prova de vida etc.

O modelo mistura conteúdo, catálogo, vendas e integração regulatória.

### `Matriculation`

É uma entidade de negócio central.

Responsabilidades:

- vínculo aluno + curso + CFC;
- status de autorização;
- ticket de ativação;
- datas de início e término;
- integração estadual;
- preço;
- emissão de e-mails;
- consumo de créditos;
- relatórios;
- documentos de conclusão.

Há callbacks relevantes em `after_create` e `after_update`, o que indica lógica implícita sensível.

### `Classroom`

Responsabilidades:

- agenda da aula;
- duração;
- vínculo com curso, instrutor, turma e CFC;
- token de acesso;
- arquivos;
- alunos;
- presenças;
- validações;
- vídeos e rastros operacionais.

É o núcleo operacional das aulas remotas.

### `Certificate`

Responsabilidades:

- geração de número e código;
- relacionamento com matrícula, aluno, curso e CFC;
- composição de número específico por UF;
- preparação para integração com DETRAN.

O método `generate_certificate_number_send_detran` concentra regras estaduais importantes.

## 8. Serviços de aplicação

Arquivos de serviço encontrados:

- `application_service.rb`
- `certificate_service.rb`
- `cfc_produtivo_services.rb`
- `conta_azul_services.rb`
- `course_service.rb`
- `create_zoom_meetings.rb`
- `detran_ac_services.rb`
- `detran_es_services.rb`
- `detran_mg_services.rb`
- `detran_ms_services.rb`
- `detran_mt_services.rb`
- `detran_pe_services.rb`
- `detran_pr_services.rb`
- `detran_rj_services.rb`
- `detran_sc_services.rb`
- `detran_signatures_service.rb`
- `detran_sp_services.rb`
- `ecnh_sp_services.rb`
- `integration_whats_app_business_service.rb`
- `jitsi_services.rb`
- `matriculation_service.rb`
- `microsoft_teams_service.rb`
- `rekognition_validator.rb`
- `shareable_methods_service.rb`
- `status_services.rb`
- `student_service.rb`
- `uniteg_pag_services.rb`
- `validator_password_service.rb`
- `zoom.rb`

### Leituras feitas

#### `CertificateService`

Implementa emissão de certificado para pelo menos:

- RS
- PR
- AL

Características:

- integrações HTTP manuais com `Net::HTTP` e `Faraday`;
- montagem manual de payloads;
- tratamento por status HTTP;
- regras diferentes por curso/UF;
- hardcode de CPF de instrutor em trechos;
- retentativas manuais em alguns fluxos.

#### `DetranMsServices`

Implementa:

- envio de matrícula;
- envio de certificado;
- consulta de dados de CFC;
- consulta de instrutor;
- consulta de aluno;
- autenticação em serviço ICE;
- fluxos para aulas remotas.

Características:

- token calculado manualmente;
- parsing manual de XML convertido em string;
- forte acoplamento ao formato do fornecedor;
- atualização direta das matrículas/certificados na resposta.

#### `ContaAzulServices`

Implementa:

- obtenção e renovação de token OAuth;
- consulta, criação e atualização de cliente;
- criação, atualização e exclusão de venda;
- listagem de serviços e bancos.

Características:

- integração síncrona;
- persistência de token em `ContaAzulCredential`;
- geração de payload financeiro baseada no estado do pedido/fechamento;
- atualização de `FinancialOrder`.

## 9. Fluxos principais do negócio

### 9.1 Cadastro/matrícula de aluno

Fluxo típico identificado:

1. aluno é localizado ou criado;
2. aluno é vinculado ao CFC;
3. matrícula é criada;
4. matrícula passa por autorização local ou integração com DETRAN;
5. callbacks definem número, preço, admin comissionado, tipo do pedido e envio de e-mail.

### 9.2 Curso EAD

Fluxo típico:

1. CFC ou API cria matrícula;
2. aluno acessa portal;
3. faz aceite de termos;
4. percorre unidades;
5. faz avaliações/simulados;
6. conclui requisitos;
7. certificado é gerado;
8. certificado pode ser enviado ao DETRAN conforme UF.

### 9.3 Aula remota

Fluxo típico:

1. CFC agenda aula;
2. alunos são vinculados;
3. aula usa Zoom/Jitsi/Webex/Teams conforme configuração;
4. ocorrem validações biométricas;
5. sistema registra presenças, imagens e vídeos;
6. aula é finalizada e pode ser integrada ao DETRAN.

### 9.4 Comercial/financeiro

Fluxo típico:

1. curso ou crédito é vendido;
2. pedido é criado;
3. item é vinculado;
4. pagamento retorna status;
5. fechamento financeiro é consolidado;
6. Conta Azul recebe cliente/venda;
7. relatórios financeiros são exportados.

## 10. Banco de dados e shard strategy

### `database.yml`

Há configuração explícita para:

- `development`
- `development_sc`
- `production`
- `production_sc`

### `shards.yml`

`ar-octopus` está configurado para:

- ambiente `development`
- ambiente `production`
- shard principal `production`
- shard `production_sc`

### Uso dos shards

Os controladores base de vários portais usam `prepend_around_action :select_shard`.

Padrão encontrado:

- se sessão/param indicar `SC`, usa shard `production_sc`;
- caso contrário, usa `production`.

Conclusão: Santa Catarina tem base separada do restante da operação.

## 11. Infraestrutura e deploy

### Container

`Dockerfile` indica:

- imagem base customizada da AWS ECR;
- instalação de Ruby, bundler, Node, ImageMagick e libs nativas;
- instalação de Passenger + Nginx;
- scripts `start_build` e `start`;
- exposição da porta `3000`.

### CI/CD

Há pasta `codebuild/` com:

- `buildspec.yaml`
- `build.sh`
- `deploy.sh`

Pipeline observado:

1. autentica no ECR;
2. builda a imagem Docker;
3. envia a imagem para o repositório;
4. assume role AWS;
5. atualiza kubeconfig do EKS;
6. faz `helm upgrade --install`.

### Helm

Há chart em `helm-chart/` com:

- deployment
- service
- ingress
- HPA
- secrets

### Observação

O `Chart.yaml` está nomeado como `unicfc-monitoramento`, o que sugere reaproveitamento de chart/template ou naming inconsistente com a aplicação real.

## 12. Configuração operacional

### `config/application.rb`

Pontos relevantes:

- timezone `Buenos Aires`
- locale `pt-br`
- exceções roteadas via `config.exceptions_app = self.routes`
- `Rack::Deflater`
- CORS liberado para qualquer origem `*`
- leitura de `config/local_env.yml`

### `config/environments/production.rb`

Concentra quase toda a configuração operacional:

- controle de produção/homologação por `environment_controll`
- Redis cache
- SSL forçado
- URLs dos DETRANs
- chaves/tokens
- credenciais de envio de e-mail
- base URLs
- S3 paths
- integrações de pagamento
- Azure/Teams
- Conta Azul
- UnitegPag

### `config/schedule.rb`

O uso de `whenever` está praticamente desativado/comentado.

## 13. Assets, interface e experiência

O projeto possui volume grande de assets estáticos:

- imagens institucionais;
- backgrounds;
- logos por marca e estado;
- certificados;
- tutoriais;
- ícones de pagamento;
- arquivos de suporte à biometria.

Arquivos principais:

- `app/assets/javascripts/backend.js`
- `app/assets/javascripts/frontend.js`
- arquivos CoffeeScript legados
- múltiplos CSS por contexto (`frontend`, `backend`, `ceatt`, `sp`, `shared`)

Há layouts dedicados para cada tipo de usuário, o que reforça a natureza multiportal.

## 14. E-mail e comunicação

`MailNotification` concentra envio de:

- confirmação de matrícula;
- confirmação de compra/pagamento;
- cancelamento/reembolso;
- aviso de vencimento contratual;
- cadastro de aluno/CFC/instrutor;
- formulário de contato;
- denúncia LGPD;
- certificado concluído em MG.

SMTP configurado com SendGrid.

## 15. Segurança

## 15.1 Pontos positivos

- Devise presente em múltiplos papéis;
- MFA administrativo;
- headers de segurança configurados;
- `force_ssl` em produção;
- filtro de parâmetros existe em initializer;
- política de senha forte em alguns modelos;
- controle de primeiro acesso e expiração de senha em áreas críticas.

## 15.2 Riscos críticos encontrados

### Credenciais hardcoded no repositório

Foram encontrados diretamente no código:

- senhas de banco;
- tokens JWT;
- segredos de Azure;
- segredos de Conta Azul;
- credenciais SendGrid;
- chaves de Pagar.me;
- credenciais UnitegPag;
- segredos e senhas de serviços DETRAN;
- credenciais de autenticação ICE;
- token fixo de API;
- senhas/defaults de usuário.

Isso é um risco crítico de segurança e compliance.

### CORS excessivamente aberto

`config.middleware.insert_before 0, Rack::Cors` libera:

- qualquer origem;
- qualquer header;
- métodos `GET`, `POST`, `DELETE`, `OPTIONS`.

Para uma aplicação com dados pessoais, financeiros e biométricos, isso é agressivo.

### `verify_mode = OpenSSL::SSL::VERIFY_NONE`

Aparece em vários serviços HTTP. Isso desabilita validação de certificado TLS e expõe a aplicação a MITM.

### Autenticação de API fraca

Há uso de:

- token estático em controller;
- basic auth com credenciais carregadas da base;
- múltiplos endpoints sem padronização central robusta.

### Senhas default previsíveis

Em alguns fluxos de API, aluno é criado com senha padrão e depois recebe variação baseada em CPF.

### Alto acoplamento de regra sensível em callbacks

Lógica de negócio importante em `after_create`/`after_update` eleva risco de efeitos colaterais difíceis de testar.

## 16. Qualidade técnica e manutenção

### Pontos fortes

- grande cobertura funcional;
- modelagem rica do domínio;
- forte aderência ao negócio regulatório;
- múltiplas integrações já consolidadas;
- deploy containerizado com Kubernetes.

### Fragilidades

- controller `ApiController` muito grande;
- grande quantidade de lógica em models e controllers;
- pouco isolamento de serviços por contrato;
- ausência de testes automatizados;
- repetição de código em integrações por UF;
- parsing e tratamento de payloads muito manuais;
- acoplamento entre camada web e regra de integração;
- mistura de responsabilidade comercial, acadêmica e operacional nos mesmos objetos;
- naming inconsistente (`Moduluse`, `Services` no plural, `zoom.rb`, etc.).

## 17. Conclusões sobre arquitetura

Arquiteturalmente, o projeto é um monólito de negócio com as seguintes características:

- orientado a domínio, mas sem separação modular forte;
- multi-tenant parcial via parametrização de CFC e shards;
- multiportal;
- multi-UF;
- fortemente integrado a órgãos externos;
- com bastante legado acumulado;
- operacionalmente crítico;
- sensível a regressões.

É um sistema que já resolve muita regra real, mas hoje cobra custo alto de manutenção, segurança e previsibilidade.

## 18. Prioridade de riscos e melhorias

### Prioridade máxima

1. remover credenciais do repositório e rotacionar tudo;
2. migrar segredos para AWS Secrets Manager / Parameter Store / variáveis de ambiente seguras;
3. eliminar `VERIFY_NONE` nas integrações;
4. revisar CORS;
5. remover tokens estáticos de API;
6. auditar senhas default e fluxos de criação de usuário.

### Prioridade alta

1. criar suíte mínima de testes de regressão para:
   - matrículas
   - certificados
   - integrações DETRAN
   - cobrança/Conta Azul
   - créditos
2. extrair integrações por UF para adapters padronizados;
3. reduzir callbacks críticos em models;
4. quebrar `ApiController` em endpoints menores;
5. centralizar cliente HTTP com timeout, retry e logging padronizados.

### Prioridade média

1. documentar contratos de API interna/externa;
2. mapear features por flag em `TrainingCenter`;
3. padronizar nomenclaturas;
4. reduzir duplicação entre áreas administrativas e de CFC;
5. revisar strategy de assets e frontend legado.

## 19. Mapa resumido de pastas

### `app/controllers`

Camada web principal, dividida por papel:

- `admin/`
- `coach/`
- `student/`
- `training_center/`
- `teacher/`
- `reseller/`
- `collection_user/`
- controladores públicos e de API

### `app/models`

Contém praticamente todo o núcleo de domínio.

### `app/services`

Concentra integrações e partes de regra de negócio procedural.

### `app/views`

Grande volume de telas Slim, incluindo HTML, JS ERB e PDFs.

### `config/`

Configuração do Rails, shards, secrets, schedule, initializers e rotas.

### `db/`

Histórico grande de migrações e `schema.rb`.

### `docker/`, `codebuild/`, `helm-chart/`

Operação, build e deploy.

## 20. Diagnóstico final

O projeto é uma plataforma operacional grande e madura, com altíssimo valor de negócio, mas também com dívida técnica e dívida de segurança relevantes.

Em termos simples:

- o sistema funciona como ERP + LMS + hub regulatório + portal comercial;
- o centro do negócio está em `TrainingCenter`, `Student`, `Matriculation`, `Course`, `Classroom` e `Certificate`;
- os maiores riscos atuais não são de funcionalidade, e sim de segurança, manutenção e regressão;
- a ausência de testes e a presença de segredos hardcoded são os principais pontos de atenção imediata.

## 21. Arquivos mais importantes para começar manutenção

- `config/routes.rb`
- `config/environments/production.rb`
- `config/database.yml`
- `config/shards.yml`
- `app/controllers/api_controller.rb`
- `app/controllers/admin_controller.rb`
- `app/controllers/training_center_controller.rb`
- `app/controllers/student_controller.rb`
- `app/models/training_center.rb`
- `app/models/student.rb`
- `app/models/course.rb`
- `app/models/matriculation.rb`
- `app/models/classroom.rb`
- `app/models/certificate.rb`
- `app/services/certificate_service.rb`
- `app/services/detran_ms_services.rb`
- `app/services/detran_sc_services.rb`
- `app/services/detran_pr_services.rb`
- `app/services/conta_azul_services.rb`

## 22. Recomendações práticas de leitura

Se alguém novo for assumir o projeto, a melhor ordem é:

1. `routes.rb`
2. controladores base por papel
3. `TrainingCenter`, `Student`, `Course`, `Matriculation`, `Classroom`, `Certificate`
4. serviços DETRAN do estado alvo
5. fluxo financeiro (`Order`, `CreditOrder`, `FinancialOrder`, `ContaAzulServices`)
6. `production.rb`
7. deploy (`Dockerfile`, `codebuild`, `helm-chart`)

---

Documento gerado a partir de leitura estática do repositório local em `C:\Users\neemi\unicfcead-rs`.
