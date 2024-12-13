from flask import Flask, request, jsonify
import ast
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexity = "O(1)"
        self.nested_loops = 0
        self.recursive_calls = 0
        self.function_name = None

    def visit_For(self, node):
        self.nested_loops += 1
        self._update_complexity()
        self.generic_visit(node)

    def visit_While(self, node):
        self.nested_loops += 1
        self._update_complexity()
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.function_name = node.name
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.function_name:
            self.recursive_calls += 1
            self.complexity = "O(T(n)) - Recursive"
        self.generic_visit(node)

    def _update_complexity(self):
        if self.nested_loops == 1:
            self.complexity = "O(n)"
        elif self.nested_loops == 2:
            self.complexity = "O(n^2)"
        elif self.nested_loops > 2:
            self.complexity = f"O(n^{self.nested_loops})"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data.get('code', '')

    try:
        tree = ast.parse(code)
        analyzer = ComplexityAnalyzer()
        analyzer.visit(tree)
        return jsonify({
            'complexity': analyzer.complexity,
            'reasoning': "The code was analyzed based on loop structures and recursion."
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)