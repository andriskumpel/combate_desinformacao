# Plataforma de Verificação Automatizada de Fatos

Uma plataforma em tempo real para verificação automática de fatos usando inteligência artificial, capaz de analisar textos, imagens e vídeos para identificar possíveis desinformações.

## Funcionalidades

- **Análise de Texto**: Verifica a veracidade de textos usando processamento de linguagem natural
- **Análise de Imagens**: Detecta manipulações e verifica a autenticidade de imagens
- **Análise de Vídeos**: Analisa frames-chave e detecta possíveis manipulações em vídeos
- **Interface Web**: Interface amigável e intuitiva para submissão de conteúdo
- **API REST**: Endpoints para integração com outros sistemas
- **Classificação Automática**: Categoriza conteúdo como Verificado, Suspeito ou Falso
- **Fontes de Verificação**: Fornece links para fontes confiáveis de verificação

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **IA/ML**: Hugging Face Transformers, OpenCV
- **Banco de Dados**: MongoDB
- **Testes**: pytest

## Requisitos

- Python 3.11+
- MongoDB
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/combate_desinformacao.git
cd combate_desinformacao
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

1. Inicie o servidor:
```bash
python -m app.main
```

2. Acesse a interface web:
```
http://localhost:8000
```

3. Para acessar a documentação da API:
```
http://localhost:8000/docs
```

## Testes

Execute os testes com:
```bash
python -m pytest tests/ -v --cov=app
```

## Estrutura do Projeto

```
combate_desinformacao/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── database.py
│   ├── services/
│   │   ├── analyzer.py
│   │   └── classifier.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   └── index.html
│   └── main.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_api.py
│   └── test_classifier.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Andris Kümpel - [@dikkopel](https://x.com/dikkopel) - andrisivankumpel@gmail.com

Link do Projeto: [https://github.com/andriskumpel/combate_desinformacao](https://github.com/andriskumpel/combate_desinformacao) 
