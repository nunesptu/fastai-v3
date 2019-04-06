# Deploy no heroku!

Gerar o modelo normalmente e salva o `export.pkl` no google drive ou dropbox (porque é de graça).

Faz um fork do repositório base que contém uma aplicação pré-pronta customizável.

Edita a aplicação para incluir:

1. Suas classes
2. O endereço do `export.pkl`
3. Está pronto para o deploy no Render!

Mas o Render é caro ($5 dólares por mês em média). O Heroku é de graça, tem um free tier bacana. Só não vai o software mais rápido do mundo!

Exige um passo extra, porque o software com modelo e tudo é grande demais pro heroku.

Mas ele tem um limite de tamanho maior para um container, então temos que criar esse container em algum lugar.

Pode ser na sua máquina, mas isso vai levar mais tempo e exige instalar o docker. Melhor usar na internet.

Se você já usa Google Cloud, você já tem um máquina, o google console!

### Vamos abrir um terminal nela!

Ative o **modo otimização**, para ela ficar um pouco mais robusta.

Clonar o seu repositório:

`git clone [https://github.com/weltonrodrigo/fastai-v3.git](https://github.com/weltonrodrigo/fastai-v3.git)`

Instalar o heroku:

`curl [https://cli-assets.heroku.com/install.sh](https://cli-assets.heroku.com/install.sh) | sh`

Logar no heroku:

`heroku login`

Criar o seu app:

`heroku create`

Logar no registro de containers do heroku:

`heroku container:login`

Construir o container "com o nome web" e enviar para o heroku

`heroku container:push web`

Colocar pra rodar!

`heroku container:release web`
