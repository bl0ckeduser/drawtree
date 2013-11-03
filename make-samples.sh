rm -f samples/*.png

for x in `ls samples/* | grep -v '\.py' | grep -v '\.png'`
do
	cat $x | ./drawtree.py --square ${x}.png
	echo ${x}.png
done

for n in 10 30 200
do
	./samples/optimal-bst.py $n | ./drawtree.py --square samples/bst-$n.png
	echo samples/bst-${n}.png
done
