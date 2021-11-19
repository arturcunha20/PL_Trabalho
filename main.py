import ply.lex as plex
import csv

linhasCount = 0
colunasCount = 0
posicaoLinha = 0
posicaoColuna = 0

class virgulas:
    tokens = ("COMMENT","QUOTATION","COMMA")
    t_ignore = ""

    def t_COMMENT(self, t):
        r"\#[^\n]+"
        return t

    def t_QUOTATION(self, t):
        r"(,?)\"[^\"]+(\"?),?"
        escreverTabela(t.value)
        return t

    def t_COMMA(self, t):
        r"(,?)[^\,]+,?"
        t.value = t.value.replace(",","")
        escreverTabela(t.value)
        return t

    def t_error(self, t):
        print(f"Unexpected tokens: {t.value[:10]}")
        exit(1)

    def __init__(self, filename):
        self.lexer = None
        self.filename = filename
        self.inside_header = False

    def cabecalho(self):
        i = 0
        file = open("teste.csv", "r")
        reader = csv.reader(file)
        for line in reader:
            if i == 0:
                numero = len(line)
            i  = i +1
        global colunasCount
        colunasCount = numero

    def verLinhas(self):
        i = 0
        file = open("teste.csv", "r")
        reader = csv.reader(file)
        for line in reader:
            i = i +1
            if line[0][0] == "#":
                i = i-1
        global linhasCount
        linhasCount = i


    def toc(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        with open(self.filename, "r") as fh:
            contents = fh.read()

        for x in contents.splitlines():
            self.lexer.input(x)
            for token in iter(self.lexer.token, None):
                #pass
                print(token)
        print("Finished processing")

    def escreverincio(self):
        text = '''<html>
        <link href="estilo.css" rel="stylesheet" media="all" />
    <body>
    <div class="container" border ="1">
        <table>'''

        file = open("tabela.html", "w")
        file.write(text)
        file.close()

    def escreverfim(self):
        text = '''
        </table >
        </div>
    </body>
</html>    
                '''
        file = open("tabela.html", "a")
        file.write(text)
        file.close()

def escreverTabela(palavra):
    file = open("tabela.html", "a")
    global posicaoLinha,linhasCount,posicaoColuna,colunasCount
    if(posicaoLinha < linhasCount):
        text = '''<td>''' + palavra + '''</td>'''
        file.write(text)
        if (posicaoLinha == linhasCount - 1):
            posicaoLinha = 0
        posicaoLinha = posicaoLinha + 1

    if(posicaoColuna == colunasCount - 1):
        text = '''<tr class="active-row">'''
        file.write(text)
        posicaoColuna = -1

    posicaoColuna = posicaoColuna + 1

    file.close()

processor = virgulas("teste.csv")
processor.verLinhas()
processor.cabecalho()
processor.escreverincio()
processor.toc()
processor.escreverfim()
print("categorais -> " ,colunasCount,linhasCount)