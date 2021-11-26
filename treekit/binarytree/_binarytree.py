# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: MIT

from typing import List, Union
from pyvis.network import Network # see also https://visjs.org/
from pathlib import Path
import webbrowser
import random


class Node:
    def __init__(self, val: Union[float, int, str] = None, left = None, right = None):
        self.val = val
        self.left = left    # left child node
        self.right = right  # right child node

    def __repr__(self) -> str:
        return f"Node({self.val})"


class binarytree(object):
    def __init__(self, data: List[Union[float, int, str]]):
        """
        data must be in level order
        """
        nodes = [None if d is None else Node(d) for d in data] # 'if d is None' is important because sometimes d = 0 but we still want Node(0)
        for i in range(1, len(nodes)):
            curr = nodes[i]
            if curr:
                # for a geometric sequence, a = 1, r = 2, a_n = a*r**(n-1) => a_1=a, a_2=ar, a_3=ar^2, ...
                # Sn = a*(1-r^n)/(1-r) = (2^n - 1) => let's say parent index: Sn-1, child index: Sn
                # then it follows: (Sn - 1)/2 = 2^n - 2 = 2*(2^n-1 - 1) = Sn-1
                # Thus, the indices for parent and child nodes follow this pattern:
                parent = nodes[(i - 1) // 2]
                if i % 2:
                    parent.left = curr
                else:
                    parent.right = curr
        self.root = nodes[0] if nodes else None
        self.treetype = 'Binary Tree'
    
    def __repr__(self) -> str:
        if self.root:
            return f"Node({self.root.val})"

    # height — The number of edges on the longest path between a node and a descendant leaf.
    @property
    def height(self): # iteration-based binary tree path
      if not self.root:
        return
      max_height = -1
      stack = [(self.root, 0)]
      while stack:
          node, height = stack.pop()
          if node.right:
              stack.append((node.right, height+1))
          if node.left:
              stack.append((node.left, height+1))
          if not node.left and not node.right:
              max_height = max(height, max_height)
      return max_height

    @property
    def inorder(self): # Don't use Morris Traversal as it will modify the original tree
        def dfs(curr):
            if curr:
              dfs(curr.left)
              res.append(curr.val)
              dfs(curr.right)
        res = []
        dfs(self.root)
        return res

    @property
    def preorder(self):
        def dfs(curr):
            if curr:
              res.append(curr.val)
              dfs(curr.left)
              dfs(curr.right)
        res = []
        dfs(self.root)
        return res

    @property
    def postorder(self):
        def dfs(curr):
            if curr:
              dfs(curr.left)
              dfs(curr.right)
              res.append(curr.val)
        res = []
        dfs(self.root)
        return res

    def show(self, filename: str = 'output.html'):
        if not self.root:
            return
        def dfs(node, level=0):
            level += 1
            if node.left:
                g.add_node(node.left.val, shape="circle", level=level, title=f"left child node of Node({node.val}), level={level}")
                g.add_edge(node.val, node.left.val)
                dfs(node.left, level=level)
            else:
                hidden_left_n_id = f"{node.val}'s left child = None"
                g.add_node(hidden_left_n_id, level=level, hidden = True) # label = ' ', color = 'white')
                g.add_edge(node.val, hidden_left_n_id, hidden = True) # color = 'white')
            if node.right:
                g.add_node(node.right.val, shape="circle", level=level, title=f"right child node of Node({node.val}), level={level}")
                g.add_edge(node.val, node.right.val)
                dfs(node.right, level=level)
            else:
                hidden_right_n_id = f"{node.val}'s right child = None"
                g.add_node(hidden_right_n_id, level=level, hidden = True) # label = ' ', color = 'white')
                g.add_edge(node.val, hidden_right_n_id, hidden = True) # color = 'white')                    
        g = Network(width='100%', height='60%')
        g.add_node(self.root.val, shape="circle", level=0, title=f"root node of the tree, level=0")
        dfs(self.root)
        g.heading = f"{self.treetype}, height = {self.height}"
        g.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 40
    }
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    },
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "sortMethod": "directed"
    }
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0,
      "springConstant": 0.2,
      "nodeDistance": 80
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  },
  "configure": {
      "enabled": true,
      "filter": "layout,physics" 
  }
}""")
        full_filename = Path.cwd() / filename
        g.write_html(full_filename.as_posix())
        webbrowser.open(full_filename.as_uri(), new = 2)
        return g


class bst(binarytree):

  def __init__(self, h=2):
    self.root = self.from_sortedarray(range(2**(h+1) - 1))
    self.treetype = 'Binary Search Tree'

  def from_sortedarray(self, array: List[Union[float, int, str]]) -> Node:
    if not array:
      return None
    mid = len(array) // 2
    root = Node(array[mid])
    root.left = self.from_sortedarray(array[:mid])
    root.right = self.from_sortedarray(array[mid+1:])
    return root

  def from_preorder(self, preorder: List[Union[float, int, str]]) -> Node:
        n = len(preorder)
        if not n:
            return None
        root = Node(preorder[0])         
        stack = [root, ]
        for i in range(1, n):
            node, child = stack[-1], Node(preorder[i])
            while stack and stack[-1].val < child.val: 
                node = stack.pop()
            if node.val < child.val:
                node.right = child 
            else:
                node.left = child 
            stack.append(child)
        return root

        