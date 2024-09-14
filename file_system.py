class INode:
    """
    Classe que representa um nó no sistema de arquivos.
    
    Atributos:
        name (str): Nome do nó.
        size (int): Tamanho do nó (0 por padrão).
        blocks (list): Lista para armazenar dados do arquivo.
        is_directory (bool): Indica se o nó é um diretório.
        children (dict): Dicionário para armazenar filhos (apenas se for um diretório).
    """
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.blocks = []
        self.is_directory = False
        self.children = {}
        self.parent = None

class FileSystem:
    """
    Classe que gerencia a estrutura do sistema de arquivos.
    
    Atributos:
        root (INode): O diretório raiz do sistema de arquivos.
        current_directory (INode): O diretório atual em que o usuário está navegando.
        parent_directory (INode): O diretório pai do diretório atual.
    """
    def __init__(self):
        """
        Inicializa o sistema de arquivos com o diretório raiz.
        """
        self.root = INode("/")
        self.root.is_directory = True
        self.current_directory = self.root

    def create(self, name, is_directory=False):
        """
        Cria um novo arquivo ou diretório no diretório atual.
        
        Parâmetros:
            name (str): Nome do arquivo ou diretório a ser criado.
            is_directory (bool): Indica se o novo nó é um diretório (padrão é False).
        """
        if name in self.current_directory.children:
            print(f"{name} já existe.")
            return
        inode = INode(name)
        inode.parent = self.current_directory
        inode.is_directory = is_directory
        self.current_directory.children[name] = inode
        print(f"{name} {'diretório' if is_directory else 'arquivo'} criado.")

    def list_directory(self):
        """
        Lista os arquivos e diretórios no diretório atual.
        """
        for name, inode in self.current_directory.children.items():
            print(f"{name}/" if inode.is_directory else name)

    def change_directory(self, name):
        """
        Muda o diretório atual.
        
        Parâmetros:
            name (str): Nome do diretório para o qual mudar. Use ".." para voltar ao diretório pai, e Use "." para se manter no diretório atual
        """
        if name == "..":
            if self.current_directory != self.root:
                self.current_directory = self.current_directory.parent
            return   
         
        elif name == ".":
            return
            
        elif name in self.current_directory.children and self.current_directory.children[name].is_directory:
            self.current_directory = self.current_directory.children[name]
        else:
            print(f"{name} não é um diretório.")
        # print(f'Diretório atual é {self.current_directory.name} e o pai é {self.current_directory.parent}')

    def rename(self, old_name, new_name):
        """
        Renomeia um arquivo ou diretório no diretório atual.
        
        Parâmetros:
            old_name (str): Nome atual do arquivo ou diretório.
            new_name (str): Novo nome para o arquivo ou diretório.
        """
        if old_name in self.current_directory.children:
            inode = self.current_directory.children.pop(old_name)
            self.current_directory.children[new_name] = inode
            print(f"{old_name} renomeado para {new_name}.")
        else:
            print(f"{old_name} não encontrado.")

    def move(self, src, dest_directory):
        """
        Move um arquivo ou diretório para outro diretório.
        
        Parâmetros:
            src (str): Nome do arquivo ou diretório de origem.
            dest_directory (str): Nome do diretório de destino.
        """
        if src in self.current_directory.children:
            inode = self.current_directory.children.pop(src)
            if dest_directory in self.current_directory.children and self.current_directory.children[dest_directory].is_directory:
                self.current_directory.children[dest_directory].children[src] = inode
                print(f"{src} movido para {dest_directory}.")
            else:
                self.current_directory.children[src] = inode  # Reverte a operação pop
                print(f"{dest_directory} não é um diretório.")
        else:
            print(f"{src} não encontrado.")

    def write_file(self, name, data):
        """
        Escreve dados em um arquivo.
        
        Parâmetros:
            name (str): Nome do arquivo.
            data (str): Dados a serem escritos no arquivo.
        """
        if name in self.current_directory.children and not self.current_directory.children[name].is_directory:
            inode = self.current_directory.children[name]
            inode.size = len(data)
            inode.blocks = [data]
            print(f"Dados escritos em {name}.")
        else:
            print(f"{name} não é um arquivo.")

    def read_file(self, name):
        """
        Lê dados de um arquivo.
        
        Parâmetros:
            name (str): Nome do arquivo.
        """
        if name in self.current_directory.children and not self.current_directory.children[name].is_directory:
            inode = self.current_directory.children[name]
            print(f"Dados de {name}: {''.join(inode.blocks)}")
        else:
            print(f"{name} não é um arquivo.")

    def delete(self, name):
        """
        Exclui um arquivo ou diretório.
        
        Parâmetros:
            name (str): Nome do arquivo ou diretório a ser excluído.
        """
        if name in self.current_directory.children:
            del self.current_directory.children[name]
            print(f"{name} excluído.")
        else:
            print(f"{name} não encontrado.")
