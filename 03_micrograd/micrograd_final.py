"""
Micrograd - A tiny autograd engine

This is the complete, final implementation.
Use this as a reference after working through the notebook.

Based on Andrej Karpathy's micrograd:
https://github.com/karpathy/micrograd
"""

import math
import random


class Value:
    """A scalar value with automatic gradient computation."""

    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    # === ADDITION ===
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            # Addition rule: gradient flows through equally
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __radd__(self, other):  # other + self
        return self + other

    # === MULTIPLICATION ===
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            # Multiplication rule: gradient = other input × output gradient
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __rmul__(self, other):  # other * self
        return self * other

    # === POWER ===
    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supports int/float powers"
        out = Value(self.data ** other, (self,), f'**{other}')

        def _backward():
            # Power rule: d/dx(x^n) = n * x^(n-1)
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward

        return out

    # === NEGATION, SUBTRACTION, DIVISION ===
    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __truediv__(self, other):
        return self * other**-1

    def __rtruediv__(self, other):
        return other * self**-1

    # === ACTIVATION FUNCTIONS ===
    def tanh(self):
        x = self.data
        t = (math.exp(2*x) - 1) / (math.exp(2*x) + 1)
        out = Value(t, (self,), 'tanh')

        def _backward():
            # Derivative of tanh: 1 - tanh²
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            # Derivative of ReLU: 0 if x < 0, else 1
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out

    def exp(self):
        x = self.data
        out = Value(math.exp(x), (self,), 'exp')

        def _backward():
            # Derivative of exp: exp(x)
            self.grad += out.data * out.grad
        out._backward = _backward

        return out

    # === BACKWARD PASS ===
    def backward(self):
        """Compute gradients for all nodes in the graph."""
        # Build topological order
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # Set output gradient to 1
        self.grad = 1.0

        # Backpropagate in reverse topological order
        for node in reversed(topo):
            node._backward()


# === NEURAL NETWORK COMPONENTS ===

class Neuron:
    """A single neuron: weighted sum of inputs + bias, through activation."""

    def __init__(self, nin, nonlin=True):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(0)
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh() if self.nonlin else act

    def parameters(self):
        return self.w + [self.b]

    def __repr__(self):
        return f"{'TanH' if self.nonlin else 'Linear'}Neuron({len(self.w)})"


class Layer:
    """A layer of neurons."""

    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"


class MLP:
    """Multi-Layer Perceptron: stack of layers."""

    def __init__(self, nin, nouts):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i+1], nonlin=i!=len(nouts)-1)
                       for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    # Demo: train a small network
    print("=" * 50)
    print("Micrograd Demo")
    print("=" * 50)

    # Create network: 3 inputs → 4 → 4 → 1 output
    net = MLP(3, [4, 4, 1])
    print(f"\nNetwork: {net}")
    print(f"Parameters: {len(net.parameters())}")

    # Training data
    xs = [
        [2.0, 3.0, -1.0],
        [3.0, -1.0, 0.5],
        [0.5, 1.0, 1.0],
        [1.0, 1.0, -1.0],
    ]
    ys = [1.0, -1.0, -1.0, 1.0]

    # Training loop
    print("\nTraining...")
    for k in range(100):
        # Forward pass
        ypred = [net(x) for x in xs]
        loss = sum((yp - yt)**2 for yp, yt in zip(ypred, ys))

        # Backward pass
        for p in net.parameters():
            p.grad = 0.0
        loss.backward()

        # Update
        for p in net.parameters():
            p.data -= 0.1 * p.grad

        if k % 20 == 0:
            print(f"  Step {k:3d}: loss = {loss.data:.4f}")

    # Final predictions
    print("\nFinal predictions:")
    for x, y in zip(xs, ys):
        pred = net(x)
        print(f"  {x} → pred: {pred.data:+.4f}, target: {y:+.1f}")
