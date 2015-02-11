# I needed a simple tree structure to store and display the discussion
# forum hierarchy from a MOOC. I tried https://github.com/caesar0301/treelib/,
# but it didn't quite do what I wanted. This is probably not very efficient,
# but I don't need to process very large structures.

# Every item has a unique id (can anything comparable and str'able)

# Example session

from collections import defaultdict
class Tree:

	def __init__(self, ary=None, root=0, reachabilityCheck=True):
		self.tree = defaultdict(lambda: [])
		self.root = root
		if ary:
			self.addMany(ary, reachabilityCheck=reachabilityCheck)

	def checkReachable(self, itemid):
		if itemid not in self.subTreeItems(self.root) + [self.root]:
			raise(Exception("Node %s is not reachable from root %s" %
				(str(itemid), str(self.root))))

	# make sure that all nodes are reachable
	def verifyTree(self):
		for k, branch in self.tree.items():
			for item in branch:
				self.checkReachable(item[1])

	def addMany(self, ary, reachabilityCheck=True):
		for itemary in ary:
			self.add(*itemary, reachabilityCheck=False)

		if reachabilityCheck:
			self.verifyTree()

	def findItem(self, itemid):
		for k, branch in self.tree.items():
			for item in branch:
				if item[0] == itemid:
					return [k, item]
		return False

	def add(self, itemid, parent=None, sorting=0, reachabilityCheck=True):
		if self.findItem(itemid):
			raise Exception("Value already exists")

		if parent is None:
			parent = self.root
		
		if reachabilityCheck:
			self.checkReachable(parent)

		self.tree[parent] = self.tree[parent] + [[itemid, parent, sorting]]

	def dump(self):
		print(self.tree)

	def render(self, head = None, level = 0, func = None):
		if not head:
			head = self.root

		if not func:
			func = self._printItem

		func(head, level)
		for branch in sorted(self.tree[head],key = lambda x: x[2]):
			self.render(head = branch[0], level = level + 1, func = func)

	def _printItem(self, item, level):
		print("%s%s" % ("--" * level, str(item)))

	def _removeItem(self, itemid):
		f = self.findItem(itemid)
		if not f:
			raise(Exception("Value %d not found" % itemid))

		self.tree[f[0]].remove(f[1])

	def subTreeItems(self, itemid):
		ary = []
		for branch in self.tree[itemid]:
			bid = branch[0]
			ary += [bid]
			if bid in self.tree:
				ary += self.subTreeItems(bid)
		return(ary)

	# removes item and all sub-items
	def remove(self, itemid):
		# remove sub-tree
		if itemid in self.tree:
			del self.tree[itemid]
		
		# remove item itself
		self._removeItem(itemid)

	def update(self, itemary):
		# make sure that you are not moving it to a child, making it unreachable
		if itemary[1] in self.subTreeItems(itemary[0]):
			raise(Exception("Cannot move item to it's own child, making it unreachable"))

		self._removeItem(itemary[0])
		self.add(*itemary)
 
if __name__ == "__main__":
	import tree

	items = [[1,0,10], [2,0,5], [10,2,5], [14,2,0], [16,14,0], [18,14,5], [3,0,0]]
	t = tree.Tree(ary=items, reachabilityCheck=True)
	t.dump()
	t.render()
	print(t.subTreeItems("Root"))

	t.render()
	t.dump()
	print("*" * 40)
	t.update([2,0,0])
	t.render()
	t.dump()
