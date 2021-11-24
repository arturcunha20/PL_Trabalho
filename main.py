import ply.lex as plex
import csv

colunasCount = 0
posicaoColuna = 0
posicaoColunaLatex = 0
countLatex = 0

class virgulas:
    tokens = ("COMMENT","QUOTATION","COMMA")
    t_ignore = ""

    def t_COMMENT(self, t):
        r"\#[^\n]+"
        return t

    def t_QUOTATION(self, t):
        r"(,?)\"[^\"]+(\"?),?"
        escreverTabela(t.value)
        escreverLatex(t.value)
        return t

    def t_COMMA(self, t):
        r"(,?)[^\,]+,?"
        t.value = t.value.replace(",","")
        escreverTabela(t.value)
        escreverLatex(t.value)
        return t

    def t_error(self, t):
        print(f"Unexpected tokens: {t.value[:10]}")
        exit(1)

    def __init__(self, filename):
        self.lexer = None
        self.filename = filename
        self.inside_header = False

    def toc(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        with open(self.filename, "r") as fh:
            contents = fh.read()

        for x in contents.splitlines():
            #x = x.replace("/n","")
            self.lexer.input(x)
            for token in iter(self.lexer.token, None):
                pass
                #print(token.value)
        print("Finished processing")

def cabecalho():
    numero = 0
    str = ""
    i = 0
    file = open("teste.csv", "r")
    reader = csv.reader(file)
    for line in reader:
        if i == 0:
            numero = len(line)
            str = line
        i+=1

    if str[-1] == "":
        numero = numero-1

    global colunasCount
    colunasCount = numero
    print(numero)

def escreverincio():
    text = '''<html>
    <link href="estilo.css" rel="stylesheet" media="all" />
    <body>
    <div class="container" border ="1">
        <table>'''

    file = open("tabela.html", "w")
    file.write(text)
    file.close()

def escreverfim():
    text = '''
        </table >
        </div>
    </body>
</html>    
            '''
    file = open("tabela.html", "a")
    file.write(text)
    file.close()

def escreverInicioLatex():
    text = '''\documentclass{article}
\/begin{document}
\/begin{center}
\/begin{tabular}'''
    text = text.replace("/", "")
    file = open("latex.tex", "w")
    file.write(text)
    file.close()

def escreverFimLatex():
    text = '''
\end{tabular}
\end{center}
\end{document}'''
    file = open("latex.tex", "a")
    file.write(text)
    file.close()

def escreverTabela(palavra):
    file = open("tabela.html", "a")
    global posicaoColuna,colunasCount
    text = '''
            <td>''' + palavra + '''</td>'''
    file.write(text)

    if(posicaoColuna == colunasCount - 1):
        text = '''
            <tr>'''
        file.write(text)
        posicaoColuna = -1

    posicaoColuna = posicaoColuna + 1

    file.close()

def escreverLatex(palavra):
    file = open("latex.tex", "a")
    global posicaoColunaLatex,colunasCount,countLatex
    if "&" in palavra:
        palavra = palavra.replace("&","\&")

    text = palavra + ''' & '''
    if countLatex == colunasCount-1:
        text = text.replace("&","")
        countLatex = -1

    file.write(text)
    if(posicaoColunaLatex == colunasCount - 1):
        text = ''' \\\\ \hline \n'''
        file.write(text)
        posicaoColunaLatex = -1

    posicaoColunaLatex = posicaoColunaLatex + 1
    countLatex = countLatex + 1

    file.close()

def escreverColunasLatex():
    file = open("latex.tex","a")
    global linhasCount
    ola = ""
    for x in range(colunasCount):
        ola = ola + "c "

    text = '''{||  ''' + ola + ''' ||}\n'''

    file.write(text)
    file.close()

processor = virgulas("teste.csv")
cabecalho()
escreverincio()
escreverInicioLatex()
escreverColunasLatex()
processor.toc()
escreverFimLatex()
escreverfim()