# Deploy do seu classificador fast.ai

Existem várias formas de colocar no ar o seu classificador baseado em fast.ai. A página de informações do curso mostra diversas opções: [https://course.fast.ai/index.html](https://course.fast.ai/index.html).

Uma opção que se destaca é o Render.com, que é uma plataforma criada pelo mesmo criador do Crestle. O tutorial oficial está em [https://course.fast.ai/deployment_render.html](https://course.fast.ai/deployment_render.html).

Outra opção, essa possível de ser utilizada totalmente gratuita é o Heroku.

A seguir vou mostrar como fazer o deploy nessas duas opções.

## Primeiro: exporte o modelo treinado.

Gere o seu modelo normalmente e salve o `export.pkl` com learn.export.

Coloque que arquivo no google drive ou dropbox (porque é de graça). É necessário gerar um link para o arquivo usando um dos dois serviços abaixo:

- Google Drive: Use [este gerador de links](https://www.wonderplugin.com/online-tools/google-drive-direct-link-generator/).
- Dropbox: Use [este gerador de links](https://syncwithtech.blogspot.com/p/direct-download-link-generator.html).

## Segundo: prepare a aplicação pré-pronta.

Faça um fork no github do repositório base que contém uma aplicação pré-pronta e customizável.

Edite, no próprio Github arquivo `app/server.py` para incluir:

1. O endereço do `export.pkl` em `export_file_url`.
2. Troque o nome das classes geradas pelo seu modelo em `classes =['macbook', 'notmacbook']`.
3. Lembre-se de usar a opção "Commit directly to the master branch".
4. Edite também o texto que aparece para os usuários da sua aplicação, no arquivo `app/views/index.html:`
    1. O título (tag `<title>`)
    2. O cabeçalho (`div class='title'`) e a explicação (tag `<p>`)
5. E pronto!

## Deploy no Render

Para fazer sua conta no Render, use o link [render.com/i/fastai](http://render.com/i/fastai) Cada conta criada por esse link vem com 5 dólares de crédito e depois disso cada aplicação custa 5 dólares por mês, faturada por segundo.

Após o cadastro crie uma nova aplicação em "New Web Service" e aponte para o seu repositório fork criado anteriormente.

1. Simples assim.
2. E pronto!

Agora, toda vez que você editar a aplicação, o Render detecta automaticamente refaz o deploy.

## Deploy no Heroku

Apesar de ser mais barato, o deploy no Heroku exige passos adicionais, que devem ser repetidos manualmente sempre que o código da aplicação for alterado na Github.

Normalmente o deploy no Heroku exige apenas o código da aplicação, mas no caso dos modelos do fastai, ela é grande demais para o método tradicional e exige o deploy em containers docker.

Para isso, é necessário executar os comandos numa máquina com docker instalado.

No entanto, como estamos usando uma máquina do Google Cloud para gerar o modelo, podemos usar o Cloud Shell para fazer o deploy.

### Acesse o console do Google Cloud.

Os passos a seguir consideram que você já tem uma conta no gcloud.

1. Acesse o dashboard em [https://console.cloud.google.com/home/dashboard](https://console.cloud.google.com/home/dashboard).
2. Abra o Cloud Shell no topo da página:

    ![](Captura_de_Tela_2019-04-10_as_13-6bc61c51-8907-4603-9c7c-df9ac066361f.33.19.png)

3. Ative o modo de otimização. Ele faz com que o Cloud Shell rode numa máquina mais potente e permita o build do container.

    ![](Captura_de_Tela_2019-04-10_as_13-306f313f-7622-4f88-bf4c-e0aebf9eda2a.36.17.png)

4. Instale o cliente da heroku:

    `curl [https://cli-assets.heroku.com/install.sh](https://cli-assets.heroku.com/install.sh) | sh`

    ![](Captura_de_Tela_2019-04-10_as_13-a8eda3de-1e0f-4b82-8a0f-ae3465294c22.41.42.png)

5. Faça o clone da aplicação modificada e entre no diretório.
    Note que o seu endereço vai ser diferente do meu.

    `git clone https://github.com/weltonrodrigo/fastai-v3.git`

    ![git clone](Untitled-7d38f5b9-7231-4dcc-80c0-c27d89432ddd.png)

6. Faça o login no heroku:

    `heroku login`
    
    O cliente heroku vai pedir que você aperte enter e depois apresentar um link para ser aberto na internet. Esse link vai te levar para a página de login. Nessa tela você pode fazer seu cadastro se ainda não tiver. Depois da autenticação bem sucedida, o cliente vai informar que está logado.

    ![heroku login](Untitled-03640a1d-0ff2-4a86-a18b-5f144d9b7b64.png)

7. Crie um novo app no Heroku para receber sua aplicação:

    `heroku create nome-da-aplicacao`

    O nome da aplicação também vai ser o endereço dela na internet. No exemplo acima, seria nome-da-aplicacao.app.herokuapp.com. Caso você não queira um nome específico, ele vai criar um nome aleatório.

    ![heroku create nome-da-aplicacao](Untitled-36588520-6e31-4263-928d-7e0fb45a7119.png)

8. É necessário informar ao cliente docker como fazer o login no heroku, mas o próprio cliente toma conta disso:

    `heroku container:login`

    ![heroku container:login](Untitled-7b6266a4-8d15-4417-83ea-3b60ee693a9f.png)

9. Agora para construir e enviar o container para o heroku:
Isso deve levar em torno de 5 minutos. O print abaixo mostra só o começo do texto de saída gerado pelo comando.

    `heroku container:push web`

    ![heroku container:push web](Untitled-c913a59c-f14b-4ab4-848a-233c0f038be4.png)

    Se a construção e envio forem bem sucedidos, deve gerar uma saída parecida com esta:

    ![heroku container:push web](Untitled-746949f5-f41b-432c-84e3-0f8e3f0435b3.png)

10. Agora é necessário informar o keroku que faça o deploy propriamente dito do container criado:

    `heroku container:release web`

    ![heroku container:release web](Untitled-022ee8e9-51b9-491b-a2fe-641c363ee8c5.png)

11. O aplicativo já estará disponível https://<nome_da_aplicação>.herokuapp.com. No nosso exemplo em https://testedoherokufastai.herokuapp.com.
