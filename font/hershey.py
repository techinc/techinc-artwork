#!/usr/bin/python3

import sys

class bbox(object):
	def __init__(self, bbox=None):
		self.coords = [ None, None, None, None ]

	def left(self):
		return self.coords[0]

	def top(self):
		return self.coords[1]

	def right(self):
		return self.coords[2]

	def bottom(self):
		return self.coords[3]

	def topleft(self):
		return tuple(self.coords[0:2])

	def bottomright(self):
		return tuple(self.coords[2:4])

	def width(self):
		return self.coords[2] - self.coords[0]

	def height(self):
		return self.coords[3] - self.coords[1]

	def dimensions(self):
		return (self.width(), self.height())

	def add_bbox(self, bbox, at=(0,0)):
		self.add_point( bbox.coords[0:2], at )
		self.add_point( bbox.coords[2:4], at )

	def add_point(self, point, at=(0,0)):
		for i, j ,minmax in ( (0, 0, min), (1, 1, min), (2, 0, max), (3, 1, max) ):
			if point[j] != None:
				if self.coords[i] == None:
					self.coords[i] = point[j]+at[j]
				else:
					self.coords[i] = minmax(point[j]+at[j], self.coords[i])

	def expand(self, n):
		t, l, b, r = self.coords
		self.coords = t-n, l-n, b+n, r+n

def hershey_num(c):
	return ord(c) - ord('R')

def hershey_coord(ab):
	return ( hershey_num(ab[0]), hershey_num(ab[1]) )

def hershey_parse(data):
	font = {}

	for line in data.split('\n'):
		try:
			glyphpath = ''
			char = chr(int(line[0:5]))
			n_poly = int(line[5:8]) -1
			left, right = hershey_num(line[8]), hershey_num(line[9])

		except ValueError:
			continue

		mid = -left
		width = right-left
		box = bbox()

		polylines = []
		curpoly = []
		for pair in ( line[10+i:12+i] for i in range(0, n_poly*2, 2) ):
			if pair == ' R':
				if curpoly != []:
					polylines.append(curpoly)
					curpoly = []
			else:
				x, y = hershey_coord(pair)
				x += mid
				box.add_point( (x, y) )
				curpoly.append( (x, y) )

		if curpoly != []:
			polylines.append(curpoly)

		font[char] = { 'polylines': polylines, 'width': width, 'bbox': box }

	return font

tiny_hjf_height = 10
tiny_hjf="""   32  1OU
   33  6QSRNRR RRTRU
   34  8OTQNQPPQ RSNSPRQ
   35 12OUQOQU RSUSO RTQPQ RPSTS
   36 16OUPTQUSUTTTSSRQRPQPPQOSOTP RRNRV
   37 15OVPPPOQOQPPP RUOPU RTUUUUTTTTU
   38 12OUTUPQPPQORPRQPSPTQURUTS
   39  4PSRNRPQQ
   40  5PTSOQQQSSU
   41  5PTQOSQSSQU
   42 12OUPRTR RRPRT RPTTP RPPTT
   43  6OUPRTR RRPRT
   44  7PTSURURTSTSUQW
   45  3OUPRTR
   46  6QTRUSUSTRTRU
   47  3OUPUTO
   48 11OUPTPPQOSOTPTTSUQUPTTP
   49  7OUPQRORU RPUTU
   50  8OUPPQOSOTPTQPUTU
   51 15OUPPQOSOTPTQSRRR RSRTSTTSUQUPT
   52  5OUSUSOPRTR
   53 11OUTOPOPRRQSQTRTTSUQUPT
   54 11OUPRSRTSTTSUQUPTPRRPTO
   55  6OUPOTOTPPTPU
   56 17OUQRSRTSTTSUQUPTPSQRPQPPQOSOTPTQSR
   57 12OUPTQUSUTTTPSOQOPPPQQRTR
   58 12QTRRSRSQRQRR RRUSUSTRTRU
   59 13PTRRSRSQRQRR RSURURTSTSUQW
   60  4OUTOPRTU
   61  6OUPSTS RPQTQ
   62  4OUPOTRPU
   63 10OUPPQOSOTPTQRS RRTRU
   64 15OUTTSUQUPTPPQOSOTPTRSSQSQQSQSS
   65  9OUPUPQROTQTU RPRTR
   66 14OUPUPOSOTPTQSRTSTTSUPU RPRSR
   67  9OUTTSUQUPTPPQOSOTP
   68  8OUPUPOSOTPTTSUPU
   69  8OUPRRR RTOPOPUTU
   70  7OURRPR RPUPOTO
   71 11OURRTRTTSUQUPTPPQOSOTP
   72  9OUPUPO RPRTR RTOTU
   73  9PTQUSU RRURO RQOSO
   74  9OUPTQURUSTSO RROTO
   75  9OUPUPO RTOPS RQRTU
   76  4OUPOPUTU
   77  6OUPUPORQTOTU
   78  5OUPUPOTUTO
   79 10OUQUPTPPQOSOTPTTSUQU
   80  8OUPUPOSOTPTRSSPS
   81 13OUQUPTPPQOSOTPTTSUQU RRSTU
   82 11OUPUPOSOTPTRSSPS RRSTU
   83 13OUPTQUSUTTTSSRQRPQPPQOSOTP
   84  6OUPOTO RRORU
   85  7OUPOPTQUSUTTTO
   86  6OUPOPSRUTSTO
   87  6OUPOPURSTUTO
   88  6OUPOTU RPUTO
   89  9OUPOPPRRRU RRRTPTO
   90  7OUPOTOTPPTPUTU
   91  5PTSOQOQUSU
   92  3OUPOTU
   93  5PTQOSOSUQU
   94  4OUPQROTQ
   95  3OUPUTU
   96  4PSQNQPRQ
   97  9OUQQSQTRTUQUPTQSTS
   98  8OUPQSQTRTTSUPUPO
   99  7OUTQQQPRPTQUTU
  100  8OUTQQQPRPTQUTUTO
  101 10OUPSTSTRSQQQPRPTQUSU
  102  7PTQRSR RRURPSO
  103 10OURWSWTVTQQQPRPTQUTU
  104  9OUPUPO RPRQQSQTRTU
  105 10PTRNRO RQQRQRU RQUSU
  106  9OSRNRO RQQRQRVQWPW
  107  9OTPUPO RPSSQ RPSSU
  108  7PTQORORU RQUSU
  109 11OUPUPQQQRRSQTRTU RRRRU
  110  6OUPUPQSQTRTU
  111 10OUPTPRQQSQTRTTSUQUPT
  112  8OUPUSUTTTRSQPQPW
  113  8OUTUQUPTPRQQTQTW
  114  7OTPUPQ RPSRQSQ
  115  9OUPUSUTTSSQSPRQQTQ
  116  7PTQQSQ RRPRTSU
  117  6OUPQPTQUTUTQ
  118  4OUPQRUTQ
  119  8OUPQPTQURTSUTTTQ
  120  6OUPQTU RPUTQ
  121 10OUPQPTQUTU RRWSWTVTQ
  122  5OUPQTQPUTU
  123 10OTSOROQPQQPRQSQTRUSU
  124  3QSRORU
  125 10PUQOROSPSQTRSSSTRUQU
  126  5OUPOQNSPTO
"""

def svg_character_path(c, font, at=(0,0)):
	x, y = at
	sym = font[c]
	path = ''.join('M' + 'L'.join( '{},{} '.format(x+dx, y+dy) for dx, dy in poly) for poly in sym['polylines'] )
	box = bbox()
	box.add_bbox(sym['bbox'], at)
	return path, box, (x+sym['width'], y)

def svg_text_path(text, font, height, at=(0,0)):

	paths = []
	box = bbox()
	cursor = at
	for c in text:
			
		if c == '\n':
			x, y = cursor
			cursor = 0, y+height
			continue

		path, cbox, cursor = svg_character_path(c, font, cursor)
		paths.append(path)
		box.add_bbox(cbox)

	return ''.join(paths), box, cursor

def header(width, height):
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="""+"\""+str(width)+"mm\""+"""
   height="""+"\""+str(height)+"mm\""+"""
   viewBox=\"0 0 """+str(width)+' '+str(height)+"""\"
   id="dhxdron"
   >"""

def background(width, height, style):
    return "<rect width=\""+str(width)+"\" height=\""+str(height)+"\"" + \
           " style=\""+style+"\" />"

def footer():
    return "</svg>"

def group(code, transform=None, id=None):
    if id:
        ident = ' id="'+id+'"'
    else:
        ident = ''

    if transform:
        trans = ' transform="'+transform+'"'
    else:
        trans = ''

    return "<g"+ident+trans+">"+code+"</g>\n"

def path(path, style=None):
    s = ''
    if style:
        s = ' style="'+style+'"'
    return '<path d="'+path+'"'+s+'/>'


if __name__ == '__main__':

	text_style = "stroke-width:.8;stroke:rgb(255,255,86);fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none"
	bg_style = 'fill:rgb(0,0,0)'

	font = hershey_parse(tiny_hjf)
	height = tiny_hjf_height
	text = sys.stdin.read()

	path_d, box, _ = svg_text_path(text, font, height)

	border = 5
	box.expand(border)

	left, top = box.topleft()
	w, h = box.dimensions()

	print (header(width=w, height=h))
	print (background(width=w, height=h, style=bg_style))
	print (group(path(path_d, style=text_style), transform="translate({},{})".format(-left, -top)))
	print (footer())

