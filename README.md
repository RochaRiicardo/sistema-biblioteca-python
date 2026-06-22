# Sistema de Biblioteca em Python 

Este é um projeto de sistema de biblioteca desenvolvido em Python para colocar em prática conceitos de programação, manipulação de arquivos e persistência de dados.

---

##  Evolução do Projeto

O projeto foi dividido em marcos de aprendizado, refletindo a minha evolução durante o curso de ADS:

###  Versão 1.2 — O Início e Manipulação de JSON
Nesta primeira fase, o foco foi estruturar as regras de negócio da biblioteca (cadastro de livros, empréstimos e usuários).
* **O que aprendi:** Aprendi a trabalhar com arquivos **JSON** para salvar os dados temporariamente.
* **Desafio:** Compreender como ler e escrever dados estruturados em arquivos de texto sem perder as informações ao fechar o programa.

###  Versão 2.0 — Migração para Banco de Dados (Atual)
Na versão atual, o sistema deu um salto de maturidade com a implementação de persistência robusta de dados.
* **O que estou aprendi:** Migrei todo o armazenamento de arquivos JSON para o **SQLite**.
* **Evolução:** Criação de tabelas, relacionamentos, chaves primárias e execução de comandos SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) direto pelo código Python usando a biblioteca `sqlite3`.

---

##  Tecnologias Utilizadas

* **Python 3** (Lógica de programação)
* **JSON** (Versão 1.2)
* **SQLite / SQL** (Versão 2.0)

---

##  Como executar o projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Clone o repositório ou baixe os arquivos.
3. Abra o terminal na pasta do projeto e execute:
   ```bash
   python "biblioteca v2.0.py"
