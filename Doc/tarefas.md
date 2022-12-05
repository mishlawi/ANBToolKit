# TAREFAS
===

Tarefa t1
 dado um dgu construir uma sua representação interna

 def  parsedgu(filename) : adgu

 adgu = DocDict
   - type
   - format
   - id
   - _body : list(STR)

===

Tarefa t2
  def dgus2latexbook( adgu* ) : LaTeX
     with  open(",...","w") as X:
       print("\document....", file= X)
       for dgu in ...
           if format == "md":
           ... print md2tex(dgu["body"]) ?????  /for each body
           elsif format == "foto":
               print \includegraphics(doc.file)
                        == album
               for each foto in album
          


===
Tarefa t3
  canivete suiço de conversores habituais

  ir juntando módulos / funções conversores

  import markdowun    ????
  def md2tex(doc):doc
     markdown2html

  pandoc ? (via modulo ou via linha de comando)

  Módulo Python

  ... alguns testes simples...
