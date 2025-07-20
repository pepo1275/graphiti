from graphiti_core.graphiti import Graphiti
import inspect

sig = inspect.signature(Graphiti.__init__)
print('Graphiti constructor parameters:')
for name, param in sig.parameters.items():
    if name != 'self':
        print(f'  {name}: {param.annotation} = {param.default}')