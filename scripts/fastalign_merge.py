# Ref. URL : https://svn.code.sf.net/p/apertium/svn/trunk/apertium-tools/ordlist-fra-fastalign.py
import sys ;

inngang = open(sys.argv[1]);
lr_alig = open(sys.argv[2]);
rl_alig = open(sys.argv[3]);

processing = True;

l_r = {};

while processing: #{

	inrow = inngang.readline();
	lr = lr_alig.readline();
	rl = rl_alig.readline();
	
	if inrow == '' or lr == '' or rl == '': #{
		processing = False;
		break;
	#}

	l = inrow.split('|||')[0];
	r = inrow.split('|||')[1];

	ll = l.split(' ');
	rr = r.split(' ');

	for o in ll: #{
		if o not in l_r: #{
			l_r[o] = {};
		#}
	#}	

	for a in lr.split(' '): #{
		a_l = int(a.split('-')[0]);
		a_r = int(a.split('-')[1]);

		o_l = ll[a_l];
		o_r = rr[a_r];

		if o_r not in l_r[o_l]: #{
			l_r[o_l][o_r] = 0;
		#}
			
		l_r[o_l][o_r] += 1.0;
	#}
#}

p = {};

for w1 in l_r: #{
	if w1 not in p: #{
		p[w1] = {};
	#}
	total = 0.0;

	for w2 in l_r[w1]: #{
		total += float(l_r[w1][w2]);
	#}

	for w2 in l_r[w1]: #{
		if w2 not in p[w1]: #{
			p[w1][w2] = l_r[w1][w2] / total;
		#}
	#}
#}

for w1 in l_r: #{
	for w2 in l_r[w1]: #{
		print('%d\t%.4f\t%s\t%s' % (l_r[w1][w2], p[w1][w2], w1, w2));
	#}
#}

