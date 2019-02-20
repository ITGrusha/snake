from pprint import pprint


space = {'namespaces': {}, 'vars': set(), 'parent': None}


def search_space(name: str, namespace: dict):
    # print('SEARCH:', name, 'in', namespace)
    # print()
    if not namespace['namespaces']:
        return None
    elif namespace['namespaces'].get(name) is None:
        for unit in namespace['namespaces']:
            res = search_space(name, namespace['namespaces'][unit])
            if res is not None:
                return res
        return None
    elif namespace['namespaces'].get(name) is not None:
        return namespace['namespaces'][name]


def get_var(var: str, namespace: str):
    global space
    if namespace == 'global':
        namesp = space
    else:
        namesp = search_space(namespace, space)
    if var not in namesp['vars'] and namesp['parent'] is not None:
        return get_var(var, namesp['parent'])
    elif var in namesp['vars']:
        return namespace
    else:
        return None


n = int(input())
for i in range(n):
    cmd, namespace, var = [i.strip() for i in input().split()]
    if cmd.lower() == 'create':
        if var == 'global':
            namesp = space
        else:
            namesp = search_space(var, space)
        namesp['namespaces'][namespace] = {'namespaces': {}, 'vars': set(), 'parent': var}
    elif cmd.lower() == 'add':
        # print(i, namespace, var)
        if namespace == 'global':
            # print("GL")
            namesp = space
        else:
            # print('`', namespace, '`', var, sep='')
            namesp = search_space(namespace, space)
        namesp['vars'].add(var)
        # pprint(space)
    elif cmd.lower() == 'get':
        res = get_var(var, namespace)
        print(res)
    # pprint(space)
