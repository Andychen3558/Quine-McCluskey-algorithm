from __future__ import division, print_function
import numpy as np

def dec_to_bin(x, n):
	return bin(x)[2:].zfill(n)

def combine(a, b):
	ans = ''
	count = 0
	for i in xrange(len(a)): 
		if(a[i] == b[i]):
			ans += a[i]
		else:
			ans += '-'
			count += 1
	if(count > 1): 
		return None
	else:            
		return ans


def find_prime_implicants(data):
	implicants = list(data)
	size = len(implicants)
	IM = []
	im = []
	im2 = []
	mark = [0]*size
	m = 0
	for i in xrange(size):
		for j in xrange(i+1, size):
			ans = combine( str(implicants[i]), str(implicants[j]) )
			if ans != None:
				im.append(str(ans))
				mark[i] = 1
				mark[j] = 1
			else:
				continue

	mark2 = [0]*len(im)
	for p in xrange(len(im)):
		for n in xrange(p+1, len(im)):
			if( p != n and mark2[n] == 0):
				if( im[p] == im[n]):
					mark2[n] = 1

	for r in xrange(len(im)):
		if(mark2[r] == 0):
			im2.append(im[r])

	for q in xrange(size):
		if( mark[q] == 0 ):
			IM.append( str(implicants[q]) )
			m = m+1

	if(m == size or size == 1):
		return IM
	else:
		return IM + find_prime_implicants(im2)

def transfer(data, tra):
	newlist = list(data)
	if newlist in tra:
		return
	if '-' not in newlist:
		tra.append(newlist)
		return
	#print(newlist)
	for i in xrange(len(newlist)):
		if newlist[i]=='-':
			newlist[i] = '0'
			transfer(newlist, tra)
			newlist[i] = '1'
			transfer(newlist, tra)
def PrintAns(ans):
	for i in xrange(len(ans)):
		for j in xrange(len(ans[i])):
			if ans[i][j]=='0':
				print(chr(j+ord('a'))+"'", end="")
			elif ans[i][j]=='1':
				print(chr(j+ord('a')), end="")
		if i < len(ans)-1:
			print(' + ', end="")
	print()

if __name__ == '__main__':
	while True:
		m = []
		d = []
		ALL = []
		try:
			(N_var, N_m, N_d) = map(int, raw_input().split())
		except:
			break

		if N_m>0:
			m = map(int, raw_input().split())
		if N_d>0:
			d = map(int, raw_input().split())
		ALL = sorted(m+d)
		for i in xrange(len(ALL)):
			ALL[i] = dec_to_bin(ALL[i], N_var)
		prime_implicants = find_prime_implicants(ALL)
		#print(prime_implicants)

		table = np.zeros(shape=(len(prime_implicants), 1<<N_var))
		for i in xrange(len(prime_implicants)):
			tra = []
			transfer(prime_implicants[i], tra)
			#print(tra)
			for j in tra:
				strr = ''.join(j)
				dec = int(strr, 2)
				if dec in m:
					table[i][dec] = 1
		#print(table)
		essential = []
		ans = []
		while True:
			if len(essential)==N_m:
				break
			for i in xrange(1<<N_var):
				if i not in m:
					continue
				index = -1
				for j in xrange(len(prime_implicants)):
					if table[j][i]==1:
						if index==-1:
							index = j
						else:
							index = -1
							break
				if index==-1:
					continue
				ans.append(prime_implicants[index])
				for k in xrange(1<<N_var):
					if table[index][k]==1:
						for r in xrange(len(prime_implicants)):
							table[r][k] = 0
						if k not in essential:
							essential.append(k)
				#print(table)
			if len(essential)==N_m:
				break

			MAX = 0
			MAX_ind = -1
			for i in xrange(len(prime_implicants)):
				SUM = 0
				for j in xrange(1<<N_var):
					SUM += table[i][j]
				if SUM>MAX:
					MAX = SUM
					MAX_ind = i
			ans.append(prime_implicants[MAX_ind])
			for j in xrange(1<<N_var):
				if table[MAX_ind][j]==1:
					for k in xrange(len(prime_implicants)):
						table[k][j] = 0
					if j not in essential:
						essential.append(j)
		PrintAns(ans)
