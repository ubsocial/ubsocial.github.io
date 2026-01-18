Fluxo completo de trabalho (COM branch, MÚLTIPLOS usuários – COM PULL REQUEST)


#####################################
# USUÁRIO 1 — trabalha no branch master
#####################################

# Garantir que está no branch master
git checkout master

# Verificar se há atualizações no repositório remoto
git fetch

# Baixar atualizações no branch master local
git pull

# Trabalhar no projeto (branch master)

# Adicionar arquivos ao Git
git add .

# Confirmar nova versão no Git (master)
git commit -m "commit do usuário 1 no branch master"

# Enviar alterações do branch master ao GitHub
git push


#####################################
# USUÁRIO 2 — cria e trabalha no branch design
#####################################

# Garantir que está no branch master (base atualizada)
git checkout master

# Verificar se há atualizações no repositório remoto
git fetch

# Baixar atualizações no branch master local
git pull

# Criar e mudar para o branch design
git checkout -b design

# Trabalhar no projeto (branch design)

# Adicionar arquivos ao Git
git add .

# Confirmar nova versão no Git (design)
git commit -m "commit do usuário 2 no branch design"

# Enviar o branch design ao GitHub
# (-u cria o vínculo entre branch local e remoto)
git push -u origin design


#################################################
# USUÁRIO 2 — CRIA O PULL REQUEST (NO GITHUB)
#################################################

# AÇÃO NO GITHUB (não é comando):
# - Abrir o repositório no GitHub
# - Criar Pull Request:
#     base: master
#     compare: design
# - Descrever as mudanças
# - Submeter o Pull Request


#################################################
# USUÁRIO 1 — REVISA E FAZ O MERGE DO PR
#################################################

# AÇÃO NO GITHUB (não é comando):
# - Usuário 1 revisa o Pull Request
# - Resolve comentários, se houver
# - Clica em "Merge Pull Request"
# - Confirma o merge no branch master


#####################################
# USUÁRIO 1 — ATUALIZA APÓS O MERGE
#####################################

# Garantir que está no branch master
git checkout master

# Verificar se há atualizações no repositório remoto
git fetch

# Baixar atualizações
# (agora contém o merge do Pull Request)
git pull

# Continuar trabalhando no branch master

# Adicionar arquivos ao Git
git add .

# Confirmar nova versão no Git
git commit -m "continuação do trabalho do usuário 1 no master"

# Enviar alterações ao GitHub
git push


#####################################
# USUÁRIO 2 — ATUALIZA E PASSA A TRABALHAR NO MASTER
#####################################

# Garantir que está no branch master
git checkout master

# Verificar se há atualizações no repositório remoto
git fetch

# Baixar atualizações
# (master agora contém o código do antigo branch design)
git pull

# (opcional) remover o branch design local
git branch -d design

# (opcional) remover o branch design remoto
git push origin --delete design

# Continuar trabalhando normalmente no branch master

# Adicionar arquivos ao Git
git add .

# Confirmar nova versão no Git
git commit -m "continuação do trabalho do usuário 2 no master"

# Enviar alterações ao GitHub
git push