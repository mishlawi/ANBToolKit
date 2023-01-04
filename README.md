# ANCESTORS NOTEBOOK TOOLKIT
## Minhas notas 

# 5/12
neste momento existem bastantes coisas desorganizadas
* é necessario organizá-las, a começar pelos casos de estudo
  -> nesta vertente convinha verificar de que forma os dados devem ser inseridos e dispostos
* seria importante adicionar forma de adicionar ficheiros
* gostaria de ter mais variedade de documentos que nao totalmente associados com a minha familia, Uminho p.e 
* procurar utilizar o flit e definir os metodos convenientemente para que sejam propriamente usados conforme recomendado pelo professor
* geração de DGUs e de Abstract DGUs está feito ou num bom caminho, conforme as recomendações dadas pelo professor na ultima reuniao
* o uso do formato YAML para os cabeçalhos está completamente integrado conforme sugerido pelo professor, encontrei tambem alguma documentação importante que JÁ me permite definir um formato base de DGUs que depois poderá servir de "superclasse" para outros formatos (user defined? ou defaults, conforme ja fomos discutindo)
  ou seja,
  ---> DGU tem os parametros id,formato, tipo, about ... 
  ---> Biografia poderá herdar os atributos da DGU e ter tambem "nome", "data de nascimento", ....
* notas a serem definidas
* falta integrar com o flit
* pré tese a ser iniciada..........


# 12/12
```
flit build
flit install -s
```

* adicionei mais comandos por via do *flit* 
* necessario *organizar codigo*
* necessario definir as notas e o seu respetivo parser
* necessario entender comodiferentes tipos de entidades (biografias, albuns....) derivam relativamente às dgus (há que haver uma correlação... certo?)
* adicionar o que recolhi ao git para ter um caso de estudo mais profundo
* argparse e flit

# 28/12

* estive a rever a forma de processamento da DSL, essa parte mantém-se funcional mas ainda nao consegui encontrar um use case convincente para poder fazer o processamento de entidades em documentos. De que forma poderia isto ser feito? Algo como `comando Pessoa Album ` ?  leva à geração de algum tipo de ficheiro (conforme tinhamos feito ao inicio com html). Mas como verifico entidades?
* Como dar uso à gramatica ? 
  * Definicao de nomenclatura de ficheiros
  * definicao de formatos aglutinadores (Pessoa por exemplo)
* Como verificar se a gramatica está correta? 
* Algum caminho para tornar a gramatica user friendly? Parece me demasiado formal
* Integração flit com argparse está decente, abre caminho para muita coisa
* De que me servem os formatos aceites? Informativo só?

### TODO
1. Ja deu para perceber a forma como valores da gramatica tem que ir como default, mas é preciso ter controlo sobre as entidades, não só instanciá-las.
2. *Beautificar* os geradores de livros
3. Pensar em adicionar geracao html
  1. Que esta geracao possa ser feita com dgus e com entidades
4.  
