import ply.lex as plex
import csv

linhasCount = 0
colunasCount = 0
posicaoLinha = 0
posicaoColuna = 0

class virgulas:
    tokens = ("COMMENT","QUOTATION","COMMA")
    t_ignore = ""

    def t_COMMENT(self,t):
        r"\#[^\n]+"
        pass

    def t_QUOTATION(self,t):
        r"(,?)\"[^\"]+(\"?),?"
        escreverTabela(t.value)
        return t

    def t_COMMA(self,t):
        r"(,?)[^\,]+,?"
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
                pass
                #print(token)
        print("Finished processing")

    def escreverincio(self):
        text = '''<html>
    <body>
        <table id = "customers">'''
        file = open("tabela.html", "a")
        file.write(text)
        file.close()

    def escreverfim(self):
        text = '''
        </table>
    </body>
</html>    
                '''
        file = open("tabela.html", "a")
        file.write(text)
        file.close()

    def escrever(self,colunas,linhas):
        text = '''<html>
    <body>
        <table id = "customers">

            '''
        file = open("tabela.html", "w")
        file.write(text)
        file.close()

        file = open("tabela.html","a")

        for i in range(linhas):
            text = "<tr>"
            file.write(text)

            for a in range(colunas):
                text = "<td>  Eu sou lindo  </td>"
                file.write(text)

        text = '''
        </table>
    </body>
</html>    
                '''
        file.write(text)
        file.close()

def styleCSS():
    text = '''
    <style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
</style>'''

    file = open("tabela.html", "w")
    file.write(text)
    file.close()


def escreverTabela(palavra):
    file = open("tabela.html", "a")
    global posicaoLinha,linhasCount,posicaoColuna,colunasCount
    print(posicaoColuna)
    if(posicaoLinha < linhasCount):
        text = '''<td>''' + palavra + '''</td>'''
        file.write(text)

        if (posicaoLinha == linhasCount - 1):
            posicaoLinha = 0
        posicaoLinha = posicaoLinha + 1

    if(posicaoColuna == colunasCount - 1):
        text = '''</tr>'''
        file.write(text)
        posicaoColuna = -1

    posicaoColuna = posicaoColuna + 1

    file.close()

processor = virgulas("teste.csv")
processor.verLinhas()
processor.cabecalho()
styleCSS()
processor.escreverincio()


processor.toc()
processor.escreverfim()
print("categorais -> " ,colunasCount,linhasCount)