## Ambiente Virtual
- explicação: https://www.alura.com.br/artigos/ambientes-virtuais-em-python
- documentação: https://docs.python.org/3/library/venv.html
- Passo a passo no Windows pelo cmd:
    - python -m venv venv --> criando a venv
    - ./venv/Scripts/activate --> ativando a venv
    - deactivate --> desativar a venv e voltar pro sistema operacional
      
## Utilizando o git
- Principais comandos:
  - **git init** (incializa o git em um repositório/folder local)
      - ***Obs: quando o git é incializado em um diretório é criado um arquivo .git que é oculto, então quando não queremos mais utilizar o git em um folder, podemos simplesmente apagá-lo***
  - **rm -rf .git** (apaga o arquivo .git)
  - **git add .** (envia para "stage" todas as modificações feitas no repositório. arquivos "staged" --> pronto para envio)
  - **git commit -m "message"** (esse comando vai criar um comit dos arquivos que estão marcados como staged)
  - **git add remote <"conexão" do repositório> <link "http" do repositório>** (configurar o acesso a repositório no GitHub)
  - **git push <"conexão" do repositório> <nome-da-branch>**  (envia as atualizações)
  - **git push -f <"conexão" do repositório> <nome-da-branch>** (ignora o que está no repositório remoto) #cuidade com esse comando, pode perder algo importante ja carregado no github)
  - **git pull origin branch** (carrega no seu repositório local as atualizações do Github)
  - **git status** (mostra o ciclo de vida dos arquivos)
  - **git branch -m <novo-nome-para-branch>** (renomeia a branch atual)
  - **git checkout -b <nome-da-nova-branch>** (cria uma nova branch e muda para ela)
  - **git remote -v** (visualizar todos os "remotes" feitos e os links dos repositórios associados)
  - **git remote show** (mostra o nome de todos os "remotes" feitos)
  - **git branch -v** (retorna o último commmit das branches existentes)
  - **git branch --list** (lista as branches existentes)
  - **git branch -r** (lista os "remotes" e suas respectivas branches)

- Ciclo de vida do git:
    - ![image](https://github.com/mlaurabs/PDP_instructions/assets/89169599/5e578c3c-01b0-403d-ac45-dbb73dde9079)


- Links interessantes:
    - Link para acessar mais comandos (é o repositótio de um amigo): https://github.com/burgues0/git-cheatsheet
    - https://medium.com/@rafaelvicio/introdu%C3%A7%C3%A3o-a-git-5ae36c303850#:~:text=Ciclo%20de%20vida%20dos%20arquivos,modified%3A%20Arquivos%20modificados.
    - https://www.alura.com.br/artigos/o-que-e-git-github
    - Vídeo sobre o git (definição, conceitos e comandos importantes):
      - parte 1: https://youtu.be/DqTITcMq68k?feature=shared
      - parte 2: https://youtu.be/UBAX-13g8OM?feature=shared
        
- Arquivos que podem ajudar no entendimento do git serão colocados no repositório

- *SOLVING PROBLEMS*
  - **"fatal: refusing to merge unrelated histories"** --> geralmente acontece quando você tenta fazer o git pull de um repositório remoto, mas o seu repositório local possuí um histórico de commits, branches, etc, diferente do que está no repositório remoto.
     - **Solução 1: git pull origin branch --allow-unrelated-histories**
