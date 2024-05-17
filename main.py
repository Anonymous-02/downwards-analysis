from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter


def sort_dict(dico, order=None):
    if order:
        return dict(sorted(dico.items(), key=lambda x: x[0]))
    return dict(sorted(dico.items(), key=lambda x: x[1]))


def uncomment(text: str, mult: int = -1) -> str:
    """remove both inline and multiline comment with a pascal syntax"""
    if mult == 1:
        a = text.find('{')
        if a == -1:
            return text
        elif text.find('}', a) == -1:
            return text[:a]
        else:
            return text[:a] + uncomment(text[text.find('}', text.find('{')) + 1:])
    elif mult == 0:
        a = text.find('//')
        if a == -1:
            return text
        elif text.find('\n', a) == -1:
            return text[:a]
        else:
            return text[:a] + uncomment(text[text.find('\n', a) + 1:])
    else:
        return uncomment(uncomment(text, 0), 1)


def remove_strings(text: str) -> str:
    """remove all single quoted strings from text, ignore exscaping chars  """
    a = text.find("'")
    if a == -1:
        return text
    elif text.find("'", a + 1) == -1:
        return text[:a]
    else:
        return text[:a] + remove_strings(text[text.find("'", a + 1) + 1:])


def separate(text: str, pos: int = 0, until: str = ';') -> (str, str):
    """split text into the part between pos and the next occurence of until and the rest"""
    return text[:pos] + text[text.find(until, pos) + len(until):], text[pos:text.find(until, pos)]


def init(filename: str, key=None) -> (str, dict):
    """read modules and functions declarations,
    stores modules in lib and functions/procedures in functions[filename]"""
    global ignore, kw, lib, functions
    if key is None:
        key = {i: [] for i in kw}
    file = remove_strings(
        uncomment(
            open(filename, 'rt').read().lower().strip()
        ).replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('  ', ' ')
    )
    for i in kw:
        offset = 0
        while file.find(i, offset) != -1:
            offset = file.find(i, offset) + 1
            key[i] += [offset - 1]
    del i, offset,
    if key[kw[2]]:
        lib += [i.strip() for i in separate(file, key[kw[2]][0])[1].replace('uses ', '').split(',') if
                i.strip() not in lib and i.strip() not in ignore]
    key.pop(kw[2])
    temp = len(kw[5])
    if filename not in functions:
        functions[filename] = {}
    for i in key[kw[5]]:
        if len(separate(file, i + temp, '(')[1].strip()) < len(separate(file, i + temp)[1].strip()):
            functions[filename][separate(file, i + temp, '(')[1].strip()] = i + temp
        else:
            functions[filename][separate(file, i + temp)[1].strip()] = i + temp
    temp = len(kw[4])
    for i in key[kw[4]]:
        if len(separate(file, i + temp, '(')[1].strip()) < len(separate(file, i + temp)[1].strip()):
            functions[filename][separate(file, i + temp, '(')[1].strip()] = i + temp
        else:
            functions[filename][separate(file, i + temp)[1].strip()] = i + temp
    return file


def sorting(temp: list) -> list:
    """sort list of tuples based on order of first element"""
    i = 0
    while i < len(temp) - 1:
        if temp[i][0] > temp[i + 1][0]:
            temp[i + 1], temp[i] = temp[i], temp[i + 1]
            i = 0
        else:
            i += 1
    return temp


def readfunc(function: str, declaration: str):
    """read a function declaration to find out what functions does this function use,
    might also be the main code instead of a function declaration"""
    global analyse
    for i in analyse:
        if i in declaration:
            operator = declaration[declaration.find(i) - 1]
            if (
                    operator in (';', ' ', '(', '[', ',')
                    and declaration[declaration.find(i) + len(i)]
                    in (';', ' ', '(', '[', ']', ')', ',')
                    and i != function
                    and i not in analyse[function]
            ):
                analyse[function] += [i]


def readfile(filename: str, fileread: str = None):
    global file, functions
    if fileread is None:
        fileread = file[filename]
    key = functions[filename]
    elem = list(key.keys())
    for i in range(len(key) - 1):
        readfunc(elem[i],
                 fileread[len(kw[7]) + fileread.find(kw[7], key[elem[i]]):key[elem[i + 1]]])
    if len(key) > 0:
        readfunc(elem[len(key) - 1],
                 fileread[len(kw[7]) + fileread.find(kw[7], key[elem[len(key) - 1]]):])


def struct(temp: dict, lastfunc: int) -> list:
    return sorting(
        [(j, i[0]) for i in temp.items() for j in i[1] if i[0] in (kw[7], kw[8]) and j >= lastfunc]
    )


def make_tree(lst: list) -> dict[list]:
    return {i: make_tree(analyse[i]) for i in lst} if lst else {}


def totree(tree: dict, x: Node) -> Node:
    """turn a tree of dictionary into a tree of node"""
    temp = None
    for i in tree:
        temp = Node(i, parent=x)
        totree(tree[i], temp)
    if x is None:
        return temp


if __name__ == '__main__':
    kw = ('program', 'unit', 'uses', 'interface', 'function', 'procedure', 'implementation', 'begin', 'end',
          'var', ';')
    error = open('error.txt', 'w')
    try:
        info = open('info.txt', 'rt')
    except Exception as N:
        error.write('error there is no info.txt\n\n')
    else:
        lib = []
        functions = {}
        filename = ''
        try:
            filename = info.readline().lower().strip()
            ignore = [i.strip() for i in info.readline().lower().strip().split(',')]
        except Exception as N:
            error.write('error, the info.txt was not written  properly, ')
            error.write('have one line as the name of the program file, ')
            error.write('ex: "main .pas" and the other as the list of external sources\n\n')
            info.close()
        else:
            info = {i: [] for i in kw}
            try:
                file = {filename: init(filename, info)} | {
                    f'{i}.pas': init(f'{i}.pas') for i in lib
                }
            except Exception as N:
                error.write(
                    f'error, something unexpected happened in one of the file: {str(N)}\n\n'
                )
            else:
                try:
                    functions = {i: sort_dict(functions[i]) for i in functions}
                    analyse = {j.strip(): [] for i in functions.values() for j in i.keys()}
                    analyse['main'] = []
                    main_has_func = len(info[kw[4]]) != 0 or len(info[kw[5]]) != 0
                    if main_has_func:
                        temp = struct(info, max(info[kw[4]][len(info[kw[4]]) - 1] if len(info[kw[4]]) else 0,
                                                info[kw[5]][len(info[kw[5]]) - 1] if len(info[kw[5]]) else 0))
                        info = 0
                        for i in temp:
                            if i[1] == kw[7]:
                                info += 1
                            else:
                                info -= 1
                                if info == -1:
                                    info = i[0] + len(kw[8]) + 1
                                    break
                    else:
                        info = file[filename].find('begin')
                    temp = file[filename][file[filename].find(kw[7], info):]
                    readfunc('main', temp)
                    if main_has_func:
                        readfile(filename, file[filename][:file[filename].find(kw[7], info)])
                    functions = {i: sort_dict(functions[i]) for i in functions}
                except Exception as N:
                    error.write(f'error, something unexpected happened while readind the declaration of {filename} function: {str(N)}')
                else:
                    del info
                    i = -1
                    try:

                        for i in file:
                            if i != filename:
                                readfile(i)
                    except Exception as N:
                        error.write(f'error when reading the declaration of {i} functions: {str(N)}')
                    else:
                        try:
                            tree = totree(make_tree(['main']), None)
                            with open('output.txt', 'w') as f:
                                for pre, fill, node in RenderTree(tree):
                                    print(f"{pre}{node.name}")
                            print()
                            try:
                                UniqueDotExporter(tree).to_picture(
                                    "analyse_descendante.png")
                            except Exception:
                                print("analyse_descendante.png n' a pas été générée car graphviz n'est pas sur cet ordinateur")
                                print(
                                    "si vous avez installé graphviz et obtenez toujours ce message, essayez de redemarrer, puis de réinstaller en cochant bien l'option add graphviz to PATH for current user")
                                print("si cela ne marche pas non plus, trouver ")
                            else:
                                print("analyse descendante.png a bien été générée")
                            i = input()
                            del i
                        except Exception as N:
                            error.write('there was an error in the last part of the code, this wasn\'t supposed to be possible: ' + str(N))
    finally:
        error.close()
