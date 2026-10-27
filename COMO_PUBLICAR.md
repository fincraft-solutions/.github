# Fincraft no GitHub — pacote da capa

## Arquivos

- `profile/README.md`: conteúdo que aparece no perfil público da organização.
- `profile/assets/fincraft-ascii.svg`: capa original (ilustração feita só com caracteres ASCII, sem imagem raster embutida).
- `profile/assets/fincraft-preview.png`: prévia raster da capa; o README usa o SVG.
- `profile/assets/systems-core-ascii.txt`: a arte em caracteres, para leitura/edição.
- `scripts/generate_art.py`: código-fonte que gera a arte e o SVG (Python; CairoSVG para a prévia PNG).
- `scripts/prepare_avatar.py`: cria PNG quadrado a partir da **logo verdadeira** quando você a fornecer.

## Como instalar a capa

1. Acesse sua **organização** Fincraft no GitHub (não o perfil pessoal).
2. Crie um repositório **público** chamado `.github` dentro dessa organização.
3. Copie a pasta `profile/` deste pacote para a raiz do repositório `.github`.
4. Faça commit de `profile/README.md` e de `profile/assets/fincraft-ascii.svg` (o PNG da prévia é opcional).
5. Reabra a aba **Overview** da organização para conferir a capa.

Estrutura esperada:

```text
Fincraft/.github/
└── profile/
    ├── README.md
    └── assets/
        └── fincraft-ascii.svg
```

**Importante:** para organizações o caminho é `.github/profile/README.md`; é diferente de um perfil pessoal.

## Logo na imagem de perfil

A logo oficial **não veio no ZIP enviado**, que contém apenas a arte do perfil pessoal. Por isso não criamos nem substituímos a identidade visual oficial.

Quando tiver a logo, preferencialmente em `SVG` ou `PNG` transparente:

```bash
pip install pillow cairosvg
python scripts/prepare_avatar.py ./minha-logo-fincraft.svg -o ./fincraft-github-avatar.png
```

O script produz um arquivo `1024 x 1024`, com fundo escuro e margem de segurança para o corte circular do GitHub. Use-o em **Organization settings > Profile > Upload new picture** (os nomes dos controles podem mudar).

Se você já tiver uma versão quadrada da sua marca, pode usá-la diretamente no GitHub sem passar pelo script.

## Escolha criativa

A referência do perfil pessoal era um terminal monocromático com retrato ASCII à esquerda e comandos à direita. Nesta proposta a imagem é um **Systems Core**: um núcleo de processamento envolto em conexões de dados e uma estrutura espacial. Ele remete a engenharia, produtos e inteligência sem reproduzir ou competir visualmente com a marca da empresa. A cor verde-água é um acento experimental da capa, **não é a paleta oficial** da Fincraft.

O texto está em inglês, acompanhando o tom do README pessoal enviado e o público do GitHub. Nenhum repositório não informado foi inventado ou mencionado como já publicado.
