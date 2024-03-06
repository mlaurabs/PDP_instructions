## Ambiente Virtual
- explicação: https://www.alura.com.br/artigos/ambientes-virtuais-em-python
- documentação: https://docs.python.org/3/library/venv.html

## Utilizando o git
- Principais comandos:
  - git init  VS rm -rf .git
  - git add .
  - git commit -m "message"
  - git add remote origin -link do repo-
  - git push origin branch / git push -f origin branch (ignora o que está no repositório remoto)
  - git pull origin branch
  - git status
  - git branch -m <novo-nome-para-branch> (renomeia a branch atual)
  - git checkout -b <nome-da-nova-branch> (cria uma nova branch e muda para ela)

- Link para acessar mais comandos (é o repositótio de um amigo): https://github.com/burgues0/git-cheatsheet
- 

- *solving problems*
  - 1- erro -fatal: refusing to merge unrelated histories- geralmente acontece quando você tenta fazer o git pull de um repositório remoto, mas o seu repositório local possuí um histórico de commits, branches, etc, diferente do que está no repositório remoto.
  -   - Solução 1: git pull origin branch --allow-unrelated-histories
