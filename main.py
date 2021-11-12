import ply.lex as plex
import csv

class virgulas:
    tokens = ("COMMENT","QUOTATION","COMMA")
    t_ignore = ""

    def t_COMMENT(self,t):
        r"\#[^\n]+"
        pass

    def t_QUOTATION(self,t):
        r"(,?)\"[^\"]+(\"?),?"
        return t

    def t_COMMA(self,t):
        r"(,?)[^\,]+,?"
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
        return numero

    def verLinhas(self):
        i = 0
        file = open("teste.csv", "r")
        reader = csv.reader(file)
        for line in reader:
            i = i +1
            if line[0][0] == "#":
                i = i-1
        return i


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

    def escrever(self,colunas,linhas):
        text = '''<html>
    <body>
        <table border = "1" padding = 10>

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


        text = '''</table>
    </body>
</html>    
        '''
        file.write(text)
        file.close()


processor = virgulas("teste.csv")
linhas = processor.verLinhas()
colunas = processor.cabecalho()
processor.escrever(colunas,linhas)
processor.toc()



#print("categorais -> " ,colunas,linhas)