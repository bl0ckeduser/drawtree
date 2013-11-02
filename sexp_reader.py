# S-expression -> python list
# based partly on parser.c from my other
# project, "wannabe-lisp"

# by blockeduser,
# Tue Oct 29 00:18:45 EDT 2013

def sexp2list_iter(sexp_str, i):
	result = None
	while i < len(sexp_str):
		# parse a list
		if sexp_str[i] == '(':
			i += 1
			result = []
			while i < len(sexp_str) and sexp_str[i] != ')':
				# consume whitespace
				while i < len(sexp_str) and (sexp_str[i] == ' ' or sexp_str[i] == '\t'):
					i += 1
				# stop if there's nothing left now
				if i >= len(sexp_str):
					break
				# try to add a list-child
				old = i
				child, i = sexp2list_iter(sexp_str, i)
				# if child-parsing failed, break
				if old == i:
					break
				else:
					# otherwise add the child and carry on
					result.append(child)
				# eat ) and terminate upon it
				if sexp_str[i] == ')':
					i += 1
					break
				i += 1
			return (result, i)
		else:
			# parse a symbol
			result = ""
			while sexp_str[i] == ' ' or sexp_str[i] == '\t':
				i += 1
			while i < len(sexp_str) and not (sexp_str[i] == ')' or sexp_str[i] == ' ' or sexp_str[i] == '\t'):
				result += sexp_str[i]
				i += 1
			return (result, i)
	return (result, i)

def sexp2list(sexp_str):
	l, end_index = sexp2list_iter(sexp_str, 0)
	return l

# testing
if __name__ == "__main__":
	print "TESTING..."
	print sexp2list("abc")
	print sexp2list("(abc def ghi)")
	print sexp2list("(abc (def (ghi jsd) dhsf (dhf jdsf)) shds (shd ks) ajs (dhf hd) hds)")
